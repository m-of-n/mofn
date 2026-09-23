"""Reduced CBOR — a deterministic encoder, written to be read rather than fast.

SPIKE. Not normative. DEC-002 is open; this explores one candidate.

Reduced from RFC 8949 in two directions:

  deterministic (RFC 8949 §4.2)   definite lengths, smallest-form integers,
                                  map keys sorted by encoded bytes
  reduced further (ARCH-0002 P1)  NO tags at all - the IANA CBOR Tags registry
                                  is a central allocator, and R-M-12 says
                                  native extension points are key-relative.
                                  Also no floats, no indefinite lengths,
                                  no undefined.

Determinism is a property of THIS encoder. It is not a claim that this is the
only deterministic encoding - sponsor, 2026-09-22.
"""
from __future__ import annotations

MAJOR_UINT, MAJOR_NINT, MAJOR_BSTR, MAJOR_TSTR, MAJOR_ARRAY, MAJOR_MAP, MAJOR_SIMPLE = 0, 1, 2, 3, 4, 5, 7


class NotReduced(ValueError):
    """Input outside the reduced profile. Rejected, never coerced."""


def _head(major: int, n: int) -> bytes:
    """Smallest form that fits — required for determinism."""
    if n < 24:
        return bytes([major << 5 | n])
    for bits, ai in ((8, 24), (16, 25), (32, 26), (64, 27)):
        if n < 1 << bits:
            return bytes([major << 5 | ai]) + n.to_bytes(bits // 8, "big")
    raise NotReduced(f"integer too large: {n}")


def encode(v) -> bytes:
    if v is True or v is False:
        return bytes([MAJOR_SIMPLE << 5 | (21 if v else 20)])
    if v is None:
        return bytes([MAJOR_SIMPLE << 5 | 22])
    if isinstance(v, int):
        return _head(MAJOR_UINT, v) if v >= 0 else _head(MAJOR_NINT, -v - 1)
    if isinstance(v, float):
        raise NotReduced("floats are outside the reduced profile — use an integer or a decimal string")
    if isinstance(v, bytes):
        return _head(MAJOR_BSTR, len(v)) + v
    if isinstance(v, str):
        b = v.encode("utf-8")
        return _head(MAJOR_TSTR, len(b)) + b
    if isinstance(v, (list, tuple)):
        return _head(MAJOR_ARRAY, len(v)) + b"".join(encode(x) for x in v)
    if isinstance(v, dict):
        items = []
        for k, val in v.items():
            if not isinstance(k, (str, bytes, int)):
                raise NotReduced(f"map key must be str, bytes or int, got {type(k).__name__}")
            items.append((encode(k), encode(val)))
        if len({k for k, _ in items}) != len(items):
            raise NotReduced("duplicate map key after encoding")
        # deterministic map ordering: bytewise on the ENCODED key
        items.sort(key=lambda kv: kv[0])
        return _head(MAJOR_MAP, len(items)) + b"".join(k + val for k, val in items)
    raise NotReduced(f"type outside the reduced profile: {type(v).__name__}")


def diagnostic(v, indent: int = 0) -> str:
    """CBOR diagnostic-ish notation, for humans reading a spike."""
    pad = "  " * indent
    if isinstance(v, dict):
        inner = ",\n".join(f'{pad}  {k!r}: {diagnostic(val, indent + 1).lstrip()}'
                           for k, val in sorted(v.items(), key=lambda kv: encode(kv[0])))
        return "{\n" + inner + "\n" + pad + "}"
    if isinstance(v, (list, tuple)):
        return "[" + ", ".join(diagnostic(x, indent) for x in v) + "]"
    if isinstance(v, bytes):
        return f"h'{v.hex()}'"
    return repr(v)
