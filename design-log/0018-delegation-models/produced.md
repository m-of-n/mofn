---
schema: "design-log/v1"
id: DL-0018
part: produced
date: "2026-11-01"
---

# DL-0018 — produced

Two PRs. **mofn#118** holds the report; **library#94** holds the two records it
needed and is merged.

## `research/0007-delegation-models/` (mofn#118)

**`report.md`** (`R-0007`, v0.2.0, `status: draft`, pinned at `library@a1aa258`).
The issue's case in the syntax of X.509, S/MIME, OpenPGP, SDSI and SPKI, with
both must-fail cases; the issue's table; its five questions; a test of the
project's claim (§7); six proposals (§8).

**`sources.md`, `searches.md`, `unverified.md`.** `unverified.md` began with
four open claims. Two are now settled by experiment and stay in place, numbered
as they were, so the report's references still resolve. Two remain open.

**`experiments/gnupg-tsign-chain.sh` and `.out`.** A throwaway-keyring
experiment with two controls and two tests.

## What the report found

- **Scoping is not the discriminator.** Every system compared except S/MIME can
  scope a delegate to `foo.com`. What differs is what the scope covers (names a
  delegate may certify, or what it may say), whether it narrows along the whole
  chain, and whether the relying party's own scope is in the format.
- **`*@eng.foo.com` is not within `*@foo.com` under SPEC-0003 §6.3**, so the
  expected result of UC-5, the project's own example, is wrong (P1).
- **OpenPGP defines no rule for combining scopes along a chain, and GnuPG does
  not narrow them.** Run on 2.5.24: with Dave → Alice scoped to `foo.com` and
  Alice → Bob scoped to `bar.com`, `carol@bar.com` comes out fully valid for
  Dave.
- **GnuPG's `--quick-tsign-key` domain scope over-matches.** Run on 2.5.24: an
  `eng.foo.com` scope accepts `carol@eng-foo.com`.

## The experiment's output

| case | Carol's validity | reading |
|---|---|---|
| control: `carol@eng.foo.com`, scope `eng.foo.com` | `f` | as expected |
| control: `carol@bar.com`, scope `eng.foo.com` | `-` | as expected |
| `carol@bar.com`, Alice widens Bob to `bar.com` | `f` | no narrowing along the chain |
| `carol@eng-foo.com`, scope `eng.foo.com` | `f` | `.` over-matches |

The script was run twice, because `tail` cut the first run's controls from view
and its exit status was lost to the pipe. The `.out` file is the second run, filtered to the version line, the
legend and the four result lines. The raw output was 114 lines, the rest being
key listings that `--quiet` does not suppress.

## Corrections to earlier work, in the report

- **R-001 §4.3** says RFC 5280 gives the relying party no channel for scoping
  an anchor. §6.1.1(h) is one, though optional and per validation (§7.3 item 1).
- **The library topic answer** cites GnuPG T6238, which current `trustdb.c`
  appears to fix (§7.3 item 2). This is a source reading, not run.
- **ARCH-0001 R-M-10** (boolean) disagrees with **SPEC-0004 §6.3** (integer
  depth) (§7.3 item 3, P3).

## Proposals P1–P6 (report §8)

P1 fixes UC-5 and SPEC-0003 §6.3. P2 states that SPEC-0004 §6.3 checks scope
against the whole path, with a vector. P3 reconciles R-M-10 with SPEC-0004. P4
records revocation's non-determinism. P5 names escrowed revocation. P6 sets the
X.509 import mapping for `nameConstraints`. **None is applied.**

## library#94 (merged as `a1aa258`)

`rfc-8550` and `sdsi-1-1` brought to the summary bar, and the `delegation-models`
topic updated to list both and point at the report. Both summaries were written
by subagents. The model skimmed them before committing and did not verify them
line by line. FX-1 was not claimed for either record.

## This entry and the housekeeping

`design-log/0018-delegation-models/`, its row in `design-log/README.md`, the
library pin moved to `a1aa258`, and `bin/manifest` output.

## What was deliberately not produced

- **No `spec/`, `ARCH-0001` or `UC-0001` edit.** P1–P6 are proposals.
- **No FX-1 extraction of `rfc-8550` or `sdsi-1-1`.** No issue owns one yet.
- **No X.509 library survey and no S/MIME client survey** (`unverified.md`
  §3–§4).
- **No study of OpenPGP implementations other than GnuPG** (report §9).
