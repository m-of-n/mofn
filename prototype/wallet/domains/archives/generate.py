#!/usr/bin/env python3
"""Write the archives domain file and its author's two statements (mofn#66, W-2).

    .venv/bin/python domains/archives/generate.py           # from prototype/wallet
    .venv/bin/python domains/archives/generate.py --check   # exit 1 if a file differs

The second domain of PLAN-0004 §3: statements about a `library` record,
identified by the SHA-256 of its bytes. Scenario: project/APP-0003.

This is tooling for a domain author, not engine code. It calls the engine's
existing encoder and signer and adds nothing to them: W-2's acceptance is
that the archives scenario runs through the same `mofn make` and `mofn check`
as supply chain with no engine change, so the engine must not learn anything
here. `mofn` has no command that publishes a definition (finding F-1 in
DL-0033), which is why this script exists.

The archivist's key comes from a fixed seed, so every byte written is
reproducible. Ed25519 signatures are deterministic. The seed is published;
the key is for this example only.

Files written beside this script:

    archives.def                 the definition, KSA-CBOR; its id is its SHA-256
    archivist.pub.stmt[.yaml]    the archivist's key-publish
    archivist-define.stmt[.yaml] the define statement that says the definition is theirs

Not written here: `record.yaml`, the example subject. It is the library
record `w3c-prov-dm`, copied byte for byte once (library@6dcbdb0) and then
frozen, because statements name its digest and the live record may change.
It is the project's own record, not a third-party document.
"""

import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from engine import definition as defs, ksatime, schema, signer, statement, suite
from engine.codecs import CODECS
from engine.encoding.ksa_cbor import encode

SEED = hashlib.sha256(b"mofn-example-archivist").digest()
PUB = suite.public_key(bytearray(SEED))
KID = suite.kid(PUB)
ISSUED = ksatime.from_text("2026-11-09T00:00:00Z")

ENUM, SCOPED, ATTESTATION, DIGEST = 1, 2, 4, 2

DEFINITION = {
    1: KID,
    2: "archives",
    3: "1",
    5: [
        [
            1,
            {
                1: "record-review",
                2: ENUM,
                3: {"en": "Record review", "es": "Revisión del registro"},
                4: {
                    "en": "How far a library record was checked against its source.",
                    "es": "Hasta qué punto se cotejó un registro de la biblioteca con su fuente.",
                },
                6: [
                    {
                        1: "reviewed",
                        2: {"en": "Reviewed", "es": "Revisado"},
                        3: {
                            "en": "read against its source and confirmed",
                            "es": "cotejado con su fuente y confirmado",
                        },
                    },
                    {
                        1: "summarized",
                        2: {"en": "Summarized", "es": "Resumido"},
                        3: {
                            "en": "summarized, but not read against its source",
                            "es": "resumido, pero no cotejado con su fuente",
                        },
                    },
                    {
                        1: "unverified",
                        2: {"en": "Unverified", "es": "Sin verificar"},
                        3: {
                            "en": "not checked against its source",
                            "es": "no cotejado con su fuente",
                        },
                    },
                ],
                8: SCOPED,
                9: [
                    {
                        1: "source",
                        2: {
                            "en": "Do the bytes that were read have the digest the record names?",
                            "es": "¿Tienen los bytes leídos el resumen que nombra el registro?",
                        },
                    }
                ],
            },
        ],
        [
            2,
            {
                1: "record-attestation",
                2: ATTESTATION,
                3: {1: [DIGEST]},
                4: [{1: {2: "record-review"}, 2: True}],
                5: 365 * 86400,
                8: {
                    "en": "{says} attests that the library record {this} was {record-review}.",
                    "es": "{says} atestigua que el registro de la biblioteca {this} fue {record-review}.",
                },
                9: {"en": "Record attestation", "es": "Atestación de registro"},
            },
        ],
    ],
}

def wanted() -> dict[str, bytes]:
    data = encode(DEFINITION)
    d = defs.load(data)
    assert d.definer == KID
    publish = signer.sign(
        bytearray(SEED), statement.key_publish(PUB, ISSUED), carry_pub=True
    )
    define = signer.sign(
        bytearray(SEED),
        {
            1: schema.KIND["define"],
            2: suite.CODE,
            3: KID,
            4: [4, d.id],
            5: {1: ISSUED, 3: ISSUED},
            6: {1: d.name, 2: d.version},
        },
    )
    out = {"archives.def": data}
    for codec in CODECS.values():
        out["archivist.pub" + codec.suffix] = codec.dump(publish)
        out["archivist-define" + codec.suffix] = codec.dump(define)
    return out


def main() -> int:
    stale = []
    for name, data in wanted().items():
        f = HERE / name
        if "--check" in sys.argv:
            if not f.is_file() or f.read_bytes() != data:
                stale.append(name)
        else:
            f.write_bytes(data)
    for name in stale:
        print(f"stale: domains/archives/{name}")
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
