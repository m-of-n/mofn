---
schema: "design-log/v1"
id: DL-0026
part: produced
date: "2026-11-05"
---

# DL-0026 — produced

No primitive and no vector. One engine change uses only the existing
libraries (PyNaCl); it adds a comparison and no cryptography.

| file | change |
|---|---|
| `spec/ARCH-0001-authorization-attestation.md` | 0.1.9. New §3.4, "OpenPGP mechanisms read against this model": six rows, each tied to the item it bears on and that item's state. `RFC9580` added to `related_rfcs` and §10. |
| `spec/ARCH-0001-CHANGELOG.md` | 0.1.9 entry. |
| `project/PLAN-0004-application-plan.md` | 0.2.0. New §6.2: OpenPGP vs §6.1/ARCH-0003 vs engine v0, three engine rules, and the declined revocation item. |
| `prototype/wallet/engine/store.py` | `Wallet.unlock` re-derives the kid from the opened seed and refuses a mismatch, wiping the seed first. |
| `prototype/wallet/tests/test_cli.py` | `test_key_file_swapped_between_personas`. It fails without the fix and passes with it; the full suite passes (227). |
| `design-log/README.md` | row for this entry. |

## The one substantive finding

RFC 9580 §5.5.3 passes the public-key packet fields as AEAD additional data
when it encrypts secret key material. Engine v0's SecretBox has no
additional data, so it authenticates the seed but not *whose* seed it is. If
two personas share a passphrase, one persona's `.key` copied over the
other's opens cleanly. Before this change the mismatch surfaced only at the
post-sign verify in `cmd_make`, which was a side effect, not a check. After
it, `unlock` refuses the seed.

The fix is a comparison after opening, not additional data in the box. It
changes no file format, so no key file needs rewriting.
