"""Absolute-path launcher: python -I -S /main/src/jeff/coordination/current.py ..."""

from pathlib import Path
import sys


if __name__ == "__main__":
    if not (sys.flags.isolated and sys.flags.no_site):
        raise SystemExit("Run this launcher with Python -I -S to exclude stale paths and site hooks.")
    source = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(source))
    from jeff.coordination.__main__ import main

    # Bind code and default board to this checkout, not the caller's CWD.
    raise SystemExit(main(checkout=source.parent))
