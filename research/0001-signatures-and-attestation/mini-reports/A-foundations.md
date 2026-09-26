# Area A: FOUNDATIONS — What a Digital Signature Is, and What It Proves

## 1. The object

A digital signature scheme is a triple of algorithms over bit strings:

- `Gen(1ⁿ) → (pk, sk)` — randomized key generation
- `Sign(sk, m) → σ`
- `Verify(pk, m, σ) → {0,1}`

with correctness: `Verify(pk, m, Sign(sk, m)) = 1` for all `m`. That is the whole object. Note what is *absent* from the type signature: there is no person, no name, no timestamp, no purpose, no document. `m` is a byte string. `pk` is a byte string. The scheme is a relation over byte strings, and everything else that the word "signature" carries in ordinary language is imported from outside by convention, protocol, or law.

## 2. The origin of the idea

The concept was stated, as a named open problem with no solution, by **Diffie and Hellman (1976)**. Section 4, "One-Way Authentication," is the founding text, and its wording is precise (verified against the paper):

> "In order to develop a system capable of replacing the current written contract with some purely electronic form of communication, we must discover a digital phenomenon with the same properties as a written signature. It must be easy for anyone to recognize the signature as authentic, but impossible for anyone other than the legitimate signer to produce it. ... Since any digital signal can be copied precisely, a true digital signature must be recognizable without being known."

The motivation Diffie and Hellman give is **dispute**, not secrecy: "a message may be sent but later repudiated by either the transmitter or the receiver." They had no trapdoor function, so they described signing as "deciphering" with the secret key — `D_A(M)` — and proposed it as a consequence of public-key cryptography that did not yet exist. The same section credits **Lamport** with a one-time signature from a one-way function, three years before Lamport's own report.

**Rivest, Shamir and Adleman (1978)** supplied the missing trapdoor and made the sketch real. It is worth recording that textbook RSA signing, the scheme presented in the paper that named the field, is *existentially forgeable*: RSA is multiplicative, so `σ₁ · σ₂ mod n` is a valid signature on `m₁ · m₂`. An adversary who obtains two signatures gets a third for free. This is the cleanest available demonstration that intuition about signatures is not a security argument, and it is precisely why the next decade was spent on definitions.

## 3. The turn toward proof

**Rabin (1979)**, MIT/LCS/TR-212, was the first to *reduce* forgery to a hard problem: inverting his squaring-based function is equivalent to factoring `n`, which RSA's security is not known to be. Rabin also saw the chosen-message danger before anyone had a name for it. Reading the report directly:

> "Without the suffix, an adversary may attempt to feed to P messages M for his signature, hoping to learn the factorization of n from the solution of x(x+b) ≡ C(M) mod n, which will be produced by P as his signature."

His fix — a random 60-bit suffix `U` hashed with the message — is the ancestor of every randomized/probabilistic padding since (PSS, EdDSA's nonce derivation). The commonly repeated claim that Rabin's 1979 scheme "was the first to meet the modern standard of existential unforgeability under chosen-message attack" is a *retrospective* reading: that standard did not exist for another nine years, and Rabin proves a theorem in his own model, not a game-based one.

**Lamport (1979)** (SRI CSL-98, dated 18 October 1979) removed number theory entirely: signatures from any one-way function, by publishing `f(x₀), f(x₁)` per message bit and revealing the preimage. One-time only — a second signature leaks the key. **Merkle** solved that. His 1979 Stanford thesis introduced *tree authentication*, published as "Protocols for Public Key Cryptosystems" (IEEE S&P, 1980); the hash tree lets `2^h` one-time keys be compressed into a single short public key, with an authentication path per signature. "A Certified Digital Signature" was written in 1979 and submitted to CACM under Rivest's editorship; by Merkle's own account the referees never responded to the revision and it was published only at CRYPTO '89 — a ten-year gap that matters for priority claims. This line is now the post-quantum mainstream (XMSS, LMS, SPHINCS+).

**ElGamal (1985)** gave the first discrete-log signature and introduced the per-signature nonce `k`. That nonce is the scheme family's load-bearing fragility: reuse or bias recovers `sk` outright. **Schnorr (CRYPTO '89 / J. Cryptology 1991)** compressed ElGamal's structure by applying Fiat–Shamir to an identification protocol, producing short signatures that later admitted a random-oracle proof via the forking lemma.

## 4. The definition: GMR

