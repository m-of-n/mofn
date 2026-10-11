---
schema: "design-log/v1"
id: DL-0010
part: review
date: "2026-10-10"
status: open
---

# DL-0010 — review

**Status: open. Human review pending** on mofn#84 / the PR for
`report/0004-uptake`. Nothing below has a human verdict yet; §3 lists what
specifically needs one.

What follows in §1 and §2 is the model's own record of material it generated or
planned and then discarded, with the reason. `design-log/README.md` asks for
the half nobody publishes; on a research report that half is mostly **sources
rejected and claims cut**, and it is unusually large here because adoption
evidence is dominated by secondary commentary.

## 1. Rejected — sources and claims that did not survive

**Seven of nine results from the main C2PA adoption search, discarded.** The
query returned mostly 2026 blog posts that contradicted each other on Nikon's
camera support, on whether Google Search verification had shipped, and on
TikTok's labelling totals, and several read as promotional or
machine-generated. None is cited. Everything they asserted is quarantined in
`unverified.md` §2. **Cost of the rule: the report has no platform-adoption
section**, which is the section a reader will most expect. R-001 §6.7 hit the
same wall; this pass did not clear it and says so rather than papering over it.

**The planned conforming-products count, abandoned.** The brief assumed the
C2PA Conformance Explorer published a live machine-readable list. The hostname
in the secondary source — `conformance.c2pa.org` — **does not resolve**. The
report pivoted to measuring the trust list instead, which turned out to be the
better measurement, but the pivot was forced rather than clever and
`unverified.md` §4 records it as a correction to the brief, not as a design.

**`text=*` dropped from the npm sampling frame.** It returned HTTP 400. Rather
than quietly sample three queries and describe the result as registry-wide, the
report narrows its own claim to "popularity-ranked within three keyword
queries" and `searches.md` #12 records the failure. The weaker claim is the
honest one.

**33.3% rejected as the sole headline.** The first run produced 100 of 300 and
that number alone would have overstated adoption, because the provenance set is
dominated by monorepos publishing many packages from one pipeline. A second
analysis by publishing scope (56 of 242) was added and both are reported, with
the bias stated against the report's own figure.

**"Over a billion Rekor entries", "16,000 packages with provenance", and three
third-party npm audit rates — all cut.** No primary publication. The npm rate
in particular was the easiest available citation and would have saved the
measurement work; it is the clearest case of the rule costing effort.

## 2. Rejected — framings, including one disagreement with a merged document

**R-001's reading of C2PA's baked-in vocabulary, partially rejected.** R-001
§6.5 calls it "a real regression in extensibility," and as a statement about
expressiveness that is correct and this report does not dispute it. The report
nonetheless argues (§4.4) that the closed vocabulary and the testable
conformance regime are **the same decision seen from two sides**, and that a
conformance program cannot test "renders any self-describing vocabulary it has
never seen." On adoption grounds the closed vocabulary is a precondition of the
thing that shipped.

This is a **disagreement with a merged document** and is flagged as the first
item needing a human verdict. It does not contradict R-001's finding; it
declines R-001's implied conclusion that late binding is a free win.

**"The PICS censorship fight is not our problem" — rejected.** The tempting
move was to treat *Reno v. ACLU* and *Fahrenheit 451.2* as political history
irrelevant to a key-centric design. §6 argues instead that the ACLU's objection
was structural — a general mechanism for third parties to make
machine-readable assertions about content, consumed automatically — and that it
**transfers to this design more directly than to C2PA**, because third-party
assessment is a first-class goal here rather than an omission. This is the most
likely section to be cut in review and the entry records that it was put in
deliberately.

**A softer §8 — rejected twice.** Two earlier framings were discarded: "lessons
to carry forward" (too comfortable; it lets the reader agree without conceding
anything) and a risks table (it turns an argument into a register). The section
as written states that **three of SPKI's five failure modes are present in this
design today**, names DEC-002 as one of them, and separates the one that is
fixable from the two that are not. `PLAN-0001` §6 asks for exactly this and the
weaker versions did not deliver it.

**An encoding recommendation — never drafted.** DEC-002 is open; §3 of the
report says nothing here is evidence for a serialisation, and the searches
deliberately did not touch encoding.

## 3. What needs a human verdict

In descending order of consequence.

1. **§8's central claim** — that reasons (a), (c) and (d) from R-001 §5.7 are
   structural properties of this design as it stands. If accepted, it belongs
   in ARCH-0001 or `LIMITATIONS.md` via `propose-arch`, not only in a research
   report. If rejected, the report's last three sections need rewriting.
2. **The four-condition model (§7)** — the report's one original analytical
   claim, and the thing to attack. It is stated with a falsification condition
   and a named candidate counterexample (OpenPGP in the Debian keyring) that
   was not investigated.
3. **§4.4's partial disagreement with R-001 §6.5** (above). Two merged-document
   readings now coexist and a human should say which the project holds.
4. **§8.3, the dual-use / censorship property** — whether it goes in
   `LIMITATIONS.md`. The model's view is that it should and that the existing
   "proves origin and integrity, not truth" line does not cover it, because the
   objection is not that the mechanism lies.
5. **§9's reordering of D9 segments** — promoting AI agent attestation on the
   grounds that agent chains are *mechanically produced* and so satisfy the
   condition PICS failed. This is a planning claim, not a research finding, and
   it is in a research report because D3 "feeds D9".
6. **§8.2's inference about the wallet model** — that its statements are
   human-authored and therefore score badly on supply-side cost. This is an
   inference from `PLAN-0004`, not a finding, and the practitioner interviews
   that would test it were not conducted.

## 4. Guardrails observed

No cryptographic primitives generated — the only cryptographic operation in
the pass was `openssl x509 -noout -subject` reading certificates that were
already published. No `DEC-*` marked accepted. No parallel architecture
document; §8 is framed as input to `propose-arch`. No third-party bytes
committed — the C2PA deployment guidance PDF is recorded by digest and locator.
No edits inside `library/`. Work done in a worktree on `report/0004-uptake`.

**One honest limitation on this entry itself.** It was written in the same
change as the report, which is the rule `DL-0001` exists to enforce, so the
rejections in §1 and §2 are contemporaneous rather than reconstructed. But the
reviewing human had not yet seen the report when it was written, so §3 is a
list of questions rather than a record of answers. The entry should be revisited
when the PR is reviewed, and that revisit is what moves this from `open` to
complete.
