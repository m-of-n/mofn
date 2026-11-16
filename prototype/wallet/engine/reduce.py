"""Trust evaluation: delegation paths (SPEC-0004 §6) and coverage (§10.2)
over one context's anchors.

Only statements that passed V1–V9 reach this module. A path starts at an
anchor of the evaluated context (§6.2) and follows trust statements under
§6.3 (`_walk`, `_follow`): each hop must be valid at the evaluation time,
within what the delegator holds (topic *and* range), within its
`may-delegate`, and must not widen it. A hop that fails is not followed, and
is kept as a `Broken` link, so an answer can name the link that broke. An
attestation is covered when a path reaches its speaker with a final scope that
contains the value (`_cover`).

An anchor may trust a name (§4.2), and a trust statement may target one
(§6.3 item 1): both are resolved by `names.py` (§5.3). Revocation and
rotation are applied to name bindings only; for paths and for thresholds they
are not in this version, and the answer says 0 revocation statements were
considered. **Short validity is the revocation mechanism here** (§7.1, §11.3).
Threshold anchors and threshold trust statements (§6.4) start no path.

An anchor may also trust a threshold set (SPEC-0004 §4.2, §6.4; T-043):
*k* of the listed kids. Keys only, no nesting: members are kids, never names
or thresholds. An attribute is covered through it when *k* distinct members
each made an attestation that would be covered by a one-key anchor to that
member with the threshold's `about` — so the same target, type and value.
Distinctness is by kid, and keys that a rotation links count once (§7.2).
Members attest directly: a threshold anchor's `may-delegate`, and threshold
trust statements as hops, are not followed yet (T-095). The answer names
every member, whether it counted, and why not. Reasoning: DL-0042.
"""

from dataclasses import dataclass, field, replace

from . import ksatime
from .definition import Definition, conforms_to_template
from .encoding.ksa_cbor import encode
from .names import T_KEY, T_NAME, Resolution, Resolver, valid_at
from .verifier import Verified

TRUST = 5
MAX_EDGES = 16  # §6.5
MAX_WORK = 4096  # trust-statement edges examined in one evaluation (§6.5, implementation-defined)


@dataclass(frozen=True)
class Threshold:
    """`{ keys: [2* kid], threshold: uint }` (SPEC-0004 §4.2): any `k` of `keys`."""

    keys: tuple[bytes, ...]
    k: int


@dataclass
class Anchor:
    context: str
    trusts: bytes | list | Threshold  # a kid, a name [7, kid, [label, ...]], or k of n kids (SPEC-0004 §4.2)
    about: list[dict]
    accepted_by: bytes
    accepted_at: int
    source: str = "local"
    note: str | None = None
    may_delegate: dict | None = None  # delegation-constraints, SPEC-0002 §8.6
    not_on_or_after: int | None = None  # the source statement's, §6.2 `cap`


def anchor_from(v: Verified, context: str, accepted_by: bytes, accepted_at: int) -> Anchor:
    """The anchor an accepted trust statement makes (§4.3, §6.2)."""
    target = v.this[1] if v.this[0] == T_KEY else v.this
    return Anchor(
        context,
        target,
        v.body[1],
        accepted_by,
        accepted_at,
        f"statement({v.digest.hex()})",
        may_delegate=v.body.get(2),
        not_on_or_after=v.statement.get(5, {}).get(2),
    )

@dataclass
class Ask:
    context: str
    subject: list
    has: list[dict]
    at: int


@dataclass
class Hop:
    """One followed trust statement, and the scope after it (§10.3)."""

    statement: Verified
    key: bytes
    scope: list[dict]


@dataclass
class Reach:
    """The §6.1 state at one key, and the hops that reached it."""

    anchor: Anchor
    key: bytes
    scope: list[dict]
    deleg: dict | None
    cap: int | None
    allow: frozenset | None  # None: every key
    exclude: frozenset
    visited: frozenset
    hops: tuple = ()


@dataclass
class Broken:
    """A link not followed: a trust statement (or, if `link` is None, the
    anchor itself) that failed §6.2 or §6.3, and the key it would have
    reached."""

    anchor: Anchor
    link: Verified | None
    to: bytes
    code: str
    detail: str
    hops: tuple = ()


@dataclass
class Covered:
    attribute: dict
    statement: Verified
    anchor: Anchor
    scope: dict
    path: tuple = ()  # the Hops after the anchor; () for one hop


