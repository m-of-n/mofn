"""Definitions (SPEC-0003): load, identify, check conformance, check values.

A definition is identified by `DefinitionId = SHA-256(KSA-CBOR(body))`. The
id is always recomputed from the bytes, never taken from a file name or a
flag (§4.2). A file path is only a locator (§4.4).

v0 implements the parts DV-1 uses. Of the base kinds only `enum` has an
algebra here; a type of any other kind is reported as not supported, so it
can never be silently treated as valid. Panels, processes and constraint
expressions (SPEC-0005, SPEC-0003 §8) are refused the same way.
"""

import hashlib
import re
from dataclasses import dataclass

from . import schema
from .encoding.ksa_cbor import decode
from .errors import DefinitionError, EncodingError, StructureError
from .ksatime import to_seconds
from .schema import Bool, Checked, Field, ListOf, Map, Tstr, Uint, Value

ENUM = 1
LABEL_RE = r"[a-z][a-z0-9-]{0,62}"
_LANG = re.compile(r"[a-z]{2,3}(-[A-Z][a-z]{3})?(-([A-Z]{2}|[0-9]{3}))?")


class LangMap:
    def check(self, v, path):
        if not isinstance(v, dict) or not v:
            schema.fail(path, "a language map has at least one entry")
        for k, x in v.items():
            if not isinstance(k, str) or not _LANG.fullmatch(k):
                schema.fail(path, f"{k!r} is not a language tag in canonical case")
            if not isinstance(x, str):
                schema.fail(path, "a language map's values are text")


LANG = LangMap()
LABEL = Tstr(LABEL_RE)
LOCAL_REF = Map(Field(1, "definition", schema.ID), Field(2, "label", LABEL, True))
VALUE_DEF = Map(
    Field(1, "value", Tstr(), True),
    Field(2, "names", LANG, True),
    Field(3, "meaning", LANG, True),
)
REVIEW_Q = Map(Field(1, "tag", LABEL, True), Field(2, "ask", LANG, True))
FIELD_DEF = Map(
    Field(1, "name", LABEL, True),
    Field(2, "type", LOCAL_REF, True),
    Field(3, "required", Bool(), True),
    Field(4, "names", LANG, True),
    Field(5, "description", LANG, True),
    Field(6, "unit", Tstr()),
)
TYPE_DEF = Map(
    Field(1, "label", LABEL, True),
    Field(2, "base", Uint(1, 11), True),
    Field(3, "names", LANG, True),
    Field(4, "short", LANG, True),
    Field(5, "long", LANG),
    Field(6, "values", ListOf(VALUE_DEF)),
    Field(7, "constraints", ListOf(Checked())),
    Field(8, "delegation", Uint(0, 2), True),
    Field(9, "review", ListOf(REVIEW_Q)),
    Field(10, "examples", ListOf(Value())),
    Field(11, "fields", ListOf(FIELD_DEF)),
    Field(12, "params", Checked()),
)
TEMPLATE_ATTR = Map(
    Field(1, "type", LOCAL_REF, True),
    Field(2, "required", Bool(), True),
    Field(3, "fixed", Value()),
    Field(4, "default", Value()),
)
TEMPLATE_DEF = Map(
    Field(1, "label", LABEL, True),
    Field(2, "function", Uint(1, 11), True),
    Field(
        3,
        "target",
        Map(
            Field(1, "types", ListOf(Uint(1, 6)), True),
            Field(2, "rules", ListOf(Checked())),
        ),
        True,
    ),
    Field(4, "attributes", ListOf(TEMPLATE_ATTR), True),
    Field(5, "max-validity", Uint()),
    Field(6, "approval", schema.TYPE_REF),
    Field(7, "issuer", Map(Field(1, "topic", LABEL, True))),
    Field(8, "sentence", LANG, True),
    Field(9, "names", LANG, True),
    Field(10, "short", LANG),
)
BODY = Map(
    Field(1, "definer", schema.KID, True),
    Field(2, "name", Tstr(), True),
    Field(3, "version", Tstr(), True),
    Field(4, "imports", ListOf(schema.ID)),
    Field(5, "entries", ListOf(Checked()), True),
)


@dataclass
class Definition:
    id: bytes
    data: bytes
    body: dict
    types: dict[str, dict]
    templates: dict[str, dict]

    @property
    def definer(self) -> bytes:
        return self.body[1]

    @property
    def name(self) -> str:
        return self.body[2]

    @property
    def version(self) -> str:
        return self.body[3]

    def type_ref(self, label: str) -> dict:
        self.type(label)
        return {1: self.id, 2: label}

    def type(self, label: str) -> dict:
        if label not in self.types:
            raise DefinitionError(
                "type-error", f"{self.name} {self.version} has no type {label!r}"
            )
        return self.types[label]

    def _enum(self, label: str) -> list[str]:
        t = self.type(label)
        if t[2] != ENUM:
            raise DefinitionError(
                "type-error",
                f"type {label!r} has base kind {t[2]}; v0 supports only enum",
            )
        return [v[1] for v in t[6]]

    def valid_assignment(self, label: str, value) -> bool:
        return isinstance(value, str) and value in self._enum(label)

    def canonical_range(self, label: str, values: list[str]) -> list[str]:
        """Return the enum range holding `values`, in the order the type lists
        them. Raises if a value is not in the type."""
        allowed = self._enum(label)
        for v in values:
            if v not in allowed:
                raise DefinitionError(
                    "type-error",
                    f"{v!r} is not a value of {label!r}; allowed: {', '.join(allowed)}",
                )
        return [v for v in allowed if v in values]

    def well_formed_range(self, label: str, rng) -> bool:
        return (
            isinstance(rng, list)
            and len(rng) > 0
            and all(isinstance(v, str) for v in rng)
            and len(set(rng)) == len(rng)
            and self.canonical_range(label, rng) == rng
        )

    def in_range(self, label: str, value, rng) -> bool:
        """`rng` None is the unbounded range of the type."""
        if not self.valid_assignment(label, value):
            return False
        return rng is None or (self.well_formed_range(label, rng) and value in rng)

    def value_def(self, label: str, value) -> dict | None:
        for v in self.type(label).get(6, []):
            if v[1] == value:
                return v
        return None


