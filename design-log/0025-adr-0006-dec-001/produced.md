---
schema: "design-log/v1"
id: DL-0025
part: produced
date: "2026-11-06"
---

# DL-0025: produced

No primitive, vector, schema or code. One new ADR and status pointers.

| file | version | change |
|---|---|---|
| `spec/ADR-0006-dec-001-slug.md` | new, **1.0.0** | decision, scope (not the protocol name, not a product name, not a freeze), why, six alternatives rejected plus "any rename now", acceptance test, consequences, evidence |
| `spec/ARCH-0001-authorization-attestation.md` | 0.1.8 → 0.1.9 | §7 DEC-001 status line; DEC-001 removed from `open_decisions` |
| `spec/ARCH-0001-CHANGELOG.md` | 0.1.9 | entry |
| `project/BACKLOG-0001.md` | 0.12.10 → 0.12.11 | T-001 cites `ADR-0006` and says the earlier line had no ADR |
| `project/PLAN-0001-project-plan.md` | 0.6.2 → 0.6.3 | §3 cites `ADR-0006` |
| `project/DECISIONS-0001.md` | 0.5.0 → 0.5.1 | "Decided and merged" cites `ADR-0006`; v0.5.1 note |
| `CLAUDE.md`, `README.md` | — | status lines: DEC-001/002/003 accepted, DEC-004/005/007 open |

Every rejection reason in the ADR's alternatives table is the agent's. They are
built from `PLAN-0001` §0, `ARCH-0001` §1/§3.3, `ADR-0002` (P6) and `ADR-0004`.

**Left as written, on purpose:**

- `src/mofn/__init__.py`'s docstring: it is code.
- `PLAN-0001` §3's `<DEC-001>` tree placeholders: a superseded layout.
- `docs/index.md`: generated, and never edited by hand.
