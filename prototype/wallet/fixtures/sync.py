#!/usr/bin/env python3
"""Write the wallet fixtures from `spec/vectors/ksa-core/vectors.json`.

    python3 fixtures/sync.py           # write the files
    python3 fixtures/sync.py --check   # exit 1 if any file differs

The fixtures are copies of published vectors, never edited by hand: DV-1
(the supply-chain definition), TV-1 (Alice's key-publish), TV-3 (Alice's
define of DV-1), TV-4 (Alice's attestation about the example artifact), and
the artifact bytes. The `.stmt.yaml` files are the same statements written by
the review-yaml codec.

For statements about a key (W-8, mofn#180): DV-2 (the naming definition),
TV-12 (Alice's define of DV-2) and TV-13, the published vector whose own note
reads "attestation about a KEY" — Alice says Bob's key has the name "fred".
Neither TV-12 nor TV-13 carries `not-on-or-after`, so goldens built from them
never expire.
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from engine.codecs import CODECS

VECTORS = HERE.parents[2] / "spec" / "vectors" / "ksa-core" / "vectors.json"
ARTIFACT = b"ksa example artifact\n"
STATEMENTS = {
    "TV-1": "tv-1-alice.pub",
    "TV-3": "tv-3-define",
    "TV-4": "tv-4-attestation",
    "TV-12": "tv-12-define-names",
    "TV-13": "tv-13-name",
}


def wanted() -> dict[str, bytes]:
    v = json.loads(VECTORS.read_text(encoding="utf-8"))
    out = {
        "dv-1.def": bytes.fromhex(v["definitions"]["DV-1"]["body"]),
        "dv-2.def": bytes.fromhex(v["definitions"]["DV-2"]["body"]),
        "artifact.bin": ARTIFACT,
    }
    for name, stem in STATEMENTS.items():
        envelope = bytes.fromhex(v["positive"][name]["envelope"])
        for codec in CODECS.values():
            out[stem + codec.suffix] = codec.dump(envelope)
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
        print(f"stale: fixtures/{name}")
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
