"""Reduced CBOR — the decoder `rcbor.py` never had. Single-pass, rejecting.

SPIKE (#73). Not normative. DEC-002 is open; this decides nothing.

WHY THIS FILE EXISTS. The `canonical-encoding` topic answer records that the
rcbor spike "has an encoder and NO DECODER", and that condition (2) — *the
decoder REJECTS non-canonical input rather than normalising it* — is therefore
unproven for CBOR. It also records the falsifier:

    "If checking canonicality on decode cannot be done without re-encoding,
     then condition (2) drags the canonicaliser of the producer back into the
     verifier, the R-O-05 separation is cosmetic, and DSSE is simply right."

So the question is not "can we parse CBOR". It is: can the TWO determinism
rules that look like they need the encoder — smallest-form integer heads, and
map keys sorted bytewise on their ENCODED form — be checked while reading
forwards, without ever encoding anything?

THE ANSWER IS YES, AND MAP ORDER IS THE INTERESTING HALF.

  smallest-form heads   purely local. A head with additional info 24 must
                        carry a value >= 24, else a 1-byte head would have
                        done. Same for 25/26/27 against 2^8, 2^16, 2^32.
                        One comparison, no context, no encoder.

  bytewise key order    the rule is "sorted by the ENCODED key bytes", and
                        the encoded key bytes ARE PRESENT IN THE INPUT — they
                        are the slice the key was just parsed from. So the
                        check is a memcmp of two slices of the buffer we are
                        already reading. Nothing is re-encoded because nothing
                        needs to be: the producer sorted on exactly the bytes
                        the consumer is looking at.

                        This is the crux. The rule SOUNDS like it needs the
                        encoder, because it is phrased in terms of an encoding.
                        It does not, because the encoding is the input.

  duplicate keys        free. STRICTLY increasing order rejects duplicates as
                        a special case — equal keys are not strictly
                        increasing. One comparison enforces both rules, which
                        is why they are not checked separately below.

WHAT MAKES IT A FAIR TEST:

  single-pass      `_pos` only increases; there is no seek and no backtrack.
                   `reads` counts consumed bytes and equals len(buf) on
                   success.
  no re-encoding   this module does not import `rcbor`. It cannot round-trip
                   to compare even by accident, and `test_decode.py` asserts
                   the absence of the import.
  no normalising   every rejection raises `NotCanonical`. Nothing is repaired,
                   reordered, defaulted or coerced.

THE PROFILE, matching `rcbor.py` exactly: definite lengths only, smallest-form
heads, no tags (major type 6 — R-M-12: the IANA registry is a central
allocator), no floats, no undefined, no simple values beyond false/true/null,
map keys restricted to int/bytes/str and strictly ascending by encoded bytes.
"""
from __future__ import annotations

MAJOR_UINT, MAJOR_NINT, MAJOR_BSTR, MAJOR_TSTR, MAJOR_ARRAY, MAJOR_MAP, MAJOR_TAG, MAJOR_SIMPLE = range(8)

# additional info -> (byte width, smallest value this width is allowed to carry)
_WIDTH = {24: (1, 24), 25: (2, 1 << 8), 26: (4, 1 << 16), 27: (8, 1 << 32)}


class NotCanonical(ValueError):
    """Input is outside the reduced profile, or inside it but not in
    canonical form. Rejected, never coerced."""


