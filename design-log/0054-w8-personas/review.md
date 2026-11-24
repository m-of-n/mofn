---
schema: "design-log/v1"
id: DL-0054
part: review
date: "2026-11-23"
---

# DL-0054 — review

**Human decisions** (wyxiao6, 2026-11-23, in the session): key targets in the
engine over the file-digest reading; `check --as` over keeping the union; full
W-8 in one PR; and the look settled by building in W-7's approved system and
handing over screenshots, rather than a mockup round. **Verdict on the code:**
pending (PR review).

## Rejected by the human

- **Tagging the persona's published key file.** A tag's subject would be the
  digest of `<name>.pub.stmt`, which needs no engine change at all. Rejected:
  the tag would then be about a *file's bytes*, so re-encoding the key
  statement — or sending it as `.stmt.yaml` instead of `.stmt` — gives a
  different digest and the tag stops following the key. A tag about a
  principal has to name the principal.
- **Deferring received tags to a follow-up.** It would have left an acceptance
  box unticked, which #180 does not allow without amending its scope first.
- **Keeping the union of every owned persona's anchors, and labelling it in
  the UI.** No engine change, but acceptance box 2 says switching persona
  changes *the trust context used in Verify*, and SPEC-0004 §4.1 says every
  evaluation is relative to exactly one context.
- **Engine first, app second, as two PRs.** The W-7 review had already said
  review is the bottleneck and asked for one PR with commits grouped by area.
- **A round of HTML mockups before any screen code** (the W-7 precedent,
  `DL-0050`). Rejected for W-8 because it adds no new visual language:
  graphite, `Card`, `Rows`, `Chain` and the `pill`/`title`/`sub` frame were
  all approved for W-7 and are reused unchanged. Screenshots of the built
  pages were handed over instead, before the PR opened.

## Rejected by the agent while building

- **Writing `ARCH-0001` or any `spec/` file.** PR #186 (W-9's proposal) was
  open, approved and mergeable, and `propose-arch` says one architecture
  change in flight at a time. W-8 needed none: the wire form it uses is
  already legal under `KIND_TARGETS[4]` and already vectored as TV-13.
- **Marking integrity *not evaluated* for every key subject.** `Answer.yes`
  requires all six lines to pass (SPEC-0004 §10.2), so `check --subject-key`
  could then never answer yes — the feature would be unusable. §10.4 also
  reserves "not evaluated" for a line with nothing to examine, and V1/V4/V5
  were examined.
- **Failing integrity when no statement is about the key.** That is the digest
  branch's sentence, which exists because there are two digests to name.
  Nothing was substituted here, and §10.4 assigns that case to authorization
  and acceptance.
- **Emitting `subject.target` for a digest ask too.** Uniform and tidier, but
  it rewrites the three `associations-*.json` goldens, and DL-0049 was
  explicitly forbidden from moving them. `target` is absent for a digest ask
  and the app reads it with a default.
- **Resolving `--subject-key` through `Wallet.find` alone.** Then no golden
  could be built from the published vectors at all: TV-13 is about Bob, and no
  key-publish statement for Bob exists, so Bob can never become a persona. The
  full-kid fallback is what makes the vector usable — and what lets a user
  check a tag given to a key they have only been told about.
- **A second persona in the shared `world` fixture.** Four W-7 tests assume
  exactly one owned persona; growing `world` would have changed what they
  mean. A separate `two` fixture was added instead.
- **Recording in the JSON which persona evaluated.** Tempting for the app, but
  "who evaluated and for whom" is export-envelope territory and DEC-005 is
  open. The app already knows which persona it passed.

## The agent's own, reversed

- **`kid_of` re-raised the wrong error.** The first version let the
  `ValueError` from `bytes.fromhex` escape, so `--subject-key nobody` printed
  *"non-hexadecimal number found in fromhex() arg at position 0"* instead of
  the wallet's own *"no persona 'nobody' in this wallet"*. Caught by running
  it, not by a test; a test now pins the message.
- **Comparing the example vocabulary by path.** A tag's vocabulary was matched
  against `core.EXAMPLE_VOCABULARY`'s path, but the wallet keeps its own copy
  under `definitions/<id>.def`, so the match never fired and every tag's
  semantics line failed *unattributed-definition*. Caught by looking at the
  first screenshot. Matched by `DefinitionId` now.
- **A "Fingerprint" row that showed a name.** `associations[].subject.key` is
  the wallet's label when it has one, so the row read "Fingerprint: Maya".
  Caught by looking at the screenshot. It is `Key id` now, showing the real
  `key:<16 hex>` and the full kid.
- **The same mistake in the Communities members table**, where the FINGERPRINT
  column printed the name. Same cause, same screenshot.
- **`deleteLater()` where the widget had to go at once.** Re-filling a page in
  one event-loop turn left the old *Act as* buttons findable, so a test saw
  two. `setParent(None)` first. This was a real defect, not a test artefact.

## Owed

- Human review of the code, and of the integrity sentence for a key subject —
  the one user-visible wording choice in the engine.
- **The k-of-n member row is design-ahead code.** `Wallet.add_anchor` stores
  `trusts` as one kid (`_hex(anchor.trusts)`), so a threshold anchor cannot be
  written to a wallet today; the row is exercised only through the pure
  `core.members`. W-9's groups are what will put one there. Keep or drop is a
  reviewer's call.
- **Two things #180 asks for that cannot be built as written**, raised on the
  issue rather than quietly dropped:
  1. *"the contexts it **acts in**"* — statements carry no context field, and
     SPEC-0001 §6.3 says a persona *MAY publish* that it acts in a context as
     a `self` or `speaks` statement. No `mofn` command writes one. The page
     shows *relies* as derived and *acts* as an explained, empty chip.
  2. Only `root add` puts a `.def` in the wallet, so a tag from a stranger
     often arrives with no local vocabulary. The page asks for one rather than
     failing the semantics line silently.
- A people-flavoured example vocabulary. `dv-1.def` offers `build-provenance`
  and `outcome` — claims about artifacts — so a tag about a person's key reads
  as *"Maya was built by an attested pipeline"*. Structurally valid, and odd
  in a December demo. Out of W-8's scope; filed here.
- `tests/test_menu.py::test_per_command_help_is_kept` fails on Python 3.14,
  which colourises argparse help. **Pre-existing on `main`**, unrelated to
  W-8; CI pins 3.12 and is green.
