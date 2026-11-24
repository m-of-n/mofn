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
from engine import ksatime, render, statement  # noqa: E402
from engine import definition as defs  # noqa: E402
from engine.codecs import CODECS, DEFAULT  # noqa: E402
from engine.errors import EncodingError, Rejected, StructureError, WalletError  # noqa: E402
from engine.schema import KINDS  # noqa: E402
from engine.store import CONTROLLERS, WALLET_FILE, Persona, Wallet  # noqa: E402
from engine.reduce import Threshold  # noqa: E402
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
class Member:
    """One key a context's anchors name, and how they name it.

    **Derived, never declared.** A context has no roster (SPEC-0004 §4.1): a
    key is shown here because an anchor in this context names it."""

    kid: bytes
    name: str
    role: str
    about: str
    threshold: str
    accepted_by: str
    known: bool
    owned: bool


@dataclass
class Community:
    """A SPEC-0004 context, in the words the Communities page shows.

    "Community" is this app's word for it; it is not a term in any SPEC.
    `acts` is None because a persona publishes that it acts in a context as a
    `self` or `speaks` statement (SPEC-0001 §6.3) and no command writes one,
    so this wallet can only show where a persona *relies*."""

    context: str
    persona: str
    anchors: list
    members: list
    relies: bool
    acts: bool | None = None


@dataclass
class Tag:
    """One attestation held here whose subject is a persona's identity key:
    a tag someone gave that persona (W-8, mofn#180)."""

    path: str
    digest: str
    says: str
    says_kid: bytes
    from_self: bool
    claim: str
    definition: str | None
    definition_id: bytes
    defines: list
    not_before: str
    not_on_or_after: str


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
        """By label. The store sorts personas by kid, which is random, so
        "the first identity" would otherwise be a coin flip once a wallet
        holds more than one (W-8)."""
        return sorted((p for p in self.personas() if p.owned), key=_by_label)

    def known(self) -> list[Persona]:
        return sorted((p for p in self.personas() if not p.owned), key=_by_label)

    def find(self, label: str) -> Persona | None:
        return next((p for p in self.personas() if p.label == label), None)

    def keys(self) -> list[dict]:
        w = self.wallet()
        return cli.key_rows(w) if w else []

    def contexts(self, persona: str | None = None) -> list[str]:
        """The contexts of one owned persona, or of the wallet. A context is
        a scope in which an owned persona acts and relies (SPEC-0001 §6.3)."""
        w = self.wallet()
        if not w:
            return ["default"]
        kid = self._kid(persona)
        if persona and kid is None:
            return ["default"]
        return sorted({"default", *w.contexts(kid)})

    def _kid(self, persona: str | None) -> bytes | None:
        p = self.find(persona) if persona else None
        return p.kid if p is not None and p.owned else None

    def anchors(self, context: str = "default", persona: str | None = None) -> list[Anchored]:
        w = self.wallet()
        if not w:
            return []
        kid = self._kid(persona)
        if persona and kid is None:
            return []
        labels = w.labels()
        out = []
        for an in w.anchors(context, kid):
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
        subject: str | None,
        definition: str,
        type_: str,
        value: str,
        valid_days: int,
        passphrase: bytes,
        out: str | None = None,
        *,
        subject_key: str | None = None,
    ) -> Result:
        if bool(subject) == bool(subject_key):
            raise ValueError("sign takes a subject file or a subject key, not both")
        args = [
            "make", "--as", as_,
            *(["--subject-key", subject_key] if subject_key else ["--subject", subject]),
            "--def", definition,
            "--type", type_, "--value", value, "--valid-days", valid_days,
        ]
        if out:
            args += ["-o", out]
        return self.run(*args, passphrase=passphrase)

    def check(
        self,
        statements: list[str],
        subject: str | None = None,
        definition: str = "",
        context: str = "default",
        at: str | None = None,
        *,
        subject_key: str | None = None,
        as_: str | None = None,
    ) -> tuple[Result, dict | None]:
        """`--as` is what makes the verdict the active persona's: it uses only
        that persona's anchors (SPEC-0001 §6.3, SPEC-0004 §4.1)."""
        if bool(subject) == bool(subject_key):
            raise ValueError("check takes an artifact or a subject key, not both")
        args = [
            "check", *statements,
            *(["--subject-key", subject_key] if subject_key else ["--artifact", subject]),
            "--def", definition,
        ]
        if as_:
            args += ["--as", as_]
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

    # ------------------------------------------- personas and communities

    def held(self) -> list:
        """Every statement this wallet holds that still verifies, as
        `(path, Verified)`. Read-only through the engine, as `screens/data.py`
        does; nothing here decides anything."""
        w = self.wallet()
        if not w:
            return []
        keystore = w.keystore()
        out = []
        for f in sorted((self.root / "statements").glob("*")):
            try:
                v = verify(CODECS[self.codec].load(f.read_bytes()), keystore)
            except (EncodingError, Rejected, StructureError, ValueError, OSError):
                continue
            out.append((str(f), v))
        return out

    def received(self, persona: str) -> list[Tag]:
        """The tags this persona was given: attestations held here whose
        subject is its identity key (`this = [1, kid]`).

        `key-publish` carries the very same target for every key in the
        wallet (`statement.key_publish`), so kind is checked first: a key's
        own publication is not a tag anyone gave it."""
        w = self.wallet()
        p = self.find(persona)
        if not w or p is None:
            return []
        labels, out = w.labels(), []
        defines = {}
        for _, v in self.held():
            if v.kind == 8 and v.this and v.this[0] == 4:
                defines.setdefault(bytes(v.this[1]), []).append(v)
        for path, v in self.held():
            if v.kind != 4 or not v.this or v.this[0] != 1 or v.this[1] != p.kid:
                continue
            for a in v.body.get(1, []):
                did = a[1][1]
                f = self.root / "definitions" / f"{did.hex()}.def"
                d = None
                if f.is_file():
                    try:
                        d = defs.load(f.read_bytes())
                    except Exception:
                        d = None
                out.append(
                    Tag(
                        path=path,
                        digest=v.digest.hex(),
                        says=render.key_name(v.says, labels),
                        says_kid=v.says,
                        from_self=v.says == p.kid,
                        claim=tag_claim(a, d),
                        definition=str(f) if f.is_file() else None,
                        definition_id=did,
                        defines=[s for s in defines.get(did, [])],
                        not_before=ksatime.to_text(v.statement[5][1]),
                        not_on_or_after=(
                            ksatime.to_text(v.statement[5][2])
                            if 2 in v.statement[5] else "no end"
                        ),
                    )
                )
        return sorted(out, key=lambda t: t.not_before, reverse=True)

    def community(self, context: str, persona: str | None = None) -> Community:
        w = self.wallet()
        anchors = self.anchors(context, persona)
        labels = w.labels() if w else {}
        owned = {p.kid for p in self.owned()}
        known = {p.kid for p in self.personas()}
        raw = w.anchors(context, self._kid(persona)) if w else []
        return Community(
            context=context,
            persona=persona or "",
            anchors=anchors,
            members=members(raw, labels, owned, known),
            relies=bool(anchors),
            acts=None,
        )

    def communities(self, persona: str | None = None) -> list[Community]:
        return [self.community(c, persona) for c in self.contexts(persona)]


