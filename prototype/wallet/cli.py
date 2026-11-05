"""mofn — the wallet engine's command line (#65, v0).

This file parses arguments, calls the engine, prints, and sets the exit
code. It does no cryptography, no encoding and no evaluation of its own.

    mofn [--wallet DIR] [--codec ksa-cbor|review-yaml] COMMAND ...

    init
    key gen LABEL [--controller KIND] [--passphrase-stdin] [-o OUT]
    key import FILE [--label NAME]
    root add KEY --as LABEL --def FILE --type TYPE [--values V1,V2] [--context NAME] [--note TEXT]
    root list [--context NAME]
    make --as LABEL --subject FILE --def FILE --type TYPE --value VALUE [--valid-days N] [-o OUT]
         [--passphrase-stdin]
    check STMT [STMT ...] --artifact FILE --def FILE [--context NAME] [--format text|json] [--at TIME]
    show FILE

A bare `mofn` prints the same menu as `mofn -h`; `mofn --version` says what
this mofn is built from.

Exit codes: 0 yes or done, 1 answer no, 2 usage or wallet error, 3 a handed
statement was invalid.
"""

import argparse
import os
import sys
from pathlib import Path

from engine import (
    check as checking,
    definition as defs,
    envelope as env,
    ksatime,
    render,
    signer,
    statement,
    suite,
    unlock,
)
from engine.codecs import CODECS, DEFAULT
from engine.encoding.ksa_cbor import decode
from engine.encoding.review_yaml import emit
from engine.errors import (
    DefinitionError,
    EncodingError,
    Rejected,
    StructureError,
    WalletError,
)
from engine.reduce import Anchor
from engine.schema import STATEMENT, SUITES
from engine.store import CONTROLLERS, Wallet, locate
from engine.verifier import verify

import engine

ISSUES = "https://github.com/m-of-n/mofn/issues"
COMMANDS = [
    ("run", "open the guided screen (start here)"),
    ("init", "create an empty wallet"),
    ("key gen LABEL", "create a persona with one key"),
    ("key import FILE", "know a key, without trusting it"),
    ("root add KEY --as YOU ...", "trust a key about one kind of claim"),
    ("root list", "print your anchors in words"),
    ("make --as LABEL --subject FILE", "make and sign one attestation"),
    ("check STMT... --artifact FILE", "check the statements you were handed"),
    ("show FILE", "print a statement or definition, decoded"),
]
OPTIONS = [
    ("-h, --help", "show this menu (same as mofn with no command)"),
    ("    --version", "show what this mofn is built from"),
    ("    --wallet DIR", "wallet directory (default: $MOFN_WALLET, else ./wallet)"),
    ("    --codec NAME", "statement file form: ksa-cbor (default), review-yaml"),
]
EXAMPLES = [
    ("mofn run", "learn it step by step"),
    ("mofn key gen me", "make your own key (asks for a passphrase)"),
    (
        "mofn check prov.stmt --artifact app.bin --def dv-1.def",
        "is this file vouched for, by someone you trust?",
    ),
]

def short(kid: bytes) -> str:
    return kid.hex()[:8] + "…"


def cmd_init(a):
    root = locate(a.wallet)
    Wallet.init(root)
    print(f"initialized wallet at {root}")


def cmd_key_gen(a):
    w = Wallet.open(locate(a.wallet))
    codec = CODECS[a.codec]
    passphrase = unlock.passphrase(a.passphrase_stdin, confirm=True, given=a.given)
    seed, pub = suite.generate()
    p = w.add_owned(a.label, a.controller, seed, pub, passphrase)
    envelope = signer.sign(
        seed, statement.key_publish(pub, ksatime.now()), carry_pub=True
    )
    v = verify(envelope, {})
    w.put_statement(v.digest, envelope)
    out = Path(a.out or f"{a.label}.pub{codec.suffix}")
    out.write_bytes(codec.dump(envelope))
    print(
        f"persona {p.label}  kid {short(p.kid)}  controller {p.controller} (self-claimed)"
    )
    print(f"wrote {out} — the key-publish statement to hand to others")


