---
schema: "design-log/v1"
id: DL-0054
part: question
title: "W-8 (mofn#180): several personas in one wallet — key subjects, anchors scoped to one persona, the Personas and Communities pages"
date: "2026-11-23"
model: "claude-opus-5[1m]"
human: wyxiao6
outcome: "prototype/wallet/ 0.11.0 (make/check --subject-key, check/root list --as); prototype/wallet-app/ Personas and Communities, Verify bound to the active persona; BACKLOG-0001 W-8/W-9 rows; PLAN-0004 §5.2."
status: open
---

# DL-0054 — question

The human asked the agent to **explain and implement W-8**, in one session,
starting from a plan.

#180 as filed. Definition of done: one wallet in the desktop app holds several
personas; the user can switch between them, see which tags each persona has
received, and see who is in which community. Five acceptance boxes:

- [ ] Create two personas in one wallet; they use separate identity keys
- [ ] Switching persona changes the signing key and the trust context used in Verify
- [ ] Each persona lists the tags it received, each with its verdict
- [ ] Each persona lists its communities and their members
- [ ] Nothing here decides DEC-004 / DEC-005

Its *Depends on* section carried an instruction the agent treated as part of
the task: *"Engine support for several owned personas in one wallet, if
`prototype/wallet/engine/` does not already have it — **find out first and say
so here**."*

## What the agent read before proposing anything

`ARCH-0003` §3.2 (persona) and §3.4 (contexts); `SPEC-0001` §3.1, §3.2, §6.1,
§6.3; `SPEC-0004` §4.1, §10.4; `GLOSSARY-0001`; `PLAN-0004` §5.1;
`DECISIONS-0001` item 28; `DL-0050` (W-7, all three parts); the engine
(`store.py`, `check.py`, `cli.py`, `reduce.py`, `schema.py`, `statement.py`)
and the whole of `prototype/wallet-app/`.

## What it found, and told the human

1. **"Community" is not a normative term.** It appears in no SPEC. It is the
   app's word for a **SPEC-0004 context**, as `PLAN-0004` §157 already decided
   ("W-8 gives contexts their own page, as communities").
2. **A key-subject attestation is already legal, and already vectored.**
   `KIND_TARGETS[4]` is every target type, and **TV-13's own note in the
   published vectors reads "attestation about a KEY"**, against TV-4's "about
   an ARTIFACT digest (not a key)". The gap was in `cli.py`, which only ever
   built a digest target, and in `check.py`, which hardcoded one.
3. **Anchors were already per persona on disk** —
   `personas/<kid>/trusts/<context>.yaml` — but `Wallet.anchors(context)`
   unioned every owned persona's, so the app could not evaluate as one.
4. **Two things #180 asks for cannot be built as written** (below).
5. **PR #186 (W-9's `ARCH-0001-PROPOSAL-v0.4.0`) was open, approved and
   mergeable**, and `propose-arch` says to serialize architecture changes. So
   W-8 had to touch no `spec/` file. It does not.

## The three questions put to the human, and the answers

| Question | Answer |
|---|---|
| A tag given to a persona: a **key target** in the engine, or the digest of the persona's `*.pub.stmt` file, or defer? | **Key target.** |
| Verify's trust context: add **`check --as PERSONA`**, or keep the union and label it? | **`check --as`.** |
| Size: full W-8 in one PR, engine-then-app, or app only? | **Full W-8, one PR.** |

A fourth was asked after the designs came back: W-7's precedent (`DL-0050`)
was that the look is settled by HTML mockups *before* any screen code. The
human chose **build in W-7's approved system, then screenshots for approval**,
because W-8 adds no new visual language — graphite, `Card`, `Rows`, `Chain`
and the page frame are reused as approved.

## Constraints carried

No `spec/` change; no DEC-* decided; no cryptographic primitive written; no
reduction logic touched; every existing golden byte-identical under both
codecs; DCO on every commit; this entry in the same change.