@dataclass
class Stopped:
    attribute: dict
    code: str
    detail: str
    statement: Verified | None = None
    anchor: Anchor | None = None
    link: Verified | None = None  # the trust statement where the chain broke
    path: tuple = ()  # the Hops followed before it


@dataclass
class Member:
    """One member of a threshold set, as the answer reports it (§10.3)."""

    key: bytes
    counted: bool
    detail: str
    statement: Verified | None = None
    code: str | None = None
    same_as: bytes | None = None  # counted already, as a key a rotation links to this one


@dataclass
class ThresholdCovered:
    attribute: dict
    anchor: Anchor
    scope: dict
    members: list[Member]

    @property
    def statements(self) -> list[Verified]:
        return [m.statement for m in self.members if m.counted]


@dataclass
class ThresholdStopped(Stopped):
    members: list[Member] = field(default_factory=list)


@dataclass
class Coverage:
    covered: list[Covered | ThresholdCovered] = field(default_factory=list)
    stopped: list[Stopped] = field(default_factory=list)
    revocations_considered: int = 0
    names: list[Resolution] = field(default_factory=list)  # §10.3: each name used

    @property
    def yes(self) -> bool:
        return not self.stopped and bool(self.covered)


def evaluate(
    ask: Ask,
    statements: list[Verified],
    anchors: list[Anchor],
    definitions: dict[bytes, Definition],
    attributed: set[bytes],
) -> Coverage:
    result = Coverage()
    mine, unresolved = _resolve_anchors(
        [a for a in anchors if a.context == ask.context], statements, definitions, ask, result
    )
    reached, broken, bounded = _walk(mine, statements, definitions, ask.at)
    if bounded:  # §6.5: a bound yields no, never a partial yes
        result.stopped += [
            Stopped(a, "work-bound", f"more than {MAX_WORK} delegation edges to examine")
            for a in ask.has
        ]
        return result
    for attr in ask.has:
        # §5.3.4: an unresolved name is reported first; it is why its anchor started no path.
        named = [
            Stopped(attr, r.reason, f"{_show(r.name)} resolves to no key", anchor=a)
            for a, r in unresolved
        ]
        candidates = [
            s
            for s in statements
            if s.kind == 4 and s.this == ask.subject and attr in s.body[1]
        ]
        if not candidates:
            result.stopped += named
            result.stopped.append(
                Stopped(
                    attr, "not-verified", "no verified attestation assigns this value"
                )
            )
            continue
        hit = None
        reasons = []
        for s in candidates:
            hit = _cover(s, attr, ask, reached, broken, definitions, attributed)
            if isinstance(hit, Covered):
                result.covered.append(hit)
                break
            reasons.append(hit)
        else:
            met, unmet = _thresholds(attr, ask, statements, mine, definitions, attributed)
            if met:
                result.covered.append(met)
            else:
                # A context that holds a threshold anchor is told first why it was not met.
                result.stopped += named + unmet + reasons
    return result


def _thresholds(attr, ask, statements, anchors, definitions, attributed):
    """§6.4 for each threshold anchor: the first one met, else why each was not."""
    unmet, resolver = [], None
    for a in anchors:
        if not isinstance(a.trusts, Threshold):
            continue
        resolver = resolver or Resolver(statements, definitions, ask.at)
        got = _threshold(a, attr, ask, statements, definitions, attributed, resolver)
        if isinstance(got, ThresholdCovered):
            return got, []
        unmet.append(got)
    return None, unmet


def _threshold(anchor, attr, ask, statements, definitions, attributed, resolver):
    """Count members of `anchor.trusts` that each have a covered attestation.

    Each member is checked as if the anchor were a one-key anchor to it, with
    the threshold's `about` (§6.4: "reached as the start of a sub-path with
    that scope"), so `_cover` gives the same reasons a one-key anchor would.
    """
    th: Threshold = anchor.trusts
    members, heads, scope = [], {}, None
    for key in dict.fromkeys(th.keys):  # distinct by kid
        alone = replace(anchor, trusts=key)
        # One hop only: members attest directly (no statements to walk), so the
        # member is reached exactly as a one-key anchor to it would be.
        reached, broken, _ = _walk([alone], [], definitions, ask.at)
        cands = [
            s
            for s in statements
            if s.kind == 4 and s.says == key and s.this == ask.subject and attr in s.body[1]
        ]
        why = None
        for s in cands:
            hit = _cover(s, attr, ask, reached, broken, definitions, attributed)
            if isinstance(hit, Covered):
                head = resolver.successor(key)
                if head in heads:
                    why = Member(key, False, f"a rotation links it to {_short(heads[head])}, counted already",
                                 s, same_as=heads[head])
                else:
                    heads[head] = key
                    scope = scope or hit.scope
                    why = Member(key, True, "made a covered attestation", s)
                break
            why = why or Member(key, False, hit.detail, s, hit.code)
        members.append(why or Member(key, False, "no verified attestation by this key assigns this value",
                                     code="not-verified"))
    counted = [m for m in members if m.counted]
    if len(counted) >= th.k:
        return ThresholdCovered(attr, anchor, scope, members)
    return ThresholdStopped(
        attr,
        "threshold-not-met",
        f"{th.k} of {len(members)} keys needed, {len(counted)} counted: "
        + "; ".join(f"{_short(m.key)} " + ("counted" if m.counted else f"not counted, {m.detail}") for m in members),
        anchor=anchor,
        members=members,
    )


