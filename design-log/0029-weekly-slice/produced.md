---
schema: "design-log/v1"
id: DL-0029
part: produced
date: "2026-11-07"
---

# DL-0029 — produced

Tooling only. No primitive, spec text, schema, mapping or vector.

| file | change |
|---|---|
| `.github/workflows/weekly-slice.yml` | new |

What the workflow does:

- **When.** `cron: '0 13 * * 1'` — Monday 13:00 UTC. Also `workflow_dispatch`
  (manual), and `pull_request` on its own file as a **dry run** that builds the
  comment and prints it without posting.
- **Clean clone.** Fresh checkout, a new `prototype/wallet/.venv` with
  `requirements.txt`, then the slice run under `sudo unshare --net` (a network
  namespace with no interfaces) and `env -i` with an empty `HOME`. Prerequisites
  are installed before the network is cut, as the slice's header documents.
- **Post.** One comment on mofn#68: date, commit, run link, green or RED with
  the slice's own summary line, a placeholder asking the slice owner for the
  verdict notes, and the full output in a `<details>` block.
- **Red.** On a non-zero exit the comment still posts, saying RED, and the job
  fails, so the Actions tab shows it.
- Guarded by `github.repository == 'm-of-n/mofn'` so forks never post.

The analysis of the verdict text is **not** automated (see review).
