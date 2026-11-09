"""SPEC-0002 Appendix B as data: the closed maps, their field names and the
types of their values.

The verifier uses `check` for step V7. The human-review codec uses `to_h` and
`from_h` to translate between integer keys and field names, and between codes
and their registered names (SPEC-0002 §11). Keeping both on one table means
the two cannot disagree about what a statement contains.

`to_h` returns plain Python values wrapped in the marker classes below, so the
emitter knows how to write each one. `from_h` takes the tree the YAML reader
builds: dicts, lists and `Scalar`s.
"""

import re
from dataclasses import dataclass

import yaml

from . import ksatime
from .encoding.ksa_cbor import INT_MAX
from .errors import StructureError

KINDS = {
    1: "key-publish",
    2: "self",
    3: "speaks",
    4: "attestation",
    5: "trust",
    6: "revoke",
    7: "rotate",
    8: "define",
    9: "review",
    10: "approve",
    11: "aggregate",
}
KIND = {v: k for k, v in KINDS.items()}
SUITES = {1: "ksa-ed25519-sha256", 8: "ksa-mldsa65-sha256"}
KEY_ALGS = {1: "ed25519", 2: "ecdsa-p256", 8: "ml-dsa-65"}
DIGEST_ALGS = {1: "sha-256", 2: "sha-384", 3: "sha-512"}
DIGEST_LEN = {1: 32, 2: 48, 3: 64}
USAGES = {
    1: "statements",
    2: "tls",
    3: "ipsec",
    4: "email",
    5: "payments",
    6: "transport",
}
CONTROLLERS = {
    1: "person",
    2: "organisation",
    3: "service",
    4: "agent",
    5: "software",
    6: "device",
}
TARGETS = {
    1: "key",
    2: "digest",
    3: "statement",
    4: "definition",
    # 5 is reserved: the locator target, withdrawn in SPEC-0002 0.6.0 (mofn#144)
    6: "description",
}
TARGET = {v: k for k, v in TARGETS.items()}
KIND_TARGETS = {
    1: {1},
    2: {1},
    3: {1},
    4: set(TARGETS),
    5: {1},
    6: {1},
    7: {1},
    8: {4},
    9: {2, 3},
    10: {2, 3},
    11: {2, 3, 4, 6},
}

_DECIMAL = re.compile(r"0|-?[1-9][0-9]*")
_HEX = re.compile(r"0x(?:[0-9a-f]{2})*")
_STR_TAG = "tag:yaml.org,2002:str"
_resolver = yaml.resolver.Resolver()
# Plain scalars YAML 1.2 or a 1.1 parser reads as non-text, though PyYAML's
# resolver calls them strings (SPEC-0002 §11.3).
_NOT_TEXT_ELSEWHERE = re.compile(
    r"[-+]?(?:\.[0-9]+|[0-9]+(?:\.[0-9]*)?)(?:[eE][-+]?[0-9]+)?|0o[0-7]+|[yYnN]"
)


class Hex(bytes):
    pass


class TimeText(str):
    pass


class Text(str):
    pass


class Name(str):
    pass


class Flow(dict):
    pass


@dataclass(frozen=True)
class Scalar:
    text: str
    quoted: bool


def fail(path: str, msg: str):
    raise StructureError(f"{path or 'statement'}: {msg}")


def plain_is_text(text: str) -> bool:
    return _resolver.resolve(
        yaml.ScalarNode, text, (True, False)
    ) == _STR_TAG and not _NOT_TEXT_ELSEWHERE.fullmatch(text)


def _scalar(h, path) -> Scalar:
    if not isinstance(h, Scalar):
        fail(path, "expected a single value")
    return h


def _decimal(h, path) -> int:
    s = _scalar(h, path)
    if s.quoted or not _DECIMAL.fullmatch(s.text):
        fail(path, f"{s.text!r} is not a decimal integer")
    return int(s.text)


def _bytes(h, path) -> bytes:
    s = _scalar(h, path)
    if not s.quoted or not _HEX.fullmatch(s.text):
        fail(path, "a byte string is quoted '0x' followed by lowercase hex")
    return bytes.fromhex(s.text[2:])


def _text(h, path) -> str:
    s = _scalar(h, path)
    if not s.quoted and not plain_is_text(s.text):
        fail(path, f"{s.text!r} is not text; quote it if it is meant as text")
    return s.text


def is_int(v) -> bool:
    return type(v) is int and -INT_MAX <= v <= INT_MAX


