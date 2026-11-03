---
schema: "library-doc/v1"
id: R-0007-searches
title: "Searches — delegation models"
type: evidence
status: draft
version: "0.1.0"
date: "2026-10-26"
updated: "2026-10-26"
---

# Searches

All retrieval took place on 2026-10-26.

## 1. No open-ended web search for the report itself

The library's `delegation-models` topic (library#29, #55) and the FX-1
extractions of library#64 had already assembled the bibliographic base. The
topic answer says these records let the report *"be written without ingesting
anything further"*. That held except for the two gaps the topic named itself,
which were closed by targeted retrieval (§2).

## 2. Targeted retrieval

| what | query or URL | yield |
|---|---|---|
| RFC 8550, the topic's gap (2) | `https://www.rfc-editor.org/rfc/rfc8550.txt`, `rfc8550.json`, errata | Fetched and digested. `rfc-8550` written to the summary bar. Spot check of RFC 5750 showed the same trust sentences, so RFC 8551 §4's stale pointer does not change #14's answer. |
| SDSI 1.1, the topic's gap (1) | `https://people.csail.mit.edu/rivest/pubs/RL96.ver-1.1.html` | Fetched and digested. `sdsi-1-1` written to the summary bar. The email mapping via `DNS!!` was **not** anticipated by the topic answer. |
| SDSI implementations | web search "SDSI 1.1 implementation" | MIT SDSI/SPKI 2.0 distribution only. No 1.1 implementation. |
| S/MIME implementations | web search on RFC 8550 conformance (Thunderbird/NSS, OpenSSL, Bouncy Castle, Outlook, Apple Mail) | None claims RFC 8550 by number. |
| GnuPG trust-signature regex | `dev.gnupg.org/source/gnupg/browse/master/g10/keyedit.c` | **Timed out** (connect). |
| same, via mirror | `raw.githubusercontent.com/gpg/gnupg/master/g10/{keyedit.c,trustdb.c,gpg.c,trustdb.h,tdbio.h}` | Fetched. Yielded the regex construction, the unescaped `.`, the per-key regex replacement and the bare-mailbox fix (`sources.md` §3). |

## 3. Library sources re-fetched for the quote audit

`bin/fetch-source rfc-5280 rfc-9580 rfc-2693 rfc-2692 rfc-8551 rfc-9804
draft-ietf-spki-cert-structure`. All seven verified byte-for-byte against
their recorded `content.sha256`.

## 4. What was looked for and not found

- **A measurement of OpenPGP trust-signature or regex use.** None. This is the
  same result as R-001 `unverified.md`.
- **An X.509 library survey of §6.1.1(h) `initial-permitted-subtrees`
  support.** Not searched. Recorded in `unverified.md` §3.
- **An email tag profile for SPKI.** Neither RFC 2693 nor the structure draft
  defines one. The §3.5 rendering is ours.
