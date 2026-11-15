#!/usr/bin/env python3
"""Copy the archives vocabulary out of the published vectors (W-2b, DL-0046).

    .venv/bin/python domains/archives/generate.py           # from prototype/wallet
    .venv/bin/python domains/archives/generate.py --check   # exit 1 if a file differs

Since W-2b there is one archives vocabulary: DV-5 `library-review` v2 in
`spec/vectors/ksa-core`. This directory holds byte-for-byte copies of it and
of its definer's two statements, never edited by hand, as `fixtures/sync.py`
does for DV-1. Until W-2b this script built a separate `archives` v1 with the
engine's encoder (DL-0033); that vocabulary is retired.

Files written beside this script:

    library-review.def           DV-5, KSA-CBOR; its id is its SHA-256
    dave.pub.stmt[.yaml]         TV-38, Dave's key-publish (the definer)
    dave-define.stmt[.yaml]      TV-39, the define statement that says DV-5 is Dave's

Not written here: `record.yaml`, the example subject. It is the library
record `w3c-prov-dm`, copied byte for byte once (library@6dcbdb0) and then
frozen, because statements name its digest and the live record may change.
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

from engine.codecs import CODECS

VECTORS = HERE.parents[3] / "spec" / "vectors" / "ksa-core" / "vectors.json"
STATEMENTS = {"TV-38": "dave.pub", "TV-39": "dave-define"}


def wanted() -> dict[str, bytes]:
    v = json.loads(VECTORS.read_text(encoding="utf-8"))
    out = {"library-review.def": bytes.fromhex(v["definitions"]["DV-5"]["body"])}
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
        print(f"stale: domains/archives/{name}")
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
