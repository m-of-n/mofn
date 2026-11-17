"""The app's one door to the engine (W-7, mofn#179). No Qt in this module.

Everything that changes the wallet, signs or checks runs the `mofn` command
it names, through `cli.main` in this process — the same path `mofn run`
takes (`screens/runner.py`). So the app's verdict is the CLI's verdict by
construction, and the status bar can show the command a shell would type.
Read-only views (personas, anchors, counts) open the wallet through the
engine's `store`, as `screens/data.py` does.

The passphrase is handed to `cli.main` as bytes. It is never put in argv or
in the environment, and this module never logs or keeps it.

This module reimplements no cryptography, encoding or reduction.
"""

import json
import os
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


def _wallet_source() -> Path:
    """Where `cli`, `engine` and `screens` live: next to this app in a
    checkout, or the bundle root in a PyInstaller build (mofn-wallet.spec
    places them at the paths their own __file__ arithmetic expects)."""
    frozen = getattr(sys, "_MEIPASS", None)
    if frozen:
        return Path(frozen)
    return Path(__file__).resolve().parents[2] / "wallet"


WALLET_SOURCE = _wallet_source()
if str(WALLET_SOURCE) not in sys.path:
    sys.path.insert(0, str(WALLET_SOURCE))

import cli  # noqa: E402
import engine  # noqa: E402
from engine import render, statement  # noqa: E402
from engine.codecs import CODECS, DEFAULT  # noqa: E402
from engine.errors import EncodingError, Rejected, StructureError, WalletError  # noqa: E402
from engine.schema import KINDS  # noqa: E402
from engine.store import CONTROLLERS, WALLET_FILE, Persona, Wallet  # noqa: E402
from engine.verifier import verify  # noqa: E402
from screens import data, learn, runner  # noqa: E402

VERSION = engine.__version__
OPEN = engine.OPEN
DEFAULT_WALLET = Path.home() / "Projects" / "wallet" / "mofn"
EXAMPLE_VOCABULARY = WALLET_SOURCE / "fixtures" / "dv-1.def"
# The example vocabulary's define statement, by its definer (TV-3): without
# it a verdict's semantics line says the vocabulary is unattributed.
EXAMPLE_DEFINE = WALLET_SOURCE / "fixtures" / "tv-3-define.stmt"
LINES = ("integrity", "authenticity", "names", "authorization", "acceptance", "semantics")
ACCEPTORS = data.ACCEPTORS
__all__ = ["CONTROLLERS", "Session", "Result", "learn_pages", "self_test"]


@dataclass
class Result:
    """One command's outcome, and how a shell would have typed it."""

    argv: list[str]
    code: int
    out: str
    err: str

    @property
    def ok(self) -> bool:
        return self.code == 0

    @property
    def error(self) -> str:
        return runner.Result(self.argv, self.code, self.out, self.err).error

    @property
    def shown(self) -> str:
        return runner.shown(self.argv)

    def json(self) -> dict | None:
        try:
            return json.loads(self.out)
        except ValueError:
            return None


@dataclass
class Anchored:
    """One anchor, in the words the Trust table shows."""

    key: str
    about: str
    values: str
    depth: int
    note: str
    accepted_by: str
    context: str


