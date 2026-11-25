# Schema

**WP1 output: encoding-neutral first.** The logical types in ARCH-0001 §4 —
`Key`, `KeyId`, `Principal`, `Name`, `Threshold`, `Tag`, `Validity`,
`ArtifactId`, `PredicateType`, `Predicate`, and the certificate kinds `NameCert`,
`AuthzCert`, `AclEntry`, `ArtifactStatement`, `Endorse` — are specified here
*without* committing to a wire format.

This is deliberate and it is the main schedule hedge: reduction (WP6, the demo
floor) could be built against the logical model while DEC-002 was open.

DEC-002 is accepted (`ADR-0004`, 2026-10-25): the concrete encoding is
KSA-CBOR, specified in `SPEC-0002` §4 with its CDDL in `SPEC-0002` Appendix B.
The neutral schema here remains normative for the logical types.
