"""Single-statement verification, SPEC-0002 §9.2, steps V1 to V9.

The steps run in order and stop at the first failure. The signature is
checked over `tbs` exactly as received, before `tbs` is decoded (V4 before
V5): nothing decoded is trusted until its signature has verified.

Checks that need other statements, definitions or time are not done here;
they belong to trust evaluation (`reduce.py`, SPEC-0004).
"""

import hashlib
from dataclasses import dataclass
from typing import Mapping

from . import envelope as env, schema, suite
from .encoding.ksa_cbor import decode
from .errors import EncodingError, Invalid, StructureError, Unverifiable

KeyStore = Mapping[tuple[int, bytes], bytes]


@dataclass(frozen=True)
class Verified:
    statement: dict
    tbs: bytes
    digest: bytes
    envelope: bytes
    pub: bytes
    key_in_store: bool

    @property
    def kind(self) -> int:
        return self.statement[1]

    @property
    def says(self) -> bytes:
        return self.statement[3]

    @property
    def this(self):
        return self.statement.get(4)

    @property
    def body(self) -> dict:
        return self.statement[6]


def verify(data: bytes, keystore: KeyStore) -> Verified:
    """Verify one envelope. Return `Verified`, or raise `Invalid` or
    `Unverifiable` with the step and the §12.9 reason code."""
    try:
        e = env.split(data)
    except EncodingError as x:
        raise Invalid("V1", "envelope", str(x)) from None

    if e.suite != suite.CODE:
        raise Unverifiable("V2", "suite", f"suite {e.suite} is not supported")

    pub = keystore.get((e.suite, e.says))
    in_store = pub is not None
    if pub is None:
        if e.pub is None:
            raise Unverifiable(
                "V3", "unknown-key", f"no key for {e.says.hex()[:16]}… in the key store"
            )
        if suite.kid(e.pub) != e.says:
            raise Invalid("V3", "key", "kid(pub) does not equal says")
        pub = e.pub
    if not suite.key_ok(pub):
        raise Invalid("V3", "key", "the public key fails the strict key rules")

    if not suite.verify(pub, e.tbs, e.sig):
        raise Invalid("V4", "signature", "the signature does not verify over DS ‖ tbs")

    try:
        s = decode(e.tbs)
    except EncodingError as x:
        raise Invalid("V5", "encoding", str(x)) from None

    if not isinstance(s, dict) or s.get(2) != e.suite or s.get(3) != e.says:
        raise Invalid(
            "V6",
            "envelope-mismatch",
            "the envelope's suite or says differs from the statement's",
        )

    try:
        schema.STATEMENT.check(s)
    except StructureError as x:
        raise Invalid("V7", "structure", str(x)) from None

    _kind_rules(s, e)

    return Verified(s, e.tbs, hashlib.sha256(e.tbs).digest(), data, pub, in_store)


def _kind_rules(s: dict, e: env.Envelope) -> None:
    """V8: the kind-specific checks of SPEC-0002 §8 that need only this
    statement."""
    kind, says, this, body = s[1], s[3], s.get(4), s[6]

    def rule(ok: bool, why: str):
        if not ok:
            raise Invalid("V8", "kind-rule", why)

    if kind in (1, 2, 3, 6):
        rule(
            this == [1, says],
            f"a {schema.KINDS[kind]} statement must be about its own key",
        )
    if kind == 1 or (kind == 2 and 1 in body):
        key = body[1]
        rule(
            key[1] == suite.KEY_ALG,
            "the published key's algorithm does not match the suite",
        )
        rule(suite.kid(key[2]) == says, "kid(body.key) does not equal says")
        rule(
            e.pub is not None and e.pub == key[2],
            "the envelope must carry pub, equal to body.key.pub",
        )
    if kind == 5:
        threshold_form = this is None
        if threshold_form:
            rule(
                3 in body and 4 in body, "the threshold form needs trusts and threshold"
            )
            rule(
                1 <= body[4] <= len(body[3]),
                "threshold must be between 1 and the number of keys",
            )
        else:
            rule(
                3 not in body and 4 not in body,
                "trusts and threshold belong only to the threshold form",
            )
    if kind in (6, 7):
        rule(
            3 in s.get(5, {}),
            f"a {schema.KINDS[kind]} statement must carry valid.issued",
        )
    if kind == 7:
        rule(this != [1, says], "a rotate cannot name its own key as successor")
