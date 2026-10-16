"""Compatibility launcher for running Icon Bundler from a source checkout."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from icon_bundler.app import main

if __name__ == "__main__":
    main()
