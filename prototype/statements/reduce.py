"""Reduction — follow a chain of signed statements to decide whether to trust one.

SPIKE. Not normative.

Sponsor, 2026-09-22: "The reduction process is simply taking a set of
cryptographically signed statements and then following the chain of inference
to determine if you trust the statement."

Earlier documents made this far more ceremonious than it is. There is no
5-tuple ritual here. There is:

    a claim you were handed
    a set of statements you also hold
    a set of trust roots you decided on yourself

...and the question "does anything connect the claim back to a root I trust,
for THIS kind of statement, within THIS range?"

Three things each step must check, and they are the whole algorithm:
    1. who said it, and is that key reachable from a root
    2. was the speaker entitled to speak on this topic
    3. does the range still cover the value after every narrowing
"""
from __future__ import annotations
from dataclasses import dataclass, field
import fnmatch


# ── ranges ────────────────────────────────────────────────────────────────
def covers(outer: str, inner: str) -> bool:
    """Does `outer` cover `inner`? Patterns are globs: '*@foo.com'."""
    if outer == inner:
        return True
    return fnmatch.fnmatchcase(inner, outer)


def narrow(a: str, b: str) -> str | None:
    """Intersection of two ranges. SPKI calls this tag intersection; for a
    glob range it is just 'the narrower one, if one contains the other'."""
    if covers(a, b):
        return b
    if covers(b, a):
        return a
    return None          # disjoint — the chain is broken here


# ── what a verifier holds ─────────────────────────────────────────────────
@dataclass
class TrustRoot:
    """A decision the verifier made for itself. Unsigned - it is local policy,
    which is why ARCH-0001's AclEntry has no speaker."""
    key: str
    topic: str
    range: str


@dataclass
class Delegation:
    """A says B may speak about (topic, range). A DIFFERENT TYPE from the
    base attestation - sponsor's note, and it matters: without a distinct
    type, holding a delegation would be indistinguishable from holding a
    claim, and anyone could promote themselves."""
    speaker: str
    subject: str
    topic: str
    range: str


@dataclass
class Attestation:
    """A says SUBJECT has VALUE, in some topic."""
    speaker: str
    subject: str
    topic: str
    value: str


@dataclass
class Step:
    why: str
    ok: bool


@dataclass
class Verdict:
    trusted: bool
    steps: list[Step] = field(default_factory=list)
    reason: str = ""

    def explain(self) -> str:
        out = []
        for s in self.steps:
            out.append(f"    {'ok  ' if s.ok else 'FAIL'}  {s.why}")
        out.append(f"\n    → {'TRUSTED' if self.trusted else 'NOT TRUSTED'}: {self.reason}")
        return "\n".join(out)


def reduce_chain(claim: Attestation, delegations: list[Delegation],
                 roots: list[TrustRoot], *, max_depth: int = 8) -> Verdict:
    """Walk back from the claim to a trust root, narrowing the range as we go."""
    v = Verdict(trusted=False)

    # Step 1 - is the claim's own speaker directly trusted for this topic?
    for r in roots:
        if r.key == claim.speaker and r.topic == claim.topic and covers(r.range, claim.value):
            v.steps.append(Step(f"{claim.speaker} is a trust root for {claim.topic} in {r.range}", True))
            v.trusted = True
            v.reason = f"{claim.speaker} is directly trusted for {claim.topic}"
            return v

    # Step 2 - otherwise, find a chain of delegations back to a root
    current, reach, depth = claim.speaker, None, 0
    v.steps.append(Step(f"{claim.speaker} says {claim.subject} has {claim.topic} = {claim.value}", True))

    while depth < max_depth:
        depth += 1
        deleg = next((d for d in delegations
                      if d.subject == current and d.topic == claim.topic), None)
        if deleg is None:
            v.steps.append(Step(f"nobody delegated {claim.topic} to {current}", False))
            v.reason = f"no delegation reaches {current} for {claim.topic}"
            return v

        reach = deleg.range if reach is None else narrow(reach, deleg.range)
        if reach is None:
            v.steps.append(Step(f"{deleg.speaker} delegates {deleg.range} — disjoint from the chain so far", False))
            v.reason = "ranges do not intersect; the chain narrows to nothing"
            return v
        v.steps.append(Step(f"{deleg.speaker} says {current} may speak about "
                            f"{claim.topic} in {deleg.range}  (reach now {reach})", True))
        current = deleg.speaker

        for r in roots:
            if r.key == current and r.topic == claim.topic:
                final = narrow(r.range, reach)
                if final is None:
                    v.steps.append(Step(f"{current} is a root but for {r.range}, disjoint", False))
                    v.reason = "root's range does not intersect the delegated reach"
                    return v
                v.steps.append(Step(f"{current} is a trust root for {claim.topic} in {r.range}", True))
                if not covers(final, claim.value):
                    v.steps.append(Step(f"{claim.value} is outside {final}", False))
                    v.reason = f"the claim falls outside the authorised range {final}"
                    return v
                v.steps.append(Step(f"{claim.value} is within {final}", True))
                v.trusted = True
                v.reason = f"chain reaches root {current}, range {final} covers {claim.value}"
                return v

    v.reason = f"no trust root within {max_depth} steps"
    return v
