---
schema: "design-log/v1"
id: DL-0051
part: review
date: "2026-11-17"
---

# DL-0051 — review

**Human decisions** (ndewedo-newbury, 2026-11-16/17, in the session): fold
#178 into #34; build the literature-plus-design publication (#34) rather than
stop at the flat bibliography; start #177 in a worktree with a styling hook.
**Verdict on this change:** pending (PR review).

## What was rejected, and why

- **Listing accepted and open DEC-\* on the landing page.** That is exactly
  what went stale: the list was right in September and wrong by November, and
  no build step could notice. The page now says *an ADR is the only acceptance*
  and links the register, which is maintained. Rejected by the agent.
- **Generating the landing page's decision list from ADR front matter.** Would
  not rot, but adds a generator for one paragraph the register already covers.
  Revisit if #33's "decision register, public" item wants it on the landing
  page itself.
- **Editing `docs/index.md` in place.** Fixes the text, keeps the cause: a
  hand-authored file inside a directory everyone is told never to edit.
- **Shortening titles in spec/ front matter.** Every touched document would
  need a `version` and `updated` bump (ARCH-0001 §9.5) for a nav label;
  `short_title` already exists, so the generator uses it and prefixes the id.
- **Renumbering the two research `0001-*` reports.** A real collision, but
  renaming changes published URLs and citations; out of scope, flagged for
  #177's follow-up.
- **A custom web font.** Material already loads Roboto; another external font
  is cost without a reader-facing reason.
- **Hiding draft pages.** PROC-0004 §9 says drafts are public and *marked*;
  the banner marks them.

## Still open on #177

- Phone readability checked only by CSS reasoning (tables scroll, codes
  wrap); not yet on a device.
- Research id collision (`0001-cbor`, `0001-signatures-and-attestation`).
- `project/PUBLISHING.md` is generated but not in the nav; left as is.
