"""Words for people: keys, targets, sentences, and the verdict.

A key is shown by the relying party's own label for it, or by a fingerprint
(`key:` and the first 8 octets of the kid in hex). Never by the label a key
gives itself (SPEC-0001 §7.3). Sentences come from a definition's template
(SPEC-0003 §10.1). Language is `en` when present, else the first tag.
"""

import json

from . import ksatime
from .definition import Definition

LIMIT = (
    "This establishes who said it and whether they were entitled to say it; "
    "it does not establish that it is true."
)
LINES = (
    "integrity",
    "authenticity",
    "names",
    "authorization",
    "acceptance",
    "semantics",
)


def lang(m: dict) -> str:
    return m["en"] if "en" in m else m[min(m)]


def fingerprint(kid: bytes) -> str:
    return "key:" + kid[:8].hex()


def key_name(kid: bytes, labels: dict[bytes, str]) -> str:
    return labels.get(kid) or fingerprint(kid)


def target(t: list, labels: dict[bytes, str]) -> str:
    kind = t[0]
    if kind == 1:
        return key_name(t[1], labels)
    if kind == 2:
        return {1: "sha-256", 2: "sha-384", 3: "sha-512"}[t[1]] + ":" + t[2][:8].hex()
    if kind == 3:
        return "statement:" + t[1][:8].hex()
    if kind == 4:
        return "definition:" + t[1][:8].hex()
    if kind == 5:
        return t[1]
    return "a described object"


def type_name(d: Definition | None, label: str) -> str:
    if d is None or label not in d.types:
        return label
    return lang(d.types[label][3]).lower()


def value_text(d: Definition | None, label: str, value, part: int = 3) -> str:
    v = d.value_def(label, value) if d is not None and label in d.types else None
    return lang(v[part]) if v else str(value)


def _template(d: Definition, statement: dict) -> dict | None:
    body = statement[6]
    if 3 in body and body[3][1] == d.id:
        return d.templates.get(body[3][2])
    labels = {a[1][2] for a in body.get(1, [])}
    for t in d.templates.values():
        if t[2] == statement[1] and labels <= {a[1][2] for a in t[4]}:
            return t
    return None


def sentence(d: Definition | None, statement: dict, labels: dict[bytes, str]) -> str:
    says, this = key_name(statement[3], labels), target(statement[4], labels)
    attrs = statement[6].get(1, [])
    if d is None or any(a[1][1] != d.id for a in attrs):
        ids = {a[1][1] for a in attrs if d is None or a[1][1] != d.id}
        return (
            f"{says} says something about {this} in unresolved vocabulary "
            + ", ".join(f"definition:{i[:8].hex()}" for i in sorted(ids))
            + "."
        )
    t = _template(d, statement)
    if t is None:
        parts = ", ".join(
            f"{type_name(d, a[1][2])} is {value_text(d, a[1][2], a[2], 2)}"
            for a in attrs
        )
        return f"{says} says that for {this}, {parts}."
    text = lang(t[8]).replace("{says}", says).replace("{this}", this)
    for a in attrs:
        label = a[1][2]
        text = text.replace("{" + label + ".name}", value_text(d, label, a[2], 2))
        text = text.replace("{" + label + "}", value_text(d, label, a[2], 3))
    return text


def verdict_text(answer) -> str:
    out = [f"{ln.name:<15}{ln.result:<15}{ln.sentence}" for ln in answer.lines]
    out += ["", f"answer: {'yes' if answer.yes else 'no'}"]
    if answer.sentences:
        out += [""] + answer.sentences
    out += ["", LIMIT]
    return "\n".join(out) + "\n"


def verdict_json(answer) -> str:
    return json.dumps(answer.to_json(), indent=2, ensure_ascii=False) + "\n"


def time_text(t: int) -> str:
    return ksatime.to_text(t)
