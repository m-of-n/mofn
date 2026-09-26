# Area C — Decentralised Naming: The Systems That Rejected a Global Namespace

## 1. The shared premise

PGP, SDSI and SPKI converge on two moves. First, the **principal is a key**, not a name: SDSI 1.1 states flatly that "SDSI principals *are* public digital signature verification keys," and that "two principals are taken as being the same if and only if they have the same public key." Second, **names are local**. RFC 2693 argues that the names people actually use "are local names… They do not need to be globally unique. Rather, they need to be unique for the one entity that maintains that address book." Where X.509 asks "is this the certificate for *CN=Alice*?", these systems ask "is this key authorised, by a chain I can follow from a key I already hold?"

## 2. OpenPGP: how much scoped delegation is really there?

RFC 4880 (November 2007; Callas, Donnerhacke, Finney, Shaw, Thayer) was obsoleted by **RFC 9580, "OpenPGP", July 2024** (Wouters ed., Huigens, Winter, Niibe; Proposed Standard), which also absorbed RFC 5581 and RFC 6637. The 2024 revision is a cryptographic modernisation (v6 keys, AEAD, errata integration) — it carries the trust machinery forward **substantively unchanged**.

That machinery is thinner than its reputation. Two signature subpackets do the work:

- **Trust Signature (type 5)**, §5.2.3.21: one octet of *level* (depth) and one of *trust amount*. Level 0 is an ordinary validity signature; level 1 marks a trusted introducer; level 2 marks a **meta-introducer** ("trusted to issue level 1 Trust Signatures"); generally level *n* delegates the right to issue level *n−1*. Amount runs 0–255, with <120 partial and ≥120 complete; implementations SHOULD emit 60 or 120.
- **Regular Expression (type 6)**, §5.2.3.22: a null-terminated UTF-8 regex (Henry Spencer syntax) used "in conjunction with Trust Signature packets (of level > 0) to limit the scope of trust that is extended." Only the target key's signatures on **User IDs matching the regex** get trust extended.

So PGP does have scoped, depth-limited delegation — but the scope predicate is a **regex over a display string**, not over a permission. The delegation is always of *the same power* (certify identities), narrowed only by which identity strings are covered. There is no way to say "trusted to certify, but only for signing releases." And crucially, RFC 9580 specifies **no trust-computation algorithm at all**: the Trust packet (§5.10) "is used only within keyrings," is not exported, and "the format of Trust packets is defined by a given implementation." The web of trust is an implementation convention, never a standardised evaluator.

Tooling narrows it further. GnuPG's `--quick-tsign-key` takes a trustspec `[T=]depth,value[,domain]` where the optional domain is "a plain domain name like `example.org`" — the arbitrary regex of the wire format is exposed to users as a domain filter only.

The empirical collapse is the decisive fact. Ulrich, Holz, Hauck and Carle (ESORICS 2011) analysed a December 2009 SKS snapshot: ~2.7M keys and 1.1M signatures, of which the actual WoT — keys that signed or were signed — was **325,410 keys with 816,785 valid signatures**, split across **240,283 strongly connected components**, with the largest SCC only **~45,000 nodes (14% of WoT keys)**. Then in June 2019 the certificate-flooding attack (**CVE-2019-13050**) exploited the append-only keyserver design: poisoned certificates carrying ~150,000 signatures caused persistent DoS in GnuPG. Upstream mitigation in GnuPG 2.2.17 was to **stop importing third-party signatures by default**, and Debian/Ubuntu switched the default keyserver to **keys.openpgp.org**, which states it "doesn't publish third-party certifications" by default. The distribution channel for the web of trust was deliberately shut off. PGP's answer to Zooko's triangle was answered, in the end, by an email-verifying central-ish directory.

## 3. SDSI (Rivest & Lampson, version 1.1, 2 October 1996)

