"""The steps of `mofn run`, as data: what the reader is told, the mofn
commands each step runs, and the line each check is expected to decide.

The reader is one person with one wallet, `./wallet` in the guide's folder.
Everything from someone else is already made: the published fixtures, handed
over as files Alice sent you. Every command is a plain `mofn …` run in that
folder.

Nothing here runs anything. `session.py` runs the commands through the CLI
itself, and `screen.py` and `check.py` only show the results.
"""

from dataclasses import dataclass

FILES = {
    "alice.pub.stmt": "tv-1-alice.pub.stmt",
    "alice-define.stmt": "tv-3-define.stmt",
    "alice.stmt": "tv-4-attestation.stmt",
    "dv-1.def": "dv-1.def",
    "artifact.bin": "artifact.bin",
}
AT = "2026-10-15T00:00:00Z"
QUESTION = "Which line will fail first?  [1–6]"


@dataclass(frozen=True)
class Action:
    argv: tuple[str, ...] = ()
    edit: str = ""
    note: str = ""
    check: bool = False
    decides: str = ""
    reason: str = ""
    code: int = 0
    secret: bool = False


@dataclass(frozen=True)
class Step:
    title: str
    heading: str
    text: str
    hint: str
    actions: tuple[Action, ...]
    question: str = ""


def check(statement="alice.stmt", artifact="artifact.bin", at=AT, **expect) -> Action:
    when = ("--at", at) if at else ()
    argv = (
        "check",
        statement,
        "alice-define.stmt",
        "--artifact",
        artifact,
        "--def",
        "dv-1.def",
        *when,
        "--format",
        "json",
    )
    return Action(argv, check=True, **expect)


STEPS = (
    Step(
        "your wallet",
        "Your wallet, and your key",
        "mofn keeps one wallet, ./wallet in the folder you run it from. init "
        "makes it; key gen makes your key, me. It asks for a passphrase and "
        "keeps the private key encrypted in the wallet.",
        "The passphrase is asked here, in a masked field, and stays in this "
        "program. It never goes on a command line or in the environment.",
        (
            Action(("init",)),
            Action(("key", "gen", "me", "-o", "me.pub.stmt"), secret=True),
        ),
    ),
    Step(
        "what Alice sent",
        "The files Alice sent you",
        "Alice sent you five files: her key (alice.pub.stmt), her vocabulary "
        "(dv-1.def) and the statement that says it is hers "
        "(alice-define.stmt), her statement about a file (alice.stmt), and "
        "the file (artifact.bin). show decodes her statement field by field; "
        "it does not verify it.",
        "A statement holds no names, only key ids and hashes. says is Alice's "
        "key id; this is the file, by its SHA-256.",
        (Action(("show", "alice.stmt")),),
    ),
    Step(
        "a key you lack",
        "Check, before you have Alice's key",
        "Alice's key is in a file in this folder, but not yet in your wallet. "
        f"Every check here is run as of {AT}, while Alice's statement was "
        "valid.",
        "A signature can only be checked with the key that made it, and the "
        "key must already be yours to look up.",
        (check(decides="authenticity", code=1),),
        question=QUESTION,
    ),
    Step(
        "not trusted yet",
        "Alice, whom you have not trusted",
        "You import Alice's key under your own label. You hold her key now, "
        "but you have not said you trust her about anything. The signature is "
        "good. Is that enough?",
        "Holding a key is not trusting it. Look for the line that asks whether "
        "Alice may say this.",
        (
            Action(("key", "import", "alice.pub.stmt", "--label", "Alice")),
            check(decides="authorization", code=1),
        ),
        question=QUESTION,
    ),
    Step(
        "trust, check again",
        "Trust Alice, and check again",
        "You decide to trust Alice about build provenance, for the values "
        "reproducible and attested, and nothing else. root list prints that "
        "decision in words. The same check now passes. Then it is run again "
        "as of now, after her statement ran out on 2026-11-01.",
        "Trust is about one kind of claim, and a statement holds only for the "
        "time it names.",
        (
            Action(
                (
                    "root",
                    "add",
                    "Alice",
                    "--as",
                    "me",
                    "--def",
                    "dv-1.def",
                    "--type",
                    "build-provenance",
                    "--values",
                    "reproducible,attested",
                )
            ),
            Action(("root", "list")),
            check(code=0),
            check(at="", decides="authorization", reason="not-valid-at-time", code=1),
        ),
    ),
    Step(
        "change the file",
        "Change one byte of the file",
        "changed.bin is artifact.bin with its first byte replaced by X. "
        "Alice's statement is still valid, but it is not about this file.",
        "The statement names the file by its SHA-256. One byte changes it.",
        (
            Action(
                edit="file",
                note="write changed.bin: artifact.bin with its first byte replaced by X",
            ),
            check(artifact="changed.bin", decides="integrity", code=1),
        ),
    ),
    Step(
        "change the stmt",
        "Flip one bit of Alice's statement",
        "changed.stmt is alice.stmt with one bit of its signature flipped. A "
        "statement that does not verify is thrown out at once, so "
        "authorization is not evaluated, and the exit code is 3.",
        "Nothing a changed statement says is read: V4, the signature, comes "
        "before its contents are used.",
        (
            Action(
                edit="statement",
                note="write changed.stmt: alice.stmt with the last bit of its last byte flipped",
            ),
            check(statement="changed.stmt", decides="integrity", reason="V4", code=3),
        ),
    ),
    Step(
        "sign your own",
        "Sign a statement of your own",
        "Now you are the one who says something: as a reviewer, you approve "
        "artifact.bin. make signs it with your key, for 30 days from now, and "
        "show prints what you would send someone else.",
        "Whoever you send mine.stmt to also needs me.pub.stmt, and has to "
        "decide to trust you, as you did Alice.",
        (
            Action(
                (
                    "make",
                    "--as",
                    "me",
                    "--subject",
                    "artifact.bin",
                    "--def",
                    "dv-1.def",
                    "--type",
                    "outcome",
                    "--value",
                    "approve",
                    "-o",
                    "mine.stmt",
                ),
                secret=True,
            ),
            Action(("show", "mine.stmt")),
        ),
    ),
)

ACTIONS = tuple((n, a) for n, s in enumerate(STEPS) for a in s.actions)


def expected(a: Action) -> str:
    return f"decides {a.decides}" if a.decides else "all six pass"


def shown(argv) -> str:
    return "mofn " + " ".join(quoted(x) for x in argv)


def quoted(arg: str) -> str:
    if arg and all(c.isalnum() or c in "-_./,:=" for c in arg):
        return arg
    return '"' + arg.replace('"', '\\"') + '"'
