# Area G — Capability Tokens and Delegation

## 1. Background: designation fused with authority

The capability model dates to Dennis and Van Horn's *Programming Semantics for Multiprogrammed Computations* (CACM 9(3), 1966), which introduced the C-list: a per-computation "sphere of protection" in which naming an object and being permitted to use it are the same act. Hardy's *The Confused Deputy (or why capabilities might have been invented)* (SIGOPS OSR 22(4), 1988) supplies the negative argument. A compiler at Tymshare, invoked with a user-supplied output path, wrote to a billing file it alone had rights to; the caller designated the target, the deputy supplied the authority, and the two came from different places. Capabilities close that gap by refusing to separate them. This is the through-line for everything below: a bearer token that says "the holder may do X" but not "on this object, for this request" is a confused-deputy generator.

## 2. Macaroons

Birgisson, Politz, Erlingsson, Taly, Vrable and Lentczner, NDSS 2014. A macaroon is minted at a target service from a high-entropy root key; its signature is a nested chain of HMACs, each value keyed by the previous one. Anyone holding the macaroon can append a *caveat* and re-chain the HMAC, producing a strictly narrower credential without contacting the issuer. **First-party caveats** are predicates the target evaluates directly against request context (`time < ...`, `operation == read`). **Third-party caveats** embed a caveat root key and a predicate encrypted for another service; the holder must obtain a *discharge macaroon* from that service and present it alongside. This is how macaroons get holder-of-key and federated attributes without public-key crypto.

The weakness is structural and the authors state it plainly: "the verification of an HMAC-based macaroon requires knowledge of its root key—and since this key confers the ability to arbitrarily modify the macaroon and its caveats, it cannot be widely shared." Every verifier is a forger. Macaroons are also not third-party-auditable: you cannot hand a chain to a log or a regulator and have it check out. The paper does claim macaroons are at least as expressive as SPKI/SDSI (via Li–Mitchell semantics, SPKI delegation reduced to third-party caveats for conjunctive holder-of-key assertions), but concedes the proof shows only that "symmetric cryptography and enough extra messages can emulate public-key-based mechanisms."

## 3. Biscuit

Biscuit (spec v3.3, now under Eclipse) fixes the symmetry. A token is an append-only sequence of signed blocks: each block carries serialized Datalog, a next public key, and a signature by the previous private key. The holder keeps the final private key to attenuate further, or seals the token with a final signature. Verification needs only the root **public** key. The authority block holds rights as facts and rules; later blocks add *checks*. Scoping rules do the security work: a block's rules see facts from the authority block, its own block, and the authorizer only — so a later block adding `right("file2","read")` cannot make an earlier check pass. Third-party blocks let an external signer contribute content with an isolated symbol table.

## 4. UCAN and ZCAP-LD

UCAN (1.0; editors Zelenka et al., with Gozalishvili, Holmgren, Krüger) names principals by DID (`did:key`) and chains delegations by reference, each either restating or attenuating the parent's capabilities; hierarchical command paths give containment (`/crypto` proves `/crypto/sign`, not `/stack/pop`). 1.0 canonically signs DAG-CBOR envelopes and splits delegation from invocation; the widely-deployed 0.x line nested JWTs. The recurring criticisms are DID-method complexity (resolution, rotation, revocation all become someone else's problem) and size: nested-JWT UCANs re-base64 the whole parent at each hop, which the 2026 AIP paper characterizes as quadratic growth in delegation depth, against macaroons' linear caveat append.

ZCAP-LD / ZCAP (W3C CCG work item, v0.4.0-rc.6, still a draft — not a W3C Recommendation) expresses the same idea in JSON-LD with Data Integrity proofs: `parentCapability` chains, `capabilityInvocation` proof purpose, `allowedAction` and path/query attenuation, mandatory expiry on delegations. Each capability in the chain inherits the caveats of its predecessors; a verifier must confirm a child's `allowedAction` is not less restrictive than its parent's.

## 5. OAuth/JWT and proof-of-possession, for contrast

