"""The signed statement envelope `[suite, says, tbs, sig, ? pub]`
(SPEC-0002 §5).

`suite` and `says` are unauthenticated hints, checked against the TBS at V6;
`tbs` is carried exactly as signed; `pub` is an optional key hint, checked
at V3. Kept apart from the verifier because DEC-005 is still open.
"""

from dataclasses import dataclass

from .encoding.ksa_cbor import decode, encode
from .errors import EncodingError


@dataclass(frozen=True)
class Envelope:
    suite: int
    says: bytes
    tbs: bytes
    sig: bytes
    pub: bytes | None = None


def build(suite: int, says: bytes, tbs: bytes, sig: bytes, pub: bytes | None = None) -> bytes:
    return encode([suite, says, tbs, sig] + ([pub] if pub is not None else []))


def split(data: bytes) -> Envelope:
    """Decode an envelope, or raise `EncodingError` if it is not an array of
    (uint, 32-octet bytes, bytes, bytes, ? bytes)."""
    v = decode(data)
    if not isinstance(v, list) or len(v) not in (4, 5):
        raise EncodingError("an envelope is an array of 4 or 5 elements")
    suite, says, tbs, sig, *rest = v
    if isinstance(suite, bool) or not isinstance(suite, int) or suite < 0:
        raise EncodingError("envelope suite is not an unsigned integer")
    if not isinstance(says, bytes) or len(says) != 32:
        raise EncodingError("envelope says is not a 32-octet byte string")
    if not all(isinstance(x, bytes) for x in [tbs, sig, *rest]):
        raise EncodingError("envelope tbs, sig and pub must be byte strings")
    return Envelope(suite, says, tbs, sig, rest[0] if rest else None)
