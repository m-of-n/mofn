"""PICS-like label types, and domains of discourse.  ARCH-0002 P3 + P4.

SPIKE. Not normative.

P3: a type IS a schema - representation, constraints on usage, semantic
    descriptions, and tags for human review, with descriptions that may be
    multilingual.
P4: a DOMAIN OF DISCOURSE is a hash-identified SET of those types. The hash
    covers the whole set, because types are not independent.

PICS published rating systems separately from the labels citing them. This is
that, with the type carrying its own rendering.
"""
from __future__ import annotations
import hashlib
from rcbor import encode


def label_type(local_label: str, *, repr_: str, values: dict,
               name: dict | None = None, short: dict | None = None,
               long: dict | None = None, attr_type: str = "enum",
               delegation_type: str = "same", constraints: dict | None = None,
               ordered: bool = False) -> dict:
    """A PICS-like bundle. Field set from the sponsor, 2026-09-22:

        encoding of the attributes .. repr_
        human readable name ........ name   {lang: str}
        short description .......... short  {lang: str}
        long description ........... long   {lang: str}
        attribute type ............. attr_type
        delegation type ............ delegation_type
        processing constraints ..... constraints

    `delegation_type` is the sponsor's note made explicit: THE ATTESTATION FOR
    DELEGATION IS A DIFFERENT TYPE FROM THE BASE TYPE. Without that distinction
    holding a delegation is indistinguishable from holding a claim, and anyone
    can promote themselves.

        same      delegating this attribute uses this same type   (rare)
        scoped    delegation carries a RANGE over this attribute  (the email case)
        none      this attribute may not be delegated at all

    `values` maps each permitted value to its renderings, by language.
    """
    return {"l": local_label, "r": repr_, "ord": ordered,
            "n": name or {}, "sd": short or {}, "ld": long or {},
            "at": attr_type, "dt": delegation_type,
            "c": constraints or {}, "v": values}


def domain(defining_key_id: bytes, name: str, types: list[dict], version: str) -> dict:
    return {"k": defining_key_id, "n": name, "ver": version, "t": types}


def domain_id(dom: dict) -> bytes:
    """The hash identifies the SET and provides integrity over all of it.

    Not per-type: types reference and constrain each other, so hashing them
    separately would let a consumer assemble a combination the author never
    published.
    """
    return hashlib.sha256(encode(dom)).digest()[:16]


def render(dom: dict, local_label: str, value: str, lang: str = "en") -> str:
    """Render a claim in words - the whole point of P3.

    A verifier that resolves the domain can say what a statement MEANS without
    any type-specific code. That is what makes legibility a property of the
    data rather than of whoever wrote the UI.
    """
    for t in dom["t"]:
        if t["l"] == local_label:
            v = t["v"].get(value)
            if v is None:
                raise KeyError(f"{value!r} is not a permitted value of {local_label!r}")
            return v.get(lang) or v.get("en") or value
    raise KeyError(f"no type {local_label!r} in domain {dom['n']!r}")


def in_range(dom: dict, local_label: str, value: str) -> bool:
    for t in dom["t"]:
        if t["l"] == local_label:
            return value in t["v"]
    return False