RFC 6749 (Hardt, 2012) defines an access token as an opaque string; RFC 6750 defines *bearer* as "any party in possession of the token can use the token in any way that any other party in possession of it can." RFC 9068 (Bertocci, 2021) standardizes the JWT profile for those access tokens. Critically, RFC 6749 §3.3 gives the client no power to narrow: the authorization server "MAY fully or partially ignore the scope requested by the client." OAuth's delegation primitive is **re-issuance by an authority**, not holder-side attenuation — the opposite design point. RFC 9396 (Lodderstedt, Richer, Campbell, 2023) adds structured `authorization_details`, which is what the agentic drafts reach for.

Proof-of-possession narrows *who may present*, not *what is authorized*: RFC 7800 (Jones, Bradley, Tschofenig, 2016) defines the `cnf` claim for JWTs, RFC 8747 (2020) ports it to CWT, and RFC 9449 DPoP (Fett et al., 2023) binds tokens to a client key via per-request signatures. These are orthogonal axes — PoP de-bearers a token; attenuation shrinks it. Biscuit and macaroons attenuate without PoP; DPoP does PoP without attenuation.

## 6. Agentic delegation, 2026

Three active individual Internet-Drafts, all verified on datatracker:
- **draft-niyikiza-oauth-attenuating-agent-tokens-01** (Niki Aimable, Tenuo, 2026-06-15) — Attenuating Authorization Tokens: RFC 9396 RAR profiled for tool-level capabilities, offline holder-side derivation, chain verified against a root trust anchor. Cites macaroons, Biscuit, Dennis 1966 and Miller 2006 — **not** SPKI, not UCAN.
- **draft-asor-wimse-agent-delegation-chain-01** (Rafael Asor, Attenu, 2026-09-03) — JWT/RAR tokens, each hop cryptographically linked, offline monotonic-decrease check. Cites SPKI as a "historical standards-track ancestor."
- **draft-hamr-oauth-agent-delegation-02** (Amr Hassan, 2026-09-19) — an `Agent-Delegation` header over RFC 9421 HTTP Message Signatures; explicitly does not define credential formats, identity systems, or revocation.

## 7. The analytical core: intersection vs. accumulation

SPKI (RFC 2693; Ellison, Frantz, Lampson, Rivest, Thomas, Ylonen, 1999) does something none of these do. Its §6.3 reduction rule is
`<I1,S1,D1,A1,V1> + <I2,S2,D2,A2,V2> → <I1,S2,D2,AIntersect(A1,A2),VIntersect(V1,V2)>`
(valid when S1 = I2 and D1 = TRUE). `AIntersect` is a **closed binary operation on authorization tags**: the intersection of two authorizations is itself an authorization of the same kind, computed element-wise over `(*)`, `(* set ...)`, `(* prefix ...)`, `(* range ...)` forms — e.g. `(tag (* set read write (foo bla) delete)) ∩ (tag (* set write read)) = (tag (* set read write))`. Two consequences follow: authority forms a meet-semilattice with a computable meet, and a chain of N certificates **reduces to a single 5-tuple**. The chain is evidence, not payload.

**Nothing in the modern family does this.** Every one of them accumulates and then checks containment:

| System | Attenuation op | Verification |
|---|---|---|
| Macaroons | append caveat, re-chain HMAC | evaluate conjunction of predicates against request |
| Biscuit | append signed block of Datalog checks | run all checks + authorizer allow/deny policies |
| UCAN | new delegation referencing parent proof | command-path containment at execution |
| ZCAP | new zcap with `parentCapability` | child's `allowedAction` ⊆ parent's, caveats inherited |
| AAT draft | derive token with narrower constraint map | normative `subsumes` per constraint type |
| draft-asor | new hop | `C ≤ P`: scope covered, bounds tighter, `C.exp ≤ P.exp`, depth ≤ |

