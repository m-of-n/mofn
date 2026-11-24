---
schema: "design-log/v1"
id: DL-0053
part: question
title: "W-9 (mofn#181): groups with a steward, enrollment by consent, group thresholds, SPEC-0004 §6.4 gaps answered — ARCH-0001-PROPOSAL-v0.4.0"
date: "2026-11-17"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "spec/ARCH-0001-PROPOSAL-v0.4.0.md (status: proposed). No DEC-* touched, no ADR, no SPEC edited, no vectors: all wait on acceptance."
status: open
---

# DL-0053 — question

The human (owner of mofn#181) asked the agent to **walk through how it would
complete issue #181**, with recommendations the human would then adjust. There
were three rounds of discussion, then: *"I accept your recommendation. Continue
with the next steps."*

#181 as filed: an enrollment protocol for delegation groups, specified and then
built in the desktop app. Its scope is spec first, then engine (T-095), then
app. It warns that enrollment "is in no spec. It needs a diff to `ARCH-0001`
through `propose-arch`, with a design-log entry, **before** any code". Its
deadline: move to the next milestone if the spec is not answered by ~Nov 26.

Context the agent read: `ARCH-0001` v0.3.2 in full; `SPEC-0004` §4.2, §5.3,
§6, §7.1, §10.4, §11.8, §14.2; `SPEC-0002` §7.2, §8.6; `SPEC-0003` §6.4;
`SPEC-0005` §4; `SPEC-0001` §8.2; `DL-0042` (the five §6.4 gaps); `BACKLOG-0001`
T-043, T-095, W-7; issues #180 (W-8) and #173 (W-3 TUI).

## The rounds

1. **Agent's first plan.** The group as a key `G` whose "roster" is a
   threshold trust statement listing members. Enrollment by an unsigned offer
   plus a signed acceptance; leaving by reissuing the roster. The agent asked
   whether an acceptance should be *required* for a member to count.
2. **Human redirect:** *"Think more along the lines of a group or community
   has an assigned trusted persona to invite other personas into the group,
   which allows them to access the group key."* The agent set out three
   readings of "access the group key": (A) a content key for confidentiality,
   with authority kept in each member's own signature; (B) every member holds
   `G`'s signing key; (C) threshold shares (FROST). It asked three questions.
3. **Human answers:** (1) **A**; (2) **one steward for now**; (3) *"I don't
   know what are the issues that could occur if the steward is not a member or
   is a member?"* The agent tabulated both and recommended that the spec allow
   either, that stewardship never give a vote, and that the app default make
   the creator the steward and a self-enrolled member. **Human: accepted.**
