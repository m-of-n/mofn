# Sources

Every citation in `report.md` resolves to a record in `m-of-n/library`. This is
enforced mechanically, not by convention: `bin/build-references` scans the
report for `[@record-id]` citations, resolves each against the library, and
**exits non-zero if any citation has no record**. The References section is
generated from that resolution and must not be hand-edited.

The rule this implements: *a reference we do not hold is not a reference we
cite.* A claim whose source is absent from the library is therefore absent from
the paper by construction, rather than by anyone remembering to check.

## Current state

- **155 citations**, all resolved.
- **273 library records** across 14 topics.

## Regenerating

```sh
bin/build-references                       # uses the pinned library submodule
bin/build-references --library ../library  # drafting against an unmerged branch
```

CI must use the first form, because the submodule pin is what makes the
bibliography reproducible. **The submodule is currently behind** — it points at
a 77-record commit while the survey needs 273. Bump it after the library PR
merges; until then the `--library` override is required.

## Coverage by area

| Area | Topic(s) in library | Status |
|---|---|---|
| A — foundations | `signature-foundations` | complete |
| B — X.509 / PKIX | `namespace-governance` | complete, incl. original measurement |
| C — decentralised naming | `namespace-governance`, `uptake-failure` | complete |
| D — content labelling | `predicate-rendering`, `uptake-failure` | complete |
| E — device attestation | `device-attestation` | complete |
| F — supply chain | `supply-chain-attestation` | complete |
| G — capability / delegation | `capability-delegation` | complete |
| H — post-quantum | `post-quantum-migration` | complete |

## Distillation status

All records ingested for this survey are **stubs** — present and citable, with
title, URL and topic, but not distilled. Distillation (normative extraction,
field tables, requirements with verbatim text and locators) is per-record work
tracked separately. The survey does not depend on it: it cites primary sources
that the research lanes read directly, and the mini-reports in `mini-reports/`
preserve what each lane quoted.

The one exception is area B, which returned **43 extracted requirements** from
RFC 5280 and the CA/B Forum baseline requirements, with verbatim text, section
locators, RFC 2119 verb and actor. Those are in `mini-reports/B-x509-pkix.md`
§3 and are the natural seed for the first distilled record.

## What is deliberately not cited

`unverified.md` is the publication gate. It collates, verbatim, every item the
eight research lanes could not establish from a primary source — 10 sections,
including several corrections to claims the drafting brief had assumed true.
Nothing in that file may be asserted as fact in the report without being
verified and ingested first.
