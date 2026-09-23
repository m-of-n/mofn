# prototype/

**Throwaway spikes. Never ships.** `CLAUDE.md`: `src/` stays empty until
DEC-002 is accepted; this directory is where we learn things without deciding
them.

| spike | what it is for |
|---|---|
| `statements/` | create statements in a reduced CBOR profile; render a PICS-like label type. Evaluates the *representation*, not the implementation |

## Why this exists now

Sponsor direction, 2026-09-22: *"we need to prototype creation of these
statements in ways that demonstrate use cases and allow evaluation of
representation of both the statements and the PICS-like semantic description of
the tags/labels."*

**The point is evaluation, not implementation.** Two things are being looked at:

1. **Statement representation** — does *A says B has C* (ARCH-0002 P2) encode
   cleanly, and is the result legible in a diagnostic form?
2. **Label-type representation** — can a PICS-style type definition carry
   representation, constraints, semantics and a human rendering (P3), and be
   hash-identified as part of a set (P4)?

Anything learned here goes into a proposal against ARCH-0001 or ARCH-0002.
**Nothing here is normative**, and no decision is made by writing code.
