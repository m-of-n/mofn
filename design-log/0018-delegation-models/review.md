---
schema: "design-log/v1"
id: DL-0018
part: review
date: "2026-11-01"
status: open
---

# DL-0018 — review

**Status: open. Human review is pending** on mofn#118. No review with content
exists, so nothing below is a human verdict on the report. One approving review
is required, from any code owner (mofn#123 removed the path rules that first
routed this PR to nymble).

**The human verdicts so far carry no comment.** davidhsiaotw approved library#94,
which Ndewedo-Newbury merged; that covers two record summaries and a topic edit,
not the report. davidhsiaotw also approved mofn#118 at `63f458d`, with no comment.
That approval was dismissed when an *Update branch* merge moved the head, and
the merge itself failed `dco`, so the branch was rebased (DL-0011). It records no
accepted, edited or rejected point, and §3 stays open until a review does.

**Written after the fact, on 2026-11-01, from the session transcript**, not from
memory; this status block was updated on 2026-11-02. §5 sets out what the transcript can and cannot support.

§1 and §2 are therefore the model's own rejections, not a human's.

## 1. Rejected by the model — the issue's own instructions and framing

**The issue's `research/NNNN-delegation-models/` in the library.** The report
went in mofn, because `research/README.md` in both repositories puts reports on
the project's subject there. The model had first said this was the user's choice,
then made it without being told to. It was disclosed in the hand-off, but it
overrides what the sponsor's issue asks for, so it needs a reviewer's agreement.

**"Ours can scope and theirs cannot."** Withdrawn in §7.1. X.509, OpenPGP and
SPKI all scope, and X.509's mail scoping is more precise than the current spec.

**"Ours is different because the root is unsigned."** Withdrawn. The issue's table
marks our root as **unsigned** as if that were distinctive, and every system
compared has an unsigned local root.

**The issue's claim, *"poorly served by all of these"*, as written.** Withdrawn as
a claim about everything compared: it is false for SPKI, which is exactly that.
A narrower claim survives in §7.2. This is the sponsor's sentence, and the model
is the one that struck it.

**The topic answer as a conclusion.** Treated as a hypothesis. The report departs
from it in three places (§7.3 items 2–4), and from merged R-001 in one (§7.3
item 1).

## 2. Rejected by the model — method and shortcuts

**A truncated RFC 8550 quote.** The sentence was first cut at *"specification."*
The audit showed that it goes on: *"but may be governed by the policies associated
with particular certification paths"*. The cut overstated it, so the whole span is
now quoted. **This is a defect the model introduced and its own audit caught.**

**A wrong locator**, the "§6 vs §6.1 fix" of the locator check. The transcript
records that fix, but neither its direction nor the sentence it fell in.

**Leaving the GnuPG claims labelled unverified.** The gate allowed it, and #14
could have closed that way. The model advised running them first, because the
chain claim carries the headline OpenPGP finding and §7.2's second bullet.

**A throwaway Debian container for the experiment.** That was the first plan, to
avoid installing anything on the host, and Docker was tried again on 2026-11-01.
The daemon was unreachable, so `gnupg` went in by `brew install` on the user's
machine instead. The install's automatic cleanup also removed Homebrew logs and a
2.3GB `docker-desktop` cache from `/opt/homebrew/var/homebrew/tmp`. The isolation
of the first plan was lost. The user was told about the cleanup.

**Hand-editing `mkdocs.nav.yml` and `PUBLISHING.md`.** Planned, then dropped when
they turned out to be generated. The first `bin/manifest` run dropped the Library
nav section, because the submodule was not initialised in the new worktree. That
output was discarded and regenerated.

**Ingesting GnuPG's source as a library record.** Files on a moving branch are not
a citable document. Digests are in `sources.md` §3 instead.

**Recording the experiment's output as a library record.** `sources.md` had
promised this. The model reversed its own earlier sentence on 2026-11-01 and kept
the output in `experiments/`, as our own reproducible measurement. **This is a
quiet reversal and a reviewer should check it.**

**Waiting for a separate pin PR.** Pin bumps are normally their own `chore:` PR,
and #120 makes the same one. #118 carries it anyway, because the report cites
two records that reach the summary bar only at `a1aa258`. Whichever merges second drops it.

**Merging by admin bypass.** `enforce_admins` is off, so the user's account could
have merged #118 without review. The instruction was to do what was necessary to
merge, and bypassing a required reviewer is not that. The model requested
nymble's review, the owner required at the time, and stopped.

## 3. What needs a human verdict

In descending order of consequence.

1. **P1: UC-5 is wrong under SPEC-0003 §6.3.** If this reading is right, the
   project's own example has the wrong expected result. Either the example
   changes or the algebra does.
2. **§7.1 and §7.2: withdrawing the issue's claim.** Is *"SPKI's model, with typed
   ranges and a wire format, for a domain where the deployed systems scope only
   names"* the claim the project wants?
3. **The report's location.** mofn, against the issue's text (§1).
4. **§7.3 item 1: the correction to merged R-001 §4.3.** Two merged documents will
   disagree until someone edits R-001.
5. **P2–P6.** Each needs a yes or no. None is applied.
6. **The GnuPG findings' weight.** One version, one platform, on the source read
   at `master`. Older release branches were not run.
7. **The `experiments/` decision** (§2).

## 4. Guardrails observed

No cryptographic primitives generated. The experiment used GnuPG, a vetted tool,
with throwaway keys in temporary keyrings. No `DEC-*` marked accepted. No edits
to `spec/`, `ARCH-0001` or `UC-0001`. No third-party bytes committed. No commits
inside the `library/` submodule; the pin moved to a merged commit.

## 5. Limits on this entry

**The rule was broken.** `CLAUDE.md` requires this entry in the same change. It
was missed when the report was written, and missed again on 2026-11-01, when the
instruction was to complete whatever was needed to merge. That pass rebased,
ran the experiment and marked the PR ready without opening mofn's `CLAUDE.md`, and
reported the PR blocked only on review. Someone else caught the omission.

**What the transcript supports.** For 2026-10-26 it preserves the instructions and
the model's narration, not its tool calls or reasoning. Hence:

- §1 and §2 record only rejections the transcript or the report states. There were
  surely others. **Drafts of `report.md` that were discarded are not recoverable**,
  and the connection dropped once during drafting.
- The transcript says Docker was available on 2026-10-26, then that it was down.
  **Why it went down is not recorded.**

**Audit coverage.** The 62-span quote audit ran on v0.1.0. v0.2.0's edits were
scripted against exact strings and changed no quoted span, but the audit was not
rerun. `bin/validate` in the library reported 160 warnings at the new pin against
159 earlier. The extra warning was not investigated.

**The review half of this entry does not exist yet.** It should be filled in when
mofn#118 is reviewed, with what was accepted, edited and rejected, and why. That
is what moves it from `open` to complete.
