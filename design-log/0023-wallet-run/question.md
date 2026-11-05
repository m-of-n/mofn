---
schema: "design-log/v1"
id: DL-0023
part: question
title: "W-6 (mofn#127), wallet 0.2.0: mofn run, the guided screen, and run --check"
date: "2026-11-04"
model: "claude-opus-5-5"
human: davidhsiaotw
outcome: "mofn run (Textual) over seven steps; run --check in CI; three new goldens; the CLI moved into cli.py and takes the passphrase in process. No spec change, no DEC-* touched."
status: open
---

# DL-0023 — question

## The brief

The second half of David's share of mofn#127 (W-6), after DL-0022 (0.1.0).
The brief, briefly: Paul's "there is no guide". David's words, his two choices
(one PR, `feat/w6-tui`; commit locally, no push) and the context supplied are in
DL-0022. This entry and DL-0022 are in the same PR.

#127 §2 asks for the following:

- **`mofn run`**: a full-screen guide in the style of rustlings, over the
  README's cases, in a throwaway wallet folder.
- **Every command shown before it runs**, spelled as the CLI would take it.
- **The passphrase** in a masked field, reaching the engine in process: never
  on a command line or in an environment variable (#65 A3).
- **Nothing reimplemented.** The screen calls the engine's own `make`, `check
  --format json` and `show`; no crypto and no reduce in UI code.
- **Expected verdicts** come from `fixtures/golden/`, the files
  `demo/slice.sh` compares with.
- **`mofn run --check`** runs every step without a screen, and CI runs it on
  every OS. With no terminal, `mofn run` refuses with exit 2.
- **Progress survives quitting.**
- **Textual**, pinned in `requirements.txt`; issue §6 gives the rejected
  options.

## Context supplied

- mofn#127 §2 and §6;
- DL-0022 and its branch;
- `prototype/wallet/` (`cli`, `unlock`, `check --format json`, the goldens,
  `tests/test_cli.py`);
- `demo/slice.sh`;
- PyPI's release dates for Textual.
