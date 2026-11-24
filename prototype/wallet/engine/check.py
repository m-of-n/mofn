"""`mofn check`: verify what was handed over, then evaluate it.

1. Verify every handed statement, V1–V9 (`verifier.py`). Only verified
   statements go further (SPEC-0004 §5.1).
2. Hash the relying party's own copy of the artifact. The ask is about that
   digest, and the integrity line also checks that a verified attestation is
   about it (SPEC-0004 §10.4, as proposed in 0.2.0). Where the ask is about a
   key instead (`--subject-key`, W-8), the subject is that kid and there is no
   copy to hash: §10.4 conditions the comparison on a digest target, so the
   integrity line reports verification alone.
3. Load the definition and check it is obtained, conforming and attributed.
4. Coverage against this context's anchors (`reduce.py`), through any
   delegation path the handed trust statements make (SPEC-0004 §6).
5. Six verdict lines (SPEC-0004 §10.4). The answer is yes only if all six
   pass.

`lang` picks the language of the vocabulary's own text in the lines and
sentences (`render.lang`); it changes no result.

Exit codes: 0 yes, 1 no, 3 a handed statement was invalid.
"""

from dataclasses import dataclass, field

from . import definition as defs, render, statement
from .definition import Definition
from .errors import DefinitionError, Rejected
from .reduce import Anchor, Ask, Coverage, Member, ThresholdCovered, evaluate
from . import schema
from .schema import TARGET
from .verifier import Verified, verify

