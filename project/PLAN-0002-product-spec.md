---
schema: "archdoc/v1"
id: PLAN-0002
title: "Product Specification — how we fill it out"
short_title: "Product Spec plan"
description: "Mapping the CS690 Product Spec template onto what the repo already answers, and naming what it does not."
type: plan
category: process
status: draft
version: "0.1.0"
date: "2026-09-25"
updated: "2026-09-25"
needs_review: true
reviewed: false
canonical_path: project/PLAN-0002-product-spec.md
companion:
  - project/PLAN-0001-project-plan.md
defers_to: ARCH-0001
---

# Product Specification — how we fill it out

**Deliverable:** `ProductSpec_Fall2026_<ProjectName>.pdf` — title page (project,
sponsor, team, "CS690 Fall 2026" + instructor, date), TOC updated, instructions
removed.

**The point of this plan:** roughly two-thirds of the ~90 questions are already
answered somewhere in this repo. **Do not write those from scratch — cite and
condense.** The real work is the third that has no source, listed in §2.

---

## 1. Already answered — assemble, don't author

| Spec section | Source | Note |
|---|---|---|
| Sponsor, company | pitch deck, `README` | Paul, personal capacity, no NDA |
| System overview · motivation · core problem | `ARCH-0001` §1, `PLAN-0001` §0 | trust collapse; syntax strong, semantics weak |
| Project description (what) | `PLAN-0001` §2 (D0–D10), `PROC-0004` | |
| **Comparative / competitive systems** | `ARCH-0001` §3.1–3.2, `library#14` | X.509, PGP, SDSI/SPKI, in-toto, SCITT, C2PA. **library#14 is exactly this question** |
| External systems | `ARCH-0001` §6 interchange matrix | in-toto, COSE, SPKI — import/export, not runtime |
| Terminology | `GLOSSARY-0001` | lift wholesale |
| MVP core features | `APP-0001` §2, `PLAN-0001` §9 I3 | the demo floor **is** the MVP |
| Extended features | `PROC-0004` §11 | what is beyond Fall 2026 |
| Security / privacy requirements | `LIMITATIONS.md`, `ARCH-0002` P5, `mofn#30` | |
| Technical stack + why | `DECISIONS-0001` DEC-002 | **say it is open, and why** — do not invent a decision |
| Version control · conventions · tools | `CONTRIBUTING.md`, `PROC-0003` | branches, worktrees, PRs, DCO |
| Design considerations — hardest problems | `DECISIONS-0001` tier 1 | DEC-002, R-M-12, reduction |
| Technical architecture | `ARCH-0001` §4, `ARCH-0002` | |
| Modules & interfaces | `APP-0001` §2, `ARCH-0001` §4.2 | |
| Data groups | `ARCH-0001` §4.1 | statements, domains, trust roots |
| Methodology · sponsor comms · task tracking | `PROC-0003` §5, `BACKLOG-0001` | weekly Zoom, GitHub issues |
| Team roles | `PROC-0003` §2, issue assignees | |
| Goals · success metrics · risks | `PLAN-0001` §12, `PROC-0004` | the cut order **is** the risk register |
| Milestones · timeline | `PLAN-0001` §9 (I0–I5) | already ≤3-week spacing |

## 2. No source — this is the actual work

| Section | Owner | Notes |
|---|---|---|
| **User personas** | both | Nothing exists. Minimum three: a **relying party** deciding whether to believe a claim, an **issuer** making one, a **domain author** defining what claims mean |
| **User goals + scenarios** | both | Start-to-end walkthrough. The Alice/Bob/Carol/Dave example in `prototype/statements/demo_email.py` is one already — write it up |
| **User stories** | both | *As a …, I want …, so that …*, for the MVP only |
| **Use environment / usability** | Ndewedo | Ties to `mofn#33`. **Function over form**, and say so |
| **UI sketches** | Ndewedo | The template asks for key views. GUI is October — **sketch anyway**, it is what forces the use cases to be concrete |
| **Database** | David | *There is no database.* Files and a git repo. Say that plainly with the reason, rather than leaving it blank |
| **Performance / scalability** | David | Honestly: **no performance requirement**. Verification is local and offline. Say it |
| **Testing strategy** | David | CI exists; a strategy does not. Test vectors are the interesting answer |
| **Sponsor meeting schedule** | Paul | weekly Zoom + async |

## 3. Order

1. **Name the two use cases** — decision **T1-A** (`DECISIONS-0001`). *Personas,
   scenarios, stories and sketches all depend on it; nothing in §2 can be written
   honestly until it is settled.*
2. Assemble §1 into a draft — mechanical, one sitting
3. Write the §2 sections
4. Diagrams — architecture, data flow, one workflow
5. Title page, TOC, export PDF, share with sponsor

## 4. Two rules for this document

**Say what is undecided.** DEC-002 through DEC-009 are open **by design**. A
spec that invents a stack decision to look complete is worse than one that
records an open decision with its acceptance test. The template asks *"explain
why the stack was selected"* — the honest answer is *not yet, here is how it
will be*.

**Do not overclaim the prototype.** `prototype/README.md` says it is **not yet
representative of the architecture**. Cite it as a spike, never as the design.

## 5. Open

- **Due date** — not in the template; it says milestones start at the *second
  status review*. Needs confirming.
- **`<ProjectName>`** for the filename — `m-of-n`? `KSA`?
- **Instructor name** for the title page.
- **T1-A**, which blocks §2 entirely.