# ----------------------------------------------------------------- helpers


def _by_label(p: Persona):
    return (p.label or "", p.kid)


def tag_claim(a: dict, d) -> str:
    """"Build provenance = Reproducible", through the held definition when
    there is one, else the labels the statement itself carries."""
    tref, value = a[1], a[2]
    known = d is not None and d.id == tref[1]
    name = render.type_name(d if known else None, tref[2])
    text = render.value_text(d if known else None, tref[2], value, 2)
    return f"{name} = {text}"


def members(anchors: list, labels: dict, owned: set, known: set) -> list[Member]:
    """The keys a context's anchors name, deduped by kid.

    This is the whole of what "who is in this community" means: a context has
    no roster, so membership is read off the anchors the persona accepted
    (SPEC-0004 §4.1, §4.2). Three anchor forms name keys — one kid, a
    threshold's set, and a name binding (`engine/reduce.py`)."""
    out: dict[bytes, Member] = {}

    def add(kid, role, about, threshold, accepted_by):
        m = out.get(kid)
        if m is None:
            out[kid] = Member(
                kid=kid,
                name=render.key_name(kid, labels),
                role=role,
                about=about,
                threshold=threshold,
                accepted_by=accepted_by,
                known=kid in known,
                owned=kid in owned,
            )
        elif about and about not in m.about:
            m.about = f"{m.about}; {about}"

    for an in anchors:
        who = render.key_name(an.accepted_by, labels)
        add(an.accepted_by, "accepts anchors here", "", "", who)
        scope = "; ".join(
            r[1][2] + (" ∈ {" + ", ".join(r[3]) + "}" if 3 in r else " (any value)")
            for r in an.about
        )
        trusts = an.trusts
        if isinstance(trusts, bytes):
            add(trusts, "trusted", scope, "", who)
        elif isinstance(trusts, Threshold):
            th = f"any {trusts.k} of {len(set(trusts.keys))}"
            for kid in dict.fromkeys(trusts.keys):
                add(kid, "one of a k-of-n set", scope, th, who)
        elif isinstance(trusts, list) and trusts and trusts[0] == 7:
            named = render.name_text(trusts, labels)
            add(trusts[1], f"names {named}", scope, "", who)
    return list(out.values())


def example_definition_id() -> bytes | None:
    """The id of the vocabulary this app ships, so a tag using it can be
    recognised wherever its bytes were read from."""
    try:
        return defs.load(EXAMPLE_VOCABULARY.read_bytes()).id
    except Exception:
        return None


def fingerprint(kid: bytes) -> str:
    """A key as the engine prints it when the wallet has no label: the
    `key:<16 hex>` form (`render.fingerprint`)."""
    return render.fingerprint(kid)


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