# A vacuous pass (SPEC-0004 §10.4, DL-0020 A1): the sentence says why there
# is nothing to fail (mofn#157 F-2).
NO_TEMPLATE = "no template is named, so there is none to meet"

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
    # False when no verified attestation is about the relying party's copy, so
    # the sentences describe another file (mofn#157 F-1, SPEC-0004 §10.4).
    sentences_about_your_file: bool = True
    # The verified attestations the answer describes, and the definition held
    # for them: what `associations` reads (W-5, mofn#69).
    described: list = field(default_factory=list)
    definition: Definition | None = None

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
                if isinstance(c, ThresholdCovered):
                    because.append(_threshold_json(c, name))
                    continue
                because.append(
                    {
                        "used": [c.statement.digest.hex()],
                        "path": [
                            {
                                "anchor": c.anchor.source,
                                "accepted-by": name(c.anchor.accepted_by),
                                "key": name(c.anchor.trusts),
                                "kid": c.anchor.trusts.hex(),
                                "scope": _scope_json(c.anchor.about),
                            }
                        ]
                        + [
                            {
                                "trust": h.statement.digest.hex(),
                                "key": name(h.key),
                                "kid": h.key.hex(),
                                "scope": _scope_json(h.scope),
                            }
                            for h in c.path
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
                        **({"link": s.link.digest.hex()} if s.link else {}),
                        **(
                            {"members": [_member_json(m, name) for m in s.members]}
                            if hasattr(s, "members")
                            else {}
                        ),
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
            # Which target type the ask was about, and the kid itself when it
            # was a key (W-8). `subject` stays the string it has always been.
            "subject-target": schema.TARGETS[self.subject[0]],
            "subject-key": (
                self.subject[1].hex() if self.subject[0] == TARGET["key"] else None
            ),
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
            "sentences_about_your_file": self.sentences_about_your_file,
            "associations": associations(self),
            "limit": render.LIMIT,
        }


# ------------------------------------------------- attribute associations (W-5)
#
# One entry per (attestation, attribute) the answer describes: who signed,
# the topic, the subject's digest, and standing. Read from the reduction's own
# result (`Coverage`); nothing here decides coverage. The shape is documented in
# README.md, "The verdict as JSON", and is what `mofn run` and W-7 render.


def associations(answer: Answer) -> list[dict]:
    files = {h.verified.digest: h.name for h in answer.handed if h.verified}
    d = answer.definition
    out = []
    for s in answer.described:
        for a in s.body.get(1, []):
            out.append(
                {
                    "statement": s.digest.hex(),
                    "file": files.get(s.digest),
                    "signed-by": _signed_by(s.says, answer),
                    "topic": _topic(a, d),
                    "subject": _subject(s.this, answer.subject, answer.labels),
                    "standing": _standing(s, a, answer),
                }
            )
    return out


def _signed_by(kid: bytes, answer: Answer) -> dict:
    names = answer.coverage.names if answer.coverage else []
    principal = next(
        (render.name_text(r.name, answer.labels) for r in names if kid in r.keys), None
    )
    return {
        "key": render.key_name(kid, answer.labels),
        "kid": kid.hex(),
        "label": answer.labels.get(kid),
        "principal": principal,
    }


def _topic(a: dict, d: Definition | None) -> dict:
    tref, value = a[1], a[2]
    known = d is not None and d.id == tref[1]
    return {
        "domain": f"{d.name} {d.version}" if known else f"definition:{tref[1][:8].hex()}",
        "definition": tref[1].hex(),
        "type": tref[2],
        "type-name": render.type_name(d if known else None, tref[2]),
        "value": value.hex() if isinstance(value, bytes) else value,
        "value-name": render.value_text(d if known else None, tref[2], value, 2),
    }


def _subject(this, yours: list, labels: dict | None = None) -> dict:
    """What the statement is about, and what you asked about.

    A digest ask keeps exactly the shape W-5 fixed (DL-0049), so the goldens
    do not move. A key ask adds the key in the same words `signed-by` uses,
    and keeps `digest` present as null so a reader written for W-7 does not
    raise (W-8, mofn#180)."""

    def full(t):
        if t and t[0] == TARGET["digest"]:
            return render.target(t, {}).split(":")[0] + ":" + t[2].hex()
        if t and t[0] == TARGET["key"]:
            return t[1].hex()
        return render.target(t, {}) if t else None

    if yours and yours[0] == TARGET["key"]:
        names = labels or {}
        is_key = bool(this) and this[0] == TARGET["key"]
        return {
            "target": "key",
            "key": render.key_name(this[1], names) if is_key else None,
            "kid": this[1].hex() if is_key else None,
            "label": names.get(this[1]) if is_key else None,
            "digest": full(this) if this and not is_key else None,
            "yours": full(yours),
            "matches": this == yours,
        }
    return {"digest": full(this), "yours": full(yours), "matches": this == yours}


def _standing(s, a: dict, answer: Answer) -> dict:
    """What the reduction found for this statement and attribute (§10.3)."""
    name = lambda k: render.key_name(k, answer.labels)
    cov = answer.coverage
    if cov is None:
        return {
            "result": "not-evaluated",
            "chain": [],
            "text": "no standing: not evaluated, the statement is not about "
            + _about_what(answer.subject),
            "reason": None,
            "detail": "no verified statement handed over is about "
            + _about_what(answer.subject),
        }
    for c in cov.covered:
        if c.attribute != a:
            continue
        if isinstance(c, ThresholdCovered):
            if s.digest not in {x.digest for x in c.statements}:
                continue
            th = c.anchor.trusts
            chain = [
                _root(c.anchor, s.says, name)
                | {"threshold": {"k": th.k, "n": len(set(th.keys))}}
            ]
        elif c.statement.digest == s.digest:
            chain = [_root(c.anchor, c.anchor.trusts, name)] + _hops(c.path, name)
        else:
            continue
        return {
            "result": "standing",
            "chain": chain,
            "text": _chain_text(chain),
            "reason": None,
            "detail": None,
        }
    for st in cov.stopped:
        if st.attribute != a:
            continue
        mine = st.statement is not None and st.statement.digest == s.digest
        member = any(
            m.statement is not None and m.statement.digest == s.digest
            for m in getattr(st, "members", [])
        )
        if not (mine or member or st.statement is None):
            continue
        chain = []
        if st.anchor is not None and isinstance(st.anchor.trusts, bytes):
            chain = [_root(st.anchor, st.anchor.trusts, name)] + _hops(st.path, name)
        out = {
            "result": "no-standing",
            "chain": chain,
            "text": f"no standing: {st.detail} ({st.code})",
            "reason": st.code,
            "detail": st.detail,
        }
        if st.link is not None:  # name the link that broke (W-3)
            out["broken"] = {
                "trust": st.link.digest.hex(),
                "from": name(st.link.says),
                "to": name(s.says),
            }
            out["text"] = (
                f"no standing: {_chain_text(chain)} ✗ {name(s.says)}: "
                f"{st.detail} ({st.code})"
            )
        return out
    return {
        "result": "not-evaluated",
        "chain": [],
        "text": "no standing: not evaluated, another statement covered this value",
        "reason": None,
        "detail": "another statement handed over covered this value",
    }


def _root(anchor: Anchor, key: bytes, name) -> dict:
    return {
        "role": "root",
        "anchor": anchor.source,
        "accepted-by": name(anchor.accepted_by),
        "key": name(key),
        "kid": key.hex(),
    }


def _hops(path, name) -> list[dict]:
    return [
        {
            "role": "delegation",
            "trust": h.statement.digest.hex(),
            "key": name(h.key),
            "kid": h.key.hex(),
        }
        for h in path
    ]


def _chain_text(chain: list[dict]) -> str:
    root = chain[0]
    first = (
        f"{root['threshold']['k']} of {root['threshold']['n']} keys, rooted by "
        f"{root['accepted-by']}; {root['key']} counted"
        if "threshold" in root
        else f"{root['key']} (root, accepted by {root['accepted-by']})"
    )
    return " → ".join([first] + [h["key"] for h in chain[1:]])


def _scope_json(about: list[dict]) -> dict:
    return {r[1][2]: r.get(3, "any") for r in about}


def _member_json(m: Member, name) -> dict:
    return {
        "key": name(m.key),
        "kid": m.key.hex(),
        "counted": m.counted,
        "statement": m.statement.digest.hex() if m.statement else None,
        "reason": m.code,
        "detail": m.detail,
    }


def _threshold_json(c: ThresholdCovered, name) -> dict:
    """§10.3 for a threshold: every member, and the statement each counted with."""
    th = c.anchor.trusts
    return {
        "used": [s.digest.hex() for s in c.statements],
        "path": [
            {
                "anchor": c.anchor.source,
                "accepted-by": name(c.anchor.accepted_by),
                "threshold": {"k": th.k, "n": len(set(th.keys))},
                "members": [_member_json(m, name) for m in c.members],
                "scope": {c.scope[1][2]: c.scope.get(3, "any")},
            }
        ],
        "covered": {c.attribute[1][2]: c.attribute[2]},
        "checks": ["verified", "types", "valid-at-time", "coverage", "threshold"],
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
    lang: str | None = None,
    subject_key: bytes | None = None,
) -> Answer:
    if (artifact is None) == (subject_key is None):
        raise ValueError("check takes an artifact or a subject key, not both")
    verified = [h.verified for h in items if h.verified]
    subject = (
        statement.key_target(subject_key)
        if artifact is None
        else statement.digest_target(artifact)
    )
    attestations = [v for v in verified if v.kind == 4]
    about = [a for a in attestations if a.this == subject]
    trusts = [v for v in verified if v.kind == 5]  # delegation hops (SPEC-0004 §6.3)

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
    coverage = evaluate(ask, about + trusts, anchors, held, attributed) if about else None

    hops = [h.statement for c in (coverage.covered if coverage else []) for h in c.path]
    used = about + hops + ([define] if define else [])
    lines = [
        _integrity(items, attestations, about, subject),
        _authenticity(items, used, labels),
        _names(used, labels),
        _authorization(about, coverage, d, context, labels, lang, subject),
        _acceptance(about, held, lang, subject),
        _semantics(d, def_error, referenced, define, labels),
    ]
    sentences = [
        render.sentence(held.get(s.body[1][0][1][1]), s.statement, labels, lang)
        for s in (about or attestations)
    ]
    return Answer(
        context, at, subject, items, lines, sentences, coverage, labels, bool(about),
        described=about or attestations, definition=held.get(d.id) if d else None,
    )


def _about_what(subject) -> str:
    """The noun §10.4's sentences use for the ask's subject. A digest ask is
    about the relying party's own file; a key ask is about a key."""
    return "your file" if subject is None or subject[0] == TARGET["digest"] else "that key"


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
    if subject[0] != TARGET["digest"]:
        # SPEC-0004 §10.4 conditions the comparison clause on a digest target:
        # "every statement used decoded canonically and its signature verified,
        # AND, WHERE THE SUBJECT IS A DIGEST TARGET ... at least one is about
        # the relying party's own copy". With a key subject there is no copy of
        # the verifier's to substitute, so the first clause stands alone.
        # Whether any statement is about that key is authorization's and
        # acceptance's question, which §10.4 assigns to them.
        if not attestations:
            return Line(
                "integrity",
                "not evaluated",
                "no verified attestation was handed over",
            )
        return Line(
            "integrity",
            "pass",
            "every statement verified; the subject is a key, so there is no "
            "copy of yours to compare",
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


def _authorization(about, coverage, d, context, labels, lang=None, subject=None) -> Line:
    if not about or coverage is None:
        return Line(
            "authorization",
            "not evaluated",
            f"no verified statement handed over is about {_about_what(subject)}",
        )
    if coverage.yes:
        c = coverage.covered[0]
        label = c.scope[1][2]
        rng = c.scope.get(3)
        scope = (
            ", ".join(render.value_text(d, label, v, 2, lang).lower() for v in rng)
            if rng
            else "any value"
        )
        if isinstance(c, ThresholdCovered):
            who = ", ".join(render.key_name(s.says, labels) for s in c.statements)
            return Line(
                "authorization",
                "pass",
                f"{c.anchor.trusts.k} of {len(set(c.anchor.trusts.keys))} keys are trusted together in "
                f"context {context} about {render.type_name(d, label, lang)} ({scope}), and {who} agree",
            )
        speaker = c.path[-1].key if c.path else c.anchor.trusts
        via = (
            f", through {_chain(c.anchor, c.path, labels)}" if c.path else ""
        )
        return Line(
            "authorization",
            "pass",
            f"{render.key_name(speaker, labels)} is trusted in "
            f"context {context} about {render.type_name(d, label, lang)} ({scope}){via}",
        )
    s = coverage.stopped[0]
    who = render.key_name(s.statement.says, labels) if s.statement else "the speaker"
    label = s.attribute[1][2]
    if s.link is not None:  # W-3: name the link that broke
        broke = f"{render.key_name(s.link.says, labels)} → {render.key_name(s.statement.says, labels)}"
        text = f"the delegation {broke} is broken: {s.detail} ({s.code})"
    elif s.code == "no-path" and s.anchor is None:
        text = (
            f"{who} was never given the right to say this: no anchor in context {context} trusts it "
            f"about {render.type_name(d, label, lang)}"
        )
    elif s.code == "no-path":
        text = (
            f"{who} is trusted in context {context}, but not about {render.type_name(d, label, lang)} "
            f"= {render.value_text(d, label, s.attribute[2], 2, lang).lower()}"
        )
    elif s.code == "threshold-not-met":
        th = s.anchor.trusts
        counted = [render.key_name(m.key, labels) for m in s.members if m.counted]
        missing = [render.key_name(m.key, labels) for m in s.members if not m.counted]
        text = (
            f"{th.k} of {len(s.members)} keys must agree in context {context} about "
            f"{render.type_name(d, label, lang)}, and {len(counted)} did"
            + (f" ({', '.join(counted)})" if counted else "")
            + f"; not counted: {', '.join(missing)} (threshold-not-met)"
        )
    else:
        text = f"{s.detail} ({s.code})"
    return Line("authorization", "fail", text)


def _chain(anchor, path, labels) -> str:
    keys = [anchor.trusts] + [h.key for h in path]
    return " → ".join(render.key_name(k, labels) for k in keys)


def _acceptance(about, held, lang=None, subject=None) -> Line:
    if not about:
        return Line(
            "acceptance",
            "not evaluated",
            f"no verified statement handed over is about {_about_what(subject)}",
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
                f"conforms to the template {render.lang(t[9], lang).lower()}",
            )
    return Line("acceptance", "pass", NO_TEMPLATE)


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
