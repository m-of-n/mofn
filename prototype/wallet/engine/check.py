"""`mofn check`: verify what was handed over, then evaluate it.

1. Verify every handed statement, V1–V9 (`verifier.py`). Only verified
   statements go further (SPEC-0004 §5.1).
2. Hash the relying party's own copy of the artifact. The ask is about that
   digest, and the integrity line also checks that a verified attestation is
   about it (#65-c2 A1: a proposed addition to SPEC-0004 §10.4).
3. Load the definition and check it is obtained, conforming and attributed.
4. Coverage against this context's anchors (`reduce.py`).
5. Six verdict lines (SPEC-0004 §10.4). The answer is yes only if all six
   pass.

Exit codes: 0 yes, 1 no, 3 a handed statement was invalid.
"""

import hashlib
from dataclasses import dataclass, field

from . import definition as defs, render
from .definition import Definition
from .errors import DefinitionError, Rejected
from .reduce import Anchor, Ask, Coverage, evaluate
from .verifier import Verified, verify

INTEGRITY = {"envelope", "signature", "encoding", "structure", "kind-rule"}


@dataclass
class Handed:
    name: str
    result: str
    step: str | None = None
    reason: str | None = None
    detail: str = ""
    verified: Verified | None = None


@dataclass
class Line:
    name: str
    result: str
    sentence: str


@dataclass
class Answer:
    context: str
    at: int
    subject: list
    handed: list[Handed]
    lines: list[Line]
    sentences: list[str]
    coverage: Coverage | None
    labels: dict = field(default_factory=dict)

    @property
    def yes(self) -> bool:
        return all(ln.result == "pass" for ln in self.lines)

    @property
    def exit_code(self) -> int:
        if any(h.result == "invalid" for h in self.handed):
            return 3
        return 0 if self.yes else 1

    def to_json(self) -> dict:
        name = lambda k: render.key_name(k, self.labels)
        because = []
        if self.coverage:
            for c in self.coverage.covered:
                because.append(
                    {
                        "used": [c.statement.digest.hex()],
                        "path": [
                            {
                                "anchor": c.anchor.source,
                                "accepted-by": name(c.anchor.accepted_by),
                                "key": name(c.anchor.trusts),
                                "kid": c.anchor.trusts.hex(),
                                "scope": {c.scope[1][2]: c.scope.get(3, "any")},
                            }
                        ],
                        "covered": {c.attribute[1][2]: c.attribute[2]},
                        "checks": ["verified", "types", "valid-at-time", "coverage"],
                    }
                )
            for s in self.coverage.stopped:
                because.append(
                    {
                        "candidate": s.statement.digest.hex() if s.statement else None,
                        "attribute": {s.attribute[1][2]: s.attribute[2]},
                        "reason": s.code,
                        "detail": s.detail,
                    }
                )
        for h in self.handed:
            if h.result != "verified":
                because.append(
                    {
                        "statement": h.name,
                        "reason": "not-verified"
                        if h.result == "invalid"
                        else "unverifiable",
                        "step": h.step,
                        "code": h.reason,
                        "detail": h.detail,
                    }
                )
        because.append({"revocations considered": 0})
        return {
            "answer": "yes" if self.yes else "no",
            "at": render.time_text(self.at),
            "context": self.context,
            "subject": render.target(self.subject, {}),
            "because": because,
            "verdict": {
                ln.name: {
                    "result": ln.result.replace(" ", "-"),
                    "sentence": ln.sentence,
                }
                for ln in self.lines
            },
            "statements": [
                {
                    "file": h.name,
                    "result": h.result,
                    "step": h.step,
                    "reason": h.reason,
                    "digest": h.verified.digest.hex() if h.verified else None,
                }
                for h in self.handed
            ],
            "sentences": self.sentences,
            "limit": render.LIMIT,
        }


def handed(
    name: str, envelope: bytes | None, keystore, load_error: str | None = None
) -> Handed:
    if envelope is None:
        return Handed(name, "invalid", "V1", "envelope", load_error or "")
    try:
        return Handed(name, "verified", verified=verify(envelope, keystore))
    except Rejected as r:
        return Handed(name, r.result, r.step, r.reason, r.detail)


def run(
    items: list[Handed],
    artifact: bytes,
    definition_bytes: bytes,
    labels: dict[bytes, str],
    anchors: list[Anchor],
    context: str,
    at: int,
) -> Answer:
    verified = [h.verified for h in items if h.verified]
    subject = [2, 1, hashlib.sha256(artifact).digest()]
    attestations = [v for v in verified if v.kind == 4]
    about = [a for a in attestations if a.this == subject]

    d, def_error = None, None
    try:
        d = defs.load(definition_bytes)
    except DefinitionError as e:
        def_error = e
    referenced = {a[1][1] for s in (about or attestations) for a in s.body[1]}
    define = defs.attributed(d, verified) if d else None
    held = {d.id: d} if d and (not referenced or d.id in referenced) else {}
    attributed = {d.id} if d and define and define.key_in_store else set()

    has = []
    for s in about:
        for a in s.body[1]:
            if a not in has:
                has.append(a)
    ask = Ask(context, subject, has, at)
    coverage = evaluate(ask, about, anchors, held, attributed) if about else None

    used = about + ([define] if define else [])
    lines = [
        _integrity(items, attestations, about, subject),
        _authenticity(items, used, labels),
        _names(used, labels),
        _authorization(about, coverage, d, context, labels),
        _acceptance(about, held),
        _semantics(d, def_error, referenced, define, labels),
    ]
    sentences = [
        render.sentence(held.get(s.body[1][0][1][1]), s.statement, labels)
        for s in (about or attestations)
    ]
    return Answer(context, at, subject, items, lines, sentences, coverage, labels)


