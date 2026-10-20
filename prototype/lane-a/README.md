# lane-a — what do the bytes look like? (mofn#13)

Throwaway experiment. Never ships; decides nothing (DEC-002, DEC-005 stay open).

## The question

Signed formats are full of **identifiers**: numbers or strings whose meaning comes from a table someone else owns, usually IANA. In a COSE header `{1: -8}`, `1` means "algorithm" and `-8` means "EdDSA" only because IANA's tables say so.

R-M-12 says ours should be **key-relative** instead: `(defining key, label)`, e.g. `{1: [<key X id>, 1]}` — "algorithm number 1 as key X defines it".

So, for each format: **list every registry identifier, replace each with a key-relative one, and record what still works.** This is *not* about canonical encoding (spaces in JSON, key order in CBOR) — that was #14/#73.

## Run

```sh
./run-all.sh                                  # 03 uses npm sigstore@2.3.1
./run-all.sh --npm NAME@VERSION               # another npm package
./run-all.sh --github OWNER/REPO ./FILE       # needs gh >= 2.49, logged in
```

Arguments go to 03 only. 04 reads 01's output, so it runs after 01. For `--github`, `FILE` must be downloaded first: 03 hashes it and asks GitHub for provenance of that hash. A file has provenance only if a workflow signed it (`actions/attest-build-provenance`). If gh fails: `unknown command "attestation"` → upgrade gh; anything else (404, no attestations) → that file was never attested; use `--npm`.

| script | builds | checked by |
|---|---|---|
| `01_cose_sign1.py` | COSE_Sign1, Ed25519 | `cryptography` over a Sig_structure rebuilt from the message |
| `02_dsse_intoto.py` | in-toto Statement in DSSE | Ed25519 over a PAE rebuilt from the envelope |
| `03_slsa_provenance.py` | real SLSA provenance | leaf-certificate key over the PAE; chain and Rekor **not** checked |
| `04_key_relative.py` | one message per identifier, with only that identifier made key-relative | the signature, **and** a real library reading the message (pycose 1.1.0; `in-toto-attestation` 0.9.3) |

`04` writes `out/key_relative.json`: one row per identifier, with the library's own error text.

**PAE** — the bytes DSSE actually signs: `DSSEv1 <len> <payloadType> <len> <payload>`. COSE's equivalent is `Sig_structure`. Both put the type inside the signature, so it cannot be changed after signing.

## Findings so far

1. **Registry identifiers.** COSE: tag 18, header labels 1/3/4, alg −8, content format 60. DSSE/in-toto: `payloadType`, `_type`, `predicateType`, `sha256`. SLSA adds `buildType`, `builder.id`, Fulcio OIDs `1.3.6.1.4.1.57264.*`.
2. **The signature layer does not care about meaning.** Each row of `04` is signed *after* its swap, and all 15 still verify. That only says a signature covers bytes; what breaks is the reader.
3. **COSE (pycose 1.1.0).**

   | made key-relative | pycose |
   |---|---|
   | header label 1 (alg) | fails: finds no algorithm (`'NoneType' object has no attribute 'verify'`) |
   | alg value −8 | rejects: `Unknown COSE attribute` |
   | content format value 60 | rejects: `CONTENT TYPE should be an unsigned integer or string` |
   | tag 18 | cannot be key-relative (a tag is one integer); left off, pycose rejects: `Message was not tagged` |
   | header label 3 (content type) | verifies, but the header is kept and **not understood** |
   | header label 4 (kid) | verifies, but the header is kept and **not understood** |
   | a payload map key | verifies |

   So: wherever pycose uses or type-checks a value (algorithm, content format, the tag), the swap breaks. An unknown label is skipped, and its meaning is lost without an error. RFC 9052 allows only `int / tstr` as a label, so an array label is not valid COSE at all — pycose is lenient to accept it.
4. **in-toto (`in-toto-attestation` 0.9.3).** Only `_type` is rejected (`Wrong statement type`). `predicateType` and the digest name `sha256` pass: `validate()` only checks that `predicateType` is not empty and that a digest exists. `buildType` and `builder.id` pass because `validate()` never reads the predicate — those two rows show nothing yet. `payloadType` is not tested — this library does not read DSSE envelopes.
5. SLSA v1.0 and v1.1 share one `predicateType`.

**So far:** key-relative names fit inside the payload; the envelope keeps registry identifiers — consistent with "COSE/DSSE for export only" (MD-3). In COSE the break is exactly the identifiers the reader uses, and an unknown label is silently ignored rather than refused.

## Not tested — read before quoting the findings

- **The key-relative form is a placeholder.** `[key id, label]` in CBOR and `"key:<key id>:<label>"` in JSON are the simplest thing that works, not a proposal. DEC-002, DEC-004 and DEC-005 stay open.
- **One library per format.** A stricter verifier (`slsa-verifier`, `gh attestation verify`) checks `predicateType` and `builder.id` against expected values and would likely reject rows that `in-toto-attestation` passes. That has not been run.
- **COSE `crit` (header label 2) is not tried.** It exists to stop exactly the silent skip in finding 3: a receiver that does not understand a label listed in `crit` must reject the message.
- **The real SLSA provenance (03) is not changed.** It is signed by a Fulcio key we do not hold, so any change breaks its signature. Its identifiers are tested through the SLSA-shaped predicate in 02.
- **No CWT claims.** The COSE payload is a plain map, so CWT claim keys from #13's list are not tested.