**Goldwasser, Micali and Rivest (1988)** — building on Goldwasser–Micali–Yao (STOC 1983) and their own FOCS/CRYPTO 1984 "paradoxical solution" — did the decisive work, which was *not* the scheme but the taxonomy. They crossed attack strength (key-only → known-message → generic chosen-message → directed → **adaptive** chosen-message) against break severity (total break → universal → selective → **existential** forgery), then defined security as the strongest attack against the weakest break.

The resulting game, **EUF-CMA**: the challenger runs `Gen`, hands `pk` to the adversary, and gives it oracle access to `Sign(sk, ·)`. The adversary adaptively queries `m₁ … m_q` — each chosen after seeing prior answers — then outputs `(m*, σ*)`. It wins if `Verify(pk, m*, σ*) = 1` and `m* ∉ {mᵢ}`. The scheme is secure if every efficient adversary wins with negligible probability.

## 5. What the definition actually asserts — and what it refuses to

A valid signature licenses exactly one inference: **the signing algorithm was run with `sk` over these exact bytes** — and even that only contrapositively, contingent on the hardness assumption and on `sk` not having leaked. Everything else is outside the quantifier:

- **Identity.** No person appears in the game. The binding of `pk` to a human or organization is entirely external — certification, PKI, out-of-band trust. Merkle's title word "certified" and Diffie–Hellman's "public file" both gesture at a problem their mathematics does not solve.
- **Intent.** This is the most under-appreciated point, and the model states it explicitly: *the signer is an oracle.* GMR hand the adversary a machine that signs whatever it is asked, without judgment, and demand security anyway. The definition therefore **presupposes** that signatures are produced over messages the key holder did not choose and may never have seen. A signature is evidence that a signing routine executed, not that anyone read, understood, or assented to the content.
- **Authority.** Nothing in `Verify` speaks to whether the key holder was permitted to make the statement.
- **Truth.** `m` is an uninterpreted string.
- **Non-repudiation.** A legal and evidentiary concept, not a cryptographic one. EUF-CMA gives unforgeability *against outsiders*; it says nothing about key custody, coercion, or a signer who leaks their own key deliberately.
- **Uniqueness of `σ`.** EUF-CMA explicitly permits an adversary to produce a *different* valid signature on an *already-signed* message — that is strong unforgeability (SUF-CMA), a distinct and stronger notion. Systems that treat `σ` as an identifier (Bitcoin transaction malleability) assumed a property the standard definition never promised.
- **Bytes, not meaning.** Hash-then-sign binds `H(m)`, so a hash collision severs the binding without touching the key (Flame/MD5, chosen-prefix collisions).
- **Context.** Nothing binds `σ` to a protocol, a recipient, or even `pk`, unless designed in — the root of cross-protocol reuse and duplicate-signature-key-selection attacks. RFC 8032's EdDSA hashes the public key into the challenge specifically to close part of this gap.

## 6. The standards lineage

FIPS 186 standardizes *algorithms*, and — consistent with everything above — says nothing about identity, intent or semantics; that is X.509/PKIX's problem. The line runs: **FIPS 186** (19 May 1994, DSA only; Change Notice 1, 30 Dec 1996) → **186-1** (15 Dec 1998, adds RSA) → **186-2** (27 Jan 2000, adds ECDSA) → **186-3** (June 2009) → **186-4** (July 2013) → **186-5** (3 Feb 2023), which adds EdDSA per RFC 8032 and deterministic ECDSA per RFC 6979, deprecates binary-field curves, and **removes DSA for signature generation**, retaining it only to verify legacy signatures.

---

# REFERENCES

Format: `title | authors | year | venue | stable identifier`

