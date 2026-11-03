---
schema: "library-doc/v1"
id: R-0007-unverified
title: "Unverified claims register — delegation models"
type: evidence
status: draft
version: "0.2.0"
date: "2026-10-26"
updated: "2026-11-01"
---

# Unverified claims register

This file is a **publication gate**. It applies the rule inherited from R-001:
a claim listed here appears in `report.md` only labelled as unverified, with
the basis named.

§1 and §2 are **settled**: they were executed on 2026-11-01 and held. They stay
here, numbered as they were, so the report's references keep resolving. §3 and
§4 remain open.

## 1. GnuPG does not narrow trust-signature scope along a chain — SETTLED, holds

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

**Result.** `experiments/gnupg-tsign-chain.sh` on GnuPG 2.5.24 (Homebrew,
macOS) printed validity `f` (full) for `carol@bar.com` with Alice's scope set to
`bar.com`. Both controls behaved: `carol@eng.foo.com` under scope `eng.foo.com`
gave `f`, and `carol@bar.com` under scope `eng.foo.com` gave `-` (unknown).
Output: `experiments/gnupg-tsign-chain.out`.

**Still not done.** Only that one version was run; older release branches were
not. `trust_regexp` assignment elsewhere (around line 2424, copying to the key
list) was read but not traced through every caller. The result makes that
tracing unnecessary for 2.5.24.

## 2. GnuPG's command-line trust-signature regex over-matches — SETTLED, holds

**Claim (report §3.3).** `--quick-tsign-key FPR 1,full,eng.foo.com` writes
`<[^>]+[@.]eng.foo.com>$`, and at evaluation `.` remains a wildcard, so the
regex also matches `<carol@eng-foo.com>`.

**Basis.**
- `keyedit.c` `parse_trustsig_string` concatenates the domain unescaped.
- `trustdb.c` `REGEXP_OPERATOR_CHARS` is `^[$()|*+?{`, without `.`.
- `sanitize_regexp`'s comment says *"the only legal regex character is "."*".

**Result.** The same run printed validity `f` for `carol@eng-foo.com` under
scope `eng.foo.com`, so `.` over-matches. Only that one look-alike was run;
§3.3's `@fooxcom` follows from the same regex and was not.

## 3. X.509 libraries' support for `initial-permitted-subtrees`

The report states only what RFC 5280 says: the input exists, and support is
not required. **No claim is made** about which libraries (Go `crypto/x509`,
OpenSSL, NSS, BoringSSL, Bouncy Castle) expose it. A survey would sharpen
§5.5's X.509 bullet.

## 4. Deployment of RFC 8550 §3's From-address check

No source held by the library measures which mail clients enforce it, or what
they do on a mismatch. The report states only the RFC's requirement.