def load(data: bytes, expected_id: bytes | None = None) -> Definition:
    """Decode a definition body, recompute its id, and check conformance
    (SPEC-0003 §4.2, §9). Raises `DefinitionError`."""
    did = hashlib.sha256(data).digest()
    if expected_id is not None and did != expected_id:
        raise DefinitionError(
            "definition-unobtainable",
            f"the bytes hash to {did.hex()[:16]}…, not {expected_id.hex()[:16]}…",
        )
    try:
        body = decode(data)
    except EncodingError as e:
        raise DefinitionError(
            "definition-non-conforming", f"not KSA-CBOR: {e}"
        ) from None
    try:
        return _conform(did, data, body)
    except StructureError as e:
        raise DefinitionError("definition-non-conforming", str(e)) from None


def _conform(did: bytes, data: bytes, body) -> Definition:
    BODY.check(body, "definition")
    imports = set(body.get(4, []))
    types, templates, labels = {}, {}, set()
    for i, entry in enumerate(body[5]):
        path = f"definition.entries[{i}]"
        if not isinstance(entry, list) or len(entry) != 2:
            schema.fail(path, "an entry is [entry-type, entry-map]")
        kind, m = entry
        if kind == 1:
            TYPE_DEF.check(m, path)
            _check_type(m, path)
            types[m[1]] = m
        elif kind == 2:
            TEMPLATE_DEF.check(m, path)
            templates[m[1]] = m
        elif kind in (3, 4):
            schema.fail(
                path, "panels and processes (SPEC-0005) are not supported in v0"
            )
        else:
            schema.fail(path, f"entry type {kind!r} is not registered")
        if m[1] in labels:
            schema.fail(path, f"label {m[1]!r} is used twice")
        labels.add(m[1])
    for label, t in templates.items():
        for a in t[4]:
            _resolve(a[1], types, imports, f"template {label}")
    for label, t in types.items():
        for f in t.get(11, []):
            _resolve(f[2], types, imports, f"type {label}")
    d = Definition(did, data, body, types, templates)
    for label, t in types.items():
        for ex in t.get(10, []):
            if t[2] == ENUM and not d.valid_assignment(label, ex):
                schema.fail(
                    f"type {label}", f"example {ex!r} is not a valid assignment"
                )
    return d


def _check_type(t: dict, path: str) -> None:
    base = t[2]
    if base == ENUM and 6 not in t:
        schema.fail(path, "an enum type must list its values")
    if base == 9 and (11 not in t or t[8] != 0):
        schema.fail(path, "a record type needs fields and delegation 0")
    if 7 in t:
        schema.fail(
            path, "constraint expressions (SPEC-0003 §8) are not supported in v0"
        )
    if 6 in t and len({v[1] for v in t[6]}) != len(t[6]):
        schema.fail(path, "enum values must be distinct")


def _resolve(ref: dict, types: dict, imports: set, where: str) -> None:
    if 1 in ref:
        if ref[1] not in imports:
            schema.fail(
                where,
                f"type reference {ref[2]!r} names a definition that is not imported",
            )
    elif ref[2] not in types:
        schema.fail(
            where, f"type reference {ref[2]!r} is not a type of this definition"
        )


def attributed(d: Definition, verified) -> object | None:
    """Return the verified `define` statement that publishes `d`, or None
    (SPEC-0003 §11.1): target `[4, id]`, speaker equal to the definer, and
    name and version equal to the body's."""
    for v in verified:
        if (
            v.kind == 8
            and v.this == [4, d.id]
            and v.says == d.definer
            and v.body[1] == d.name
            and v.body[2] == d.version
        ):
            return v
    return None


def conforms_to_template(d: Definition, t: dict, statement: dict) -> str | None:
    """SPEC-0003 §7.1 conformance. Return None if the statement conforms,
    else the reason in words."""
    if statement[1] != t[2]:
        return "the statement's kind is not the template's function"
    target = statement.get(4)
    if target is None or target[0] not in t[3][1]:
        return "the statement's target type is not one the template allows"
    if 2 in t[3]:
        return "target rules are not supported in v0"
    has = {a[1][2]: a[2] for a in statement[6].get(1, []) if a[1][1] == d.id}
    if len(has) != len(statement[6].get(1, [])):
        return "the statement has an attribute from another definition"
    allowed = {a[1][2]: a for a in t[4]}
    for label, a in allowed.items():
        if a[2] and label not in has:
            return f"the required attribute {label} is missing"
        if 3 in a and label in has and has[label] != a[3]:
            return f"{label} must be {a[3]!r}"
    for label, value in has.items():
        if label not in allowed:
            return f"{label} is not an attribute of the template"
        if not d.valid_assignment(label, value):
            return f"{value!r} is not a valid {label}"
    if 5 in t:
        valid = statement.get(5, {})
        if 1 not in valid or 2 not in valid:
            return "the template needs both not-before and not-on-or-after"
        if to_seconds(valid[2]) - to_seconds(valid[1]) > t[5]:
            return f"the validity is longer than {t[5] // 86400} days"
    return None
