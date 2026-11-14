"""SDSI name resolution (SPEC-0004 §5.3; ADR-0008; T-040).

`resolve` rewrites a name `[7, issuer, [label, ...]]` to the set of keys it
denotes at one evaluation time. It runs before coverage and takes nothing from
it: no anchor is consulted, and a binding confers no trust (§5.3.1). Coverage
(`reduce.py`) uses only the resulting keys.

Inputs are statements that passed V1–V9. A binding is used only if its
speaker's key is in the key store, every type it references is held and its
values are valid (§5.2), it is valid at the time, it is not revoked (§7.1), and
§7.2 still uses it after a rotation. v0 does not read compromise marks
(SPEC-0001 §9.6), and of two rotations from one key it follows the earlier.
"""

from dataclasses import dataclass, field

from . import ksatime
from .definition import Definition
from .errors import DefinitionError
from .verifier import Verified

T_KEY, T_NAME = 1, 7
KEY_PUBLISH, ATTESTATION, REVOKE, ROTATE = 1, 4, 6, 7
MAX_DEPTH = 16  # §5.3.5
MAX_ROTATIONS = 4  # §7.2


def valid_at(v: Verified, at: int) -> bool:
    valid, t = v.statement.get(5, {}), ksatime.to_seconds(at)
    return (1 not in valid or ksatime.to_seconds(valid[1]) <= t) and (
        2 not in valid or t < ksatime.to_seconds(valid[2])
    )


@dataclass(frozen=True)
class Failure:
    """One failing branch (§5.3.4), or `work-bound` for the whole name (§5.3.5)."""

    code: str
    issuer: bytes
    label: str | None
    detail: str


@dataclass
class Resolution:
    name: list
    keys: set[bytes] = field(default_factory=set)
    bindings: list[Verified] = field(default_factory=list)  # the bindings used, in order
    failures: list[Failure] = field(default_factory=list)

    @property
    def resolved(self) -> bool:
        return bool(self.keys)

    @property
    def reason(self) -> str | None:
        """None when the name resolved; else the code of the first failure."""
        if self.keys:
            return None
        bound = [f for f in self.failures if f.code == "work-bound"]
        return (bound or self.failures)[0].code if self.failures else "name-unresolved"


class _Bound(Exception):
    pass


class Resolver:
    """The usable bindings and rotation links of one statement set at one time."""

    def __init__(self, statements: list[Verified], definitions: dict[bytes, Definition], at: int):
        self.at = at
        live = [s for s in statements if s.key_in_store and valid_at(s, at)]
        revoked = {
            (r.says, r.body.get(1))
            for r in live
            if r.kind == REVOKE and 1 in r.statement.get(5, {})
        }
        live = [s for s in live if (s.says, s.digest) not in revoked]
        published = {s.says for s in live if s.kind == KEY_PUBLISH and s.this == [T_KEY, s.says]}
        # §7.2: K → (K′, issued of the rotate); the link needs K′'s own key-publish
        # and a not-before at or before the time.
        self.links: dict[bytes, tuple[bytes, int | None]] = {}
        for r in sorted(
            (r for r in live if r.kind == ROTATE and 1 in r.statement.get(5, {})),
            key=lambda r: ksatime.to_seconds(r.statement[5].get(3, r.statement[5][1])),
        ):
            this = r.this
            if this and this[0] == T_KEY and this[1] in published and r.says not in self.links:
                self.links[r.says] = (this[1], r.statement[5].get(3))
        self.bindings: list[tuple[Verified, str]] = []
        for s in live:
            if s.kind != ATTESTATION or not s.this or s.this[0] not in (T_KEY, T_NAME):
                continue
            if not self._past_only(s):
                continue
            labels = _naming_labels(s, definitions)
            self.bindings += [(s, label) for label in labels or ()]

    def _past_only(self, s: Verified) -> bool:
        """§7.2: after a link, the old key's statements count only if issued earlier."""
        link = self.links.get(s.says)
        if link is None:
            return True
        issued, cut = s.statement.get(5, {}).get(3), link[1]
        return issued is not None and cut is not None and ksatime.to_seconds(issued) < ksatime.to_seconds(cut)

    def successor(self, k: bytes) -> bytes:
        for _ in range(MAX_ROTATIONS):
            if k not in self.links:
                return k
            k = self.links[k][0]
        if k in self.links:
            raise _Bound(f"more than {MAX_ROTATIONS} rotations")
        return k

    def namespace(self, k: bytes) -> set[bytes]:
        """`k`'s namespace: its successor and every key that rotates into it (§5.3.2 step 2)."""
        head = self.successor(k)
        return {j for j in {k, head, *self.links} if self.successor(j) == head}

    def resolve(self, name: list) -> Resolution:
        out = Resolution(name)
        try:
            out.keys = self._resolve(name[1], tuple(name[2]), 1, set(), out)
        except _Bound as e:
            out.keys = set()
            out.failures.append(Failure("work-bound", name[1], None, str(e)))
        return out

    def _resolve(self, issuer: bytes, labels: tuple, depth: int, stack: set, out: Resolution) -> set:
        if depth > MAX_DEPTH:
            raise _Bound(f"resolution nested more than {MAX_DEPTH} deep")
        if not labels:
            return {self.successor(issuer)}
        call = (issuer, labels)
        if call in stack:
            out.failures.append(
                Failure("name-cycle", issuer, labels[0], "reached while the same call was in progress")
            )
            return set()
        ns = self.namespace(issuer)
        first, rest = labels[0], labels[1:]
        found = [b for b, label in self.bindings if label == first and b.says in ns]
        if not found:
            foreign = any(label == first and b.says not in ns for b, label in self.bindings)
            out.failures.append(
                Failure(
                    "name-foreign" if foreign else "name-unresolved",
                    issuer,
                    first,
                    "bound only by another speaker, in that speaker's namespace"
                    if foreign
                    else "no usable binding in this namespace",
                )
            )
            return set()
        stack.add(call)
        keys: set = set()
        for b in found:
            if b not in out.bindings:
                out.bindings.append(b)
            if b.this[0] == T_KEY:
                keys |= self._resolve(b.this[1], rest, depth + 1, stack, out)
            else:
                for k in self._resolve(b.this[1], tuple(b.this[2]), depth + 1, stack, out):
                    keys |= self._resolve(k, rest, depth + 1, stack, out)
        stack.discard(call)
        return keys


def _naming_labels(s: Verified, definitions: dict[bytes, Definition]) -> list[str] | None:
    """The labels `s` binds, or None if a §5.2 type check fails."""
    labels = []
    for a in s.body[1]:
        d = definitions.get(a[1][1])
        if d is None or a[1][2] not in d.types:
            return None
        try:
            if not d.valid_assignment(a[1][2], a[2]):
                return None
        except DefinitionError:  # a base kind v0 cannot check: not a usable statement
            return None
        if d.is_naming(a[1][2]):
            labels.append(a[2])
    return labels


def resolve(name: list, statements: list[Verified], definitions: dict[bytes, Definition], at: int) -> Resolution:
    return Resolver(statements, definitions, at).resolve(name)
