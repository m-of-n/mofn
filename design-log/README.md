# Design log

The project claims **AI-assisted protocol design** as part of its contribution.
That is only a contribution if it is instrumented from day one — retrofitted in
November it produces a narrative, not evidence.

One entry per design decision:

```
NNNN-slug/
  question.md   what was asked, and the context supplied
  produced.md   what the model produced (spec text, schema, code, vectors)
  review.md     what a human accepted, edited, or REJECTED — and why
  → outcome: the ADR, or the reason there is none
```

Every generated artifact elsewhere in the repo carries a header naming its
source: which document section, which prompt, which model, which date.

**Write up the failures.** The half where a human overruled the model is what
makes the claim credible, and it is the half nobody else publishes. A design log
containing only successes is evidence of poor record-keeping, not of good design.

**Guardrail:** no generated cryptographic primitives, ever. Vetted libraries
only. AI assistance applies to specification, schema, encoding, mappings, test
vectors, and tooling.

## Entries

| id | subject | status |
|---|---|---|
| `0001-arch-0001-genesis` | ARCH-0001 v0.1.0 | **partial** — reconstructed a week late, and permanently degraded as a result |
| `0002-arch-0002-cycle` | ARCH-0002, ADR-0001 | complete |
| `0003-cbor-reference-sweep` | library +51 records, 2 topics; RPT-0001 | complete |
| `0004-library-body-field` | library `body` — scope §4, record schema v0.6.0; the three defects it turned up | **open** — human review pending on library#34, #37, mofn#55 |
| `0005-cipher-suite` | what a cipher suite is, critique of the external `cipher_suite.py` | **open** — human review pending; no code change; DEC-002 untouched |
| `0006-canonical-encoding-close` | RFC 9804 scored, DSSE read out, two claims withdrawn; library#57 | complete |
| `0007-library-harness-role` | what the library is for — README in both repos; the one-way `bears_on` edge | **open** — human review pending; no spec change; FX-1 untouched |
| `0007-rejecting-decoder-spike` | the rejecting-decoder spike — canonicality decidable by parse alone; the falsifier does not fire; mofn#78 | complete |
| `0008-quotes-md-retirement` | `quotes.md` and the pre-FX-1 companion vocabulary — record schema v0.7.0 | **open** — human review pending; no spec change; library#63 |
| `0009-adr-0002-draft` | `ADR-0002` at `status: proposed`; the register sync mofn#80 | **open** — human review pending; no DEC-* accepted; ARCH-0001 untouched |
| `0010-uptake-report` | D3 *uptake & applications* report `R-0004`; two original measurements; the SPKI/PICS failure analysis turned on our own design | **open** — human review pending on mofn#84 |
| `0011-dco-merge-commits` | exempting merge commits from the `dco` check | **rejected** — mofn#92 closed unmerged; check stays strict, contributors rebase, `dco` now required |
| `0012-d3-context-and-mechanism` | D3 *context* `R-0005` and *mechanism* `R-0006` reports (T-025, T-026); four claims retracted against `ADR-0003` | **open** — human review pending on mofn#99/#100; merged in mofn#103 |
| `0012-lane-a-key-relative` | LANE A (mofn#13): what breaks when registry identifiers are key-relative — the signature never does, the reader does | complete — reviewed 2026-11-05; library records and the topic `answer` still to come, in the library repo |
| `0013-publish-research-reports` | research reports reach the validator — mofn#88. The publishing half shipped separately in mofn#103 | **open** — human review pending |
| `0014-cbor-cose-handover` | mofn#112 — the CBOR/COSE extraction checked against DEC-002, DEC-003, the acceptance test and P1; ARCH-0001 v0.1.3, ARCH-0002 P1.1, proposal rev.5 | **open** — human review pending; no DEC-* accepted |
| `0015-dec-002-dec-003-adrs` | DEC-002 → option 5 (`ADR-0004`), DEC-003 → `kid` (`ADR-0005`), P1.1 → reject; under the sponsor's delegation (mofn#116) | **open** — ADR text review pending; T-031 in `0019` |
| `0016-wallet-engine-v0` | W-1 wallet engine v0 (mofn#65): KSA-CBOR, V1–V9, the human-review codec, coverage and the six-line verdict; PyNaCl over `cryptography` for N-4 | **open** — human review pending; no DEC-* touched; A1, C1, C4 and the open items decided in DL-0020 |
| `0017-proc-0002-v0-3` | PROC-0002 v0.3 — completing mofn#18: stage 8 is a harness over a vetted library, never a primitive; `artifacts/` → `harness/`; DL-0009's two rules bind | **open** — human review pending |
| `0018-delegation-models` | D3, library L-040: delegation and trust across X.509, S/MIME, OpenPGP and SDSI/SPKI, `R-0007`; UC-5 wrong under SPEC-0003 §6.3; two GnuPG claims run on 2.5.24; written after the fact, from the transcript | **open** — human review pending on mofn#118; no DEC-* accepted; P1–P6 unapplied |
| `0019-threshold-fixture` | T-031 — threshold and `NameCert` vectors for DEC-002's acceptance test; `n = len(members)` holds by construction, so V8 owns only the range; no defect in option 5 | **open** — human review pending |
| `0020-w-1-decisions-slice` | W-1 decisions A1, C1, C4 and DL-0016's open items; `demo/slice.sh`; SPEC-0002 0.4.0, SPEC-0003 0.1.1, SPEC-0004 0.2.0 | **open** — spec diffs accepted by ndewedo-newbury 2026-11-03; code review pending; C2, C3, C5 unidentified; no DEC-* touched |
| `0021-sponsor-delegation-w1-close` | the sponsor's October delegation recorded (all three decide, the decider carries it); A2, A3 and the six-line rule decided; SPEC-0002 0.5.0 §6.1, SPEC-0004 0.3.0 §10.2; W-3 next | **open** — written sponsor confirmation not recorded; no DEC-* touched |
| `0022-wallet-menu-version` | W-6 (mofn#127) wallet 0.1.0: a bare `mofn` prints the menu, `--version`, the one-line dependency message, UTF-8/LF output, CHANGELOG, `ci.yml` on three OS; then `key list`, `key export`, `hash` from `gpg`, and the `gpg` commands left out | **open** — reviewed by David 2026-11-05; Windows and macOS not yet run; no DEC-* touched |
| `0023-wallet-run` | W-6 (mofn#127) wallet 0.2.0: `mofn run` is the wallet as a terminal app — forms that run the command they show, and Learn, which runs nothing; DV-1 ships as the example vocabulary; two goldens added; David rejected the executing tutorial | **open** — reviewed by David 2026-11-05; Windows and macOS not yet run; no DEC-* touched |
| `0024-adr-0002-accept` | `ADR-0002` accepted (mofn#6): P2, P3, P5 as amended, P6 normative; P4, P7 draft; the agent recommended *split* and the human overruled it | **open** — second reader for P5.1/P5.2 owed; no DEC-* touched |
| `0025-delegation-depth` | T-012c (mofn#136): integer depth kept (SPEC-0004), R-M-10 to be rewritten; `trust … about … may-delegate` named, `may-speak` retired; boolean rejected with RFC 2693 §4.1.4 carried as a stated limit | **open** — R-M-10 text owed to T-012a; no DEC-* touched |
| `0026-openpgp-transfer` | what to take from OpenPGP (mofn#128): ARCH-0001 0.1.9 §3.4 research inputs, PLAN-0004 0.2.0 §6.2 engine rules, `unlock` binds the seed to its kid; revocation-at-creation declined | **open** — human review pending; no DEC-* touched |
| `0027-adr-0006-dec-001` | `ADR-0006`: DEC-001 accepted, `m-of-n` / `mofn`; ratifies names in use since 2026-09-17; all five listed options rejected; the agent's first offer (leave it open) declined | **open**: second reader owed |
| `0030-locator-digest` | T-048 (mofn#144): `SPEC-0002` 0.6.0 withdraws target type 5, so every target binds a digest (R-M-07); a locator is an attribute; N-11; `ARCH-0001` 0.2.1 closes the §5.5 row; aliases, second target and body field rejected | **open**: second reader owed; `ARCH-0003` §3.7 owed to the sponsor; no DEC-* touched |
| `0028-arch-0001-v0-2-0` | ARCH-0001 v0.2.0 (mofn#134): proposal folded in, §4.2 one form, R-M-10/11, R-O-05/06, §5.5 gaps; DEC-007 accepted (`ADR-0007`); the agent recommended leaving DEC-007 open and the human closed it | **open** — second reader owed; mofn#143, #144 owed by SPECs |
| `0029-weekly-slice` | weekly `demo/slice.sh` run posted on mofn#68 by cron CI; verdict notes meant to stay human, but the first week's were AI-drafted at the owner's instruction (session 2); findings → mofn#157 | complete — workflow reviewed on mofn#147; cron to be narrowed after the Nov 11 floor |
| `0031-delegation-vectors` | T-012c/T-049 (mofn#136): SPEC-0002 0.7.0 TV-14…20 and evaluations E-1…E-4 (`depth`, `widening`); SPEC-0004 0.4.0 Appendix A asks 3–6; TV-13 sentence test | **open** |
| `0032-target-applications` | T-012b (mofn#135): ARCH-0001 0.3.0 §2.3 supply chain + archives; DV-3, TV-21…26, E-5…E-7 (SPEC-0002 0.8.0); AI agents motivation only | **open** |
| `0033-second-domain` | W-2 (mofn#66): APP-0002/0003 scenarios, `domains/archives/` through the same `make`/`check` with no engine change, `--lang` (wallet 0.4.0), APP-0004 five views, PLAN-0002 0.4.0 §6.5; the agent misattributed the `--lang` decision to the sponsor and corrected it; DV-3 in #152 overlaps | **open** — owner (@nymble) confirmation of `--lang` owed |
| `0034-plan-0004-build-and-status` | PLAN-0004 0.3.0: §7.1 schedule status (2026-11-09) and §9 build and release; decision #28 stays open | **open** |
| `0035-verdict-wording` | mofn#157: SPEC-0004 0.5.0 §10.4: sentences about another file are framed (F-1); the vacuous acceptance pass says why (F-2); wallet 0.4.1; drop-the-sentence and not-evaluated rejected | **open**: David's review pending |

**Two ids are shared: `0007` and `0012`.** `0007-library-harness-role` and
`0007-rejecting-decoder-spike`, and later `0012-d3-context-and-mechanism`
(mofn#103) and `0012-lane-a-key-relative` (mofn#109), were opened in parallel
lanes and each took the next free number. All four directories are on `main`,
so none is renamed here — a design-log id is cited from PRs and must not
silently retarget. A third `0012`, opened for mofn#88, was renumbered `0013`
before it merged; nothing outside its own PR cited it. Likewise
`0014-wallet-engine-v0`, for mofn#65, was renumbered `0016` before it
merged, when `0014` and `0015` reached `main` first, and
`0016-proc-0002-v0-3`, for mofn#121, was renumbered `0017` before it merged,
when `0016-wallet-engine-v0` reached `main` first. `0018-delegation-models`
was held for mofn#118, so `0019-threshold-fixture` skipped it. `0020-w-1-decisions-slice`
skipped `0018` and `0019`. `0022-openpgp-transfer`, for mofn#129, was renumbered `0026` before it merged, when `0022-wallet-menu-version` reached `main` first. `0025-adr-0006-dec-001`, for this ADR, was renumbered `0027` before it merged, when `0025-delegation-depth` reached `main` first. `0027-arch-0001-v0-2-0`, for mofn#145, was renumbered `0028` (and its `ADR-0006` to `ADR-0007`) before it merged, when mofn#142 reached `main` first. `0029-delegation-vectors`, for mofn#148, was renumbered `0031` before it merged, when `0029-weekly-slice` reached `main` first and `0030` was held by mofn#149. `0033-second-domain`, for mofn#66, took `0033` while `0032` was held by mofn#152. `0033-plan-0004-build-and-status`, for mofn#153, was renumbered `0034` before it merged, when mofn#154 reached `main` first with `0033-second-domain`. The next new entry takes `0036`.

`DL-0001` is the argument for the rule: **write the entry in the same change.**
The prompts, and what the human rejected, were not recoverable a week later —
including whether ARCH-0001 §4.2's five statement kinds were proposed or
directed, which register item 6a now has to decide without that evidence.
