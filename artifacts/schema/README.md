# Schema

**WP1 output: encoding-neutral first.** The logical types in ARCH-0001 §4 —
`Key`, `KeyId`, `Principal`, `Name`, `Threshold`, `Tag`, `Validity`,
`ArtifactId`, `PredicateType`, `Predicate`, and the certificate kinds `NameCert`,
`AuthzCert`, `AclEntry`, `ArtifactStatement`, `Endorse` — are specified here
*without* committing to a wire format.

This is deliberate and it is the main schedule hedge: reduction (WP6, the demo
floor) can be built against the logical model while DEC-002 is still open.

Concrete encodings are added once DEC-002 is accepted, as sibling files, with
the neutral schema remaining normative.
