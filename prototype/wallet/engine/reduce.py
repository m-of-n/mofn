"""Trust evaluation for v0: coverage (SPEC-0004 §10.2) over one context's
anchors.

Only statements that passed V1–V9 reach this module. v0 has no delegation,
so a path is one hop: an anchor in the evaluated context whose `trusts` is
the attestation's speaker and whose `about` holds a range of the attribute's
type that contains the value. Revocation, rotation and thresholds are not in
v0; the answer says 0 revocation statements were considered.
"""

from dataclasses import dataclass, field

from . import ksatime
from .definition import Definition, conforms_to_template
from .verifier import Verified


@dataclass
class Anchor:
    context: str
    trusts: bytes
    about: list[dict]
    accepted_by: bytes
    accepted_at: int
    source: str = "local"
    note: str | None = None


@dataclass
class Ask:
    context: str
    subject: list
    has: list[dict]
    at: int


@dataclass
class Covered:
    attribute: dict
    statement: Verified
    anchor: Anchor
    scope: dict


@dataclass
class Stopped:
    attribute: dict
    code: str
    detail: str
    statement: Verified | None = None
    anchor: Anchor | None = None


@dataclass
class Coverage:
    covered: list[Covered] = field(default_factory=list)
    stopped: list[Stopped] = field(default_factory=list)
    revocations_considered: int = 0

    @property
    def yes(self) -> bool:
        return not self.stopped and bool(self.covered)


def valid_at(v: Verified, at: int) -> bool:
    valid, t = v.statement.get(5, {}), ksatime.to_seconds(at)
    return (1 not in valid or ksatime.to_seconds(valid[1]) <= t) and (
        2 not in valid or t < ksatime.to_seconds(valid[2])
    )


def evaluate(
    ask: Ask,
    statements: list[Verified],
    anchors: list[Anchor],
    definitions: dict[bytes, Definition],
    attributed: set[bytes],
) -> Coverage:
    result = Coverage()
    mine = [a for a in anchors if a.context == ask.context]
    for attr in ask.has:
        candidates = [
            s
            for s in statements
            if s.kind == 4 and s.this == ask.subject and attr in s.body[1]
        ]
        if not candidates:
            result.stopped.append(
                Stopped(
                    attr, "not-verified", "no verified attestation assigns this value"
                )
            )
            continue
        reasons = []
        for s in candidates:
            hit = _cover(s, attr, ask, mine, definitions, attributed)
            if isinstance(hit, Covered):
                result.covered.append(hit)
                break
            reasons.append(hit)
        else:
            result.stopped += reasons
    return result


def _cover(
    s: Verified,
    attr: dict,
    ask: Ask,
    anchors: list[Anchor],
    definitions: dict[bytes, Definition],
    attributed: set[bytes],
):
    tref, value = attr[1], attr[2]
    if not s.key_in_store:
        return Stopped(
            attr, "unverifiable", "the speaker's key is not in the key store", s
        )
    if not valid_at(s, ask.at):
        return Stopped(
            attr, "not-valid-at-time", f"not valid at {ksatime.to_text(ask.at)}", s
        )
    for a in s.body[1]:
        d = definitions.get(a[1][1])
        if d is None:
            return Stopped(
                attr,
                "definition-unobtainable",
                f"definition {a[1][1].hex()[:16]}… is not held",
                s,
            )
        if a[1][2] not in d.types or not d.valid_assignment(a[1][2], a[2]):
            return Stopped(attr, "type-error", f"{a[2]!r} is not a valid {a[1][2]}", s)
    if 3 in s.body:
        d = definitions.get(s.body[3][1])
        t = d.templates.get(s.body[3][2]) if d else None
        why = (
            "the named template is not held"
            if t is None
            else conforms_to_template(d, t, s.statement)
        )
        if why:
            return Stopped(attr, "template", why, s)
    d = definitions[tref[1]]
    if d.id not in attributed:
        return Stopped(
            attr,
            "unattributed-definition",
            f"{d.name} {d.version} has no verified define statement",
            s,
        )
    trusted = [a for a in anchors if a.trusts == s.says]
    for anchor in trusted:
        for r in anchor.about:
            if r[1] == tref and d.in_range(tref[2], value, r.get(3)):
                return Covered(attr, s, anchor, r)
    if trusted:
        return Stopped(
            attr, "no-path", "trusted, but not about this value", s, trusted[0]
        )
    return Stopped(attr, "no-path", "no anchor in this context trusts the speaker", s)
