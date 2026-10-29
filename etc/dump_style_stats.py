#!/usr/bin/env python3

"""Run Servo with style statistics on the single HTML file in a directory."""

import argparse
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="directory containing exactly one .html or .htm file")
    args = parser.parse_args()

    directory = args.directory.resolve()
    if not directory.is_dir():
        parser.error(f"not a directory: {directory}")

    html_files = sorted(
        path for path in directory.iterdir() if path.is_file() and path.suffix.lower() in {".html", ".htm"}
    )
    if len(html_files) != 1:
        parser.error(f"expected exactly one .html or .htm file in {directory}, found {len(html_files)}")

    repo_root = Path(__file__).resolve().parent.parent
    servo = repo_root / "target" / "debug" / "servo.exe"
    if not servo.is_file():
        parser.error(f"Servo executable not found: {servo}")

    command = [str(servo), "--headless", "-Z", "dump-style-stats", "-x", html_files[0].as_uri()]
    return subprocess.run(command, cwd=repo_root, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
