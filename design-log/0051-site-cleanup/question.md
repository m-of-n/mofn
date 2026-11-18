---
schema: "design-log/v1"
id: DL-0051
part: question
title: "#177: site cleanup — status banner, grouped nav, site-src/ for site-only pages, styling hook"
date: "2026-11-17"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "bin/manifest groups the nav by front-matter type under short titles; site-src/ holds the landing and download pages, extra.css and a Material override that prints a status banner from front matter; docs/ is now wholly generated; mkdocs checks anchors."
status: open
---

# DL-0051 — question

The human filed #177 ("Update and clean the mofn website") and, after asking
how the site's look could be changed, asked the agent to start it in a
worktree. Context supplied: #177's checklist (audit pages, correct decision
status everywhere, dead links, generated nav, `--strict`, readable on a phone),
#33 (site structure, PROC-0004 §9), and the agent's own suggestion that
styling land in this PR.

In the same session the human also merged #178 (bibliography publication)
into #34 on the agent's recommendation, and chose to build that publication
page rather than accept the existing flat bibliography — separate work, not
this change.
