"""Opt-in sampled M9 limits; no model operations or random draws."""

import json
import os
from pathlib import Path
import resource
import sys
import time


class ResourceGuards:
    def __init__(self, prefix):
        self.prefix = Path(prefix)
        self.started = time.monotonic()
        self.torch = None
        self.device = None
        self.samples = 0
        self.first_update_attempted = False
        self.closed = False
        self.events = Path(str(self.prefix) + ".jsonl").open("x", encoding="utf-8")
        self._sync_directory()

    def _sync_directory(self):
        descriptor = os.open(self.prefix.parent, os.O_RDONLY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)

    def _event(self, data):
        data["elapsed_seconds"] = time.monotonic() - self.started
        self.events.write(json.dumps(data, allow_nan=False) + "\n")
        self.events.flush()
        os.fsync(self.events.fileno())

    def bind(self, torch, device):
        self.torch, self.device = torch, device
        threads = torch.get_num_threads()
        self._event({"stage": "bind", "torch_threads": threads})
        if threads != 4:
            raise RuntimeError("M9 requires exactly four torch CPU threads")
        self.check("before_load")

    def check(self, stage):
        sample = {"stage": stage}
        try:
            if self.device is None or self.device.type != "mps":
                raise RuntimeError("M9 resource guards require MPS; no CPU fallback")
            self.torch.mps.synchronize()
            rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            sample["cpu_lifetime_max_rss_bytes"] = rss if sys.platform == "darwin" else rss * 1024
            for key, name in (("mps_driver_bytes", "driver_allocated_memory"),
                              ("mps_recommended_max_bytes", "recommended_max_memory")):
                value = getattr(self.torch.mps, name)()
                if type(value) is not int or value < 0:
                    raise RuntimeError(f"Invalid MPS telemetry: {name}")
                sample[key] = value
            if sample["cpu_lifetime_max_rss_bytes"] <= 0 or sample["mps_recommended_max_bytes"] <= 0:
                raise RuntimeError("Invalid RSS/recommended telemetry")
            sample["mps_recommended_headroom_bytes"] = (
                sample["mps_recommended_max_bytes"] - sample["mps_driver_bytes"])
            if sample["cpu_lifetime_max_rss_bytes"] > 8589934592:
                raise RuntimeError("M9 RSS exceeds 8 GiB")
            if sample["mps_driver_bytes"] > 8589934592:
                raise RuntimeError("M9 MPS driver exceeds 8 GiB")
            if sample["mps_recommended_headroom_bytes"] < 2147483648:
                raise RuntimeError("M9 recommended MPS headroom below 2 GiB")
        except Exception as error:
            sample.update(status="failed", error_type=type(error).__name__, error=str(error))
            self._event(sample)
            raise
        sample["status"] = "ok"
        self._event(sample)
        self.samples += 1

    def first_update(self):
        if not self.first_update_attempted:
            # Persist before step: an interrupted/failed step is not safe to retry.
            marker = Path(str(self.prefix) + ".first-update-attempt.json")
            with marker.open("x", encoding="utf-8") as stream:
                json.dump({"first_optimizer_step_attempted": True,
                           "elapsed_seconds": time.monotonic() - self.started}, stream)
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
            self._sync_directory()
            self.first_update_attempted = True
            self._event({"stage": "first_optimizer_step_attempt", "durable_marker": str(marker)})

    def finish(self, error=None):
        if self.closed:
            return
        if error is None:
            self.check("before_publication")
        self._event({"stage": "guard_completion", "status": "failed" if error else "completed",
                     "error": None if error is None else str(error),
                     "first_update_attempted": self.first_update_attempted})
        self.events.close()
        with Path(str(self.prefix) + ".summary.json").open("x", encoding="utf-8") as stream:
            json.dump({"status": "failed" if error else "completed", "samples": self.samples,
                       "elapsed_seconds": time.monotonic() - self.started,
                       "first_update_attempted": self.first_update_attempted,
                       "error": None if error is None else str(error),
                       "scope": "sampled limits, not continuous peaks; parent owns external supervision"}, stream)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        self._sync_directory()
        self.closed = True