class Uint:
    def __init__(self, lo: int = 0, hi: int = INT_MAX):
        self.lo, self.hi = lo, hi

    def check(self, v, path):
        if not is_int(v) or not self.lo <= v <= self.hi:
            fail(path, f"expected an integer in {self.lo}..{self.hi}")

    def to_h(self, v):
        return v

    def from_h(self, h, path):
        return _decimal(h, path)


class Code(Uint):
    """A registered code, written by its name in the human form. When `open`,
    unregistered codes are allowed and written as decimal integers."""

    def __init__(self, table: dict[int, str], open: bool = False):
        super().__init__()
        self.table, self.open = table, open
        self.names = {v: k for k, v in table.items()}

    def check(self, v, path):
        super().check(v, path)
        if not self.open and v not in self.table:
            fail(path, f"code {v} is not registered")

    def to_h(self, v):
        return Name(self.table[v]) if v in self.table else v

    def from_h(self, h, path):
        s = _scalar(h, path)
        if s.text in self.names:
            return self.names[s.text]
        if self.open and _DECIMAL.fullmatch(s.text) and not s.quoted:
            return int(s.text)
        fail(path, f"{s.text!r} is not a registered name")


class Bool:
    def check(self, v, path):
        if not isinstance(v, bool):
            fail(path, "expected true or false")

    def to_h(self, v):
        return v

    def from_h(self, h, path):
        s = _scalar(h, path)
        if s.quoted or s.text not in ("true", "false"):
            fail(path, "expected true or false")
        return s.text == "true"


class Bstr:
    def __init__(self, size: int | None = None):
        self.size = size

    def check(self, v, path):
        if not isinstance(v, bytes) or (self.size is not None and len(v) != self.size):
            fail(
                path,
                f"expected a byte string{f' of {self.size} octets' if self.size else ''}",
            )

    def to_h(self, v):
        return Hex(v)

    def from_h(self, h, path):
        v = _bytes(h, path)
        self.check(v, path)
        return v


class Tstr:
    def __init__(self, pattern: str | None = None):
        self.pattern = re.compile(pattern) if pattern else None

    def check(self, v, path):
        if not isinstance(v, str):
            fail(path, "expected text")
        if self.pattern and not self.pattern.fullmatch(v):
            fail(path, f"{v!r} does not match {self.pattern.pattern}")

    def to_h(self, v):
        return Text(v)

    def from_h(self, h, path):
        return _text(h, path)


class Time:
    def check(self, v, path):
        if not is_int(v) or not ksatime.is_time(v):
            fail(path, "expected a KSA time")

    def to_h(self, v):
        return TimeText(ksatime.to_text(v))

    def from_h(self, h, path):
        s = _scalar(h, path)
        if not s.quoted:
            fail(path, "a time is quoted text")
        try:
            return ksatime.from_text(s.text)
        except ValueError as e:
            fail(path, str(e))


class Value:
    """Any value of the data model: int, bool, bytes, text, array, or a map
    with text keys."""

    def check(self, v, path):
        if isinstance(v, bool) or isinstance(v, (bytes, str)) or is_int(v):
            return
        if isinstance(v, list):
            for i, x in enumerate(v):
                self.check(x, f"{path}[{i}]")
            return
        if isinstance(v, dict):
            for k, x in v.items():
                if not isinstance(k, str):
                    fail(path, "a map inside a value has text keys")
                self.check(x, f"{path}.{k}")
            return
        fail(path, "not a value of the data model")

    def to_h(self, v):
        if isinstance(v, bool) or isinstance(v, int):
            return v
        if isinstance(v, bytes):
            return Hex(v)
        if isinstance(v, str):
            if _HEX.fullmatch(v):
                raise StructureError(
                    f"text {v!r} would read back as bytes; it cannot be written in a value"
                )
            return Text(v)
        if isinstance(v, list):
            return [self.to_h(x) for x in v]
        return {k: self.to_h(x) for k, x in v.items()}

    def from_h(self, h, path):
        if isinstance(h, list):
            return [self.from_h(x, f"{path}[{i}]") for i, x in enumerate(h)]
        if isinstance(h, dict):
            return {k: self.from_h(x, f"{path}.{k}") for k, x in h.items()}
        s = _scalar(h, path)
        if s.quoted:
            return bytes.fromhex(s.text[2:]) if _HEX.fullmatch(s.text) else s.text
        if _DECIMAL.fullmatch(s.text):
            return int(s.text)
        if s.text in ("true", "false"):
            return s.text == "true"
        return _text(h, path)