class Session:
    """One wallet folder. Every command names it with `--wallet`."""

    def __init__(self, root: Path | str, codec: str = DEFAULT):
        self.root = Path(root).expanduser()
        self.codec = codec

    # ------------------------------------------------------------- running

    def argv(self, *args) -> list[str]:
        pre = ["--wallet", str(self.root)]
        if self.codec != DEFAULT:
            pre += ["--codec", self.codec]
        return [*pre, *map(str, args)]

    def run(self, *args, passphrase: bytes | None = None) -> Result:
        r = runner.run(self.argv(*args), passphrase)
        return Result(r.argv, r.code, r.out, r.err)

    # ------------------------------------------------------------- reading

    @property
    def exists(self) -> bool:
        return (self.root / WALLET_FILE).is_file()

    @property
    def suffix(self) -> str:
        return CODECS[self.codec].suffix

    def wallet(self) -> Wallet | None:
        if not self.exists:
            return None
        try:
            return Wallet.open(self.root)
        except (WalletError, OSError):
            return None

    def personas(self) -> list[Persona]:
        w = self.wallet()
        return w.personas() if w else []

    def owned(self) -> list[Persona]:
        return [p for p in self.personas() if p.owned]

    def known(self) -> list[Persona]:
        return [p for p in self.personas() if not p.owned]

    def keys(self) -> list[dict]:
        w = self.wallet()
        return cli.key_rows(w) if w else []

    def contexts(self) -> list[str]:
        w = self.wallet()
        return sorted({"default", *(w.contexts() if w else [])})

    def anchors(self, context: str = "default") -> list[Anchored]:
        w = self.wallet()
        if not w:
            return []
        labels = w.labels()
        out = []
        for an in w.anchors(context):
            trusts = an.trusts if isinstance(an.trusts, bytes) else None
            for r in an.about:
                out.append(
                    Anchored(
                        key=render.key_name(trusts, labels) if trusts else str(an.trusts),
                        about=r[1][2],
                        values=", ".join(r[3]) if 3 in r else "any value",
                        depth=(an.may_delegate or {}).get(1, 0),
                        note=an.note or "",
                        accepted_by=render.key_name(an.accepted_by, labels),
                        context=context,
                    )
                )
        return out

    def counts(self) -> dict:
        w = self.wallet()
        if not w:
            return {}
        ps = w.personas()
        contexts = self.contexts()
        return {
            "owned": [p for p in ps if p.owned],
            "known": [p for p in ps if not p.owned],
            "anchors": sum(len(self.anchors(c)) for c in contexts),
            "statements": len(list((self.root / "statements").glob("*"))),
            "definitions": len(list((self.root / "definitions").glob("*.def"))),
            "contexts": contexts,
        }

    # ------------------------------------------------------------- doing

    def init(self) -> Result:
        self.root.mkdir(parents=True, exist_ok=True)
        return self.run("init")

    def key_gen(self, label: str, controller: str, passphrase: bytes) -> Result:
        out = self.root / f"{label}.pub{self.suffix}"
        return self.run(
            "key", "gen", label, "--controller", controller, "-o", out,
            passphrase=passphrase,
        )

    def key_import(self, file: str, label: str | None) -> Result:
        return self.run("key", "import", file, *(["--label", label] if label else []))

    def key_export(self, label: str, out: str) -> Result:
        return self.run("key", "export", label, "-o", out, "--format", "json")

    def root_add(
        self,
        key: str,
        as_: str,
        definition: str,
        type_: str,
        values: list[str],
        depth: int = 0,
        context: str = "default",
        note: str = "",
    ) -> Result:
        args = ["root", "add", key, "--as", as_, "--def", definition, "--type", type_]
        if values:
            args += ["--values", ",".join(values)]
        if depth:
            args += ["--depth", depth]
        if context and context != "default":
            args += ["--context", context]
        if note:
            args += ["--note", note]
        return self.run(*args)

    def sign(
        self,
        as_: str,
        subject: str,
        definition: str,
        type_: str,
        value: str,
        valid_days: int,
        passphrase: bytes,
        out: str | None = None,
    ) -> Result:
        args = [
            "make", "--as", as_, "--subject", subject, "--def", definition,
            "--type", type_, "--value", value, "--valid-days", valid_days,
        ]
        if out:
            args += ["-o", out]
        return self.run(*args, passphrase=passphrase)

    def check(
        self,
        statements: list[str],
        subject: str,
        definition: str,
        context: str = "default",
        at: str | None = None,
    ) -> tuple[Result, dict | None]:
        args = ["check", *statements, "--artifact", subject, "--def", definition]
        if context and context != "default":
            args += ["--context", context]
        if at:
            args += ["--at", at]
        r = self.run(*args, "--format", "json")
        return r, r.json()

    def show(self, file: str) -> Result:
        return self.run("show", file)

    def inspect(self, file: str) -> dict:
        """What Show puts above the decoded text: the kind, who says it, and
        whether its signature verifies against the keys this wallet knows."""
        raw = Path(file).read_bytes()
        out = {"digest": statement.digest_target(raw), "size": len(raw)}
        if file.endswith(".def"):
            out["kind"] = "definition"
            return out
        try:
            envelope = CODECS[self.codec].load(raw)
        except (EncodingError, StructureError, ValueError):
            try:
                envelope = CODECS["review-yaml" if self.codec == DEFAULT else DEFAULT].load(raw)
            except (EncodingError, StructureError, ValueError):
                return out
        w = self.wallet()
        try:
            v = verify(envelope, w.keystore() if w else {})
        except Rejected as r:
            out["kind"] = "statement"
            out["verified"] = False
            out["why"] = f"{r.result}: {r.reason} {r.detail}".strip()
            return out
        except (EncodingError, StructureError, ValueError):
            return out
        labels = w.labels() if w else {}
        out.update(
            kind=KINDS.get(v.kind, str(v.kind)),
            verified=True,
            says=render.key_name(v.says, labels),
            statement=v.digest.hex(),
        )
        return out


