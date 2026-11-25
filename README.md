# m-of-n

**Key-centric Semantic Attestations (KSA).** Authorization, local names, and artifact
attestation with a model whose principals are keys, whose names are relative to a
naming key, whose subjects may be *k*-of-*n*, and whose statements carry meaning
a person can read.

USF CS690 Master's Project, Fall 2026. Sponsor: Paul Lambert.

> **This proves origin and integrity. It does not prove truth.**
> See [LIMITATIONS.md](LIMITATIONS.md).

## Where to start

| | |
|---|---|
| [Site](https://m-of-n.github.io/mofn/) | The published documents, each marked with its status |
| [`ARCH-0001`](spec/ARCH-0001-authorization-attestation.md) | **Architecture — the source of truth.** Read first. |
| [`SPEC-0001`…`SPEC-0005`](spec/) | The KSA specifications (drafts): architecture, core, definitions, trust evaluation, processes |
| [`spec/vectors/`](spec/vectors/) | Published test vectors — the interop contract |
| [`DECISIONS-0001`](project/DECISIONS-0001.md) | Open decision register: what is open, and what it blocks |
| [`PLAN-0001`](project/PLAN-0001-project-plan.md) · [`BACKLOG-0001`](project/BACKLOG-0001.md) | Execution plan and tasks |
| [`prototype/wallet/`](prototype/wallet/README.md) | The wallet engine and `mofn` command line |
| [`prototype/wallet-app/`](prototype/wallet-app/README.md) | The desktop wallet (PySide6, macOS) |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Branches, worktrees, PRs, review, DCO |

## Status

**Research prototype.** The architecture (`ARCH-0001` v0.3.x) and the KSA
specifications (`SPEC-0001`…`SPEC-0005`) are drafts.

- **Decided** — only by an ADR: `ADR-0001`…`ADR-0008` are accepted, including
  DEC-001 (`ADR-0006`), DEC-002 (`ADR-0004`, KSA-CBOR), DEC-003 (`ADR-0005`,
  key id = SHA-256 of the public key) and DEC-007 (`ADR-0007`).
- **Open** — DEC-004 (tag language), DEC-005 (envelope), DEC-008 and DEC-009.
  No tag language or envelope is selected.
- **Software** — the wallet engine and CLI (`prototype/wallet/`) and the desktop
  wallet (`prototype/wallet-app/`) implement statements, verification, trust
  anchors, delegation chains (depth, no widening, validity intersection) and
  *k*-of-*n* thresholds against the published vectors. They ship as
  `wallet-v*` **pre-releases** on the
  [releases page](https://github.com/m-of-n/mofn/releases), with SHA256SUMS
  and a build-provenance attestation. Do not use real keys.
- **Not yet** — revocation is not enforced: short validity is the only
  mechanism today (see [LIMITATIONS.md](LIMITATIONS.md)).

## The library

[`library/`](library/) is a submodule pinned to a commit, and it is **part of
the harness** — the evidence layer this specification cites, not a bibliography
appended at the end.

Every record names what it `bears_on` (a `DEC-*`, an `R-M-*`), so *"every
normative reference bearing on DEC-002"* is a query rather than a memory. The
documents we build against go further: they are fully extracted under FX-1, so
a requirement in a standard carries a stable id and the specification can cite
**a requirement** rather than **a document**. Most records are stubs, and that
is a resting state, not a backlog — a stub preserves a source we can find
again.

Pinned means a report's bibliography is reproducible as `library@<commit>`.
`bin/lib-sync --check` fails if the pin moved without being staged.

> Working on records? **Open `library/` as the project** — skills do not load
> through a submodule. See [`library/README.md`](library/README.md).

## Layout

```
spec/               ARCH, ADR, SPEC, UC — the normative work  (archdoc/v1)
spec/schema/        encoding-neutral schema for the logical types
spec/vectors/       published test vectors — the interop contract
project/            PLAN, BACKLOG, PROC, APP, DECISIONS       (archdoc/v1)
prototype/wallet/   wallet engine + `mofn` CLI (Python)
prototype/wallet-app/  desktop wallet (PySide6)
prototype/          other spikes (statements/, lane-a/)
demo/slice.sh       end-to-end demo: sign, verify, delegate, threshold
src/mofn/           placeholder — no code yet; the working code is prototype/
design-log/         AI-assisted design record
research/           research reports
library/            submodule → the reference library (evidence layer)
site-src/, bin/     site sources and generators → GitHub Pages
```

## Quick start

```sh
git clone --recurse-submodules https://github.com/m-of-n/mofn
cd mofn && bin/lib-sync --check && bin/validate-archdoc
pip install -r prototype/wallet/requirements.txt
cd prototype/wallet && python -m pytest -q        # engine tests
cd ../.. && demo/slice.sh                         # the demo
```

## License

Code is licensed under [Apache-2.0](LICENSE); specifications and documentation
under [CC-BY-4.0](LICENSE-docs). `library/` is a separate repository with its
own terms.
