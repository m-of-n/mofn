---
schema: "design-log/v1"
id: DL-0010
part: produced
date: "2026-10-10"
---

# DL-0010 — produced

All of it in `mofn/`, on branch `report/0004-uptake`. **Nothing in `library/`**
— the three stub records this report leans on are named as follow-on work
rather than fixed here, because fixing them is library-repo work with its own
skills and its own PR (`PROC-0003` §1), and mixing the two would have put
record edits on a detached submodule HEAD.

## `research/0004-uptake-and-applications/` — four files

**`report.md`** (705 lines, `R-0004`, `status: draft`, `library_pin:
library@93891c9`). Ten sections. The structure is not R-001's, deliberately:
R-001 is a taxonomy, this is an argument in four moves — what is being adopted,
what the ancestors did instead, a model that separates them, and the model
turned on this project.

**`sources.md`** (157 lines) — nine primary retrievals with what each settled,
the 56 R-001 records relied on *without* re-retrieval and why, both
measurements' full output including the 30-certificate subject listing, and
four ingestion candidates.

**`searches.md`** (62 lines) — fourteen numbered queries and retrievals,
verbatim, with yields. **Four are explicit misses**, and three of those changed
what the report claims; §3 below says how.

**`unverified.md`** (127 lines) — the publication gate. Fifteen claims that did
not survive, every one absent from `report.md`, plus one correction to an
assumption the brief started with.

## Two original measurements

Neither was planned. Both exist because a primary source for the number does
not, and the alternative was citing a blog.

**The C2PA root of trust is 30 certificates.** `C2PA-TRUST-LIST.pem` fetched
from `c2pa-org/conformance-public` (37,911 bytes, sha256 `75cacc98…64aea5`),
split on `BEGIN CERTIFICATE`, each subject/issuer/expiry read with `openssl
x509`, root classified as subject == issuer. Result: **30 certificates, 17
organisations, 19 self-signed roots, 11 intermediates**; `C=US` 20, `C=CN` 8,
`C=NL` 1, `C=DE` 1. Google holds 6, DigiCert 4. Three of the 17 — DigiCert,
SSL.com and TrustAsia — are incumbent WebPKI CAs.

This is the measurement the report is built around, because of what it shows:
content provenance, under eighteen months of statutory pressure, **rebuilt
X.509's root-program structure**, commercial CAs included. That is precisely
the trust-anchor installation path R-001 §5.7(d) identifies as the thing SPKI
did not have and could not supply.

**npm provenance: 100 of 300 packages, but 56 of 242 publishers.** Sampled from
the npm registry search API on pure popularity weighting across three keyword
queries, deduplicated to the top 300; provenance tested as presence of
`dist.attestations` on the latest version. 0 fetch errors.

The two readings differ by ten points and the gap is the finding: **provenance
is a per-pipeline switch, not a per-package decision**, so per-package counts
are inflated by monorepos. `@inquirer` contributes 16 packages and one
decision. The report states both numbers and flags that its own headline figure
has the bias.

## `design-log/0010-uptake-report/` and the README

This entry, three files. `design-log/README.md` gains its row. `DL-0007`
through `DL-0009` are taken on unmerged branches, so this is **0010**; the id
was chosen by listing `design-log/` across all remote branches rather than
across `main`, which would have collided.

## What was deliberately not produced

- **No `library/` changes.** Four ingestion candidates and three stub upgrades
  are named in `sources.md` §4 and `report.md` §10, for a library PR.
- **No ARCH-0001 diff.** §8 is an argument that this design carries three of
  SPKI's five failure modes. If that survives review it belongs in the
  architecture document via `propose-arch`, not in a research report, and §10
  files it that way.
- **No `LIMITATIONS.md` edit**, although §8.3 argues one is needed.
- **No regenerated `docs/`, `mkdocs.nav.yml` or `PUBLISHING.md`** beyond what
  `bin/manifest` produces; CI drift-checks them (#62).
