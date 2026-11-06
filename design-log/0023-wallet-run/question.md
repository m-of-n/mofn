---
schema: "design-log/v1"
id: DL-0023
part: question
title: "W-6 (mofn#127), wallet 0.2.0: mofn run, the wallet as a terminal app, with Learn"
date: "2026-11-04"
model: "claude-opus-5-5"
human: davidhsiaotw
outcome: "mofn run opens your own wallet as forms (first run, Wallet, Keys, Trust, Sign, Check, Open), each running the mofn command it shows; Learn is the tutorial and runs nothing; DV-1 ships as the example vocabulary; goldens statement-changed and expired added, the four earlier ones unchanged; the executing guide and run --check withdrawn. No spec change, no DEC-* touched."
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

## Updated brief, 2026-11-05

David rewrote #127 §2 and told the agent: "I updated the issue, make changes
according to it". The new §2 says:

- **one reader, one wallet**, in a throwaway folder;
- **what comes from someone else is already made**: the existing fixtures,
  presented as files Alice sent you. These are TV-1, DV-1 with TV-3, TV-4,
  and `artifact.bin`;
- **eight steps**: your wallet, what Alice sent, a key you lack, not trusted
  yet, trust and check again, change the file, change the statement, sign
  your own;
- **checks run `--at 2026-10-15T00:00:00Z`**, while TV-4 was valid. Step 4
  also checks now, to show not-valid-at-time;
- **the deciding line each step expects is written next to the step**, and the
  files are the fixtures `demo/slice.sh` already uses.

Asked by the agent, David chose three things:

- overwrite an uncommitted change to `guide/steps.py`; a copy of it was kept
  outside the repo;
- remove the three goldens the first version had added;
- ask "which line fails first?" at both step 2 and step 3. The issue's table
  puts it at step 2, and its mock-up at step 3.

## Second update, 2026-11-05: the wallet as a terminal app

After trying the eight-step guide, David rewrote #127 §2 again and told the
agent:

> I updated the issue
>
> current mofn is like a pure tutorial, I think that's a good stuff but not I
> really expect
> mofn should use blocks, questions, etc to guide user to use the wallet
> original tutorial is great to keep, but don't execute command
>
> I hope these matches the issue, if not tell me

The new §2 says:

- **`mofn run` opens the user's own wallet**, the one the CLI opens.
- **Screens with forms, tables and questions**: first run, Wallet, Keys,
  Trust, Sign, Check, and Open a file. The user fills in what they want;
  `mofn run` runs the command behind it.
- **Choices come from what you already have.** Every form shows its command
  on a *Runs* line, and an engine error appears next to its field.
- **The passphrase** goes in a masked field, in process.
- **Nothing is reimplemented.**
- **No terminal**: `mofn run` exits 2.
- **CI** drives every screen with the pilot.
- **Learn**: the tutorial, reading not doing. It runs no command and touches
  no wallet. Its example output is the goldens, its words are the README's,
  and every page links to its screen.

The agent's answer was that the issue matches the message, with two gaps. It
asked about both, and David chose:

- **Re-add `statement-changed` and `expired`** as new goldens, because Learn
  shows those cases and only four goldens existed. The four existing goldens
  stay byte for byte.
- **Ship DV-1 inside mofn** as the example vocabulary. A downloaded mofn
  otherwise has no vocabulary, and the acceptance hand-off between David and
  Chip would fail semantics.

