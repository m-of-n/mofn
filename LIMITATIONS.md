# What this system does not do

Stated plainly, and stated by the software itself in every verdict it emits.

**It does not prove truth.** It proves that a key made a statement, that the
statement is intact, and that the key had standing to make it. Whether the
statement is *correct* is outside the system entirely. A perfectly valid
attestation can assert something false.

**It does not prove identity.** Principals are keys. The system never asserts
that a key belongs to a particular human or organization. Names are relative to
a naming key and mean only what that key says they mean.

**It does not do revocation at scale.** Short validity windows are preferred to
revocation-heavy design. Revocation is representable; it is not solved.

**It is not a CA and does not replace WebPKI.** X.509 is an interchange target,
never the native model (ARCH-0001 R-M-01, NG1).

**It does not verify builds.** Mapping to in-toto and SLSA is interchange. We do
not execute or reproduce builds.

## Not in the first release

Transparency-service receipts, OpenPGP introducer import, X.509 import, nested
threshold subjects, zero-knowledge proofs, production key management.
