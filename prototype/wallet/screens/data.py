"""What the forms offer as choices, read from the wallet and the chosen
vocabulary through the engine. Nothing here writes."""

from dataclasses import dataclass
from pathlib import Path

import cli
from engine import definition as defs
from engine.errors import DefinitionError, EncodingError, StructureError, WalletError
from engine.render import fingerprint
from engine.store import Persona, Wallet

ACCEPTORS = ("person", "organisation")


@dataclass
class View:
    wallet: Wallet | None

    @classmethod
    def of(cls, place) -> "View":
        if not place.exists:
            return cls(None)
        try:
            return cls(Wallet.open(place.wallet))
        except (WalletError, OSError):
            return cls(None)

    @property
    def personas(self) -> list[Persona]:
        return self.wallet.personas() if self.wallet else []

    @property
    def owned(self) -> list[Persona]:
        return [p for p in self.personas if p.owned]

    @property
    def known(self) -> list[Persona]:
        return [p for p in self.personas if not p.owned]

    @property
    def acceptors(self) -> list[Persona]:
        return [p for p in self.owned if p.controller in ACCEPTORS]

    @property
    def contexts(self) -> list[str]:
        found = self.wallet.contexts() if self.wallet else []
        return sorted({"default", *found})

    def anchor_lines(self, context: str) -> list[str]:
        if not self.wallet:
            return []
        labels = self.wallet.labels()
        return [cli.anchor_line(a, labels) for a in self.wallet.anchors(context)]


def ref(p: Persona) -> str:
    return p.label or p.kid.hex()[:16]


def name(p: Persona) -> str:
    return p.label or fingerprint(p.kid)


def choices(people: list[Persona]) -> list[tuple[str, str]]:
    return [
        (f"{name(p)} ({p.controller})" if p.controller else name(p), ref(p))
        for p in people
    ]


def vocabulary(path: str):
    try:
        return defs.load(Path(path).read_bytes())
    except (OSError, DefinitionError, EncodingError, StructureError, ValueError):
        return None


def claims(d) -> list[str]:
    return [t for t in d.types if d.type(t).get(6)] if d else []


def values(d, claim: str) -> list[str]:
    if not d or claim not in d.types:
        return []
    return [v[1] for v in d.type(claim).get(6, [])]
