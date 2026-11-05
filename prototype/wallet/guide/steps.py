"""The steps of `mofn run`, as data: what the reader is told, the mofn
commands each step runs, and the golden verdict each check must match.

mofn has one wallet, `./wallet` in the folder it is run from. The sender is
someone else, so the guide gives the sender a folder of its own, `sender/`,
and gives you `receiver/`. Every command is a plain `mofn …` run in one of
them; only files cross from one folder to the other.

Nothing here runs anything. `session.py` runs the commands through the CLI
itself, and `screen.py` and `check.py` only show the results.
"""

from dataclasses import dataclass

SENDER = "sender"
RECEIVER = "receiver"
ALICE = "tv-1-alice.pub.stmt"
DEFINE = "tv-3-define.stmt"
FILES = {
    SENDER: ("artifact.bin", "dv-1.def"),
    RECEIVER: ("artifact.bin", "dv-1.def", ALICE, DEFINE),
}
LATER = "2099-01-01T00:00:00Z"


@dataclass(frozen=True)
class Action:
    where: str = RECEIVER
    argv: tuple[str, ...] = ()
    edit: str = ""
    note: str = ""
    golden: str = ""
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


def check(*statements: str, artifact: str = "artifact.bin", extra=()) -> tuple:
    return (
        "check",
        *statements,
        "--artifact",
        artifact,
        "--def",
        "dv-1.def",
        *extra,
        "--format",
        "json",
    )


STEPS = (
    Step(
        "sender and you",
        "The sender's folder, and yours",
        "mofn keeps one wallet, in the folder you run it from. The sender is "
        "someone else, on their own machine; here the sender is mofn run in "
        "another folder, sender/, and you are receiver/. Each runs mofn init "
        "and makes one key, which asks for a passphrase and is kept encrypted. "
        "Then you take Alice's key, the author of the vocabulary the "
        "statements use, and give it your own label.",
        "The passphrase is asked here, in a masked field, and stays in this "
        "program. It never goes on a command line or in the environment.",
        (
            Action(SENDER, ("init",)),
            Action(
                SENDER,
                (
                    "key",
                    "gen",
                    "sender",
                    "--controller",
                    "service",
                    "-o",
                    "sender.pub.stmt",
                ),
                secret=True,
            ),
            Action(RECEIVER, ("init",)),
            Action(RECEIVER, ("key", "gen", "me", "-o", "me.pub.stmt"), secret=True),
            Action(
                RECEIVER,
                ("key", "import", ALICE, "--label", "Alice (definer)"),
            ),
        ),
    ),
    Step(
        "sign a file",
        "The sender signs a file",
        "The sender says one thing about artifact.bin: it was built "
        "reproducibly. show decodes the statement field by field; it does not "
        "verify it. Then the sender hands you two files, the key-publish "
        "statement and prov.stmt, and you import the key under your own label.",
        "A statement holds no names, only key ids and hashes. The label "
        "\"release machine\" is yours, not the sender's.",
        (
            Action(
                SENDER,
                (
                    "make",
                    "--as",
                    "sender",
                    "--subject",
                    "artifact.bin",
                    "--def",
                    "dv-1.def",
                    "--type",
                    "build-provenance",
                    "--value",
                    "reproducible",
                    "-o",
                    "prov.stmt",
                ),
                secret=True,
            ),
            Action(SENDER, ("show", "prov.stmt")),
            Action(
                RECEIVER,
                (
                    "key",
                    "import",
                    "../sender/sender.pub.stmt",
                    "--label",
                    "release machine",
                ),
            ),
        ),
    ),
    Step(
        "not trusted yet",
        "A sender you have not trusted",
        "You hold the sender's key, but you have not said you trust it about "
        "anything. The signature is good. Is that enough?",
        "Holding a key is not trusting it. Look for the line that asks whether "
        "this sender may say this.",
        (
            Action(
                RECEIVER,
                check("../sender/prov.stmt", DEFINE),
                golden="unauthorized",
                code=1,
            ),
        ),
        question="Which line will fail first?  [1–6]",
    ),
    Step(
        "trust, check again",
        "Trust the sender, and check again",
        "You decide to trust the release machine about build provenance, for "
        "the values reproducible and attested, and nothing else. root list "
        "prints that decision in words. The same check now passes.",
        "Trust is about one kind of claim. The same key saying anything else "
        "would still fail authorization.",
        (
            Action(
                RECEIVER,
                (
                    "root",
                    "add",
                    "release machine",
                    "--as",
                    "me",
                    "--def",
                    "dv-1.def",
                    "--type",
                    "build-provenance",
                    "--values",
                    "reproducible,attested",
                ),
            ),
            Action(RECEIVER, ("root", "list")),
            Action(
                RECEIVER,
                check("../sender/prov.stmt", DEFINE),
                golden="green",
                code=0,
            ),
        ),
    ),
    Step(
        "change the file",
        "Change one byte of the file",
        "changed.bin is your artifact.bin with its first byte replaced by X. "
        "The statement is still valid, but it is not about this file.",
        "The statement names the file by its SHA-256. One byte changes it.",
        (
            Action(
                edit="file",
                note="write changed.bin: artifact.bin with its first byte replaced by X",
            ),
            Action(
                RECEIVER,
                check("../sender/prov.stmt", DEFINE, artifact="changed.bin"),
                golden="tampered",
                code=1,
            ),
        ),
    ),
    Step(
        "change the stmt",
        "Flip one bit of the statement",
        "changed.stmt is the sender's prov.stmt with one bit of its signature "
        "flipped. A statement that does not verify is thrown out at once, so "
        "authorization is not evaluated, and the exit code is 3.",
        "Nothing a changed statement says is read: V4, the signature, comes "
        "before its contents are used.",
        (
            Action(
                edit="statement",
                note="write changed.stmt: ../sender/prov.stmt with the last bit of its last byte flipped",
            ),
            Action(
                RECEIVER,
                check("changed.stmt", DEFINE),
                golden="statement-changed",
                code=3,
            ),
        ),
    ),
    Step(
        "vocabulary, expiry",
        "Leave out the vocabulary; check later",
        "First the check is run without Alice's define statement, so nothing "
        "says who published the vocabulary. Then it is run as if it were "
        f"{LATER}, long after the statement's 30 days.",
        "--at sets the time of the check. The statement itself is unchanged.",
        (
            Action(
                RECEIVER,
                check("../sender/prov.stmt"),
                golden="vocabulary-unsigned",
                code=1,
            ),
            Action(
                RECEIVER,
                check("../sender/prov.stmt", DEFINE, extra=("--at", LATER)),
                golden="expired",
                code=1,
            ),
        ),
    ),
)

ACTIONS = tuple((n, a) for n, s in enumerate(STEPS) for a in s.actions)


def shown(argv) -> str:
    return "mofn " + " ".join(quoted(x) for x in argv)


def quoted(arg: str) -> str:
    if arg and all(c.isalnum() or c in "-_./,:=" for c in arg):
        return arg
    return '"' + arg.replace('"', '\\"') + '"'
