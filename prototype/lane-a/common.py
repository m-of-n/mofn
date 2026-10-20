"""Shared dump helpers for the LANE A byte experiment (mofn#13).

Every output is written out three ways, because the point of the experiment is to look at the bytes:

  <name>.bin / .json   the exact bytes that were signed or verified
  <name>.hex           xxd-style dump, for quoting in a record
  <name>.edn           CBOR diagnostic notation (RFC 8949 Appendix G)
"""

import json
import pathlib
from collections.abc import Mapping, Sequence

import cbor2

OUT = pathlib.Path(__file__).resolve().parent / "out"


def hexdump(data: bytes, width: int = 16) -> str:
    lines = []
    for off in range(0, len(data), width):
        chunk = data[off : off + width]
        hexpart = " ".join(f"{b:02x}" for b in chunk)
        text = "".join(chr(b) if 0x20 <= b < 0x7F else "." for b in chunk)
        lines.append(f"{off:08x}  {hexpart:<{width * 3 - 1}}  |{text}|")
    lines.append(f"{len(data):08x}  ({len(data)} bytes)")
    return "\n".join(lines) + "\n"


def diag(obj, _depth: int = 0) -> str:
    """CBOR diagnostic notation. Byte strings stay opaque as h'..' — nested CBOR is dumped as its own file rather than silently inlined, because whether a bstr is "just bytes" or "a serialised map" is exactly what COSE's bstr-wrapped protected header makes ambiguous."""
    if isinstance(obj, cbor2.CBORTag):
        return f"{obj.tag}({diag(obj.value, _depth + 1)})"
    if isinstance(obj, bytes):
        return "h'" + obj.hex() + "'"
    if isinstance(obj, str):
        return json.dumps(obj)
    if isinstance(obj, bool) or obj is None:
        return {True: "true", False: "false", None: "null"}[obj]
    if isinstance(obj, (int, float)):
        return repr(obj)
    pad = "  " * (_depth + 1)
    close = "  " * _depth
    if isinstance(obj, Mapping):
        if not obj:
            return "{}"
        items = ",\n".join(
            f"{pad}{diag(k, _depth + 1)}: {diag(v, _depth + 1)}" for k, v in obj.items()
        )
        return "{\n" + items + "\n" + close + "}"
    if isinstance(obj, Sequence):
        if not obj:
            return "[]"
        items = ",\n".join(pad + diag(v, _depth + 1) for v in obj)
        return "[\n" + items + "\n" + close + "]"
    raise TypeError(f"no diagnostic notation for {type(obj)!r}")


def emit(name: str, data: bytes, *, cbor: bool = False, pretty_json: bool = False):
    """Write one output and its views. Returns the path of the raw bytes."""
    OUT.mkdir(exist_ok=True)
    suffix = ".json" if pretty_json else ".bin"
    raw = OUT / (name + suffix)
    raw.write_bytes(data)
    (OUT / (name + ".hex")).write_text(hexdump(data))
    if cbor:
        (OUT / (name + ".edn")).write_text(diag(cbor2.loads(data)) + "\n")
    print(f"  {raw.name:<34} {len(data):>6} bytes")
    return raw


def pae(payload_type: str, body: bytes) -> bytes:
    """DSSE Pre-Authentication Encoding: "DSSEv1" SP LEN(type) SP type SP LEN(body) SP body. Lengths are decimal ASCII of the *byte* length. This is what a DSSE signature is computed over — never the envelope, and never the bare payload."""
    t = payload_type.encode()
    return b"DSSEv1 %d %s %d %s" % (len(t), t, len(body), body)