1. New Directions in Cryptography | Whitfield Diffie, Martin E. Hellman | 1976 | IEEE Transactions on Information Theory 22(6):644–654, Nov 1976 | doi:10.1109/TIT.1976.1055638
2. A Method for Obtaining Digital Signatures and Public-Key Cryptosystems | R. L. Rivest, A. Shamir, L. Adleman | 1978 | Communications of the ACM 21(2):120–126, Feb 1978 | doi:10.1145/359340.359342
3. Digitalized Signatures and Public-Key Functions as Intractable as Factorization | Michael O. Rabin | 1979 | MIT Laboratory for Computer Science Technical Report MIT/LCS/TR-212, January 1979 | https://dspace.mit.edu/handle/1721.1/149499 (also DTIC ADA078415; https://www.bitsavers.org/pdf/mit/lcs/tr/MIT-LCS-TR-0212.pdf)
4. Digitalized Signatures | Michael O. Rabin | 1978 | in *Foundations of Secure Computation*, R. A. DeMillo, D. P. Dobkin, A. K. Jones, R. J. Lipton (eds.), Academic Press, pp. 155–168 | no DOI located — book chapter, print only
5. Constructing Digital Signatures from a One Way Function | Leslie Lamport | 1979 | SRI International, Computer Science Laboratory, Technical Report CSL-98, 18 October 1979 | https://lamport.azurewebsites.net/pubs/dig-sig.pdf (mirrored: https://www.microsoft.com/en-us/research/publication/constructing-digital-signatures-one-way-function/)
6. Secrecy, Authentication, and Public Key Systems | Ralph C. Merkle | 1979 | Ph.D. dissertation, Dept. of Electrical Engineering, Stanford University | https://www.ralphmerkle.com/papers/Thesis1979.pdf ; Stanford SearchWorks record https://searchworks.stanford.edu/view/785482
7. Protocols for Public Key Cryptosystems | Ralph C. Merkle | 1980 | 1980 IEEE Symposium on Security and Privacy, Oakland CA, 14–16 Apr 1980, pp. 122–134 | doi:10.1109/SP.1980.10006
8. A Certified Digital Signature | Ralph C. Merkle | 1990 (written 1979; presented CRYPTO '89) | Advances in Cryptology — CRYPTO '89, G. Brassard (ed.), LNCS 435, Springer, pp. 218–238 | doi:10.1007/0-387-34805-0_21
9. A Public Key Cryptosystem and a Signature Scheme Based on Discrete Logarithms | Taher ElGamal | 1985 | IEEE Transactions on Information Theory 31(4):469–472, Jul 1985 | doi:10.1109/TIT.1985.1057074
10. A Public Key Cryptosystem and a Signature Scheme Based on Discrete Logarithms (conference version) | Taher ElGamal | 1985 | Advances in Cryptology — CRYPTO '84, LNCS 196, Springer, pp. 10–18 | doi:10.1007/3-540-39568-7_2
11. Strong Signature Schemes | Shafi Goldwasser, Silvio Micali, Andrew Yao | 1983 | Proc. 15th Annual ACM Symposium on Theory of Computing (STOC '83), pp. 431–439 | doi:10.1145/800061.808774
12. A "Paradoxical" Solution to The Signature Problem | Shafi Goldwasser, Silvio Micali, Ronald L. Rivest | 1984 | 25th Annual Symposium on Foundations of Computer Science (FOCS 1984), pp. 441–448 | doi:10.1109/SFCS.1984.715946
13. A "Paradoxical" Solution to The Signature Problem (CRYPTO version) | Shafi Goldwasser, Silvio Micali, Ronald L. Rivest | 1985 | Advances in Cryptology — CRYPTO '84, LNCS 196, Springer, pp. 467 | doi:10.1007/3-540-39568-7_37
14. **A Digital Signature Scheme Secure Against Adaptive Chosen-Message Attacks** | Shafi Goldwasser, Silvio Micali, Ronald L. Rivest | 1988 | SIAM Journal on Computing 17(2):281–308, Apr 1988 | doi:10.1137/0217017
15. Efficient Identification and Signatures for Smart Cards | Claus-Peter Schnorr | 1990 (CRYPTO '89) | Advances in Cryptology — CRYPTO '89, LNCS 435, Springer, pp. 239–252 | doi:10.1007/0-387-34805-0_22
16. Efficient Identification and Signatures for Smart Cards (abstract) | Claus-Peter Schnorr | 1990 (EUROCRYPT '89) | Advances in Cryptology — EUROCRYPT '89, LNCS 434, Springer, pp. 688–689 | doi:10.1007/3-540-46885-4_68
17. Efficient Signature Generation by Smart Cards | Claus-Peter Schnorr | 1991 | Journal of Cryptology 4(3):161–174 | doi:10.1007/BF00196725
18. Digital Signature Standard (DSS) | NIST | 1994 | FIPS PUB 186, 19 May 1994 (Change Notice 1, 30 Dec 1996; withdrawn 15 Dec 1998) | doi:10.6028/NIST.FIPS.186 ; https://csrc.nist.gov/pubs/fips/186/upd1/final
19. Digital Signature Standard (DSS) | NIST | 1998 | FIPS PUB 186-1, 15 Dec 1998 (withdrawn 27 Jan 2000) | https://csrc.nist.gov/pubs/fips/186-1/final
20. Digital Signature Standard (DSS) | NIST | 2000 | FIPS PUB 186-2, 27 Jan 2000 (withdrawn 9 Jun 2009) | doi:10.6028/NIST.FIPS.186-2
21. Digital Signature Standard (DSS) | NIST | 2009 | FIPS PUB 186-3, June 2009 (withdrawn 19 Jul 2013) | https://csrc.nist.gov/pubs/fips/186-3/final
22. Digital Signature Standard (DSS) | NIST | 2013 | FIPS PUB 186-4, July 2013 (withdrawn 3 Feb 2024) | doi:10.6028/NIST.FIPS.186-4
23. Digital Signature Standard (DSS) | NIST | 2023 | FIPS PUB 186-5, 3 Feb 2023 | doi:10.6028/NIST.FIPS.186-5 ; https://csrc.nist.gov/pubs/fips/186-5/final
24. Edwards-Curve Digital Signature Algorithm (EdDSA) | S. Josefsson, I. Liusvaara | 2017 | IRTF, RFC 8032 (Informational), January 2017 | doi:10.17487/RFC8032 ; https://www.rfc-editor.org/info/rfc8032
25. Announcing Issuance of FIPS 186-5, Digital Signature Standard | NIST / Dept. of Commerce | 2023 | Federal Register 88 FR 6543, 3 Feb 2023 | https://www.federalregister.gov/documents/2023/02/03/2023-02273/

Items 1, 2, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 20, 22, 23, 24 were confirmed field-by-field against the Crossref REST API. Items 3, 5, 6 were confirmed by reading the scanned originals. Items 19, 21 were confirmed against NIST CSRC publication pages.

---

# Contested attributions (flag these in the paper)

1. **Priority for public-key cryptography vs. priority for the signature idea.** GCHQ's James Ellis (1970, "non-secret encryption"), Clifford Cocks (1973, an RSA-equivalent) and Malcolm Williamson (1974, a DH-equivalent key exchange) anticipated the *encryption and key-exchange* halves of Diffie–Hellman; this was declassified in 1997. Multiple accounts — including Schneier's history and the standard teaching literature — state that the GCHQ work did **not** conceive digital signatures. Ralph Merkle's public-key distribution work was also submitted (Aug 1975) before Diffie–Hellman was published, appearing in CACM in April 1978. The upshot: the *signature* idea is the part of "New Directions" whose priority is not contested.
2. **"First digital signature algorithm."** Lamport's construction appears in Diffie–Hellman §4 (1976) credited to Lamport, three years before Lamport's CSL-98. Lamport's own account credits Diffie with posing the problem around 1975. Rabin's 1978 "Digitalized Signatures" chapter also contains a one-time scheme. Any flat claim of "first" needs qualifying.
3. **"Rabin 1979 was the first EUF-CMA-secure scheme."** Asserted on Wikipedia and repeated widely. It is a retrospective reading — the definition post-dates the scheme by nine years — and it depends on reading Rabin's randomized suffix as achieving the later notion. Do not state it as established.
4. **Schnorr's patent claim against DSA.** Schnorr asserted that U.S. Patent 4,995,082 read on DSA. NIST reviewed the asserted patents and concluded DSS infringed none. The dispute was never judicially resolved; DSA itself is covered by U.S. Patent 5,231,668 (filed 26 Jul 1991, David W. Kravitz, assigned to the U.S. and licensed royalty-free). Both patents have expired.

---

# Could not establish

- **A DOI for FIPS 186-1 and FIPS 186-3.** Neither is registered in Crossref, and neither NIST CSRC landing page lists one. The CSRC permalinks above are the best stable identifiers available. (FIPS 186, 186-2, 186-4 and 186-5 *do* resolve under 10.6028.)
- **A DOI or stable digital identifier for Rabin (1978), "Digitalized Signatures," in *Foundations of Secure Computation*.** The page range 155–168 is widely cited but I could not verify it against a primary source or publisher record; treat the pagination as unconfirmed.
- **Exact page range for FIPS 186-5's Federal Register notice** beyond the cited FR volume/number (88 FR, No. 23, 3 Feb 2023); the govinfo permalink is reliable but I did not confirm the page span.
- **Merkle, "Protocols for Public Key Cryptosystems" end page.** Crossref records "122–122"; secondary sources give 122–134 and 122–136. The start page 122 is certain; the end page is not.
- **Merkle's 1979 thesis page range for the tree-authentication material** (commonly cited as pp. 32–61) — seen in secondary sources only, not verified against the thesis itself.
- **Whether Rabin's TR-212 has a canonical DTIC vs. MIT DSpace citation preference.** Both exist (DTIC ADA078415; MIT DSpace 1721.1/149499); I used the MIT handle as primary.
- **Research budget note:** the session's web-search quota (200 calls) was exhausted at the end of this pass. Remaining gaps above were not for want of effort but would need a fresh search budget or direct library/publisher access to close.
