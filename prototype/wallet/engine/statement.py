"""Build the statement maps v0 signs (SPEC-0002 §7, §8). Integer keys follow
Appendix B: 1 kind, 2 suite, 3 says, 4 this, 5 valid, 6 body."""

import hashlib

from . import schema, suite


def digest_target(data: bytes) -> list:
    return [2, 1, hashlib.sha256(data).digest()]


def key_target(kid: bytes) -> list:
    """`this = [1, kid]` (SPEC-0002 §7.2, target type 1): the statement is
    about a key, not a file. `key_publish` and `trust` already take this form,
    and so does TV-13, the published vector for an attestation about a key."""
    return [1, kid]


def attestation(
    says: bytes,
    this: list,
    has: list[dict],
    not_before: int,
    not_on_or_after: int,
    issued: int,
    template: dict | None = None,
) -> dict:
    body = {1: has}
    if template is not None:
        body[3] = template
    return {
        1: schema.KIND["attestation"],
        2: suite.CODE,
        3: says,
        4: this,
        5: {1: not_before, 2: not_on_or_after, 3: issued},
        6: body,
    }


def trust(
    says: bytes,
    this: list,
    about: list[dict],
    not_before: int,
    not_on_or_after: int,
    issued: int,
    may_delegate: dict | None = None,
) -> dict:
    """A `trust` statement to one key or name (SPEC-0002 §8.6). Its validity
    window is how the delegation ends: there is no revocation list."""
    body = {1: about}
    if may_delegate is not None:
        body[2] = may_delegate
    return {
        1: schema.KIND["trust"],
        2: suite.CODE,
        3: says,
        4: this,
        5: {1: not_before, 2: not_on_or_after, 3: issued},
        6: body,
    }


def key_publish(pub: bytes, issued: int) -> dict:
    kid = suite.kid(pub)
    return {
        1: schema.KIND["key-publish"],
        2: suite.CODE,
        3: kid,
        4: [1, kid],
        5: {1: issued, 3: issued},
        6: {1: {1: suite.KEY_ALG, 2: pub}},
    }
