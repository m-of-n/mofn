---
schema: "library-doc/v1"
id: R-0007-unverified
title: "Unverified claims register — delegation models"
type: evidence
status: draft
version: "0.1.0"
date: "2026-10-26"
updated: "2026-10-26"
---

# Unverified claims register

This file is a **publication gate**. It applies the rule inherited from R-001:
a claim listed here appears in `report.md` only labelled as unverified, with
the basis named.

## 1. GnuPG does not narrow trust-signature scope along a chain

**Claim (report §3.3, §6, §7.2).** With `--trust-model pgp`, a key's onward
scope is the regex of the latest trust signature on it, and that regex
*replaces* rather than intersects any regex further up the chain. Therefore:
- Dave → Alice (level 2, `foo.com`), then
- Alice → Bob (level 1, `bar.com`), then
- Bob → `carol@bar.com` (level 0)

makes `carol@bar.com` valid for Dave.

**Basis.** A reading of `g10/trustdb.c` `validate_one_keyblock` (digest in
`sources.md` §3):
- the signer's recorded `trust_regexp` is checked against the target User ID;
- then `pk->trust_regexp = sig->trust_regexp` is set when the new signature
  has one;
- the comment *"If the trust sig contains a regexp, record it on the pk for
  the next round"*;
- no code path that combines two regexes was found.

**Not done.** The code was not built or run. No released version was
checked. `trust_regexp` assignment elsewhere (around line 2424, copying to the
key list) was read but not traced through every caller.

**To settle.** Run `experiments/gnupg-tsign-chain.sh` in a disposable
environment (it makes its own `GNUPGHOME` in a temp directory). Record the
`gpg --version` output and the validity printed for `carol@bar.com`.
- If it prints `full` or `marginal`, the claim holds.
- If it prints `unknown` or `never`, strike it from §3.3, §6 item 2 and §7.2,
  and the second "what survives" bullet goes.

## 2. GnuPG's command-line trust-signature regex over-matches

**Claim (report §3.3).** `--quick-tsign-key FPR 1,full,eng.foo.com` writes
`<[^>]+[@.]eng.foo.com>$`, and at evaluation `.` remains a wildcard, so the
regex also matches `<carol@eng-foo.com>`.

**Basis.**
- `keyedit.c` `parse_trustsig_string` concatenates the domain unescaped.
- `trustdb.c` `REGEXP_OPERATOR_CHARS` is `^[$()|*+?{`, without `.`.
- `sanitize_regexp`'s comment says *"the only legal regex character is "."*".

**To settle.** The same script, step 3, prints the validity of
`carol@eng-foo.com`.

## 3. X.509 libraries' support for `initial-permitted-subtrees`

The report states only what RFC 5280 says: the input exists, and support is
not required. **No claim is made** about which libraries (Go `crypto/x509`,
OpenSSL, NSS, BoringSSL, Bouncy Castle) expose it. A survey would sharpen
§5.5's X.509 bullet.

## 4. Deployment of RFC 8550 §3's From-address check

No source held by the library measures which mail clients enforce it, or what
they do on a mismatch. The report states only the RFC's requirement.