def cmd_key_import(a):
    w = Wallet.open(locate(a.wallet))
    envelope = CODECS[a.codec].load(Path(a.file).read_bytes())
    v = verify(envelope, {})
    if v.kind == 1 or (v.kind == 2 and 1 in v.body):
        pub = v.body[1][2]
    else:
        raise WalletError(f"{a.file} is not a key-publish statement")
    p = w.add_known(
        a.label,
        pub,
        {
            "how": "imported",
            "from": str(a.file),
            "when": ksatime.to_text(ksatime.now()),
            "statement": v.digest.hex(),
        },
    )
    name = f" ({p.label})" if p.label else ""
    print(f"known: {short(p.kid)}{name} — not trusted for anything")


def anchor_line(an: Anchor, labels: dict[bytes, str]) -> str:
    scope = "; ".join(
        r[1][2] + (" ∈ {" + ", ".join(r[3]) + "}" if 3 in r else " (any value)")
        for r in an.about
    )
    return (
        f"anchor: {short(an.trusts)} ({render.key_name(an.trusts, labels)}) trusted in {an.context} "
        f"about {scope} — accepted by {render.key_name(an.accepted_by, labels)}"
    )


def cmd_root_add(a):
    w = Wallet.open(locate(a.wallet))
    key, acceptor = w.find(a.key), w.find(a.as_)
    d = defs.load(Path(a.def_).read_bytes())
    tref = d.type_ref(a.type)
    values = [v for v in (a.values or "").split(",") if v]
    about = {1: tref, 3: d.canonical_range(a.type, values)} if values else {1: tref}
    anchor = Anchor(
        a.context, key.kid, [about], acceptor.kid, ksatime.now(), note=a.note
    )
    w.add_anchor(anchor)
    w.put_definition(d.id, d.data)
    print(anchor_line(anchor, w.labels()))


def cmd_root_list(a):
    w = Wallet.open(locate(a.wallet))
    anchors, labels = w.anchors(a.context), w.labels()
    if not anchors:
        print(
            f"no anchors in context {a.context}: you trust no key about anything here"
        )
    for an in anchors:
        print(f"{anchor_line(an, labels)} on {ksatime.to_text(an.accepted_at)}")
        if an.note:
            print(f"  note: {an.note}")


def cmd_make(a):
    w = Wallet.open(locate(a.wallet))
    codec = CODECS[a.codec]
    p = w.find(a.as_)
    if not p.owned:
        raise WalletError(f"{a.as_} is not a persona this wallet owns")
    d = defs.load(Path(a.def_).read_bytes())
    if not d.valid_assignment(a.type, a.value):
        allowed = ", ".join(v[1] for v in d.type(a.type).get(6, []))
        raise WalletError(f"{a.value!r} is not a value of {a.type}; allowed: {allowed}")
    now = ksatime.now()
    s = statement.attestation(
        p.kid,
        statement.digest_target(Path(a.subject).read_bytes()),
        [{1: d.type_ref(a.type), 2: a.value}],
        now,
        ksatime.add_days(now, a.valid_days),
        now,
    )
    seed = w.unlock(p, unlock.passphrase(a.passphrase_stdin, given=a.given))
    envelope = signer.sign(seed, s)
    v = verify(envelope, w.keystore())
    w.put_statement(v.digest, envelope)
    out = (
        Path(a.out)
        if a.out
        else w.root / "statements" / f"{v.digest.hex()}{codec.suffix}"
    )
    out.write_bytes(codec.dump(envelope))
    print(f"wrote {out}")
    print(render.sentence(d, v.statement, w.labels()))


def cmd_check(a):
    w = Wallet.open(locate(a.wallet))
    codec, keystore = CODECS[a.codec], w.keystore()
    items = []
    for f in a.stmt:
        try:
            items.append(checking.handed(f, codec.load(Path(f).read_bytes()), keystore))
        except EncodingError as e:
            items.append(checking.handed(f, None, keystore, str(e)))
    at = ksatime.from_text(a.at) if a.at else ksatime.now()
    answer = checking.run(
        items,
        Path(a.artifact).read_bytes(),
        Path(a.def_).read_bytes(),
        w.labels(),
        w.anchors(a.context),
        a.context,
        at,
    )
    sys.stdout.write(
        render.verdict_json(answer)
        if a.format == "json"
        else render.verdict_text(answer)
    )
    return answer.exit_code


