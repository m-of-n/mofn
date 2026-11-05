"""One run of the guide in one folder: copy in the files Alice sent, run each
step's commands through the CLI in this process, compare each check with the
line its step expects to decide, and remember how far the reader got.

The commands are the CLI's own `main`, so nothing here signs, verifies or
reduces. They run in the guide's folder, whose `./wallet` is the reader's
one wallet, so `$MOFN_WALLET` is set aside while they run. The passphrase is
handed to `main` directly; it is never put in argv or in the environment.
"""

import contextlib
import io
import json
import os
import re
import shutil
import stat
import sys
from dataclasses import dataclass, field
from pathlib import Path

import cli
from guide.steps import ACTIONS, FILES, STEPS, Action

WALLET = Path(__file__).resolve().parents[1]
FIXTURES = WALLET / "fixtures"
LINES = ("integrity", "authenticity", "names", "authorization", "acceptance", "semantics")
PROGRESS = "progress.json"


def default_folder() -> Path:
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA") or Path.home() / "AppData" / "Local")
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Caches"
    else:
        base = Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache")
    return base / "mofn" / "run"


def deciding(verdict: dict) -> str:
    return next((n for n in LINES if verdict["verdict"][n]["result"] == "fail"), "")


@dataclass
class Outcome:
    action: Action
    code: int = 0
    out: str = ""
    err: str = ""
    verdict: dict | None = None
    problems: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.problems


class Session:
    def __init__(self, folder: Path, passphrase: bytes | None = None):
        self.folder = Path(folder)
        self.passphrase = passphrase

    def prepare(self) -> None:
        self.folder.mkdir(parents=True, exist_ok=True)
        for name, fixture in FILES.items():
            if not (self.folder / name).exists():
                shutil.copyfile(FIXTURES / fixture, self.folder / name)

    @property
    def started(self) -> bool:
        return (self.folder / "wallet").exists()

    @property
    def done(self) -> int:
        try:
            n = json.loads((self.folder / PROGRESS).read_text(encoding="utf-8"))["done"]
        except (OSError, ValueError, KeyError, TypeError):
            return 0
        return n if isinstance(n, int) and 0 <= n <= len(ACTIONS) else 0

    def save(self, done: int) -> None:
        (self.folder / PROGRESS).write_text(
            json.dumps({"done": done}) + "\n", encoding="utf-8"
        )

    def reset(self) -> None:
        if self.folder.exists():
            for p in self.folder.iterdir():
                if p.is_dir():
                    shutil.rmtree(p)
                else:
                    p.unlink()
        self.prepare()

    @property
    def step(self) -> int:
        n = self.done
        return ACTIONS[n][0] if n < len(ACTIONS) else len(STEPS)

    def pending(self, step: int) -> list[Action]:
        return [a for i, (s, a) in enumerate(ACTIONS) if s == step and i >= self.done]

    def needs_passphrase(self, step: int) -> bool:
        return self.passphrase is None and any(a.secret for a in self.pending(step))

    def run(self, argv) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        aside = os.environ.pop("MOFN_WALLET", None)
        try:
            with contextlib.chdir(self.folder), contextlib.redirect_stdout(
                out
            ), contextlib.redirect_stderr(err):
                try:
                    code = cli.main(list(argv), passphrase=self.passphrase)
                except SystemExit as e:
                    code = e.code if isinstance(e.code, int) else 2
        finally:
            if aside is not None:
                os.environ["MOFN_WALLET"] = aside
        return code, out.getvalue(), err.getvalue()

    def edit(self, kind: str) -> None:
        if kind == "file":
            data = (self.folder / "artifact.bin").read_bytes()
            (self.folder / "changed.bin").write_bytes(b"X" + data[1:])
        elif kind == "statement":
            data = bytearray((self.folder / "alice.stmt").read_bytes())
            data[-1] ^= 0x01
            (self.folder / "changed.stmt").write_bytes(bytes(data))
        else:
            raise ValueError(kind)

    def do(self, action: Action) -> Outcome:
        o = Outcome(action)
        if action.edit:
            self.edit(action.edit)
            return o
        o.code, o.out, o.err = self.run(action.argv)
        if not action.check:
            if o.code != 0:
                o.problems.append(f"exit {o.code}: {o.err.strip()}")
            return o
        if o.code != action.code:
            o.problems.append(f"exit {o.code}, expected {action.code}")
        try:
            o.verdict = json.loads(o.out)
        except ValueError:
            o.problems.append(f"no verdict: {o.err.strip() or o.out.strip()}")
            return o
        got = deciding(o.verdict)
        if got != action.decides:
            o.problems.append(
                f"the first line to fail is {got or 'none'}, expected "
                f"{action.decides or 'none'}"
            )
        elif action.reason and action.reason not in o.verdict["verdict"][got]["sentence"]:
            o.problems.append(f"{got} does not say {action.reason}")
        if not action.decides and o.verdict["answer"] != "yes":
            o.problems.append(f"answer {o.verdict['answer']}, expected yes")
        return o

    def advance(self) -> Outcome | None:
        n = self.done
        if n >= len(ACTIONS):
            return None
        o = self.do(ACTIONS[n][1])
        if o.ok:
            self.save(n + 1)
        return o

    def key_files(self) -> list[str]:
        rows = []
        for f in sorted(self.folder.glob("wallet/personas/*/keys/*.key")):
            rel = short(f.relative_to(self.folder).as_posix())
            mode = (
                "mode not enforced on Windows"
                if sys.platform == "win32"
                else f"mode {stat.S_IMODE(f.stat().st_mode):04o}"
            )
            fields = dict(
                line.split(": ", 1)
                for line in f.read_text(encoding="utf-8").splitlines()
                if ": " in line
            )
            rows.append(
                f"{rel}  {mode}, encrypted with "
                f"{fields.get('kdf', '?')} + {fields.get('cipher', '?')}"
            )
        return rows

    def folders(self) -> list[str]:
        wallet = self.folder / "wallet"
        return [
            short(p.relative_to(self.folder).as_posix()) + "/"
            for p in sorted(wallet.rglob("*"))
            if p.is_dir()
        ]


def short(path: str) -> str:
    return re.sub(r"[0-9a-f]{64}", lambda m: m.group()[:8] + "…", path)
