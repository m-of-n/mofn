"""The wallet directory (ARCH-0003 §9, the subset v0 needs; #65-c2 A2).

```
DIR/
  wallet.yaml
  personas/<kid>/persona.yaml          control, controller claim, label, provenance
  personas/<kid>/keys/<kid>.yaml       public key, suite, state
  personas/<kid>/keys/<kid>.key        encrypted private key, owned personas only (0600)
  personas/<kid>/trusts/<context>.yaml anchors, owned personas only
  definitions/<DefinitionId>.def       canonical bytes; the file name is the hash
  statements/<digest>.stmt             exact envelope bytes
```

A persona is **owned** when this wallet holds its private key and **known**
when it holds only the public key. A key enters the key store only from a
verified `key-publish` or by generation here; its kid is always re-derived
(SPEC-0002 §10). A key in the key store is known, not trusted: trust comes
only from an anchor (SPEC-0004 §4).

The private seed is encrypted with a key derived from the passphrase by
Argon2id, in a libsodium SecretBox (XSalsa20-Poly1305).
"""

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

import nacl.exceptions
import nacl.pwhash
import nacl.secret
import nacl.utils
import yaml

from . import ksatime, suite
from .errors import WalletError
from .reduce import Anchor

WALLET_FILE = "wallet.yaml"
CONTROLLERS = ("person", "organisation", "service", "agent", "software", "device")
OPSLIMIT = nacl.pwhash.argon2id.OPSLIMIT_INTERACTIVE
MEMLIMIT = nacl.pwhash.argon2id.MEMLIMIT_INTERACTIVE
CONTEXT = re.compile(r"[a-z][a-z0-9-]{0,62}")


def locate(flag: str | None) -> Path:
    """`--wallet DIR`, else `$MOFN_WALLET`, else `./wallet`."""
    return Path(flag or os.environ.get("MOFN_WALLET") or "wallet")


def _hex(b: bytes) -> str:
    return "0x" + b.hex()


def _unhex(s: str) -> bytes:
    if not isinstance(s, str) or not s.startswith("0x"):
        raise WalletError(f"wallet file holds {s!r} where a 0x… byte string belongs")
    return bytes.fromhex(s[2:])


def _context(context: str) -> str:
    """A context name becomes a file name, so it must be a plain label."""
    if not isinstance(context, str) or not CONTEXT.fullmatch(context):
        raise WalletError(
            f"context {context!r} is not a name: use lowercase letters, digits and -"
        )
    return context


def _trusts(persona_dir: Path, context: str) -> Path:
    return persona_dir / "trusts" / f"{_context(context)}.yaml"


def _read(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _write(path: Path, data, mode: int = 0o644) -> None:
    text = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, "O_BINARY", 0)
    fd = os.open(path, flags, mode)
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.chmod(path, mode)


@dataclass
class Persona:
    kid: bytes
    label: str | None
    control: str
    controller: str | None
    provenance: dict = field(default_factory=dict)

    @property
    def owned(self) -> bool:
        return self.control == "owned"


