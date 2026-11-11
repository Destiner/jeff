"""Score one prediction file without importing a trainer or model."""
from __future__ import annotations

import argparse
import sys

from .common import ReferenceError, fingerprint, guard_final, load_examples, write_json
from .metrics import score_examples


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--examples", required=True)
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--allow-final", action="store_true", help="Only after frozen checkpoint selection; keep final outputs isolated")
    args = parser.parse_args()
    try:
        examples = load_examples(args.examples)
        guard_final(examples, args.output, args.allow_final)
        report = score_examples(examples, args.predictions)
        report["examples_file"] = fingerprint(args.examples)
        report["split"] = examples[0]["split"] if examples else None
        write_json(args.output, report)
        print(f'{report["status"]}: {report["overall"]["coverage"]}; report={args.output}')
        return 0 if report["status"] == "ok" else 1
    except ReferenceError as exc:
        # Fail closed: malformed references may contain final content.
        print("Invalid reference examples; no output written", file=sys.stderr)
        print(f"{len(exc.failures)} reference validation failures", file=sys.stderr)
        return 2
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
