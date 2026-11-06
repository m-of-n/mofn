---
schema: "design-log/v1"
id: DL-0025
part: review
date: "2026-11-06"
---

# DL-0025 — review

**Human decision:** 1a and 2a, the agent's recommendation on both.

## What was rejected, and why

- **1b, boolean.** Rejected. It supersedes part of `ADR-0003` and reverses
  SPEC-0002 §8.6, TV-5 and the wallet engine. What it buys over 1a is
  expressible in 1a anyway. **The rejected position is not weak**, and the
  R-M-10 rewrite must carry it: RFC 2693 §4.1.4 (depth is unpredictable, since
  one can always add a temporary key; depth does not bound width). The
  library's `rfc-2693` notes side with RFC 2693. That contradiction is now
  recorded against them, not resolved.
- **2b, `may-speak`.** Rejected. It appeared only in the mofn#6 thread, never
  in a SPEC. Renaming the SPECs to match an informal gloss inverts ADR-0003's
  "the SPEC governs". ARCH-0002's *"can speak about (Domain, Topic)"* stays as
  prose.

## Owed

- R-M-10 rewrite and §4.2 change, inside T-012a (mofn#134).
- A vector for depth exhaustion and widening.
- Library: the `rfc-2693` design notes, items 2 and 7, still say "we side with
  RFC 2693". Correct them in the library repo (PROC-0003 §1), not here.