def _short(kid: bytes) -> str:
    return f"key:{kid.hex()[:16]}…"


def _resolve_anchors(anchors, statements, definitions, ask, result):
    """Replace each name anchor by one anchor per key it resolves to (§5.3, §6.2)."""
    out, unresolved, resolver = [], [], None
    for a in anchors:
        if not (isinstance(a.trusts, list) and a.trusts[0] == T_NAME):
            out.append(a)
            continue
        resolver = resolver or Resolver(statements, definitions, ask.at)
        r = resolver.resolve(a.trusts)
        result.names.append(r)
        if not r.keys:
            unresolved.append((a, r))
        out += [replace(a, trusts=k) for k in sorted(r.keys)]
    return out, unresolved


def _show(name: list) -> str:
    return f"key:{name[1].hex()[:16]}…'s " + " ".join(name[2])


def _cover(
    s: Verified,
    attr: dict,
    ask: Ask,
    reached: list[Reach],
    broken: list[Broken],
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
    trusted = [r for r in reached if r.key == s.says]
    for p in trusted:
        if not _before(ask.at, p.cap):  # §10.2 item 3
            continue
        for r in p.scope:
            if r[1] == tref and d.in_range(tref[2], value, r.get(3)):
                return Covered(attr, s, p.anchor, r, p.hops)
    if trusted:
        p = trusted[0]
        return Stopped(
            attr, "no-path", "trusted, but not about this value", s, p.anchor, path=p.hops
        )
    cut = [b for b in broken if b.to == s.says]
    if cut:  # the speaker was reachable but for this link (§10.3: name it)
        b = cut[0]
        return Stopped(attr, b.code, b.detail, s, b.anchor, b.link, b.hops)
    return Stopped(attr, "no-path", "no anchor in this context trusts the speaker", s)


# ---------------------------------------------------------------- §6 paths


def _before(at: int, cap: int | None) -> bool:
    return cap is None or ksatime.to_seconds(at) < ksatime.to_seconds(cap)


def _earliest(*caps):
    real = [c for c in caps if c is not None]
    return min(real, key=ksatime.to_seconds) if real else None


def _walk(anchors: list[Anchor], statements: list[Verified], definitions, at: int):
    """Every §6.1 state reachable from `anchors` (§6.2), breadth first, and
    every link that was not followed (§6.3). Returns (reached, broken,
    bounded); `bounded` is True when §6.5's work bound was exceeded."""
    trusts = sorted(
        (s for s in statements if s.kind == TRUST and s.this is not None),
        key=lambda s: s.digest,
    )
    resolver = None
    reached, broken, frontier, work = [], [], [], 0
    for a in anchors:
        if not isinstance(a.trusts, bytes):  # a threshold anchor (§6.4)
            continue
        if not _before(at, a.not_on_or_after):
            broken.append(Broken(a, None, a.trusts, "not-valid-at-time", "the anchor's statement has expired"))
            continue
        frontier.append(
            Reach(a, a.trusts, a.about, a.may_delegate, a.not_on_or_after,
                  None, frozenset(), frozenset({a.trusts}))
        )
    while frontier:
        r = frontier.pop(0)
        reached.append(r)
        for s in trusts:
            if s.says != r.key:
                continue
            if s.this[0] == T_NAME:  # §6.3 item 1: each key a name resolves to is an edge
                resolver = resolver or Resolver(statements, definitions, at)
                targets = sorted(resolver.resolve(s.this).keys)
            else:
                targets = [s.this[1]] if s.this[0] == T_KEY else []
            for k in targets:
                if k in r.visited:
                    continue
                work += 1
                if work > MAX_WORK:
                    return reached, broken, True
                nxt = _follow(r, s, k, definitions, at)
                if isinstance(nxt, Reach):
                    frontier.append(nxt)
                else:
                    broken.append(Broken(r.anchor, s, k, *nxt, r.hops))
    return reached, broken, False


def _follow(r: Reach, s: Verified, k: bytes, definitions, at: int):
    """§6.3: the state at `k` after following `s` from `r`, or (code, detail)."""
    if len(r.hops) + 1 >= MAX_EDGES:  # the anchor is the first edge
        return ("work-bound", f"a path may have at most {MAX_EDGES} edges")
    if not s.key_in_store:
        return ("unverifiable", "the delegator's key is not in the key store")
    if not valid_at(s, at):  # item 2; short expiry is how a delegation ends
        after = 2 in s.statement.get(5, {}) and not _before(at, s.statement[5][2])
        return ("not-valid-at-time", "the delegation has expired" if after else "the delegation is not yet valid")
    d = r.deleg
    if d is None or d.get(1, 0) < 1:  # item 3
        return ("depth", "the delegator was not given the right to delegate"
                if d is None else "no delegation depth remains")
    if not _before(at, d.get(5)):
        return ("not-valid-at-time", "the delegator's right to delegate has expired")
    for rng in s.body[1]:  # item 4: topic and range
        why = _range_ok(rng, r.scope, "what the delegator is trusted about", definitions)
        if why is None and 2 in d:
            why = _range_ok(rng, d[2], "what the delegator may pass on", definitions)
        if why:
            return why
    allow = r.allow
    if 3 in d:
        allow = frozenset(d[3]) if allow is None else allow & frozenset(d[3])
    exclude = r.exclude | frozenset(d.get(4, ()))
    if allow is not None and k not in allow:  # item 5
        return ("key-not-allowed", "the delegate's key is not one the chain allows")
    if k in exclude:
        return ("key-excluded", "the delegate's key is one the chain excludes")
    onward = s.body.get(2)
    if onward is not None:  # item 6
        why = _onward_ok(onward, d, s.body[1], allow, exclude, definitions)
        if why:
            return why
    cap = _earliest(r.cap, d.get(5), s.statement.get(5, {}).get(2))
    return Reach(r.anchor, k, s.body[1], onward, cap, allow, exclude,
                 r.visited | {k}, r.hops + (Hop(s, k, s.body[1]),))


def _range_ok(rng: dict, pool: list[dict], where: str, definitions):
    """§6.3 item 4 for one attribute range: delegable, and within some range
    of the same type in `pool`; equal to it if the type's delegation is 1."""
    tref = rng[1]
    d = definitions.get(tref[1])
    if d is None:
        return ("definition-unobtainable", f"definition {tref[1].hex()[:16]}… is not held")
    if tref[2] not in d.types:
        return ("type-error", f"{d.name} {d.version} has no type {tref[2]!r}")
    mode = d.types[tref[2]][8]  # SPEC-0003 §5.4
    if mode == 0:
        return ("type-error", f"{tref[2]} may not be delegated")
    same = [p for p in pool if p[1] == tref]
    if not same:
        return ("widening", f"{tref[2]} is not a topic of {where}")
    if mode == 1:
        ok = any(_same(rng, p) for p in same)
        return None if ok else ("widening", f"{tref[2]} may be delegated only with the same range as {where}")
    ok = any(d.range_within(tref[2], rng.get(3), p.get(3)) for p in same)
    return None if ok else ("widening", f"{_show_range(rng)} is not within {where}")


def _same(a: dict, b: dict) -> bool:
    """`delegation: 1`. Ranges are canonical (SPEC-0003 §6), so the same
    range is the same bytes: this is the comparison, and nothing else is."""
    return encode(a) == encode(b)


def _onward_ok(onward: dict, d: dict, about: list[dict], allow, exclude, definitions):
    """§6.3 item 6: `s.may-delegate` does not widen `deleg`."""
    left = d.get(1, 0) - 1
    if onward.get(1, 0) > left:
        return ("widening", f"it passes on depth {onward.get(1, 0)} where at most {left} remains")
    pool = d.get(2, about)
    for rng in onward.get(2, []):
        why = _range_ok(rng, pool, "what the delegator may pass on", definitions)
        if why:
            return why
    for k in onward.get(3, []):
        if (allow is not None and k not in allow) or k in exclude:
            return ("widening", "its allow-keys admit a key the chain forbids")
    return None


def _show_range(rng: dict) -> str:
    return rng[1][2] + (" {" + ", ".join(map(str, rng[3])) + "}" if 3 in rng else " (any value)")
