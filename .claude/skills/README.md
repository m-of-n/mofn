# Skills that act on m-of-n

**Claude Code loads skills from the project root only** — never transitively
through a submodule, never from a parent directory. So these load when `mofn/`
is opened as the project.

| skill | for |
|---|---|
| `propose-arch` | changing ARCH-0001 without violating its §9 |
| `close-topic` | when a topic is answered rather than merely read |

**Skills that act on library records live in `library/.claude/skills/`** —
`ingest-reference`, `summarize`, `distill`. Open `library/` as the project for
record work. They are not duplicated here: duplicates drift, and a drifted
skill is worse than a missing one because it looks authoritative.

See `project/PROC-0003-team-coordination.md` §1.
