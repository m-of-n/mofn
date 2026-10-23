---
schema: "design-log/v1"
id: DL-0014
part: produced
date: "2026-10-23"
---

# DL-0014 — produced

## Artifacts

| file | change |
|---|---|
| `spec/ARCH-0001-authorization-attestation.md` | v0.1.3 (PATCH, additive per §9.1 — the 0.1.2 precedent). §7 DEC-002 and DEC-003 each gain an *inputs the ADR must answer* block |
| `spec/ARCH-0001-CHANGELOG.md` | 0.1.3 entry |
| `spec/ARCH-0002-key-relative-naming.md` | v0.8.0 (MINOR). P1.1 *what a foreign `kid` is not*, `[draft]`; relationship-table row for DEC-003 |
| `spec/ARCH-0002-CHANGELOG.md` | 0.8.0 entry |
| `spec/ARCH-0001-PROPOSAL-v0.2.0.md` | rev.5. One sentence in option 5 pinning RFC 8949 §4.2.1 order with a rejecting decoder |

## Verdict per #112 checkbox

"Survives" means the governing text already does what the finding asks.
"Gap" means the text was silent and now is not.

| #112 item | governing text | verdict | where it went |
|---|---|---|---|
| DEC-002: ranking reversed on detectability of order-only divergence | `SPEC-0002` §4.2(3), §4.3 | **survives for native objects** — order divergence is a V5 rejection — but **gap**: DEC-002's drivers never named the criterion, and option 5 reaches it only by a stated rule | `ARCH-0001` §7 DEC-002 |
| DEC-002: "no IANA tags" narrower than it sounds | `SPEC-0002` §4.1, §4.3 | **survives** — tags forbidden and rejected; **gap**: the property was described as the format's, and as tag-only | `ARCH-0001` §7 DEC-002; proposal rev.5 |
| DEC-002: does our profile pin map order? | `SPEC-0002` §4.2(3) | **survives** — bytewise lexicographic, §4.2.1. RFC 8747's printed order is exactly this order. **Gap** in option 5's own text | proposal rev.5 |
| DEC-002: do not carry `cnf` | `SPEC-0002` (no `cnf`; native PoP §6.4) | **survives**; boundary rule was unwritten | `ARCH-0002` P1.1 |
| Acceptance test: threshold invariant unschemable | `SPEC-0002` §8.6, V8 | **survives** — V8 owns it, which is the second of #112's two remedies; **gap**: ARCH-0001's test did not say so, and `spec/vectors/ksa-core/` has no threshold vector | `ARCH-0001` §7 DEC-002 |
| DEC-003: RFC 9679 ADAPT, three blockers | `SPEC-0002` §4.5 | **survives** — `kid` is not a COSE_Key thumbprint | `ARCH-0001` §7 DEC-003 |
| DEC-003: PQ `KeyId` contains an IANA allocation | `SPEC-0002` §6.5 | **survives** — suite 8 hashes the raw FIPS 204 key; the finding disqualifies the *thumbprint option*, not our derivation | `ARCH-0001` §7 DEC-003 |
| DEC-003: canonical key bytes if derived? | `SPEC-0002` §6.1, §6.3, §6.5 | **survives** — per-suite public-key encoding. **New question found** (below) | `ARCH-0001` §7 DEC-003 |
| P1: RFC 8747 §3.4 contrast | `ARCH-0002` P1 | **survives**; contrast unwritten, and `SPEC-0002` calls its derived identifier `kid` | `ARCH-0002` P1.1 |
| P1: two places for one `kid` — which wins? | — | **gap** → neither; compute from the key, report disagreement | `ARCH-0002` P1.1 |
| P1: §6 intentional collision | — | **gap** → impossible under derivation; continuity carried elsewhere | `ARCH-0002` P1.1 |

## One finding the model added

**The inverse of RFC 9679's AKP defect.** RFC 9679's problem is an algorithm
*inside* the preimage. `SPEC-0002`'s `kid` has *no* algorithm in the preimage,
so identical key octets under two suites give one `kid`. Suites 1 and 8 cannot
collide (32 vs 1952 octets); a future equal-length suite could. Recorded as a
question for the DEC-003 ADR, deliberately not answered: putting the suite code
in the preimage would put **our own** registry number in the identifier, which
is the same shape of objection #112 raises against IANA's.
