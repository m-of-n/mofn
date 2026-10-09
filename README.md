# m-of-n

**Key-centric semantic assertions.** Authorization, local names, and artifact
attestation with a model whose principals are keys, whose names are relative to a
naming key, whose subjects may be *k*-of-*n*, and whose statements carry meaning
a person can read.

USF CS690 Master's Project, Fall 2026. Sponsor: Paul Lambert.

> **This proves origin and integrity. It does not prove truth.**
> See [LIMITATIONS.md](LIMITATIONS.md).

## Where to start

| | |
|---|---|
| [`ARCH-0001`](spec/ARCH-0001-authorization-attestation.md) | **Architecture — the source of truth.** Read first. |
| [`ARCH-0001-PROPOSAL-v0.2.0`](spec/ARCH-0001-PROPOSAL-v0.2.0.md) | Open proposal against it. Nothing accepted. |
| [`PLAN-0001`](project/PLAN-0001-project-plan.md) | Execution plan, increments, risks |
| [`BACKLOG-0001`](project/BACKLOG-0001.md) | Tasks |
| [`PROC-0001`](project/PROC-0001-agents-and-topics.md) | Agents, topics, parallel work |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Branches, worktrees, PRs, review |
| [`CLAUDE.md`](CLAUDE.md) | Constraints for agents and humans; `.claude/skills/` |

## Status

Pre-implementation. The architecture is at v0.1.0 draft with **DEC-001 … DEC-005
and DEC-007 open**. No encoding, tag language, or envelope is selected. Do not
infer a decision from code that does not exist yet.

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
spec/               ARCH, ADR, MAP — the normative work      (archdoc/v1)
spec/schema/        encoding-neutral schema for the logical types (WP1)
spec/vectors/       published test vectors — the interop contract
project/            PLAN, BACKLOG, PROC — how we run it       (archdoc/v1)
src/mofn/           reference implementation
prototype/          throwaway spikes. never ships
design-log/         AI-assisted design record
library/            submodule → the reference library (evidence layer)
docs/               → GitHub Pages
```

## Quick start

```sh
git clone --recurse-submodules https://github.com/m-of-n/mofn
cd mofn && bin/lib-sync --check && bin/validate-archdoc
```