class _Reader:
    def __init__(self, buf: bytes):
        self._buf = buf
        self._pos = 0
        self.reads = 0

    def _take(self, n: int) -> bytes:
        end = self._pos + n
        if end > len(self._buf):
            raise NotCanonical(
                f"truncated at offset {self._pos}: wanted {n} byte(s), "
                f"{len(self._buf) - self._pos} remain")
        out = self._buf[self._pos:end]
        self._pos = end
        self.reads += n
        return out

    def _head(self) -> tuple[int, int, int]:
        """Returns (major, additional-info, argument).

        The additional info is returned alongside the argument because major
        type 7 needs it: there, 25/26/27 mean float16/32/64 and the following
        bytes are a FLOAT PAYLOAD, not an integer argument. An earlier draft
        of this file returned only (major, argument) and applied the
        smallest-form rule to major 7 as well. Every float was still rejected,
        so the fixtures stayed green on the result — but for the wrong reason,
        with the wrong diagnostic, and only because a float's payload happened
        to look like a non-smallest integer. The fixture suite caught it. Kept
        in the comments because a decoder that rejects correctly by accident
        is not evidence of anything.
        """
        at = self._pos
        b = self._take(1)[0]
        major, ai = b >> 5, b & 0x1F
        if ai < 24:
            return major, ai, ai
        if ai == 31:
            raise NotCanonical(
                f"indefinite-length item at offset {at}: the reduced profile "
                f"is definite lengths only (RFC 8949 §4.2.1)")
        if ai in (28, 29, 30):
            raise NotCanonical(
                f"reserved additional info {ai} at offset {at}")
        width, floor = _WIDTH[ai]
        raw = self._take(width)
        if major == MAJOR_SIMPLE:
            # Not an integer argument. Caller decides on `ai` alone; the
            # smallest-form rule below would be meaningless on float bits.
            return major, ai, int.from_bytes(raw, "big")
        n = int.from_bytes(raw, "big")
        if n < floor:
            raise NotCanonical(
                f"non-smallest head at offset {at}: {n} is encoded in "
                f"{width} byte(s) but fits in a shorter form. Deterministic "
                f"encoding requires the smallest head that fits "
                f"(RFC 8949 §4.2.1)")
        return major, ai, n

    def _item(self, depth: int = 0):
        if depth > 256:
            raise NotCanonical("nesting deeper than 256; refusing to recurse")
        at = self._pos
        major, ai, arg = self._head()

        if major == MAJOR_UINT:
            return arg
        if major == MAJOR_NINT:
            return -1 - arg
        if major == MAJOR_BSTR:
            return self._take(arg)
        if major == MAJOR_TSTR:
            raw = self._take(arg)
            try:
                return raw.decode("utf-8")
            except UnicodeDecodeError as e:
                # Validation, not normalisation: the bytes are rejected, never
                # replaced or repaired. Note this scans the string's own bytes
                # once, which keeps the single pass.
                raise NotCanonical(
                    f"text string at offset {at} is not valid UTF-8: {e}") from None
        if major == MAJOR_ARRAY:
            return [self._item(depth + 1) for _ in range(arg)]
        if major == MAJOR_MAP:
            return self._map(arg, depth)
        if major == MAJOR_TAG:
            raise NotCanonical(
                f"tag {arg} at offset {at}: the reduced profile excludes major "
                f"type 6 entirely. CBOR tags are IANA-allocated, and R-M-12 "
                f"requires native extension points to be key-relative; "
                f"private-use ranges give escape, not a namespace")
        # major == MAJOR_SIMPLE — decided on `ai`, never on the argument value
        if ai in (25, 26, 27):
            raise NotCanonical(
                f"float{ {25: 16, 26: 32, 27: 64}[ai] } at offset {at}: the "
                f"reduced profile has no floats — carry an integer or a "
                f"decimal string")
        if ai == 24:
            raise NotCanonical(
                f"1-byte simple value {arg} at offset {at} is outside the profile")
        if ai == 20:
            return False
        if ai == 21:
            return True
        if ai == 22:
            return None
        if ai == 23:
            raise NotCanonical(f"`undefined` at offset {at} is outside the profile")
        raise NotCanonical(f"simple value {ai} at offset {at} is outside the profile")

    def _map(self, n: int, depth: int):
        out = {}
        prev = None                     # (start, end) of the previous key's BYTES
        for _ in range(n):
            start = self._pos
            key = self._item(depth + 1)
            end = self._pos
            if not isinstance(key, (int, bytes, str)) or isinstance(key, bool):
                raise NotCanonical(
                    f"map key at offset {start} is {type(key).__name__}; the "
                    f"profile allows int, bytes and str")
            if prev is not None:
                # THE CHECK. Two slices of the input buffer, compared bytewise.
                # No encoder, no re-encoding, no buffering: the producer sorted
                # on exactly these bytes and they are still in front of us.
                before, now = self._buf[prev[0]:prev[1]], self._buf[start:end]
                if before == now:
                    raise NotCanonical(
                        f"duplicate map key at offset {start}: encoded key "
                        f"{now.hex()} already appeared")
                if before > now:
                    raise NotCanonical(
                        f"map keys out of order at offset {start}: encoded key "
                        f"{now.hex()} sorts before {before.hex()}. Deterministic "
                        f"encoding requires keys ascending by encoded bytes "
                        f"(RFC 8949 §4.2.1)")
            prev = (start, end)
            out[key] = self._item(depth + 1)
        return out

    def parse(self):
        v = self._item()
        if self._pos != len(self._buf):
            raise NotCanonical(
                f"{len(self._buf) - self._pos} trailing byte(s) after a "
                f"complete item at offset {self._pos}")
        return v


def loads(buf: bytes):
    """Decode reduced-CBOR bytes, or raise NotCanonical.

    Accepting IS the canonicality check. There is no second validation pass
    and no comparison against a re-encoding — which is the whole point of the
    experiment.
    """
    if not isinstance(buf, (bytes, bytearray)):
        raise NotCanonical(f"expected bytes, got {type(buf).__name__}")
    return _Reader(bytes(buf)).parse()


def is_canonical(buf: bytes) -> bool:
    try:
        loads(buf)
        return True
    except NotCanonical:
        return False


def passes(buf: bytes) -> int:
    """Bytes consumed. Equals len(buf) on success — the single-pass witness."""
    r = _Reader(bytes(buf))
    r.parse()
    return r.reads
