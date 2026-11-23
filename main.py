#!/usr/bin/env python3
"""Entry program for news-image-20261122 (the grader runs this; stdlib only).

Copies the committed entry.png to the output location the grader wants:
argv[1] if given, else the MAKEFUN_OUTPUT_DIR environment variable,
else /output. Exits 0 on success, 1 on failure.
"""
import os
import shutil
import sys


def resolve_output():
    """Pick the output destination in the grader's order of preference."""
    if len(sys.argv) > 1 and sys.argv[1]:
        return sys.argv[1]
    env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env:
        return env
    return "/output"


def main():
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    if not os.path.isfile(src):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1
    dest = resolve_output()
    try:
        if os.path.isdir(dest):
            dest = os.path.join(dest, "entry.png")
        parent = os.path.dirname(dest)
        if parent:
            os.makedirs(parent, exist_ok=True)
        shutil.copyfile(src, dest)
        if os.path.getsize(dest) != os.path.getsize(src):
            print("copy failed: size mismatch for %s" % dest, file=sys.stderr)
            return 1
    except OSError as exc:
        print("copy failed: %s" % exc, file=sys.stderr)
        return 1
    print("wrote %s" % dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
