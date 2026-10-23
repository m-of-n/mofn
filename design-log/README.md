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
| `0012-lane-a-key-relative` | LANE A (mofn#13): what breaks when registry identifiers are key-relative — the signature never does, the reader does | **open** — human review pending; library records not yet written |
| `0013-publish-research-reports` | research reports reach the validator — mofn#88. The publishing half shipped separately in mofn#103 | **open** — human review pending |
| `0014-cbor-cose-handover` | mofn#112 — the CBOR/COSE extraction checked against DEC-002, DEC-003, the acceptance test and P1; ARCH-0001 v0.1.3, ARCH-0002 P1.1, proposal rev.5 | **open** — human review pending; no DEC-* accepted |

**Two ids are shared: `0007` and `0012`.** `0007-library-harness-role` and
`0007-rejecting-decoder-spike`, and later `0012-d3-context-and-mechanism`
(mofn#103) and `0012-lane-a-key-relative` (mofn#109), were opened in parallel
lanes and each took the next free number. All four directories are on `main`,
so none is renamed here — a design-log id is cited from PRs and must not
silently retarget. A third `0012`, opened for mofn#88, was renumbered `0013`
before it merged; nothing outside its own PR cited it. The next new entry
takes `0015`.

`DL-0001` is the argument for the rule: **write the entry in the same change.**
The prompts, and what the human rejected, were not recoverable a week later —
including whether ARCH-0001 §4.2's five statement kinds were proposed or
directed, which register item 6a now has to decide without that evidence.
