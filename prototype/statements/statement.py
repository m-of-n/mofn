"""Statements: *A says B has C*  —  ARCH-0002 P2.

SPIKE. Not normative.

Every statement has one shape. What varies is the predicate type, which is
KEY-RELATIVE (P1): a pair of (defining key, local label). There is no registry.

Functions demonstrated here:
  attestation   A says B has C
  naming        A says B has name "fred"      - P6: a name is an attested string
  delegation    A says B can speak about (Domain, Topic)
  constraint    A says <narrowing over a label type>
"""
from __future__ import annotations
import hashlib
from rcbor import encode, diagnostic


def keyid(key_bytes: bytes) -> bytes:
    """A principal is a key. Its id is a digest of it - ARCH-0001 R-M-02."""
    return hashlib.sha256(key_bytes).digest()[:16]


def ptype(defining_key: bytes, local_label: str) -> dict:
    """A key-relative predicate type. THIS is R-M-12 / P1 in one function.

    Key K's 'build-provenance' and key K2's 'build-provenance' are different
    types, distinguishable with no coordination and no registry.
    """
    return {"k": keyid(defining_key), "l": local_label}


def statement(speaker: bytes, subject: dict, predicate_type: dict, claim, *, at: int) -> dict:
    """A says B has C. `says` is the signature, applied separately."""
    return {"a": keyid(speaker), "b": subject, "t": predicate_type, "c": claim, "ts": at}


# --- subject identification, ARCH-0002 R-M-11 -------------------------------
def by_digest(d: bytes) -> dict:      return {"m": "d", "v": d}
def by_locator(uri: str) -> dict:     return {"m": "l", "v": uri}
def by_description(desc: dict) -> dict:
    """Things you cannot hash: describe, canonicalise, and the digest IS the id."""
    return {"m": "s", "v": hashlib.sha256(encode(desc)).digest()[:16]}


def sign(stmt: dict, secret: bytes) -> dict:
    """Stand-in. A real signature is a vetted library - CLAUDE.md forbids
    generated primitives. What matters for the spike is WHAT gets signed:
    the canonical bytes, verbatim, with the type authenticated (R-O-05)."""
    payload = encode(stmt)
    mac = hashlib.sha256(b"rcbor/statement/v0" + secret + payload).digest()[:16]
    return {"typ": "rcbor/statement/v0", "payload": payload, "sig": mac}


def verify(envelope: dict, secret: bytes) -> bool:
    """Verify the bytes received, THEN decode. Never canonicalise to verify."""
    expect = hashlib.sha256(b"rcbor/statement/v0" + secret + envelope["payload"]).digest()[:16]
    return expect == envelope["sig"]
