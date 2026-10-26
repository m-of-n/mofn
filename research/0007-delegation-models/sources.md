---
schema: "library-doc/v1"
id: R-0007-sources
title: "Sources consulted — delegation models"
type: evidence
status: draft
version: "0.1.0"
date: "2026-10-26"
updated: "2026-10-26"
---

# Sources

The bibliography is pinned at **`library@f15fd76`**, plus `rfc-8550` and
`sdsi-1-1` as brought to the summary bar in the library PR that closes
library#14. Every `[@key]` in `report.md` resolves at that state.

**Quote audit.** Every verbatim quotation in `report.md` was checked by script
against the sources below: 62 italic quoted spans. The whole span was checked,
not fragments, with whitespace and RFC page furniture normalised. All
quotations from primary sources resolve. The spans that do not resolve
against a cached source are quotations of our own documents: library#14's
body, UC-0001, R-001 and the `delegation-models` topic answer. Each was
checked by reading that document.

## 1. Library records read

| record | bar at the pin | what `report.md` takes from it |
|---|---|---|
| `[@rfc-5280]` PKIX | FX-1 `full` | §4.2.1.9 `pathLenConstraint`; §4.2.1.10 mailbox/host/domain forms, fail-open, MUST-critical; §6 anchor *"a matter of policy"*; §6.1.1(d) out-of-band anchor; **§6.1.1(h)/(i) initial subtrees and the "not required to support" sentence**; §6.1.3(b); §6.1.4(g) intersection; §6.2 *"free to process or ignore"*; §3.3; §6.3.3 `UNDETERMINED`; §8 one name form does not protect another; §4.1.2.6 `emailAddress` |
| `[@rfc-8551]` S/MIME 4.0 messages | FX-1 `full` | §4: certificates are out of scope |
| `[@rfc-8550]` S/MIME 4.0 certificates | **summary bar, written for this report** | §2.3 anchor guidance; §3 From/Sender check and its conditions; §4.1 revocation MUSTs and CRL scope; §4.2 RFC 5280 validation MUST; §4.4 critical-extension SHOULD NOT; §4.4.2–§4.4.4 |
| `[@rfc-9580]` OpenPGP | FX-1 `full` | §5.2.3.21 trust signature levels and amounts; §5.2.3.22 regex scope; §5.2.3.23 Revocation Key deprecated; §5.10 Trust packet; §13.9 escrowed revocation |
| `[@rfc-2693]` SPKI theory | FX-1 `full` | §1.1 ACL; §2.6 SDSI names; §4.1.3–§4.1.4 boolean over integer; §5.1–§5.2 CRL determinism; §6.1–§6.3.1 5-tuple, 4-tuple, AIntersect and the *-forms |
| `[@rfc-2692]` SPKI requirements | FX-1 `full` | background for §5.4 only |
| `[@rfc-9804]` S-expressions | FX-1 `full` | §7.2: the encoding standardised in 2025 |
| `[@draft-ietf-spki-cert-structure]` | summarized | `<cert>` grammar, `(propagate)`, ACL syntax, used for the §3.5 rendering |
| `[@sdsi-1-1]` SDSI 1.1 | **summary bar, written for this report** | §2 email mapping and `!!` roots; §2/§6.4 `Delegation-Cert`; §5.2 `DNS!!` resolution; §6.2 reconfirmation; §7 groups |

Records cited **through** R-001 and not re-read: `[@survey-2026-nameconstraints-measurement]`,
`[@go-nameconstraint-cves]`, `[@openssl-2022-email-overflow]`, `[@rfc-9598]`,
`[@rfc-5937]`, `[@liu-2015-revocation]`, `[@cabforum-sc063]`, `[@rfc-9608]`,
`[@ulrich-2011-openpgp-wot]`, `[@keys-openpgp-org-faq]`. These are all stubs at
the pin (library#45). `report.md` attributes their facts to R-001, not to the
records.

## 2. Project documents read (mofn, at `e02ee84`)

| document | used for |
|---|---|
| `spec/UC-0001` §UC-5 | the case |
| `spec/SPEC-0003` §6, §6.1, §6.3 | email and dns-name algebra; the §2.2 defect |
| `spec/SPEC-0004` §4.2–§4.4, §6.1–§6.3, §7.1 | anchors, path following, integer depth, widening, revocation |
| `spec/ARCH-0001` §4.2, §5, §6 | R-M-04, R-M-10, R-I-04, R-I-05; the interchange matrix |
| `research/0001-signatures-and-attestation` §4–§5, §9, `unverified.md` | X.509 history, the measurement, OpenPGP's collapse; the §7.3 correction |
| `research/0002-wallets` §5.3 | GnuPG trust-signature defaults |
| `library/topics/delegation-models.yaml` | the starting hypothesis |

## 3. Implementation source (GnuPG)

Fetched from the GitHub mirror of the GnuPG repository (`gpg/gnupg`, branch
`master`) on 2026-10-26. `dev.gnupg.org` did not respond. Read, not built or
run.

| file | sha256 of fetched bytes | used for |
|---|---|---|
| `g10/keyedit.c` | `a12295c7b9773cd04bd06d49ce5d2a7a08fc6835ffda296aa19d820759e6fe67` | `parse_trustsig_string`, which builds `<[^>]+[@.]DOMAIN>$` without escaping; the interactive `trustsig_prompt`, which escapes |
| `g10/trustdb.c` | `eb89514c3ba169cbccec5b417667c110dc6e1612bf80d0f711b5a9f839c11110` | `REGEXP_OPERATOR_CHARS`, `sanitize_regexp`, `check_regexp` (bare-mailbox wrapping), `validate_one_keyblock` (regex replaced per key, depth min'd) |
| `g10/gpg.c` | not recorded | `--quick-tsign-key` argument shape `depth,[m\|f][,domain]` |

**Not ingested into the library.** Source files of a moving branch are not a
citable document. If R-0007's GnuPG claims become load-bearing, the
experiment in `experiments/` should be run against a released version and its
output recorded as a library record.
