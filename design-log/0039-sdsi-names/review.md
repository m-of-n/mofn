---
schema: "design-log/v1"
id: DL-0039
part: review
date: "2026-11-12"
---

# DL-0039 — review

**Human answers:** the agent's recommendation on all seven forks
(`question.md`). The human gave no reasons of their own. The reasons in
`ADR-0008` are the agent's, and the human can reject them in PR review. The
human has not reviewed the text yet. `ADR-0008` is `proposed`, and accepting it
is the human's act.

## What was rejected, and why

All of these are options the agent offered and the human declined.

- **A name only as a trust subject.** It loses name-to-name bindings, which are
  SDSI's linked namespaces (`ARCH-0001` §3.1). Without them no cycle can arise,
  so the issue's cycle vector would have had nothing to test.
- **No wire form.** Nothing on the wire could delegate to a name, which
  weakens G1 and §4.3 procedure 1 to an evaluator-internal convenience.
- **A per-context list of name types.** Every relying party would have to
  configure one, and by default no name would resolve.
- **Hard-wiring DV-2's `name`.** That makes a global type, which `ARCH-0002` P1
  and `ADR-0001` reject.
- **Covering bindings with an anchor path.** It merges name resolution into
  authorization reduction, which `ARCH-0001` §4.3 forbids ("must not be
  collapsed into one graph walk").
- **Ambiguity as failure.** It differs from SDSI, and an issuer could disable
  its own name by adding a binding.
- **`widening` for a trust to a name.** It would test §6.3 again, not names.
- **Bindings that do not follow rotation.** Every rotation would leave names
  stale.
- **Spec text first, vectors in a second PR.** That would leave #143 open with
  text that no vector had checked.

## What the agent got wrong, and corrected

- **The first "foreign" framing was wrong.** In round 2 the agent described the
  foreign-namespace case as "a type-7 attestation whose kid ≠ says". That
  describes TV-30, a legitimate name-to-name binding: *Carol's builder is
  Alice's fred's sam*. Under §5.3.1 the namespace is always the speaker's, so
  "Bob binds Alice's fred" cannot be written at all. The case that **can** be
  written is the one R-7 tests: a resolver that matched on the label alone
  would accept Bob's `fred` as Alice's. `name-foreign` is therefore a
  **diagnostic** refinement of `name-unresolved`, not a separate failure the
  wire can express. The human chose the option before seeing this. If they
  want a different reading of "widening", R-7 is where it changes.
- **`bin/wt` branches from the local `HEAD`, and local `main` was 15 commits
  behind `origin/main`.** The worktree was made with `git worktree add … -b
  spec/sdsi-names-143 origin/main` instead.

## Owed

- `ADR-0008` acceptance by a decision maker, and a text review of
  `SPEC-0004` §5.3 by a second reader.
- T-040: a resolver in the engine that passes R-1…R-7 and E-8…E-10.
- A name-rotation vector, which needs a `key-publish` for bob2.

**Update 2026-11-13 (`DL-0040`).** `ADR-0008` is accepted, T-040 is in
review with `engine/names.py`, and R-8…R-10 with TV-35 are the rotation
vectors. The second reader's review of §5.3 is still owed.
