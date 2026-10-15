#!/usr/bin/env python3
"""Fail when agent tooling vendored from ProjectPICA/Pica.Claude was edited in place.

`.claude/shared.lock` lists every vendored file with its SHA-256. The source of truth is `shared/` in
Pica.Claude; `scripts/sync-agent-tooling.py` there regenerates the files and the lock. CI runs this
script, so a local edit of a vendored file fails the build instead of drifting silently.

Exit 0: all files match. Exit 1: the lock or a listed file is missing, or a file differs.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LOCK = REPO / ".claude" / "shared.lock"


def main() -> int:
    if not LOCK.is_file():
        # This script is itself vendored, so its presence means the lock must be there too: a deleted
        # lock must not turn the drift check green.
        print("check_shared: .claude/shared.lock is missing; re-run scripts/sync-agent-tooling.py in Pica.Claude")
        return 1
    expected = json.loads(LOCK.read_text(encoding="utf-8"))["files"]
    problems = []
    for rel, digest in sorted(expected.items()):
        path = REPO / rel
        if not path.is_file():
            problems.append(f"missing: {rel}")
        elif hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            problems.append(f"edited in place: {rel}")
    if problems:
        print("Vendored agent tooling differs from ProjectPICA/Pica.Claude:")
        for p in problems:
            print(f"  {p}")
        print("Change the file under shared/ in Pica.Claude and run scripts/sync-agent-tooling.py there.")
        return 1
    print(f"check_shared: {len(expected)} vendored files match")
    return 0


if __name__ == "__main__":
    sys.exit(main())