class Wallet:
    def __init__(self, root: Path):
        self.root = Path(root)

    @classmethod
    def init(cls, root: Path) -> "Wallet":
        root = Path(root)
        if (root / WALLET_FILE).exists():
            raise WalletError(f"{root} already holds a wallet")
        for sub in ("personas", "definitions", "statements"):
            (root / sub).mkdir(parents=True, exist_ok=True)
        _write(root / WALLET_FILE, {"format": "mofn-wallet/v0", "suites": [suite.CODE]})
        return cls(root)

    @classmethod
    def open(cls, root: Path) -> "Wallet":
        if not (Path(root) / WALLET_FILE).is_file():
            raise WalletError(
                f"{root} is not a wallet; run `mofn --wallet {root} init`"
            )
        return cls(root)

    def _dir(self, kid: bytes) -> Path:
        return self.root / "personas" / kid.hex()

    def personas(self) -> list[Persona]:
        out = []
        for p in sorted((self.root / "personas").glob("*/persona.yaml")):
            d = _read(p)
            out.append(
                Persona(
                    _unhex(d["kid"]),
                    d.get("label"),
                    d["control"],
                    d.get("controller"),
                    d.get("provenance", {}),
                )
            )
        return out

    def find(self, ref: str) -> Persona:
        """A persona by this wallet's label for it, or by a kid hex prefix of
        at least 8 digits."""
        ps = self.personas()
        hits = [p for p in ps if p.label == ref]
        if not hits and len(ref) >= 8:
            hits = [
                p for p in ps if p.kid.hex().startswith(ref.lower().removeprefix("0x"))
            ]
        if len(hits) != 1:
            raise WalletError(
                f"no persona {ref!r} in this wallet"
                if not hits
                else f"{ref!r} is ambiguous"
            )
        return hits[0]

    def _check_label(self, label: str | None) -> None:
        if label is not None and any(p.label == label for p in self.personas()):
            raise WalletError(f"a persona labelled {label!r} already exists")

    def _add(self, persona: Persona, pub: bytes) -> Path:
        d = self._dir(persona.kid)
        if d.exists():
            raise WalletError(
                f"key {persona.kid.hex()[:16]}… is already in this wallet"
            )
        keys = d / "keys"
        keys.mkdir(parents=True)
        os.chmod(keys, 0o700)
        _write(
            d / "persona.yaml",
            {
                "kid": _hex(persona.kid),
                "label": persona.label,
                "control": persona.control,
                "controller": persona.controller,
                "provenance": persona.provenance,
            },
        )
        _write(
            keys / f"{persona.kid.hex()}.yaml",
            {
                "suite": suite.CODE,
                "alg": "ed25519",
                "pub": _hex(pub),
                "state": "active",
            },
        )
        return keys

    def add_owned(
        self,
        label: str,
        controller: str,
        seed: bytearray,
        pub: bytes,
        passphrase: bytes,
    ) -> Persona:
        if controller not in CONTROLLERS:
            raise WalletError(f"controller must be one of {', '.join(CONTROLLERS)}")
        self._check_label(label)
        p = Persona(
            suite.kid(pub),
            label,
            "owned",
            controller,
            {"how": "generated", "when": ksatime.to_text(ksatime.now())},
        )
        keys = self._add(p, pub)
        salt = nacl.utils.random(nacl.pwhash.argon2id.SALTBYTES)
        key = nacl.pwhash.argon2id.kdf(
            nacl.secret.SecretBox.KEY_SIZE,
            passphrase,
            salt,
            opslimit=OPSLIMIT,
            memlimit=MEMLIMIT,
        )
        box = nacl.secret.SecretBox(key).encrypt(bytes(seed))
        _write(
            keys / f"{p.kid.hex()}.key",
            {
                "kdf": "argon2id",
                "opslimit": OPSLIMIT,
                "memlimit": MEMLIMIT,
                "salt": _hex(salt),
                "cipher": "xsalsa20-poly1305",
                "box": _hex(bytes(box)),
            },
            mode=0o600,
        )
        return p

    def add_known(self, label: str | None, pub: bytes, provenance: dict) -> Persona:
        if not suite.key_ok(pub):
            raise WalletError("the key fails the strict key rules")
        self._check_label(label)
        p = Persona(suite.kid(pub), label, "known", None, provenance)
        self._add(p, pub)
        return p

    def unlock(self, persona: Persona, passphrase: bytes) -> bytearray:
        if not persona.owned:
            raise WalletError(
                f"{persona.label or persona.kid.hex()[:16]} is not owned by this wallet"
            )
        d = _read(self._dir(persona.kid) / "keys" / f"{persona.kid.hex()}.key")
        key = nacl.pwhash.argon2id.kdf(
            nacl.secret.SecretBox.KEY_SIZE,
            passphrase,
            _unhex(d["salt"]),
            opslimit=d["opslimit"],
            memlimit=d["memlimit"],
        )
        try:
            seed = bytearray(nacl.secret.SecretBox(key).decrypt(_unhex(d["box"])))
        except nacl.exceptions.CryptoError:
            raise WalletError("wrong passphrase") from None
        # The box authenticates the seed, not whose seed it is. RFC 9580 binds
        # the public key into the AEAD; v0 checks the same thing after opening
        # (#128), so a .key file copied under another persona is refused here.
        if suite.kid(suite.public_key(seed)) != persona.kid:
            seed[:] = bytes(len(seed))
            raise WalletError(
                f"the private key in {persona.kid.hex()}.key belongs to another key"
            )
        return seed

    def keystore(self) -> dict[tuple[int, bytes], bytes]:
        out = {}
        for p in (self.root / "personas").glob("*/keys/*.yaml"):
            d = _read(p)
            pub = _unhex(d["pub"])
            if suite.kid(pub).hex() == p.stem and suite.key_ok(pub):
                out[(d["suite"], suite.kid(pub))] = pub
        return out

    def labels(self) -> dict[bytes, str]:
        return {p.kid: p.label for p in self.personas() if p.label}

    def contexts(self) -> list[str]:
        """The contexts in which any of this wallet's own personas has an
        anchor, from the names of their trusts/ files."""
        return sorted(
            {
                f.stem
                for f in (self.root / "personas").glob("*/trusts/*.yaml")
                if CONTEXT.fullmatch(f.stem)
            }
        )

    def anchors(self, context: str) -> list[Anchor]:
        _context(context)
        out = []
        for p in self.personas():
            f = _trusts(self._dir(p.kid), context)
            if p.owned and f.is_file():
                for a in _read(f) or []:
                    out.append(
                        Anchor(
                            context,
                            _unhex(a["trusts"]),
                            [
                                {
                                    1: {
                                        1: _unhex(r["type"]["definition"]),
                                        2: r["type"]["label"],
                                    },
                                    **({3: r["range"]} if "range" in r else {}),
                                }
                                for r in a["about"]
                            ],
                            p.kid,
                            ksatime.from_text(a["accepted at"]),
                            a["source"],
                            a.get("note"),
                        )
                    )
        return out

    def add_anchor(self, anchor: Anchor) -> Path:
        acceptor = next(
            (p for p in self.personas() if p.kid == anchor.accepted_by), None
        )
        if acceptor is None or not acceptor.owned:
            raise WalletError("an anchor is accepted by a persona this wallet owns")
        if acceptor.controller not in ("person", "organisation"):
            raise WalletError(
                f"{acceptor.label} is a {acceptor.controller}; only a person or an organisation "
                f"may accept an anchor (SPEC-0004 §4.4)"
            )
        if not anchor.about:
            raise WalletError("an anchor with an empty about must not exist")
        f = _trusts(self._dir(acceptor.kid), anchor.context)
        f.parent.mkdir(exist_ok=True)
        items = (_read(f) or []) if f.is_file() else []
        entry = {
            "source": anchor.source,
            "trusts": _hex(anchor.trusts),
            "about": [
                {
                    "type": {"definition": _hex(r[1][1]), "label": r[1][2]},
                    **({"range": r[3]} if 3 in r else {}),
                }
                for r in anchor.about
            ],
            "accepted by": _hex(anchor.accepted_by),
            "accepted at": ksatime.to_text(anchor.accepted_at),
        }
        if anchor.note:
            entry["note"] = anchor.note
        _write(f, items + [entry])
        return f

    def put_definition(self, did: bytes, data: bytes) -> Path:
        f = self.root / "definitions" / f"{did.hex()}.def"
        f.write_bytes(data)
        return f

    def put_statement(self, digest: bytes, envelope: bytes) -> Path:
        f = self.root / "statements" / f"{digest.hex()}.stmt"
        f.write_bytes(envelope)
        return f