The AAT draft comes closest and is worth singling out, because it independently reinvents most of SPKI's tag algebra. Its constraint vocabulary — `exact`, `range`, `one_of`, `not_one_of`, `contains`, `subset`, `wildcard`, `all`, `any` — is close to isomorphic to SPKI's `*`-forms, and it imposes a decidability requirement on extensions ("MUST terminate in finite time... MUST NOT require solving problems that are undecidable or computationally intractable"). But its normative primitive is `subsumes(C, P)` — a **decision procedure** answering "is the child within the parent?" — not a **meet** computing `C ⊓ P`. The partial order is there; the lattice operation is not exposed. That is a real, implementable gap: on that constraint fragment the meet is computable, and computing it would let a chain collapse to one normalized token. Same for draft-asor's `C ≤ P`.

Why did the field abandon intersection? Not oversight — a semantic shift. SPKI tags describe a *static permission space*, closed under meet. Macaroon-style caveats describe a *dynamic admissibility predicate over request context*: `time < T`, `ip = ...`, or a third-party discharge obligation. You cannot intersect "holder proves membership in group G at service A" into a tag, because it is not a tag; it is deferred evidence. Once caveats are arbitrary predicates, the meet degenerates to conjunction, and conjunction has no normal form. Biscuit makes this maximally explicit: a Datalog program's authority is only ever defined extensionally, relative to an authorizer's facts. You can ask "is this request permitted?" but not "what does this token authorize?" — a question SPKI could answer in closed form. The price is paid in size (monotone growth — quadratic for nested-JWT UCANs, linear for macaroons, versus SPKI's compression to a single tuple) and in static analysis (no offline "is token A weaker than token B?" without a solver).

## 8. Naming: feature or gap?

These systems delegate to keys and mostly decline to say who the keys are. Macaroons and Biscuit name no subject at all — they are bearer credentials whose "principal" is whoever holds the bytes. UCAN and ZCAP do name principals (DIDs, controller URLs), and that is precisely where they take the most criticism. The 2026 drafts bind hops by key and proof-of-possession while explicitly disclaiming identity: draft-hamr says outright it "does not define credential formats, identity systems, or revocation."

The case for it being a feature is strong and is the original argument: the confused deputy is fixed by designating authority *with* the request, not by asking the deputy "who are you." Unnamed keys also give privacy (no correlatable identifier), offline verification (no name-resolution round trip), and clean composition.

The case for it being a gap is that four things the deployed world wants all turn out to be naming problems in disguise. **Revocation**: you cannot revoke an authority you cannot name — hence status lists, short expiries, and Biscuit's sealing as workarounds. **Rotation**: a key is not a stable identity. **Accountability and audit**: the entire 2026 agentic literature is about *delegation provenance* — showing an auditor which human sits at the root of a chain — and a chain of ephemeral `did:key`s and single-use Ed25519 block keys cannot answer that. **Organizational policy**: "anyone in group G" is inexpressible over raw keys; macaroons smuggle it back in via third-party caveats, Biscuit via authorizer-supplied facts.

SPKI, again, had the better architecture and it is the piece the field dropped. RFC 2693 is *two* systems: 5-tuples carrying authorizations over keys, and SDSI 4-tuple **name certificates** — `(name (hash sha1 |TLCg...|) jim)` — resolving locally-meaningful names to keys, with names usable as subjects in authorization tuples. Two layers: names resolve to keys, keys hold authority, and neither is required to do the other's job. Macaroons, Biscuit, and the agent drafts collapsed to one layer and are now rediscovering, under the banner of provenance, that they need the second. My assessment for the survey: the omission is an *unbundling*, not a flaw in the capability model — but it is an unbundling the ecosystem has not re-bundled, and the 2026 agentic drafts are where the bill is coming due.

---

# REFERENCES

`title | authors | year | venue | stable id`

- Programming semantics for multiprogrammed computations | Jack B. Dennis, Earl C. Van Horn (MIT) | 1966 | Communications of the ACM 9(3):143–155 | doi:10.1145/365230.365252
- The Confused Deputy (or why capabilities might have been invented) | Norm Hardy | 1988 | ACM SIGOPS Operating Systems Review 22(4):36–38 | doi:10.1145/54289.871709
- SPKI Certificate Theory | C. Ellison, B. Frantz, B. Lampson, R. Rivest, B. Thomas, T. Ylonen | 1999 (Sept) | IETF RFC 2693 (Experimental) | RFC 2693
- Macaroons: Cookies with Contextual Caveats for Decentralized Authorization in the Cloud | Arnar Birgisson (Chalmers), Joe Gibbs Politz (Brown), Úlfar Erlingsson, Ankur Taly, Michael Vrable, Mark Lentczner (Google) | 2014 (22 Feb) | NDSS Symposium 2014 | https://www.ndss-symposium.org/ndss2014/ndss-2014-programme/macaroons-cookies-contextual-caveats-decentralized-authorization-cloud/ (PDF: https://theory.stanford.edu/~ataly/Papers/macaroons.pdf)
- Biscuit Specification v3.3 | Eclipse Biscuit project (contributors; see repo) | 2024–2026 (living) | Eclipse Foundation / project specification | https://doc.biscuitsec.org/reference/specifications.html ; https://github.com/eclipse-biscuit/biscuit/blob/master/SPECIFICATIONS.md
- UCAN Specification v1.0.0 | Editor: Brooklyn Zelenka (Witchcraft Software); Authors: Irakli Gozalishvili, Daniel Holmgren, Philipp Krüger, Brooklyn Zelenka | 2024 (v1.0.0) | UCAN Working Group specification | https://github.com/ucan-wg/spec
- Authorization Capabilities (ZCAP / ZCAP-LD) v0.4.0-rc.6 | W3C Credentials Community Group (editors not listed on the fetched rendering; v0.3 attributed in secondary sources to C. Lemmer-Webber, M. Sporny, M. S. Miller) | v0.3 2022/2023; v0.4.0-rc.6 current draft | W3C CCG draft work item (not a W3C Recommendation) | https://w3c-ccg.github.io/zcap-spec/
- The OAuth 2.0 Authorization Framework | D. Hardt (Ed.), Microsoft | 2012 (Oct) | IETF RFC 6749 (Standards Track) | RFC 6749
- The OAuth 2.0 Authorization Framework: Bearer Token Usage | M. Jones (Microsoft), D. Hardt | 2012 (Oct) | IETF RFC 6750 (Standards Track) | RFC 6750
- JSON Web Token (JWT) Profile for OAuth 2.0 Access Tokens | Vittorio Bertocci (Auth0) | 2021 (Oct) | IETF RFC 9068 (Standards Track) | RFC 9068
- OAuth 2.0 Rich Authorization Requests | T. Lodderstedt (yes.com), J. Richer (Bespoke Engineering), B. Campbell (Ping Identity) | 2023 (May) | IETF RFC 9396 (Standards Track) | RFC 9396
- Proof-of-Possession Key Semantics for JSON Web Tokens (JWTs) | M. Jones (Microsoft), J. Bradley (Ping Identity), H. Tschofenig (ARM) | 2016 (Apr) | IETF RFC 7800 (Standards Track) | RFC 7800
- Proof-of-Possession Key Semantics for CBOR Web Tokens (CWTs) | M. Jones (Microsoft), L. Seitz (Combitech), G. Selander (Ericsson), S. Erdtman (Spotify), H. Tschofenig (Arm) | 2020 (Mar) | IETF RFC 8747 (Standards Track) | RFC 8747
- OAuth 2.0 Demonstrating Proof of Possession (DPoP) | D. Fett (Authlete), B. Campbell (Ping Identity), J. Bradley (Yubico), T. Lodderstedt (Tuconic), M. Jones (Self-Issued Consulting), D. Waite (Ping Identity) | 2023 (Sept) | IETF RFC 9449 (Standards Track) | RFC 9449
- Attenuating Authorization Tokens for Agentic Delegation Chains | Niki Aimable (Tenuo) | 2026-06-15 (v-01; expires 2026-12-17) | IETF Internet-Draft, individual submission | draft-niyikiza-oauth-attenuating-agent-tokens-01
- Verifiable Attenuated Delegation for AI Agent Chains | Rafael Asor (Attenu) | 2026-09-03 (v-01) | IETF Internet-Draft, individual submission (WIMSE-adjacent, no WG adoption) | draft-asor-wimse-agent-delegation-chain-01
- An Attenuated Delegation Profile for Automated Agents | Amr Hassan (Independent) | 2026-09-19 (v-02) | IETF Internet-Draft, individual submission | draft-hamr-oauth-agent-delegation-02
- AIP: Agent Identity Protocol for Verifiable Delegation Across MCP and A2A | Sunil Prakash | 2026-03-25 | arXiv preprint (not peer-reviewed) | arXiv:2603.24775
- CAPMAS: Capability-Based Delegation of Privileges in Multi-Agent Systems | Rasmus Moorits Veski, Rachid Guerraoui, David Froelicher | 2026-09-06 | arXiv preprint (not peer-reviewed) | arXiv:2609.06500

Supporting RFCs mentioned in passing: RFC 9421 (HTTP Message Signatures), cited by draft-hamr — not independently verified in this pass.

---

# COULD NOT ESTABLISH

1. **Mark S. Miller, *Robust Composition* (2006).** Cited secondhand — draft-niyikiza §1.3 lists "capability-based security (Dennis 1966, Miller 2006)". I could not fetch the thesis itself: erights.org and combex.com both refused connections during this session. Full citation (Johns Hopkins University PhD thesis, 2006) is from memory and should be re-verified before use.
2. **Miller, Yee, Shapiro, "Capability Myths Demolished."** Standard reference for object-capability vs. ACL comparison and the confused-deputy analysis. Host `srl.cs.jhu.edu` no longer resolves (DNS failure), and the session's web-search budget (200 calls) was exhausted before I could find a mirror. Year (2003) and report series (SRL2003-02) are unverified.
3. **Macaroons DOI.** NDSS Symposium papers carry no DOI. The stable identifiers are the NDSS programme page and the authors' PDF, both listed above.
4. **ZCAP editors and date for v0.4.0-rc.6.** The rendered spec page I fetched did not list editors or a publication date. A search snippet attributed v0.3 to Lemmer-Webber, Sporny and M. S. Miller with date 2023-01-22, but I could not confirm this from the document itself. Also note ZCAP has *never* been a W3C Recommendation — it is a CCG work item, and the survey should say so.
5. **Biscuit authorship/provenance.** The specification site names no individual authors and does not state the originating organization. The project is now under Eclipse; secondary sources attribute its origin to Clever Cloud, which I could not confirm from a primary source.
6. **draft-asor's treatment of subject identity.** My claim that it does not mention DIDs, SPIFFE or workload identity rests on a single summarization pass over the draft HTML, not a full read. Given it is a WIMSE-adjacent draft using proof-of-possession, treat "binds hops to keys but defines no naming layer" as the defensible statement and re-read §§1–4 before asserting the stronger version.
7. **UCAN quadratic token growth.** Sourced to Prakash 2026 (arXiv:2603.24775), a non-peer-reviewed preprint, as a secondary claim. I found no independent measurement, and the growth characteristic differs between UCAN 0.x (nested JWT, the version the criticism targets) and UCAN 1.0 (DAG-CBOR envelopes with CID-referenced proofs, which should be linear). The survey should scope the criticism to 0.x explicitly.
8. **Whether any deployed system computes a true meet.** I checked macaroons, Biscuit, UCAN, ZCAP, and all three 2026 drafts, and found only containment/subsumption checking. I did not exhaustively survey every capability token system (e.g. Tahoe-LAFS, Waterken, CapBAC/ACE-OAuth, Google's internal successors), so "nothing does intersection" should be stated as "none of the systems surveyed here," not as a universal claim.
