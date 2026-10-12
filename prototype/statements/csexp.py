"""Canonical S-expression reader — single-pass, rejecting, no re-encoding.

SPIKE (#73). Not normative. DEC-002 is open; this tests ONE claim about
option 1 and decides nothing.

THE CLAIM UNDER TEST, from the `canonical-encoding` topic answer:

    "If checking canonicality on decode cannot be done without re-encoding,
     then condition (2) drags the canonicaliser of the producer back into the
     verifier, the R-O-05 separation is cosmetic, and DSSE is simply right."

Condition (2) is *the decoder REJECTS non-canonical input rather than
normalising it*. This file is the experiment for DEC-002 option 1.

WHAT MAKES IT A FAIR TEST. Three properties, each enforced rather than
asserted in prose:

  single-pass      `_pos` only ever increases. Every read goes through
                   `_byte`/`_take`, which advance it. There is no seek, no
                   backtrack, and no lookahead beyond the one byte that
                   `_byte` has already consumed.
  no re-encoding   this module imports nothing. In particular it does not
                   import an encoder, so it cannot canonicalise-and-compare
                   even by accident. `test_decode.py` asserts the absence.
  no normalising   every rejection raises. Nothing is repaired, defaulted,
                   coerced or silently accepted.

THE GRAMMAR (RFC 9804 §7.2, verbatim, see the record's canonical.abnf):

    c-sexp    =  c-string / ("(" *c-sexp ")")
    c-string  =  [ "[" verbatim "]" ] verbatim

and from §7.1, the two rules §7.2 depends on and does not restate:

    verbatim  =  decimal ":" *OCTET
    decimal   =  %x30 / (%x31-39 *DIGIT)

READ `decimal` CLOSELY — it is the finding. `%x30 / (%x31-39 *DIGIT)` is
"zero, or a nonzero digit followed by any digits". Leading zeros are not
merely non-canonical, they are UNGRAMMATICAL. `03:abc` fails to parse. The
smallest-form rule that CBOR has to state as an encoder obligation (RFC 8949
§4.2.1) is, here, a property of the grammar — so the decoder gets it for free
and cannot forget it.
"""
from __future__ import annotations


class NotCanonical(ValueError):
    """Input is not a canonical S-expression. Rejected, never repaired."""


class Atom:
    """An octet-string, with its display hint if one was written.

    `hint is None` and `hint == b"..."` are DIFFERENT VALUES here, deliberately.
    RFC 9804 §4.6 says a default hint is neither written out nor stripped, and
    §4.7 makes the hint part of equality — so collapsing them at parse time
    would be exactly the silent normalisation condition (2) forbids. The
    consequence is recorded in the record's design-notes as option 1's one
    crack on the identity path: two spellings, one value, two digests. A
    PROFILE rule closes it. A decoder cannot, and this one does not pretend to.
    """
    __slots__ = ("data", "hint")

    def __init__(self, data: bytes, hint: bytes | None = None):
        self.data, self.hint = data, hint

    def __eq__(self, other):
        return (isinstance(other, Atom)
                and self.data == other.data and self.hint == other.hint)

    def __repr__(self):
        h = "" if self.hint is None else f"[{self.hint!r}]"
        return f"{h}{self.data!r}"


