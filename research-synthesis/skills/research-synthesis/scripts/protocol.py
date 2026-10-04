#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Freeze, check and amend the run protocol (protocol.md).

Practice implemented: a protocol is written and fixed BEFORE searching so deviations and selective
reporting can be detected; every later change is an identified amendment (what changed, when, why) and the
updated protocol gets a new version number [P05, P06 item 4 'Amendments', P01 items 24a-c, P17 'Protocol'].
There is no registry for agent runs; the SHA-256 recorded here is the substitute record (marked [INFERENCE]
in methodology-process.md section 9, 'Protocol' row).

  protocol.py freeze  --run RUN [--by NAME]     refuse if any `TODO` remains; record version 1, time, sha256
  protocol.py check   --run RUN                 exit 1 if the frozen sections were edited without an amendment
  protocol.py amend   --run RUN --change ... --reason ... --effect ...   (edit protocol.md FIRST, then amend)

The hash covers everything above the `## Freeze` heading. `discover.py search|snowball` calls `check`
and refuses to run on an unfrozen or silently edited protocol (override: --no-protocol-check, for smoke tests only).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path

FREEZE_H = "## Freeze"


def split(text: str) -> tuple[str, str]:
    i = text.find("\n" + FREEZE_H)
    if i < 0:
        raise SystemExit(f"protocol.md has no '{FREEZE_H}' section")
    return text[: i + 1], text[i + 1 :]


def digest(body: str) -> str:
    return hashlib.sha256(re.sub(r"[ \t]+\n", "\n", body).strip().encode()).hexdigest()


def set_line(tail: str, label: str, value: str) -> str:
    pat = re.compile(rf"^- {re.escape(label)}:.*$", re.M)
    line = f"- {label}: {value}"
    return pat.sub(lambda m: line, tail, count=1) if pat.search(tail) else tail.replace(FREEZE_H, f"{FREEZE_H}\n{line}", 1)


def state_path(run: Path) -> Path:
    return run / "protocol.sha256.json"


def check(run: Path, quiet: bool = False) -> int:
    p, sp = run / "protocol.md", state_path(run)
    if not p.exists() or not sp.exists():
        if not quiet:
            print(f"protocol not frozen: run `protocol.py freeze --run {run}` before searching", file=sys.stderr)
        return 2
    body, _ = split(p.read_text(encoding="utf-8"))
    st = json.loads(sp.read_text())
    if digest(body) != st["sha256"]:
        if not quiet:
            print(f"protocol.md was edited after freeze v{st['version']} without an amendment: "
                  f"revert the edit, or record it with `protocol.py amend` (change, reason, effect)", file=sys.stderr)
        return 1
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for n in ("freeze", "check", "amend"):
        s = sub.add_parser(n)
        s.add_argument("--run", required=True)
    sub.choices["freeze"].add_argument("--by", default="agent")
    for k in ("change", "reason", "effect"):
        sub.choices["amend"].add_argument(f"--{k}", required=True)
    a = ap.parse_args()
    run = Path(a.run)
    p = run / "protocol.md"
    if a.cmd == "check":
        rc = check(run)
        print("protocol OK" if rc == 0 else "protocol check FAILED")
        return rc
    text = p.read_text(encoding="utf-8")
    body, tail = split(text)
    now = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    if a.cmd == "freeze":
        if state_path(run).exists():
            print("already frozen; use `amend`", file=sys.stderr)
            return 1
        todo = [i for i, l in enumerate(body.splitlines(), 1) if not l.lstrip().startswith(">") and re.search(r"\bTODO\b|\{\{", l)]
        if todo:
            print(f"refusing to freeze: unfilled TODO/placeholder on lines {todo[:15]}", file=sys.stderr)
            return 1
        sha = digest(body)
        tail = set_line(tail, "Version", "1")
        tail = set_line(tail, "Frozen at", now)
        tail = set_line(tail, "SHA-256 of sections above", sha)
        tail = set_line(tail, "Frozen by", a.by)
        p.write_text(body + tail, encoding="utf-8")
        state_path(run).write_text(json.dumps({"version": 1, "frozen_at": now, "sha256": sha}), encoding="utf-8")
        print(f"frozen v1 sha256={sha[:12]}")
        return 0
    # amend
    sp = state_path(run)
    if not sp.exists():
        print("not frozen yet: edit protocol.md freely, then freeze", file=sys.stderr)
        return 1
    st = json.loads(sp.read_text())
    sha = digest(body)
    if sha == st["sha256"]:
        print("no change to the frozen sections since last freeze/amendment; nothing to amend", file=sys.stderr)
        return 1
    v = st["version"] + 1
    row = f"| {now[:10]} (v{v}) | {a.change} | {a.reason} | {a.effect} |"
    tail = tail.rstrip("\n") + "\n" + row + "\n"
    tail = set_line(tail, "Version", str(v))
    tail = set_line(tail, "SHA-256 of sections above", sha)
    p.write_text(body + tail, encoding="utf-8")
    sp.write_text(json.dumps({"version": v, "frozen_at": st["frozen_at"], "sha256": sha, "amended_at": now}), encoding="utf-8")
    print(f"amended -> v{v} sha256={sha[:12]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
