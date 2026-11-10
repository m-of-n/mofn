---
schema: "design-log/v1"
id: DL-0029
part: question
title: "Automating the weekly demo slice run (mofn#68)"
date: "2026-11-07"
model: "claude-opus-5-5"
human: Ndewedo-Newbury
outcome: "`.github/workflows/weekly-slice.yml`: Monday cron runs `demo/slice.sh` from a clean clone with no network and posts the output on mofn#68. The verdict notes stay human. No spec, schema, vector or DEC-* touched."
status: complete
---

# DL-0029 — question

## The brief

Chip (GitHub `Ndewedo-Newbury`), who owns mofn#68 (W-4), asked: *is there a way
to automate issue #68's problem?* Then asked which option the agent recommends,
and said "go".

mofn#68 asks for three things each Monday: run `demo/slice.sh` from a clean
clone (documented prerequisites only, no network, no keychain); post the run
output on the issue; and write notes on what the verdict says — is each of the
six lines understandable to a relying party, does the authorization line say
why, is the limit line present — filing findings against mofn#65.

## Context supplied

- mofn#68 body and comments, including the 2026-11-01 run note.
- `demo/slice.sh` and `.github/workflows/ci.yml` on `main`. The `wallet` job
  already runs the slice on every push and PR (Linux and macOS).