# ----------------------------------------------------------------- helpers


def digest_text(path: str) -> str:
    """A file's digest as a statement names it, through the engine."""
    t = statement.digest_target(Path(path).read_bytes())
    return render.target(t, {}).split(":")[0] + ":" + t[2].hex()


def vocabulary(path: str):
    return data.vocabulary(path)


def claims(d) -> list[str]:
    return data.claims(d)


def values(d, claim: str) -> list[str]:
    return data.values(d, claim)


def learn_pages() -> list:
    return learn.pages()


def standing_words(standing: dict, signer: str) -> str:
    """The Standing card's *In words* view: the chain the engine returned,
    said as sentences. Presentation only; the result and reason are the
    engine's."""
    chain = standing.get("chain") or []
    out = []
    if chain:
        root = chain[0]
        if "threshold" in root:
            t = root["threshold"]
            out.append(f"You trust any {t['k']} of {t['n']} keys together, accepted by {root['accepted-by']}.")
        else:
            out.append(f"You trust {root['key']} (accepted by {root['accepted-by']}).")
        prev = root["key"]
        for hop in chain[1:]:
            out.append(f"{prev} passed that on to {hop['key']}.")
            prev = hop["key"]
    if standing.get("result") == "standing":
        out.append(f"So {signer} may say this.")
    elif standing.get("broken"):
        b = standing["broken"]
        out.append(f"But the link {b['from']} → {b['to']} is broken: {standing.get('detail')}.")
    else:
        out.append(standing.get("text", "").removeprefix("no standing: ").capitalize() + ".")
    return " ".join(out)


def self_test() -> int:
    """`mofn-wallet --self-test`: the release smoke. A throwaway wallet, a
    key, Alice imported and trusted, and TV-4 checked green with the four
    attributes — through the same Session the window uses. No window."""
    fx = WALLET_SOURCE / "fixtures"
    with tempfile.TemporaryDirectory() as tmp:
        s = Session(Path(tmp) / "wallet")
        steps = [
            s.init(),
            s.key_gen("me", "person", b"self-test passphrase, not a secret"),
            s.key_import(str(fx / "tv-1-alice.pub.stmt"), "Alice"),
            s.root_add("Alice", "me", str(EXAMPLE_VOCABULARY), "build-provenance", ["reproducible"]),
        ]
        for r in steps:
            if not r.ok:
                print(f"self-test: {r.shown}: {r.error}", file=sys.stderr)
                return 1
        r, j = s.check(
            [str(fx / "tv-4-attestation.stmt"), str(fx / "tv-3-define.stmt")],
            str(fx / "artifact.bin"),
            str(EXAMPLE_VOCABULARY),
            at="2026-10-15T00:00:00Z",
        )
        a = (j or {}).get("associations") or [{}]
        if not (r.ok and j and j["answer"] == "yes" and {"signed-by", "topic", "subject", "standing"} <= set(a[0])):
            print(f"self-test: check was not green: {r.err or r.out}", file=sys.stderr)
            return 1
    print(f"mofn-wallet {VERSION} self-test: ok")
    return 0


def resolve_wallet(flag: str | None = None) -> Path:
    """The wallet the app opens first: an explicit choice, else
    $MOFN_WALLET (as the CLI), else ~/Projects/wallet/mofn."""
    return Path(flag or os.environ.get("MOFN_WALLET") or DEFAULT_WALLET).expanduser()