SDSI's contribution is **linked local namespaces**. Every principal defines its own bindings; "the principal you call alice-smith may be different from the principal I call alice-smith." Names *chain* across namespaces — `(ref: bob alice)`, sugared as `bob's alice`, and extensible to `bob's alice's mother`. Groups and group-membership certificates give ACLs a vocabulary. The stated motivation is that X.509-style schemes "are both excessively complex and incomplete," their complexity arising from "dependence on global name spaces." Global roots (VeriSign!!, DNS!!) survive only as optional conveniences.

## 4. SPKI (RFC 2692 and RFC 2693, both September 1999, both **Experimental**)

RFC 2692 "SPKI Requirements" (Ellison) sets the goal: certificates that authorise actions rather than bind names. RFC 2693 "SPKI Certificate Theory" (Ellison, Frantz, Lampson, Rivest, Thomas, Ylonen) supplies the calculus, and explicitly records the merge: "Ron Rivest and Butler Lampson showed with SDSI 1.0 that one can not only use local names locally, one can use local names globally. The clear security advantage and operational simplicity of SDSI names caused us in the SPKI group to adopt SDSI names as part of the SPKI standard." SPKI 2.0 names are S-expressions: `(name fred)`, chained as `(name fred sam)`.

The core objects:

- **The 5-tuple** (§6.1): ⟨Issuer, Subject, **Delegation** (boolean), Authorization (an S-expression), Validity dates⟩. Name certificates get a separate **4-tuple** ⟨Issuer, Name, Subject, Validity⟩.
- **Reduction** (§6.3): ⟨I1,S1,D1,A1,V1⟩ + ⟨I2,S2,D2,A2,V2⟩ → ⟨I1,S2,D2,AIntersect(A1,A2),VIntersect(V1,V2)⟩ provided S1 = I2 and **D1 = TRUE**. The delegation bit is a hard gate on chain composition.
- **Tag intersection** (§6.3.1): authorisations intersect element-wise; a longer list wins, so "additional elements of a list must restrict the permission granted." `(ftp (host ftp.clark.net))` ∩ `(ftp (host ftp.clark.net) (dir /pub/cme))` = the latter. Wildcards `(*)`, `(* set …)`, `(* prefix …)`, `(* range …)` give a small set-algebra over tags. Monotone attenuation is *structural*.
- **Threshold subjects** (§6.3.3): K-of-N subordinate subjects, reduced by selecting K that reduce to the same subject and intersecting their validity, authorisation and delegation.
- **Path discovery** (§6.3.4) is pushed onto the prover: "All reduction operations are in the order provided by the prover."

## 5. RFC 9804 (June 2025) — why now?

**"Simple Public Key Infrastructure (SPKI) S-Expressions," Rivest (MIT CSAIL) and Eastlake 3rd; Informational, IETF stream, June 2025.** Its own §1.3 explains the 28-year gap: the S-expressions came from SDSI in 1996, were refined "during the merger of SDSI and SPKI during the first half of 1997," and "although a specification was made publicly available as a file named `draft-rivest-sexp-00.txt` on 4 May 1997, that file was never actually submitted to the IETF." The 2025 RFC is "a clarified and modernized version."

The motive is **live interoperability, not revival**: §1.1 says these S-expressions "are in active use today between GnuPG and Ribose's RNP," via Libgcrypt and the C++ `sexpp` parser, with further implementations in C, Ruby, OCaml, Inferno. Two OpenPGP implementations needed a citable spec for a private-key serialisation format. RFC 9804 standardises **the encoding layer of SPKI and nothing else** — no 5-tuples, no delegation, no reduction. That is a precise measure of what survived: the syntax did, the authorisation theory did not.

## 6. Why the SPKI WG shipped no standards-track output

The WG (Security Area; chairs Metzger and Bellovin) targeted IESG submission by May 1997. What it published, in September 1999, was two **Experimental** RFCs — the requirements and the theory. The actual bits-on-the-wire document, **draft-ietf-spki-cert-structure-05 (16 March 1998, Lampson, Ylonen, Rivest, Frantz, Ellison, Thomas), expired and was never published**. The WG is recorded as concluded, charter last updated 2001-02-10. Read structurally: the group standardised the *rationale* and abandoned the *format*. A theory RFC with no wire format and no conformance target cannot be implemented interoperably, which is close to a sufficient explanation for zero deployment on its own.

## 7. Modern descendants

**W3C DID Core 1.0** became a Recommendation on **19 July 2022** (Sporny, Guy, Sabadello, Reed); **DID v1.1** was a Candidate Recommendation Snapshot as of 5 March 2026. DID Core is deliberately empty where SPKI was full: it "does not presuppose any particular technology or cryptography," defines `capabilityInvocation` and `capabilityDelegation` as *verification relationships* whose semantics are left to methods and applications, and pushes everything real into DID methods — of which there were 100+ experimental specs at 1.0 publication. That is a registry of namespaces, not a resolution of the naming problem.

**did:key** is the purest SDSI position in modern dress: "purely generative, requiring no look ups in a registry," with the identifier a multibase/multicodec encoding of the raw public key, and DID documents expanded algorithmically. It is also the honest one about the cost — "Since `did:key` values are not stored in any registry, they cannot be updated or deactivated." The key *is* the name, so there is no rotation and no revocation. The spec remains **v0.9, a Community Group draft**, registered in the DID Extensions registry, never a Recommendation.

**Keybase** took the opposite tack: rather than solve naming, it *borrowed* namespaces, letting a key claim Twitter/GitHub/DNS identities via signed, publicly-auditable proofs in a per-user sigchain. It substituted "many weak global namespaces, cross-checked" for "one strong global namespace." It was acquired by Zoom on **7 May 2020** for $42.9M and effectively ceased to be an independent identity layer — which is its own datum about the business model.

**Zooko's triangle** (Wilcox-O'Hearn, 2001, "Names: Decentralized, Secure, Human-Meaningful: Choose Two") names the trade-off these systems navigate. Was it resolved? Honestly: **no, it was relocated.** Namecoin/Blockstack/ENS demonstrate that a consensus ledger can deliver all three *for first-come-first-served registration*, but they buy decentralised agreement with a global consensus artefact — which is a global namespace, just one without a corporate registrar — and they inherit squatting, renewal economics and Sybil exposure. SDSI's move was different and cleaner: deny that a name must be global at all, accepting that "human-meaningful" is only ever meaningful *to someone*. `did:key` and PGP fingerprints sit at secure+decentralised, non-human-meaningful. Nothing has escaped the triangle; systems have chosen corners more self-consciously.

## 8. The analytical core: why none displaced X.509

Not "ahead of their time." Five concrete, evidenced reasons:

**(a) No wire format, no conformance target, no standards-track status.** SPKI's structure draft expired; its two published RFCs are Experimental and carry no MUSTs an implementer can be tested against. OpenPGP standardised subpackets but no trust evaluator. You cannot ship interop against a rationale.

**(b) The bootstrapping problem is *quadratic* and the payoff is *deferred*.** X.509 requires one party (the server operator) to act; the relying party inherits a root store they never touch. SPKI/PGP require *both* endpoints to hold keys and to have constructed a path. Wang, Jha, Reps, Schwoon and Stubblebine (ESORICS 2006) state it bluntly: "trust-management systems such as KeyNote and SPKI/SDSI have seen limited deployment in the real world. One reason for this is that both systems require a public-key infrastructure for authentication, and PKI has proven difficult to deploy, because each user is required to manage his/her own private/public key pair." Their proposed fix was to *back SPKI onto Kerberos* — an admission that the key-per-user premise was the blocker.

**(c) Certificate path discovery was externalised to the prover.** RFC 2693 §6.3.4 hands the client the job of finding and ordering the chain. X.509 clients get a flat root store and a depth-bounded search. "Bring your own proof" is fine for a grid job and hostile for a browser.

**(d) No browser or OS integration, and no path to one.** The trust anchors in X.509 live in a handful of root programs (Microsoft, Apple, Mozilla, Google). Those programs are the actual product. A key-centric scheme has no place to install an anchor and no entity to audit; there is no CA/Browser Forum equivalent for "keys my friends signed." Ulrich et al.'s 240,283-component graph is what a trust fabric looks like without a root program.

**(e) X.509 removed the incentive to switch — twice.** Ellison and Schneier's "Ten Risks of PKI" (*Computer Security Journal* XVI(1), 2000) opens by naming the problem: "Certificates provide an attractive business model. They cost almost nothing to make, and if you can convince someone to buy a certificate each year for $5, that times the population of the Internet is a big yearly income." The decentralised systems had no replacement revenue model — but the CA rent was then destroyed *from inside X.509*, not from outside: **RFC 8555 (ACME, March 2019)** made issuance free and automatic, and **Certificate Transparency (RFC 6962, then RFC 9162, 2021)** supplied the accountability that "who do we trust, and for what?" demanded. X.509 also absorbed the delegation story: **RFC 3820 (June 2004, Tuecke et al., Proposed Standard)** gave grid computing restricted proxy certificates with `pCPathLenConstraint` limiting further delegation — SPKI's delegation bit and depth control, inside the incumbent format, on the standards track. Once the incumbent is free, automated, audited and delegating, the migration case evaporates.

## 9. Did tag intersection and delegation ever ship in production?

**SPKI's own machinery: essentially no.** What I could verify in production is the *encoding* — canonical S-expressions between GnuPG/Libgcrypt and Ribose's RNP, which is exactly why RFC 9804 exists. Academic implementations exist (MIT theses, the Wisconsin chain-discovery work, JSDSI); I found no verified mainstream product doing 5-tuple reduction with AIntersect and threshold subjects. The ESORICS 2006 authors, writing as SPKI's friends, say "limited deployment in the real world."

**The *idea* shipped, renamed and simplified.** Macaroons (Birgisson, Politz, Erlingsson, Taly, Vrable, Lentczner, NDSS 2014) use caveats that "attenuate and contextually confine" a credential, cite SPKI/SDSI as prior art, and *are* in production — Fly.io replaced its OAuth2 tokens with macaroons, with the guarantee that "adding caveats to a token can only ever weaken it," including third-party caveats (Ptacek, 31 January 2024). UCAN 1.0.0 (Zelenka) states outright: "SPKI/SDSI is closely related to UCAN. A different encoding format is used, and some details vary (such as a delegation-locking bit), but the core idea and general usage pattern are very close," and it requires DIDs as subjects and mandates that "each direct delegation MUST either directly restate or attenuate (diminish) its capabilities."

The pattern is consistent: **monotone attenuation survived; tag intersection as a general S-expression algebra did not.** Production systems adopt a linear caveat chain — each hop only ever narrows — because that is cheap to verify and easy to reason about, and drop SPKI's symmetric intersection lattice and K-of-N threshold subjects, which are expensive and need a path-discovery story nobody wanted to own.

---

# REFERENCES

`title | authors | year | venue | stable id`

1. OpenPGP | P. Wouters (Ed.), D. Huigens, J. Winter, Y. Niibe | 2024 | IETF, Proposed Standard (obsoletes RFC 4880, 5581, 6637) | RFC 9580 — https://www.rfc-editor.org/info/rfc9580
2. OpenPGP Message Format | J. Callas, L. Donnerhacke, H. Finney, D. Shaw, R. Thayer | 2007 | IETF, Proposed Standard (obsoleted by RFC 9580) | RFC 4880 — https://www.rfc-editor.org/info/rfc4880
3. SDSI — A Simple Distributed Security Infrastructure, version 1.1 | Ronald L. Rivest (MIT LCS), Butler Lampson (Microsoft) | 1996 (2 October) | Working document / MIT CSAIL | https://people.csail.mit.edu/rivest/pubs/RL96.ver-1.1.html
4. SPKI Requirements | C. Ellison | 1999 (September) | IETF, Experimental | RFC 2692 — https://www.rfc-editor.org/info/rfc2692
5. SPKI Certificate Theory | C. Ellison, B. Frantz, B. Lampson, R. Rivest, B. Thomas, T. Ylonen | 1999 (September) | IETF, Experimental | RFC 2693 — https://www.rfc-editor.org/info/rfc2693
6. Simple Public Key Certificate (draft-ietf-spki-cert-structure-05) | B. Lampson, T. Ylonen, R. Rivest, W. Frantz, C. Ellison, B. Thomas | 1998 (16 March) | IETF Internet-Draft, **expired, never published as RFC** | https://datatracker.ietf.org/doc/draft-ietf-spki-cert-structure/
7. Simple Public Key Infrastructure (SPKI) S-Expressions | Ronald L. Rivest (MIT CSAIL), Donald E. Eastlake 3rd | 2025 (June) | IETF, Informational | RFC 9804 — https://www.rfc-editor.org/info/rfc9804
8. Simple Public Key Infrastructure (spki) working group — charter and documents | chairs P. Metzger, S. Bellovin | charter last updated 2001-02-10; WG state "Concluded" | IETF Security Area | https://datatracker.ietf.org/wg/spki/about/ ; https://datatracker.ietf.org/doc/charter-ietf-spki/
9. Investigating the OpenPGP Web of Trust | Alexander Ulrich, Ralph Holz, Peter Hauck, Georg Carle | 2011 | ESORICS 2011, LNCS 6879, pp. 489–507 | doi:10.1007/978-3-642-23822-2_27
10. CVE-2019-13050 — SKS keyserver / GnuPG certificate spamming attack | — | 2019 | CVE / Red Hat advisory | https://access.redhat.com/articles/4264021
11. keys.openpgp.org FAQ (third-party certification policy) | keys.openpgp.org operators | accessed 2026-09-26 | service documentation | https://keys.openpgp.org/about/faq
12. GnuPG manual — OpenPGP Key Management (`tsign`, `--quick-tsign-key` trustspec `[T=]depth,value[,domain]`) | GnuPG project | accessed 2026-09-26 | software manual | https://www.gnupg.org/documentation/manuals/gnupg/OpenPGP-Key-Management.html
13. Ten Risks of PKI: What You're not Being Told about Public Key Infrastructure | Carl Ellison, Bruce Schneier | 2000 | Computer Security Journal, Volume XVI, Number 1 | https://www.schneier.com/academic/paperfiles/paper-pki.pdf
14. Reducing the Dependence of SPKI/SDSI on PKI | Hao Wang, Somesh Jha, Thomas Reps, Stefan Schwoon, Stuart Stubblebine | 2006 | ESORICS 2006 | doi:10.1007/11863908_11
15. Decentralized Identifiers (DIDs) v1.0 | M. Sporny, A. Guy, M. Sabadello, D. Reed (eds.) | 2022 (19 July) | W3C Recommendation | https://www.w3.org/TR/did-1.0/
16. Decentralized Identifiers (DIDs) v1.1 | M. Sporny, D. Zagidulin et al. (eds.) | 2026 (5 March) | W3C Candidate Recommendation Snapshot | https://www.w3.org/TR/did-1.1/
17. The did:key Method v0.9 | M. Sporny, D. Zagidulin, D. Longley (eds.) | draft, accessed 2026-09-26 | W3C CCG Draft Community Group Report | https://w3c-ccg.github.io/did-key-spec/
18. DID Extensions: Methods (registry) | W3C | 2026 (Group Note) | W3C Group Note | https://www.w3.org/TR/did-extensions-methods/
19. Names: Decentralized, Secure, Human-Meaningful: Choose Two | Zooko Wilcox-O'Hearn | 2001 | personal site (archived 20 Oct 2001) | https://web.archive.org/web/20011020191610/http://zooko.com/distnames.html (cited via https://en.wikipedia.org/wiki/Zooko%27s_triangle)
20. Zoom Acquires Keybase… | Zoom Video Communications | 2020 (7 May) | corporate press release / GlobeNewswire; $42.9M cash | https://blog.zoom.us/zoom-acquires-keybase-and-announces-goal-of-developing-the-most-broadly-used-enterprise-end-to-end-encryption-offering/
21. Macaroons: Cookies with Contextual Caveats for Decentralized Authorization in the Cloud | Arnar Birgisson, Joe Gibbs Politz, Úlfar Erlingsson, Ankur Taly, Michael Vrable, Mark Lentczner | 2014 | NDSS, Internet Society | https://research.google/pubs/macaroons-cookies-with-contextual-caveats-for-decentralized-authorization-in-the-cloud/
22. Macaroons Escalated Quickly | Thomas Ptacek | 2024 (31 January) | Fly.io engineering blog | https://fly.io/blog/macaroons-escalated-quickly/
23. User Controlled Authorization Network (UCAN) Specification v1.0.0 | Brooklyn Zelenka (ed.) | accessed 2026-09-26 | UCAN Working Group | https://github.com/ucan-wg/spec/blob/main/README.md
24. Internet X.509 Public Key Infrastructure (PKI) Proxy Certificate Profile | S. Tuecke, V. Welch, D. Engert, L. Pearlman, M. Thompson | 2004 (June) | IETF, Proposed Standard | RFC 3820 — https://www.rfc-editor.org/info/rfc3820
25. Automatic Certificate Management Environment (ACME) | R. Barnes, J. Hoffman-Andrews, D. McCarney, J. Kasten | 2019 (March) | IETF, Proposed Standard | RFC 8555 — https://www.rfc-editor.org/info/rfc8555
26. Certificate Transparency Version 2.0 | B. Laurie, E. Messeri, R. Stradling | 2021 | IETF, Experimental (obsoletes RFC 6962) | RFC 9162 — https://www.rfc-editor.org/info/rfc9162

---

# COULD NOT ESTABLISH

- **Exact conclusion date of the IETF SPKI working group.** Datatracker records WG state "Concluded" and charter state "Approved," last updated **2001-02-10**, but publishes no explicit conclusion date; secondary sources say only "around 2001." The 2001-02-10 timestamp should be cited as *charter last-updated*, not as the conclusion date.
- **DOIs for RFC 9580 and RFC 9804.** The rfc-editor info pages I fetched did not display them. RFC DOIs follow the `10.17487/RFCxxxx` pattern, but I did not verify these two specifically — cite by RFC number/URL.
- **HP eSpeak's use of SPKI certificates for delegated access control.** This appeared in a search summary but Carl Ellison's primary page (`theworld.com/~cme/html/spki.html`) is no longer resolvable, and I found no citable primary source. **Do not use this claim without an independent source** — it is the single most-repeated "SPKI shipped somewhere" assertion and I could not substantiate it.
- **Whether UCAN is genuinely in production at Storacha/web3.storage.** The documentation URL 301-redirects to `fil.one`, whose page makes no mention of UCAN, DIDs, delegation or attenuation. Fly.io's macaroon use is the one production attenuation deployment I verified directly.
- **Adoption rate of OpenPGP trust signatures.** Ulrich et al. (2011) measure the signature graph but report no figure for how many keys carry type-5 Trust Signature subpackets or regex scoping. I found no study that measures this. The argument in §2 rests on spec/tooling analysis plus the graph data, not on a direct measurement of tsign usage.
- **Verbatim text of Zooko's 2001 post.** `web.archive.org` is blocked in this environment; the title, date and formulation are taken from the Wikipedia article's citation of the archived page. Verify against the archive before quoting.
- **Current Let's Encrypt headline figures** (active certificates / FQDNs). The stats page (last updated 24 Sept 2026) renders its numbers client-side and returned no figures. §8(e)'s argument does not depend on a specific number, but if the survey wants one, it needs a separate source.
- **Whether any browser or operating system ever shipped SPKI/SDSI certificate validation.** I found no evidence either way; I assert only the absence of a trust-anchor installation path, which follows from the format never being standardised. Phrased as "no path to integration" rather than "was rejected by vendors."
- **DID v1.1's status as of today (2026-09-26).** Verified only as a Candidate Recommendation Snapshot dated 5 March 2026, with the note that it was not expected to advance before 5 April 2026; `https://www.w3.org/TR/did/` still resolves to the 1.0 Recommendation of 19 July 2022. Whether 1.1 has since become a Recommendation is unconfirmed.

*(Report body: ~1,470 words.)*

Note on method: the WebSearch budget for this session was exhausted (200/200) partway through; the remaining verification was done by direct WebFetch and by downloading and parsing RFC/paper text locally. All RFC facts above come from the fetched RFC text itself, not from search summaries.
