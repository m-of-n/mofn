---
schema: "design-log/v1"
id: DL-0050
part: review
date: "2026-11-17"
---

# DL-0050 — review

**Human decisions** (ndewedo-newbury, 2026-11-16/17, in the session): the
stack (PySide6 + PyInstaller, this repo); graphite; identity-first sidebar;
Verify as rows; standing as timeline rows with an *In words* toggle; no context
switcher; a foldable sidebar; several wallets, the first at
`~/Projects/wallet/mofn`; a **New identity** button the issue lacked; a Trust
screen, and most of the TUI's forms in this first draft; the `wallet-v*` tag;
one PR. **Verdict on the code:** pending (PR review, David).

## What was rejected, and why

### The stack (set by the human 2026-11-16; reasons recorded here)

- **Toga / BeeWare.** Thinner widget set and nobody on the team has used it;
  Qt's tables, forms, stylesheets and headless test runner are what the pages
  need.
- **SwiftUI.** Breaks *Python throughout* (item 28): a second language, and
  the UI could no longer call the engine in process.
- **Reviving Tauri.** A second toolchain (Rust, TypeScript, a sidecar) for one
  window; withdrawn once already (DL-0038).
- **A separate repository now.** The engine is not a pip package, so the app
  would vendor or submodule it; CI, DCO and the release would be duplicated.
  Revisit when the engine ships as a package.
- **Closing #69.** The TUI would have lost the attributes; #69 shipped them in
  the engine (DL-0049) and this app reuses them as given.

### The look (agent's mockups, rejected by the human)

- **Navy theme** (v1). "I do not like navy." → graphite.
- **Context switcher on Overview** (v1, the agent's). The human asked what it
  was for; the agent's reason — every verdict is computed in one context —
  did not justify a top-level control in a wallet that usually has one
  context. → under *More options* on Verify and Trust; W-8 gives contexts a
  page as communities.
- **Five check bubbles and attribute columns** (v1). "Rows, not columns." →
  one checks row; subject, signer, standing as full-width rows.
- **Wallet switcher at the top of the sidebar** (v1). The human: identities
  first, "otherwise where would W-8 come in?" → identity on top, wallet at the
  foot.
- **Standing options B (breadcrumb pills) and D (node graph).** B squeezes the
  reasons and cannot show k-of-n; D's labels crowd and it suits W-9's full
  graph better. → A, with C as a toggle.
- **A fixed sidebar.** → folds to icons (the human's one change to v3).

### Release and scope

- **A separate `wallet-app-v*` tag and its own version** (in #179 as filed;
  the agent's first plan). The human asked whether the app could use the
  existing tag; the agent agreed: one version, one workflow, one `SHA256SUMS`,
  and the CLI and app always built from the same engine. Cost: an app-only
  fix bumps the wallet version.
- **A separate `release-app.yml`.** Fell with the separate tag.
- **Several PRs.** The human: review is the bottleneck. One PR, with commits
  grouped by area so it can be read commit by commit.
- **Signing and notarization now.** Not rejected — deferred: no Apple
  Developer ID ($99/yr). APP-0005 documents *Open Anyway* and `xattr`.

### The agent's own, reversed

- **"One wallet at `~/.mofn`."** The agent's first plan said so; it was wrong
  — the engine has no `~/.mofn` (the CLI defaults to `./wallet`) and any folder
  is a wallet. Corrected before code; the app's default is the human's
  `~/Projects/wallet/mofn`.
- **Lifting `cmd_check` / `cmd_make` into engine functions** — the agent's
  recommended "engine seam", which the human approved ("do your pick").
  Reversed while building: `screens/runner.py` already runs `cli.main` in
  process, so calling it gives the CLI's verdict by construction and changes
  no shared file, which is the smaller review the human asked for. **The human
  has not yet seen this reversal; it is flagged in the PR for review.**
- **Bundling `screens` wholesale in the spec.** `collect_submodules("screens")`
  pulls `screens.app` and with it Textual; the spec names the three Qt-free
  modules instead.
- **Verify-it handing over only the new statement.** The semantics line then
  failed (the vocabulary had no define statement). With the example
  vocabulary, *Verify it* also hands over its definer's define statement
  (TV-3), as a relying party would be handed it.

## Owed

- A human launch of the downloaded `.app` on a clean Mac after the first
  `wallet-v0.10.0` tag run (Gatekeeper step as documented).
- W-8 (#180) and W-9 (#181) on this scaffold.