def _integrity(items, attestations, about, subject) -> Line:
    bad = [h for h in items if h.result == "invalid" and h.reason in INTEGRITY]
    if bad:
        h = bad[0]
        more = f" (and {len(bad) - 1} more)" if len(bad) > 1 else ""
        return Line(
            "integrity",
            "fail",
            f"{h.name} is invalid at {h.step} ({h.reason}) and was not used{more}",
        )
    if attestations and not about:
        claimed = render.target(attestations[0].this, {})
        return Line(
            "integrity",
            "fail",
            f"your file is not the one described: it hashes to "
            f"{render.target(subject, {})}, the statement is about {claimed}",
        )
    if not about:
        return Line(
            "integrity",
            "not evaluated",
            "no verified attestation to compare your file with",
        )
    return Line(
        "integrity",
        "pass",
        "every statement verified, and your file is the one described",
    )


def _authenticity(items, used, labels) -> Line:
    for h in items:
        if h.result == "unverifiable" and h.reason == "unknown-key":
            return Line(
                "authenticity",
                "fail",
                f"{h.name}: the speaker's key is not in your key store",
            )
        if h.result == "unverifiable":
            return Line("authenticity", "fail", f"{h.name}: {h.detail}")
        if h.result == "invalid" and h.reason not in INTEGRITY:
            return Line(
                "authenticity", "fail", f"{h.name} is invalid at {h.step} ({h.reason})"
            )
    for v in used:
        if not v.key_in_store:
            return Line(
                "authenticity",
                "fail",
                f"{render.key_name(v.says, labels)} signed with a key that is "
                f"not in your key store",
            )
    return Line(
        "authenticity",
        "pass",
        "every speaker's key is in your key store, and each envelope "
        "agrees with its statement",
    )


def _names(used, labels) -> Line:
    if all(v.says in labels for v in used):
        return Line("names", "pass", "every key is shown by your own label for it")
    return Line("names", "pass", "keys you have not labelled are shown by fingerprint")


def _authorization(about, coverage, d, context, labels) -> Line:
    if not about or coverage is None:
        return Line(
            "authorization",
            "not evaluated",
            "no verified statement handed over is about your file",
        )
    if coverage.yes:
        c = coverage.covered[0]
        label = c.scope[1][2]
        rng = c.scope.get(3)
        scope = (
            ", ".join(render.value_text(d, label, v, 2).lower() for v in rng)
            if rng
            else "any value"
        )
        return Line(
            "authorization",
            "pass",
            f"{render.key_name(c.anchor.trusts, labels)} is trusted in "
            f"context {context} about {render.type_name(d, label)} ({scope})",
        )
    s = coverage.stopped[0]
    who = render.key_name(s.statement.says, labels) if s.statement else "the speaker"
    label = s.attribute[1][2]
    if s.code == "no-path" and s.anchor is None:
        text = (
            f"{who} was never given the right to say this: no anchor in context {context} trusts it "
            f"about {render.type_name(d, label)}"
        )
    elif s.code == "no-path":
        text = (
            f"{who} is trusted in context {context}, but not about {render.type_name(d, label)} "
            f"= {render.value_text(d, label, s.attribute[2], 2).lower()}"
        )
    else:
        text = f"{s.detail} ({s.code})"
    return Line("authorization", "fail", text)


def _acceptance(about, held) -> Line:
    if not about:
        return Line(
            "acceptance",
            "not evaluated",
            "no verified statement handed over is about your file",
        )
    for s in about:
        if 3 in s.body:
            d = held.get(s.body[3][1])
            t = d.templates.get(s.body[3][2]) if d else None
            if t is None:
                return Line(
                    "acceptance",
                    "fail",
                    "the named template is not in a definition you hold",
                )
            why = defs.conforms_to_template(d, t, s.statement)
            if why:
                return Line("acceptance", "fail", why)
            return Line(
                "acceptance",
                "pass",
                f"conforms to the template {render.lang(t[9]).lower()}",
            )
    return Line("acceptance", "pass", "no template is named")


def _semantics(d: Definition | None, error, referenced, define, labels) -> Line:
    if d is None:
        return Line(
            "semantics",
            "fail",
            f"the definition cannot be used: {error.detail} ({error.reason})",
        )
    if referenced and d.id not in referenced:
        return Line(
            "semantics",
            "fail",
            f"the definition you gave is definition:{d.id[:8].hex()}, not the one "
            f"the statement names (definition-unobtainable)",
        )
    if define is None:
        return Line(
            "semantics",
            "fail",
            f"{d.name} {d.version} is unattributed: no verified define statement by "
            f"its definer was handed over (unattributed-definition)",
        )
    if not define.key_in_store:
        return Line(
            "semantics",
            "fail",
            f"{d.name} {d.version} is published by a key that is not in your key store",
        )
    return Line(
        "semantics",
        "pass",
        f"{d.name} {d.version} is published by its definer, "
        f"{render.key_name(d.definer, labels)}",
    )
