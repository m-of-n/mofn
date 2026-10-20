---
schema: "design-log/v1"
id: DL-0012
part: produced
date: "2026-10-19"
---

# DL-0012 — produced

All in `prototype/lane-a/`. Nothing in `spec/`, nothing in `src/`, no library
change. Model: Claude Opus 5.5.

| file | change |
|---|---|
| `04_key_relative.py` | **new.** One message per identifier, with only that identifier made key-relative. Each is signed, then checked twice: the signature (rebuilt Sig_structure or PAE), and a real library reading it |
| `requirements.txt` | `in-toto-attestation==0.9.3` added |
| `run-all.sh` | runs `04` after `01` and `02` |
| `README.md` | `04` in the table; findings 2–4 rewritten from `04`'s results; a "Not tested" section |
| `01`–`03`, `common.py` | "artifact" → "sample" / "output"; `01`'s `build_eddsa` docstring tidied, meaning kept |

The key-relative form is a placeholder: `[sha256(public key), label]` in CBOR,
`"key:<hex>:<label>"` in JSON. It is not a proposal.

`04` checks itself against `01` and `02`: its unchanged COSE message must be
byte-identical to `01`'s, and its unchanged Statement to `02`'s.

## Result (`out/key_relative.json`)

| format | made key-relative | signature | library | library said |
|---|---|---|---|---|
| COSE | — (baseline) | yes | yes | verified |
| COSE | header label 1 (alg) | yes | **no** | `AttributeError: 'NoneType' object has no attribute 'verify'` |
| COSE | alg value −8 | yes | **no** | `CoseException: Unknown COSE attribute …` |
| COSE | header label 3 (content type) | yes | yes | verified; label kept but not understood |
| COSE | content format 60 | yes | **no** | `ValueError: CONTENT TYPE should be an unsigned integer or string` |
| COSE | header label 4 (kid) | yes | yes | verified; label kept but not understood |
| COSE | tag 18 (left off) | yes | **no** | `AttributeError: Message was not tagged.` |
| COSE | a payload map key | yes | yes | verified |
| in-toto | — (baseline) | yes | yes | `validate()` passed |
| in-toto | `payloadType` | yes | – | not tested: the library does not read DSSE envelopes |
| in-toto | `_type` | yes | **no** | `ValueError: Wrong statement type` |
| in-toto | `predicateType` | yes | yes | `validate()` passed |
| in-toto | digest name `sha256` | yes | yes | `validate()` passed |
| in-toto | `buildType` | yes | yes | `validate()` passed |
| in-toto | `builder.id` | yes | yes | `validate()` passed |

Two full `run-all.sh` runs gave identical `SHA256SUMS` (32 files).

## What it says about R-M-12

The signature never breaks: it covers bytes, not meaning. What breaks is the
reader, and only for identifiers the reader must act on — the algorithm, the
content format, the COSE tag, the in-toto `_type`. A label the reader can
skip is skipped without an error, so its meaning is lost quietly. This is
evidence for, not a decision on, "COSE/DSSE for export only".