def cmd_run(a):
    from guide import session

    if a.check:
        from guide import check

        return check.run_all()
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        raise WalletError(
            "run needs a terminal; mofn run --check runs every step without one"
        )
    try:
        from guide import screen
    except ModuleNotFoundError as e:
        if (e.name or "").split(".")[0] not in ("textual", "rich"):
            raise
        raise WalletError(
            f"mofn run needs Textual; install the requirements: {sys.executable} "
            f"-m pip install -r {Path(__file__).resolve().parent / 'requirements.txt'}"
        )
    return screen.main(Path(a.dir) if a.dir else session.default_folder())


def cmd_show(a):
    data = Path(a.file).read_bytes()
    if a.file.endswith(".def"):
        d = defs.load(data)
        print(f"definition {d.id.hex()}")
        print(
            f"  the SHA-256 of these {len(data)} bytes. A definition is not signed "
            f"itself; a define statement names it by this id\n"
        )
        sys.stdout.write(emit(defs.to_h(d)))
        return
    e = env.split(CODECS[a.codec].load(data))
    s = decode(e.tbs)
    STATEMENT.check(s)
    pub = f"0x{e.pub.hex()}" if e.pub is not None else "absent"
    print(
        "envelope — what is sent. suite and says are hints, checked against the statement"
    )
    print(f"  suite  {SUITES.get(e.suite, e.suite)}")
    print(f"  says   0x{e.says.hex()}")
    print(
        f"  tbs    {len(e.tbs)} bytes, the statement below as signed: {e.tbs[:16].hex()}…"
    )
    print(f"  sig    0x{e.sig.hex()}")
    print(f"  pub    {pub}")
    print(
        f"\nstatement — the {len(e.tbs)} signed bytes, decoded. Not verified: use check"
    )
    sys.stdout.write(emit(STATEMENT.to_h(s)))


def rows(pairs, width: int) -> list[str]:
    out = []
    for left, right in pairs:
        if len(left) < width:
            out.append(f"  {left:<{width}}{right}")
        else:
            out += [f"  {left}", f"  {'':<{width}}{right}"]
    return out


def menu() -> str:
    return "\n".join(
        [
            f"mofn {engine.__version__} (prototype: "
            f"{' and '.join(engine.OPEN)} are open; do not use real keys)",
            "",
            "Syntax: mofn [options] COMMAND [args]",
            "Sign a file, and check what you were handed: who said it, and "
            "whether you trust them to say it",
            "",
            "Commands:",
            *rows(COMMANDS, 33),
            "",
            "Options:",
            *rows(OPTIONS, 33),
            "",
            "Examples:",
            *rows(EXAMPLES, 44),
            "",
            f"Report problems at {ISSUES}",
            "",
        ]
    )


def shown(path: Path) -> str:
    text = str(path)
    if path.is_absolute() or text.startswith("."):
        return text
    return os.path.join(".", text)


def version(a) -> str:
    codecs = [DEFAULT + " (default)"] + sorted(set(CODECS) - {DEFAULT})
    return "\n".join(
        [
            f"mofn {engine.__version__} (prototype)",
            f"Follows: {', '.join(engine.FOLLOWS)}; {', '.join(engine.ADRS)}",
            f"Open:    {', '.join(engine.OPEN)}",
            f"Codecs:  {', '.join(codecs)}",
            f"Suite:   {SUITES[suite.CODE]}, over {suite.library()}",
            f"Wallet:  {shown(locate(a.wallet))}",
            "",
        ]
    )


class Menu(argparse.Action):
    def __init__(self, option_strings, dest, **kw):
        super().__init__(option_strings, dest, nargs=0, **kw)

    def __call__(self, parser, namespace, values, option_string=None):
        sys.stdout.write(menu())
        parser.exit(0)