class Checked:
    """A slot whose shape another table checks (the statement body)."""

    def check(self, v, path):
        pass

    def to_h(self, v):
        return v


class ListOf:
    def __init__(self, item, min: int = 1):
        self.item, self.min = item, min

    def check(self, v, path):
        if not isinstance(v, list) or len(v) < self.min:
            fail(path, f"expected an array of at least {self.min}")
        for i, x in enumerate(v):
            self.item.check(x, f"{path}[{i}]")

    def to_h(self, v):
        return [self.item.to_h(x) for x in v]

    def from_h(self, h, path):
        if not isinstance(h, list):
            fail(path, "expected an array")
        return [self.item.from_h(x, f"{path}[{i}]") for i, x in enumerate(h)]


@dataclass(frozen=True)
class Field:
    code: int
    name: str
    type: object
    required: bool = False


class Map:
    """A closed map: an unknown key is always an error (SPEC-0002 §7.1)."""

    def __init__(self, *fields: Field, flow: bool = False):
        self.fields = fields
        self.by_code = {f.code: f for f in fields}
        self.by_name = {f.name.replace("-", " "): f for f in fields}
        self.flow = flow

    def check(self, v, path):
        if not isinstance(v, dict):
            fail(path, "expected a map")
        for k in v:
            if k not in self.by_code:
                fail(path, f"unknown field {k!r}")
        for f in self.fields:
            if f.code in v:
                f.type.check(v[f.code], f"{path}.{f.name}" if path else f.name)
            elif f.required:
                fail(path, f"missing required field {f.name}")

    def to_h(self, v):
        out = Flow() if self.flow else {}
        for f in self.fields:
            if f.code in v:
                out[f.name.replace("-", " ")] = f.type.to_h(v[f.code])
        return out

    def from_h(self, h, path):
        if not isinstance(h, dict):
            fail(path, "expected a map")
        out = {}
        for name, x in h.items():
            if name.startswith("_"):
                continue
            f = self.by_name.get(name)
            if f is None:
                fail(path, f"unknown field {name!r}")
            out[f.code] = f.type.from_h(x, f"{path}.{f.name}" if path else f.name)
        for f in self.fields:
            if f.required and f.code not in out:
                fail(path, f"missing required field {f.name}")
        return out


KID = Bstr(32)
ID = Bstr(32)
LABEL = Tstr()
VALUE = Value()
TIME = Time()
TYPE_REF = Map(
    Field(1, "definition", ID, True), Field(2, "label", LABEL, True), flow=True
)
ATTRIBUTE = Map(Field(1, "type", TYPE_REF, True), Field(2, "value", VALUE, True))
ATTRIBUTE_RANGE = Map(Field(1, "type", TYPE_REF, True), Field(3, "range", VALUE))
PUBLIC_KEY = Map(
    Field(1, "alg", Code(KEY_ALGS), True), Field(2, "pub", Bstr(), True), flow=True
)
VALIDITY = Map(
    Field(1, "not-before", TIME),
    Field(2, "not-on-or-after", TIME),
    Field(3, "issued", TIME),
)
DELEGATION = Map(
    Field(1, "depth", Uint()),
    Field(2, "ranges", ListOf(ATTRIBUTE_RANGE)),
    Field(3, "allow-keys", ListOf(KID)),
    Field(4, "exclude-keys", ListOf(KID)),
    Field(5, "not-on-or-after", TIME),
)

BODIES = {
    1: Map(Field(1, "key", PUBLIC_KEY, True)),
    2: Map(
        Field(1, "key", PUBLIC_KEY),
        Field(2, "label", Tstr()),
        Field(3, "uses", ListOf(Code(USAGES, open=True))),
        Field(4, "created", TIME),
        Field(5, "controller", Code(CONTROLLERS, open=True)),
    ),
    3: Map(Field(1, "definitions", ListOf(ID), True)),
    4: Map(Field(1, "has", ListOf(ATTRIBUTE), True), Field(3, "template", TYPE_REF)),
    5: Map(
        Field(1, "about", ListOf(ATTRIBUTE_RANGE), True),
        Field(2, "may-delegate", DELEGATION),
        Field(3, "trusts", ListOf(KID, min=2)),
        Field(4, "threshold", Uint()),
    ),
    6: Map(Field(1, "revokes", Bstr(32), True)),
    7: Map(Field(1, "note", Tstr())),
    8: Map(
        Field(1, "name", Tstr(), True),
        Field(2, "version", Tstr(), True),
        Field(3, "supersedes", ID),
    ),
    9: Map(
        Field(1, "has", ListOf(ATTRIBUTE), True),
        Field(2, "comment", Tstr()),
        Field(3, "template", TYPE_REF),
    ),
    10: Map(
        Field(1, "has", ListOf(ATTRIBUTE)),
        Field(2, "comment", Tstr()),
        Field(3, "template", TYPE_REF),
    ),
    11: Map(
        Field(1, "process", TYPE_REF, True),
        Field(2, "inputs", ListOf(Bstr(32)), True),
        Field(3, "result", Bool(), True),
    ),
}


