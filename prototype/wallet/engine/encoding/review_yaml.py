"""The human-review form (SPEC-0002 §11).

The file is YAML: the statement's fields by name, then `signed` with the
signature and, optionally, the envelope's `pub`. Reading it encodes the
fields into the TBS with KSA-CBOR and rebuilds the envelope
`[suite, says, tbs, signed.value, ? signed.pub]`; the verifier then checks
the signature over those bytes as usual. Nothing is adjusted to make the two
forms agree: if the YAML does not encode to the bytes that were signed, V4
fails.

The reader is strict where YAML is loose:

- explicit tags, anchors, aliases and multiple documents are rejected;
- a plain scalar is a decimal integer, `true`, `false`, or text that YAML
  would read as a string. `null`, `~`, floats, timestamps, `yes`/`on`, and
  hex, octal, `+1`, `01`, `1_000` or `1:30` style numbers are rejected;
- byte strings are quoted `'0x…'` in lowercase hex; times are quoted
  `YYYY-MM-DDTHH:MM:SSZ`;
- a duplicate key is rejected; a key starting with `_` is an annotation and
  is dropped.

Targets are written `{key: '0x…'}`, `{statement: '0x…'}` and so on, and inside
a generic value a quoted `'0x…'` is read as bytes, so text that looks like that
cannot be written there (§11.3, as proposed in SPEC-0002 0.4.0).
"""

import json
import re

import yaml

from .. import envelope as env
from ..errors import EncodingError, StructureError
from ..schema import (
    STATEMENT,
    Bstr,
    Field,
    Hex,
    Map,
    Name,
    Scalar,
    Text,
    TimeText,
    plain_is_text,
)
from .base import Codec
from .ksa_cbor import decode, encode

SIGNED = Map(Field(1, "value", Bstr(), True), Field(2, "pub", Bstr()))
_SAFE_PLAIN = re.compile(r"[A-Za-z0-9][A-Za-z0-9 ._/()-]*")


def _scalar_text(v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, Hex):
        return f"'0x{v.hex()}'"
    if isinstance(v, TimeText):
        return f'"{v}"'
    if isinstance(v, (Name, Text, str)):
        return _text(v)
    raise EncodingError(f"cannot write {type(v).__name__}")


def _text(s: str) -> str:
    if (
        _SAFE_PLAIN.fullmatch(s)
        and not s.endswith(" ")
        and ": " not in s
        and " #" not in s
        and plain_is_text(s)
    ):
        return s
    return json.dumps(s, ensure_ascii=False)


def _inline(v) -> str:
    if isinstance(v, dict):
        return "{" + ", ".join(f"{_text(k)}: {_inline(x)}" for k, x in v.items()) + "}"
    if isinstance(v, list):
        return "[" + ", ".join(_inline(x) for x in v) + "]"
    return _scalar_text(v)


def _is_block(v) -> bool:
    return (type(v) is dict and len(v) > 0) or (
        isinstance(v, list) and any(type(x) is dict or isinstance(x, list) for x in v)
    )


def _block_map(d: dict, indent: int) -> list[str]:
    pad, lines = " " * indent, []
    for k, v in d.items():
        if type(v) is dict and v:
            lines.append(f"{pad}{_text(k)}:")
            lines += _block_map(v, indent + 2)
        elif _is_block(v):
            lines.append(f"{pad}{_text(k)}:")
            lines += _block_seq(v, indent + 2)
        else:
            lines.append(f"{pad}{_text(k)}: {_inline(v)}")
    return lines


def _block_seq(seq: list, indent: int) -> list[str]:
    pad, lines = " " * indent, []
    for x in seq:
        if type(x) is dict and x:
            sub = _block_map(x, indent + 2)
            sub[0] = pad + "- " + sub[0][indent + 2 :]
            lines += sub
        else:
            lines.append(pad + "- " + _inline(x))
    return lines


def emit(h: dict) -> str:
    return "\n".join(_block_map(h, 0)) + "\n"


def _tree(node):
    if isinstance(node, yaml.ScalarNode):
        return Scalar(node.value, node.style is not None)
    if isinstance(node, yaml.SequenceNode):
        return [_tree(x) for x in node.value]
    out = {}
    for k, x in node.value:
        if not isinstance(k, yaml.ScalarNode):
            raise EncodingError("a map key must be a single value")
        if k.style is None and not plain_is_text(k.value):
            raise EncodingError(f"map key {k.value!r} is not text")
        if k.value in out:
            raise EncodingError(f"duplicate key {k.value!r}")
        out[k.value] = _tree(x)
    return out


def parse(text: str):
    """Read YAML text into dicts, lists and `Scalar`s, rejecting what the
    human form forbids at the lexical level."""
    try:
        docs = 0
        for ev in yaml.parse(text, Loader=yaml.SafeLoader):
            if isinstance(ev, yaml.AliasEvent) or getattr(ev, "anchor", None):
                raise EncodingError("anchors and aliases are not allowed")
            if (
                isinstance(
                    ev,
                    (yaml.ScalarEvent, yaml.MappingStartEvent, yaml.SequenceStartEvent),
                )
                and ev.tag
            ):
                raise EncodingError(f"explicit tag {ev.tag} is not allowed")
            if isinstance(ev, yaml.DocumentStartEvent):
                docs += 1
        if docs != 1:
            raise EncodingError("expected exactly one YAML document")
        return _tree(yaml.compose(text, Loader=yaml.SafeLoader))
    except yaml.YAMLError as e:
        raise EncodingError(f"not YAML: {e}") from None


class ReviewYamlCodec(Codec):
    name = "review-yaml"
    suffix = ".stmt.yaml"

    def dump(self, envelope: bytes) -> bytes:
        e = env.split(envelope)
        s = decode(e.tbs)
        try:
            STATEMENT.check(s)
            h = STATEMENT.to_h(s)
        except StructureError as x:
            raise EncodingError(f"cannot write the human form: {x}") from None
        h["signed"] = {
            "value": Hex(e.sig),
            **({"pub": Hex(e.pub)} if e.pub is not None else {}),
        }
        return emit(h).encode("utf-8")

    def load(self, data: bytes) -> bytes:
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as x:
            raise EncodingError(f"not UTF-8: {x}") from None
        h = parse(text)
        if not isinstance(h, dict) or "signed" not in h:
            raise EncodingError("the human form of a signed statement ends with signed")
        try:
            signed = SIGNED.from_h(h["signed"], "signed")
            s = STATEMENT.from_h({k: x for k, x in h.items() if k != "signed"})
        except StructureError as x:
            raise EncodingError(str(x)) from None
        return env.build(s[2], s[3], encode(s), signed[1], signed.get(2))