class _Reader:
    def __init__(self, buf: bytes):
        self._buf = buf
        self._pos = 0
        self.reads = 0          # bytes consumed; the single-pass witness

    # ---- the only two ways to look at the input, and both advance ----

    def _byte(self) -> int:
        if self._pos >= len(self._buf):
            raise NotCanonical(f"truncated at offset {self._pos}")
        b = self._buf[self._pos]
        self._pos += 1
        self.reads += 1
        return b

    def _take(self, n: int) -> bytes:
        end = self._pos + n
        if end > len(self._buf):
            raise NotCanonical(
                f"length {n} at offset {self._pos} runs {end - len(self._buf)} "
                f"bytes past the end")
        out = self._buf[self._pos:end]
        self._pos = end
        self.reads += n
        return out

    def _peek(self) -> int | None:
        """The ONE place that looks without consuming, and it looks at one
        byte. Needed because `*c-sexp` has to know whether the next thing is
        `)` or another element. This is lookahead of 1, not backtracking: the
        byte is consumed by the next `_byte()` call, never re-examined after
        a decision is taken."""
        return self._buf[self._pos] if self._pos < len(self._buf) else None

    # ---- grammar ----

    def _decimal(self) -> int:
        """decimal = %x30 / (%x31-39 *DIGIT). Leading zeros are ungrammatical."""
        b = self._byte()
        if b == 0x30:                       # "0" stands alone
            return 0
        if not 0x31 <= b <= 0x39:
            raise NotCanonical(
                f"expected a length digit at offset {self._pos - 1}, got "
                f"{bytes([b])!r}; a canonical octet-string is "
                f"<decimal>:<octets> and nothing else")
        n = b - 0x30
        while True:
            nxt = self._peek()
            if nxt is None or not 0x30 <= nxt <= 0x39:
                return n
            n = n * 10 + (self._byte() - 0x30)

    def _verbatim(self) -> bytes:
        n = self._decimal()
        b = self._byte()
        if b != 0x3A:                       # ":"
            raise NotCanonical(
                f"expected ':' after length {n} at offset {self._pos - 1}, got "
                f"{bytes([b])!r}")
        return self._take(n)

    def _c_string(self, first: int) -> Atom:
        hint = None
        if first == 0x5B:                   # "["
            hint = self._verbatim()
            b = self._byte()
            if b != 0x5D:                   # "]"
                raise NotCanonical(
                    f"expected ']' closing the display hint at offset "
                    f"{self._pos - 1}, got {bytes([b])!r}")
            return Atom(self._verbatim(), hint)
        # `first` is the opening digit of the length; put it to work rather
        # than unreading it — unreading is the thing we are not allowed to do.
        if first == 0x30:
            n = 0
        elif 0x31 <= first <= 0x39:
            n = first - 0x30
            while True:
                nxt = self._peek()
                if nxt is None or not 0x30 <= nxt <= 0x39:
                    break
                n = n * 10 + (self._byte() - 0x30)
        else:
            raise NotCanonical(
                f"expected '(', '[' or a length digit at offset "
                f"{self._pos - 1}, got {bytes([first])!r}")
        b = self._byte()
        if b != 0x3A:
            raise NotCanonical(
                f"expected ':' after length {n} at offset {self._pos - 1}, got "
                f"{bytes([b])!r}")
        return Atom(self._take(n), None)

    def _c_sexp(self, depth: int = 0):
        if depth > 256:
            raise NotCanonical("nesting deeper than 256; refusing to recurse")
        b = self._byte()
        if b == 0x28:                       # "("
            items = []
            while True:
                nxt = self._peek()
                if nxt is None:
                    raise NotCanonical("unterminated list: input ended before ')'")
                if nxt == 0x29:             # ")"
                    self._byte()
                    return items
                items.append(self._c_sexp(depth + 1))
        return self._c_string(b)

    def parse(self):
        v = self._c_sexp()
        if self._pos != len(self._buf):
            raise NotCanonical(
                f"{len(self._buf) - self._pos} trailing byte(s) after a "
                f"complete S-expression at offset {self._pos}; a canonical "
                f"form is exactly one S-expression")
        return v


def loads(buf: bytes):
    """Parse canonical S-expression bytes, or raise NotCanonical.

    Returns nested lists of `Atom`. Accepting is the same act as recognising
    canonicality: there is no second validation step, because the canonical
    grammar admits nothing else.
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
    """Bytes consumed while parsing. Equals len(buf) on success — the
    single-pass witness: every byte read exactly once, none read twice."""
    r = _Reader(bytes(buf))
    r.parse()
    return r.reads
