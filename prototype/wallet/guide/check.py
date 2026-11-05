"""`mofn run --check`: every step of the guide, with no screen, in a folder
that is thrown away afterwards. Each check must decide the line its step
expects, with the exit code it expects. Exit 0 when every step passes, 1
otherwise.

It does not import Textual, so it runs wherever the engine runs.
"""

import sys
import tempfile
from pathlib import Path

from guide.session import Session
from guide.steps import ACTIONS, STEPS, expected, shown

PASSPHRASE = b"mofn run --check, not a secret"


def run_all(out=None) -> int:
    out = out or sys.stdout
    failures = 0
    with tempfile.TemporaryDirectory(prefix="mofn-run-") as d:
        s = Session(Path(d), passphrase=PASSPHRASE)
        s.prepare()
        for n, action in ACTIONS:
            o = s.advance()
            what = action.note if action.edit else shown(action.argv)
            against = f" — {expected(action)}, exit {o.code}" if action.check else ""
            if o.ok:
                out.write(f"[ok] {n} {STEPS[n].title}: {what}{against}\n")
                continue
            failures += 1
            out.write(f"[FAILED] {n} {STEPS[n].title}: {what}\n")
            for p in o.problems:
                out.write(f"    {p}\n")
            break
    if failures:
        out.write("run --check: FAILED\n")
        return 1
    out.write(f"run --check: {len(STEPS)} steps, {len(ACTIONS)} actions passed\n")
    return 0
