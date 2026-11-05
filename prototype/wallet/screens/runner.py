"""Run one mofn command in this process, exactly as the CLI would, and
spell it the way a shell would take it.

The passphrase, when a command needs one, is handed to `cli.main` directly.
It is never put in argv or in the environment.
"""

import contextlib
import io
from dataclasses import dataclass
from pathlib import Path

import cli
from engine.codecs import CODECS, DEFAULT
from engine.store import WALLET_FILE, locate


@dataclass
class Result:
    argv: list[str]
    code: int
    out: str
    err: str

    @property
    def error(self) -> str:
        lines = [l for l in self.err.splitlines() if l.strip()]
        text = lines[-1] if lines else f"exit {self.code}"
        return text.removeprefix("mofn: error: ").removeprefix("mofn: ")


def run(argv, passphrase: bytes | None = None) -> Result:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = cli.main(list(argv), passphrase=passphrase)
        except SystemExit as e:
            code = e.code if isinstance(e.code, int) else 2
    return Result(list(argv), code, out.getvalue(), err.getvalue())


def quoted(arg: str) -> str:
    if arg and all(c.isalnum() or c in "-_./,:=@+" for c in arg):
        return arg
    return '"' + arg.replace('"', '\\"') + '"'


def shown(argv) -> str:
    return "mofn " + " ".join(quoted(str(x)) for x in argv)


@dataclass
class Place:
    """Which wallet the app has open, and how a shell would name it."""

    wallet: Path
    flag: str | None = None
    codec: str | None = None

    @classmethod
    def resolve(cls, flag: str | None, codec: str | None) -> "Place":
        return cls(locate(flag), flag, codec)

    @property
    def exists(self) -> bool:
        return (self.wallet / WALLET_FILE).is_file()

    @property
    def suffix(self) -> str:
        return CODECS[self.codec or DEFAULT].suffix

    def move(self, where: str) -> None:
        if Path(where) != self.wallet:
            self.wallet, self.flag = Path(where), where

    def argv(self, *args) -> list[str]:
        pre = ["--wallet", self.flag] if self.flag else []
        if self.codec and self.codec != DEFAULT:
            pre += ["--codec", self.codec]
        return [*pre, *map(str, args)]
