# prototype/

> **This is NOT yet representative of the right architecture.**
> Sponsor, 2026-09-23. It encodes *one reading* of the model at one moment, and
> that reading is still wrong in ways we have not found. **More iteration and
> more examples to do.** Do not take any shape here — the statement layout, the
> range language, the reduction algorithm, the label-type fields — as settled.
> `src/` stays empty precisely so that nothing here can become normative by
> being the only thing that runs.

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

## Known to be unrepresentative

Not a to-do list — a list of places the spike is **known to mislead** if read as
architecture:

- **Ranges are globs.** `*@foo.com` is a placeholder for whatever DEC-004
  settles. Real tags need intersection semantics per type (R-M-08), and a glob
  has none worth the name.
- **Reduction trusts its inputs.** `reduce.py` never checks a signature. A real
  verifier checks authenticity *before* walking anything.
- **One topic per delegation.** Nothing composes across topics, or across
  domains of discourse — which is where P4's "domains are the unit of authority
  scope" would actually be tested.
- **No revocation, no validity windows, no thresholds.** ARCH-0001 R-M-06 makes
  *k*-of-*n* first-class; the spike has no notion of it.
- **The statement layout is arbitrary.** `a`/`b`/`t`/`c`/`ts` is short, not
  considered. It is not a wire format proposal.
- **The trust root is a flat list.** Real trust management is a wallet holding
  roots, delegations and claims with provenance for each — `APP-0001` §2.
- **One example, one shape.** Email addresses. Until a second, genuinely
  different domain runs through the same code, nothing here demonstrates
  generality — which is the whole P3/P4 claim.

## What would make it representative

More examples, deliberately unlike each other, and the architecture questions
answered first rather than assumed:

1. a second domain that is **not** an identifier namespace — build provenance,
   or a document attribute
2. signature checking inside reduction
3. a real range/tag language once DEC-004 has a direction
4. thresholds, so R-M-06 is exercised rather than deferred
5. the same claim expressed **two ways** to show the encoding is a choice, not
   the model
