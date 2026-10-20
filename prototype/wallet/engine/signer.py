"""Sign a statement: encode it, sign `DS ‖ TBS`, wrap it in an envelope.

The private seed is held in a bytearray and overwritten with zeros as soon
as the signature is made. In Python this is best effort: the library and the
interpreter may keep copies we cannot reach.
"""

from . import envelope, suite
from .encoding.ksa_cbor import encode


def sign(seed: bytearray, statement: dict, carry_pub: bool = False) -> bytes:
    try:
        tbs = encode(statement)
        pub = suite.public_key(seed)
        sig = suite.sign(seed, tbs)
    finally:
        seed[:] = bytes(len(seed))
    return envelope.build(statement[2], statement[3], tbs, sig, pub if carry_pub else None)
