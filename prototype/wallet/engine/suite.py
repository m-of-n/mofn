"""Cipher suite 1, `ksa-ed25519-sha256` (SPEC-0002 §6.3), over PyNaCl.

Every primitive comes from libsodium. This module holds no curve math.

- Strict key rules: `crypto_core_ed25519_is_valid_point` rejects a
  non-canonical encoding, a point not on the curve, a point of small order,
  and a point outside the prime-order subgroup. An honestly generated key is
  never affected.
- Strict signature rules: libsodium's verify rejects S ≥ L and a small-order
  or non-canonical R before it checks the equation.

`cryptography` (OpenSSL) was tried as well and is not used: it exposes no
point check, so N-4 could only be met by writing one by hand (design-log
0016).
"""

import hashlib

import nacl.bindings
import nacl.exceptions
import nacl.signing

CODE = 1
NAME = "ksa-ed25519-sha256"
KEY_ALG = 1
DS = b"KSA-STMT-SIG-v1\x00"
PUB_LEN = 32
SIG_LEN = 64


def kid(pub: bytes) -> bytes:
    return hashlib.sha256(pub).digest()


def key_ok(pub: bytes) -> bool:
    return (
        isinstance(pub, bytes)
        and len(pub) == PUB_LEN
        and nacl.bindings.crypto_core_ed25519_is_valid_point(pub)
    )


def verify(pub: bytes, tbs: bytes, sig: bytes) -> bool:
    if len(sig) != SIG_LEN:
        return False
    try:
        nacl.signing.VerifyKey(pub).verify(DS + tbs, sig)
        return True
    except nacl.exceptions.BadSignatureError:
        return False


def generate() -> tuple[bytearray, bytes]:
    """Return (seed, public key) for a new key pair."""
    sk = nacl.signing.SigningKey.generate()
    return bytearray(bytes(sk)), bytes(sk.verify_key)


def public_key(seed: bytearray) -> bytes:
    return bytes(nacl.signing.SigningKey(bytes(seed)).verify_key)


def sign(seed: bytearray, tbs: bytes) -> bytes:
    return nacl.signing.SigningKey(bytes(seed)).sign(DS + tbs).signature
