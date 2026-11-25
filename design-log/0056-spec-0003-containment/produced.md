---
schema: "design-log/v1"
id: DL-0056
part: produced
date: "2026-11-24"
---

# DL-0056 — produced

`SPEC-0003` 0.3.0:

- **§6.** A new *Patterns* paragraph defines within once for kinds 4, 5 and
  11, as inclusion of matched sets. That is §6.3's wording, made general. It
  rejects patterns that match nothing, and states that within is
  antisymmetric. The equal-bytes sentence is kept, and says what "equal"
  means.
- **§6.1.** `*.L` with `L` longer than 251 octets is rejected. Within is given
  as four syntactic cases.
- **§6.2.** Within is defined for prefixes. Three canonical-range conditions
  are added: no containment, no siblings, and IPv4 first and then by address
  octets. A sketch shows that these make the range unique, and a range that
  is not canonical is rejected, not aggregated.
- **§6.3.** The §6.1 rule is applied to `*@p`. Within is given as four cases.
- **The status line** records the version reasoning.

No code changes: the engine implements none of these kinds.