class Target:
    """`this` (SPEC-0002 §7.2). Written in the human form as a one-key map
    named by the target type: `{digest: {alg: sha-256, value: '0x…'}}`."""

    def check(self, v, path):
        if (
            not isinstance(v, list)
            or len(v) < 2
            or not is_int(v[0])
            or v[0] not in TARGETS
        ):
            fail(path, "a target is an array starting with a registered target type")
        t, n = v[0], len(v)
        if t == 2:
            if n != 3 or not is_int(v[1]) or v[1] not in DIGEST_ALGS:
                fail(path, "a digest target is [2, digest-alg, bytes]")
            Bstr(DIGEST_LEN[v[1]]).check(v[2], path)
        elif t == 6:
            if n != 3:
                fail(path, "a description target is [6, type-ref, value]")
            TYPE_REF.check(v[1], path)
            VALUE.check(v[2], path)
        elif n != 2:
            fail(path, f"a {TARGETS[t]} target has two elements")
        else:
            Bstr(32).check(v[1], path)

    def to_h(self, v):
        t = v[0]
        if t == 2:
            inner = Flow(alg=Name(DIGEST_ALGS[v[1]]), value=Hex(v[2]))
        elif t == 6:
            inner = Flow(type=TYPE_REF.to_h(v[1]), value=VALUE.to_h(v[2]))
        else:
            inner = Hex(v[1])
        return Flow({TARGETS[t]: inner})

    def from_h(self, h, path):
        if not isinstance(h, dict) or len(h) != 1:
            fail(path, "a target is a map with exactly one target type")
        ((name, x),) = h.items()
        t = TARGET.get(name)
        if t is None:
            fail(path, f"{name!r} is not a target type")
        if t == 2:
            m = Map(
                Field(1, "alg", Code(DIGEST_ALGS), True),
                Field(2, "value", Bstr(), True),
            ).from_h(x, path)
            v = [2, m[1], m[2]]
        elif t == 6:
            m = Map(
                Field(1, "type", TYPE_REF, True), Field(2, "value", VALUE, True)
            ).from_h(x, path)
            v = [6, m[1], m[2]]
        else:
            v = [t, _bytes(x, path)]
        self.check(v, path)
        return v


TARGET_TYPE = Target()


class Statement:
    """The statement map (SPEC-0002 §7.1). The body's shape depends on the
    kind, and `this` must be a target type the kind allows (§8.1)."""

    head = Map(
        Field(1, "kind", Code(KINDS), True),
        Field(2, "suite", Code(SUITES, open=True), True),
        Field(3, "says", KID, True),
        Field(4, "this", TARGET_TYPE),
        Field(5, "valid", VALIDITY),
        Field(6, "body", Checked(), True),
    )

    def check(self, v, path=""):
        self.head.check(v, path)
        kind = v[1]
        BODIES[kind].check(v[6], "body")
        if 4 in v:
            if v[4][0] not in KIND_TARGETS[kind]:
                fail(
                    "this",
                    f"a {KINDS[kind]} statement cannot be about a {TARGETS[v[4][0]]}",
                )
        elif kind != 5:
            fail(path, "missing required field this")

    def to_h(self, v):
        out = self.head.to_h(v)
        out["body"] = BODIES[v[1]].to_h(v[6])
        return out

    def from_h(self, h, path=""):
        if not isinstance(h, dict) or "kind" not in h:
            fail(path, "missing required field kind")
        kind = self.head.by_name["kind"].type.from_h(h["kind"], "kind")
        body = h.get("body")
        rest = {k: x for k, x in h.items() if k != "body"}
        out = Map(*[f for f in self.head.fields if f.code != 6]).from_h(rest, path)
        if body is None:
            fail(path, "missing required field body")
        out[6] = BODIES[kind].from_h(body, "body")
        self.check(out)
        return out


STATEMENT = Statement()
