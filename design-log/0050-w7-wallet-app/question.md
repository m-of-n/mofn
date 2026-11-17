---
schema: "design-log/v1"
id: DL-0050
part: question
title: "W-7: the desktop wallet app — PySide6 + PyInstaller macOS .app, Sign and Verify with W-5's attributes; DECISIONS-0001 item 28 amended (mofn#179)"
date: "2026-11-17"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "prototype/wallet-app/ (PySide6, in-process engine via cli.main); wallet 0.10.0 publishes the .app zip on the wallet-v* tag; DECISIONS-0001 0.8.0 item 28 amended; PLAN-0002 0.5.0, PLAN-0004 0.6.0 (§5.1), APP-0005 0.2.0, BACKLOG-0001 0.16.0 W-7 row."
status: open
---

# DL-0050 — question

The human (owner of #179) asked the agent to talk through what completing W-7
needs, without changing anything, then — after six rounds of questions and
three rounds of mockups — to build it.

#179 as filed, with the stack the human set on 2026-11-16 and asked not to be
re-opened:

- **PySide6 (Qt) + PyInstaller**, Python throughout; the app at
  `prototype/wallet-app/`, importing `prototype/wallet/engine/`; a separate
  repo only once the engine ships as a pip package.
- One PR: the item 28 amendment (DECISIONS-0001, PLAN-0002 §5.1, PLAN-0004 §4)
  and this entry with its rejections — Toga, SwiftUI, Tauri, a separate repo,
  closing #69 — land with the app.
- An app shell (window, wallet open/create, keys); **Sign** (≈ PLAN-0004 view
  3) with a masked passphrase never on argv or in the environment; **Verify**
  (≈ view 5) with the authorization line prominent, the sentence, the limit
  line, and #69's four attributes from the same output as
  `mofn check --format json`.
- A macOS arm64 `.app`, published as a pre-release with `SHA256SUMS`; tests.
- Acceptance: runs with no server or network; for the W-4 slice cases the app
  shows the CLI's verdict; every verdict shows who signed, topic, digest,
  standing; README carries the prototype warning.

Questions the human answered along the way (2026-11-16/17):

1. *When is the look decided?* Before any screen code: from the human's two
   reference images (a dark dashboard; a node-link identity graph), as HTML
   mockups approved in the thread, then built.
2. *Can the CLI and the GUI work together?* (asked as "the seal line" — a
   speech-to-text "CLI"; the agent first could not place it).
3. *Release tag?* The human asked whether the app could ride the existing
   `wallet-v*` tag rather than a new `wallet-app-v*` one.
4. *One wallet or many?* The human first said one wallet with one persona,
   then — told the engine treats any folder as a wallet — asked for a wallet
   switcher. Where should the first wallet go? `~/Projects/wallet/mofn`.
5. *Personas?* The sidebar should lead with identities, so W-8 (#180) has
   somewhere to land.
6. *Fewer PRs?* Code review is the bottleneck: one PR, grouped commits.

Constraints: no DEC-* decided; `src/` stays empty; no cryptography, encoding
or reduction reimplemented; DCO on every commit; this entry in the same PR.
