"""KSA-CBOR (SPEC-0002 §4.2) and its validating decoder (§4.3).

The encoder is `ksa_cbor()` from `spec/vectors/ksa-core/generate.py`. The
decoder is the single-pass reader of `prototype/statements/rcbor_decode.py`,
changed in four ways to match §4.1: `null` is rejected, integers are bounded
to ±(2^53 − 1), map keys are unsigned integers or text only, and every
rejection raises `EncodingError`.

The decoder never re-encodes and never repairs. Map key order is checked by
comparing the raw key bytes of the input, so one forward pass decides
canonicality (mofn#78).
"""

import struct

from ..errors import EncodingError
from .base import Codec

INT_MAX = 2**53 - 1
MAX_DEPTH = 256

_WIDTH = {24: (1, 24), 25: (2, 1 << 8), 26: (4, 1 << 16), 27: (8, 1 << 32)}


def _head(major: int, n: int) -> bytes:
    if n < 24:
        return bytes([major << 5 | n])
    if n < 2**8:
        return bytes([major << 5 | 24, n])
    if n < 2**16:
        return bytes([major << 5 | 25]) + struct.pack(">H", n)
    if n < 2**32:
        return bytes([major << 5 | 26]) + struct.pack(">I", n)
    return bytes([major << 5 | 27]) + struct.pack(">Q", n)


def encode(v) -> bytes:
    """Encode a value of the KSA data model. Raises `EncodingError` for
    anything outside it: floats, None, tags, integers past ±(2^53 − 1),
    duplicate map keys."""
    if v is True:
        return b"\xf5"
    if v is False:
        return b"\xf4"
    if isinstance(v, int):
        if not -INT_MAX <= v <= INT_MAX:
            raise EncodingError(f"integer {v} is outside ±(2^53 − 1)")
        return _head(0, v) if v >= 0 else _head(1, -1 - v)
    if isinstance(v, bytes):
        return _head(2, len(v)) + v
    if isinstance(v, str):
        b = v.encode("utf-8")
        return _head(3, len(b)) + b
    if isinstance(v, list):
        return _head(4, len(v)) + b"".join(encode(x) for x in v)
    if isinstance(v, dict):
        for k in v:
            if isinstance(k, bool) or not (
                isinstance(k, str) or (isinstance(k, int) and k >= 0)
            ):
                raise EncodingError(
                    f"map key {k!r} is neither an unsigned integer nor text"
                )
        items = sorted(
            ((encode(k), encode(x)) for k, x in v.items()), key=lambda kv: kv[0]
        )
        return _head(5, len(items)) + b"".join(k + x for k, x in items)
    raise EncodingError(f"not in the KSA data model: {type(v).__name__}")


class _Reader:
    def __init__(self, buf: bytes):
        self.buf = buf
        self.pos = 0

    def take(self, n: int) -> bytes:
        end = self.pos + n
        if end > len(self.buf):
            raise EncodingError(f"truncated at offset {self.pos}: wanted {n} byte(s)")
        out = self.buf[self.pos : end]
        self.pos = end
        return out

    def head(self) -> tuple[int, int, int]:
        """Return (major, additional info, argument). In major type 7 the
        bytes after ai 25/26/27 are float bits, not an argument, so the
        smallest-head rule is not applied to them."""
        at = self.pos
        b = self.take(1)[0]
        major, ai = b >> 5, b & 0x1F
        if ai < 24:
            return major, ai, ai
        if ai == 31:
            raise EncodingError(f"indefinite-length item at offset {at}")
        if ai in (28, 29, 30):
            raise EncodingError(f"reserved additional info {ai} at offset {at}")
        width, floor = _WIDTH[ai]
        n = int.from_bytes(self.take(width), "big")
        if major != 7 and n < floor:
            raise EncodingError(
                f"non-smallest head at offset {at}: {n} in {width} byte(s)"
            )
        return major, ai, n

    def item(self, depth: int):
        if depth > MAX_DEPTH:
            raise EncodingError(f"nesting deeper than {MAX_DEPTH}")
        at = self.pos
        major, ai, arg = self.head()
        if major == 0:
            if arg > INT_MAX:
                raise EncodingError(f"integer at offset {at} is above 2^53 − 1")
            return arg
        if major == 1:
            if arg > INT_MAX - 1:
                raise EncodingError(f"integer at offset {at} is below −(2^53 − 1)")
            return -1 - arg
        if major == 2:
            return self.take(arg)
        if major == 3:
            raw = self.take(arg)
            try:
                return raw.decode("utf-8")
            except UnicodeDecodeError as e:
                raise EncodingError(
                    f"text at offset {at} is not valid UTF-8: {e}"
                ) from None
        if major == 4:
            return [self.item(depth + 1) for _ in range(arg)]
        if major == 5:
            return self.map(arg, depth)
        if major == 6:
            raise EncodingError(
                f"tag {arg} at offset {at}: tags are not in the KSA data model"
            )
        if ai in (25, 26, 27):
            raise EncodingError(f"floating-point value at offset {at}")
        if ai == 20:
            return False
        if ai == 21:
            return True
        if ai == 22:
            raise EncodingError(f"null at offset {at}")
        if ai == 23:
            raise EncodingError(f"undefined at offset {at}")
        raise EncodingError(f"simple value {arg if ai == 24 else ai} at offset {at}")

    def map(self, n: int, depth: int) -> dict:
        out = {}
        prev = None
        for _ in range(n):
            start = self.pos
            key = self.item(depth + 1)
            end = self.pos
            if isinstance(key, bool) or not (
                isinstance(key, str) or (isinstance(key, int) and key >= 0)
            ):
                raise EncodingError(
                    f"map key at offset {start} is neither an unsigned integer nor text"
                )
            if prev is not None:
                before, now = self.buf[prev[0] : prev[1]], self.buf[start:end]
                if before == now:
                    raise EncodingError(f"duplicate map key at offset {start}")
                if before > now:
                    raise EncodingError(f"map keys out of order at offset {start}")
            prev = (start, end)
            out[key] = self.item(depth + 1)
        return out


def decode(buf: bytes):
    """Decode KSA-CBOR bytes, or raise `EncodingError`. Accepting is the
    canonicality check."""
    if not isinstance(buf, bytes):
        raise EncodingError(f"expected bytes, got {type(buf).__name__}")
    r = _Reader(buf)
    v = r.item(0)
    if r.pos != len(buf):
        raise EncodingError(f"{len(buf) - r.pos} trailing byte(s) at offset {r.pos}")
    return v


class KsaCborCodec(Codec):
    """The file is the envelope bytes themselves (ARCH-0003 §9: `.stmt` holds
    the exact signed bytes)."""

    name = "ksa-cbor"
    suffix = ".stmt"

    def dump(self, envelope: bytes) -> bytes:
        return envelope

    def load(self, data: bytes) -> bytes:
        return data
