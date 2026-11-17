---
schema: "design-log/v1"
id: DL-0049
part: review
date: "2026-11-16"
---

# DL-0049 — review

**Human verdict:** pending (PR review; David reviews the engine use per #69's
multi-agent note).

## What #173 still adds

The engine already reports delegation chains, and the Check tab renders them
(E-2, slice ④). What the TUI cannot yet do is **make** a chain: there is no
Trust-tab control for `root add --depth` or a `mofn delegate` form, so a
`mofn run` user only sees a multi-hop standing when handed a trust statement
made on the command line. #173 adds that; no change here should be needed.

## What the agent rejected, and why

- **Calling the key `attributes`.** "Attribute" is normative here (the
  `[type-ref, value]` pairs of a statement body), and `because[].covered`
  already holds them. `associations` is the issue's own word and collides
  with nothing.
- **Recomputing standing in the TUI or in a second walker.** The TUI must
  reimplement no reduction (#69). Standing is read from `Coverage` as the
  reduction left it; the only new logic is matching an entry to its
  `Covered`/`Stopped`.
- **Showing who signed for a statement that did not verify** (unknown key,
  bad signature), by decoding the envelope anyway. Its `says` is unproven;
  printing it beside a verdict would present an unverified claim as an
  attribute of the verdict. `associations` is `[]` and the tab says why.
  The CLI's authenticity/integrity line still names the file.
- **A two-value standing (`standing` / `no-standing`) only.** For integrity
  fail no reduction runs, so "no standing" would claim a result that was not
  computed. `not-evaluated` is the honest third value, as the six lines
  already use it.
- **Adding the four to the text verdict.** That changes every
  `fixtures/golden/*.txt` the slice compares byte for byte, for no
  done-when item. Left as a follow-up if wanted.
- **One entry per statement** rather than per (statement, attribute). Topic
  and standing are per attribute (`Covered.attribute`), so a statement with
  two attributes would have to merge or drop one.
- **Golden JSON for the whole verdict.** `statements[].file` differs per
  codec and per run, and a whole-verdict golden would pin the full §10.3
  `because` trace, which is not this issue's surface. The goldens hold only
  `associations` without `file`; those contain vector keys only, so they are
  stable under both codecs.

## Gaps flagged, not fixed

- `principal` is filled only from name **anchors** (`Coverage.names`). A
  trust-statement hop that targets a name resolves inside `_walk` and is not
  recorded; such a signer shows `principal: null`. Recording it is an engine
  change for #65's owner.
- A threshold anchor's member sub-paths are not followed (T-095), so a
  threshold standing chain is always one root entry.