def parser() -> argparse.ArgumentParser:
    top = argparse.ArgumentParser(prog="mofn", add_help=False)
    top.add_argument("-h", "--help", action=Menu, help="show the menu")
    top.add_argument(
        "--version", action="store_true", help="show what this mofn is built from"
    )
    top.add_argument(
        "--wallet",
        metavar="DIR",
        help="wallet directory (default: $MOFN_WALLET, else ./wallet)",
    )
    top.add_argument(
        "--codec", choices=sorted(CODECS), default=DEFAULT, help="statement file form"
    )
    sub = top.add_subparsers(dest="command")

    run = sub.add_parser(
        "run",
        help="the guided screen, over a throwaway pair of wallets",
        description="Open the guided screen: seven steps, each showing the mofn "
        "commands it runs. It uses its own folder, never --wallet.",
    )
    run.add_argument(
        "--check",
        action="store_true",
        help="run every step without a screen, in a temporary folder; exit 0 if all match",
    )
    run.add_argument(
        "--dir",
        metavar="DIR",
        help="the guide's folder (default: a mofn/run folder in your user cache)",
    )
    run.set_defaults(run=cmd_run)

    sub.add_parser("init", help="create an empty wallet").set_defaults(run=cmd_init)

    key = sub.add_parser("key", help="personas and keys").add_subparsers(
        dest="key_command", required=True
    )
    gen = key.add_parser("gen", help="create an owned persona with one key")
    gen.add_argument("label")
    gen.add_argument("--controller", choices=CONTROLLERS, default="person")
    gen.add_argument("--passphrase-stdin", action="store_true")
    gen.add_argument("-o", dest="out", metavar="OUT")
    gen.set_defaults(run=cmd_key_gen)
    imp = key.add_parser("import", help="know a key, without trusting it")
    imp.add_argument("file")
    imp.add_argument("--label")
    imp.set_defaults(run=cmd_key_import)

    root = sub.add_parser("root", help="anchors").add_subparsers(
        dest="root_command", required=True
    )
    add = root.add_parser("add", help="anchor a known key in a context")
    add.add_argument("key")
    add.add_argument("--as", dest="as_", required=True, metavar="LABEL")
    add.add_argument("--def", dest="def_", required=True, metavar="FILE")
    add.add_argument("--type", required=True)
    add.add_argument("--values")
    add.add_argument("--context", default="default")
    add.add_argument("--note")
    add.set_defaults(run=cmd_root_add)
    ls = root.add_parser("list", help="print the anchors of a context")
    ls.add_argument("--context", default="default")
    ls.set_defaults(run=cmd_root_list)

    make = sub.add_parser("make", help="make and sign one attestation")
    make.add_argument("--as", dest="as_", required=True, metavar="LABEL")
    make.add_argument("--subject", required=True, metavar="FILE")
    make.add_argument("--def", dest="def_", required=True, metavar="FILE")
    make.add_argument("--type", required=True)
    make.add_argument("--value", required=True)
    make.add_argument("--valid-days", type=int, default=30)
    make.add_argument("-o", dest="out", metavar="OUT")
    make.add_argument("--passphrase-stdin", action="store_true")
    make.set_defaults(run=cmd_make)

    chk = sub.add_parser("check", help="evaluate the statements you were handed")
    chk.add_argument("stmt", nargs="+")
    chk.add_argument("--artifact", required=True, metavar="FILE")
    chk.add_argument("--def", dest="def_", required=True, metavar="FILE")
    chk.add_argument("--context", default="default")
    chk.add_argument("--format", choices=("text", "json"), default="text")
    chk.add_argument(
        "--at",
        metavar="TIME",
        help="evaluation time, YYYY-MM-DDTHH:MM:SSZ (default: now)",
    )
    chk.set_defaults(run=cmd_check)

    show = sub.add_parser(
        "show", help="print a statement or a .def definition, decoded, for reading"
    )
    show.add_argument("file")
    show.set_defaults(run=cmd_show)
    return top


def plain_streams() -> None:
    for s in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", newline="\n")


def main(argv=None, passphrase: bytes | None = None) -> int:
    """Run one command. `passphrase` is for a caller in the same process,
    such as `mofn run`, so it never goes on a command line or in the
    environment."""
    a = parser().parse_args(argv)
    a.given = passphrase
    if a.version:
        sys.stdout.write(version(a))
        return 0
    if a.command is None:
        sys.stdout.write(menu())
        return 0
    try:
        return a.run(a) or 0
    except (
        WalletError,
        DefinitionError,
        EncodingError,
        Rejected,
        StructureError,
        OSError,
        ValueError,
    ) as e:
        print(f"mofn: error: {e}", file=sys.stderr)
        return 2
