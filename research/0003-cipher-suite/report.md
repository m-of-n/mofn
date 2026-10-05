---
schema: "archdoc/v1"
id: R-0003
title: "Cipher suite — definition, the existing implementation, and what a statement must be able to cite"
short_title: "Cipher suite"
description: "What a cipher suite is, what the existing cipher_suite.py actually implements, which functions are present, wrong, or missing, and one existing suite written out as data. Does not design the wallet, attestation, or delegation schemas, and does not close DEC-002."
type: research
category: security
status: draft
version: "0.1.0"
date: "2026-10-02"
updated: "2026-10-02"
needs_review: true
reviewed: false
canonical_path: research/0003-cipher-suite/report.md
informs: [APP-0001, PLAN-0004]
open_decisions: [DEC-002]
---

# Cipher suite

**Status: draft. A definition and a critique. Not a schema, not a decision.**

This memo does not close DEC-002. It does not pick a wire format, a signature
algorithm, or a key-exchange design. It does not specify the wallet, an
attestation, or a delegation. Those stay where APP-0001 and PLAN-0004 left
them: a local file wallet, keys as files, unsigned local trust roots, short
expiry instead of a revocation protocol, and an engine that is files plus
reduce/check. Crypto stays in the Python engine. There is no knowledge graph,
no cloud HSM, and no keyless OIDC principal.

`library/` was not touched. The HPKE identifiers below are cited from the RFC
fetched on 2026-10-02, not from a library record. Ingesting that RFC is
separate work.

There is no `cipher_suite.py` in this repository. `src/` is empty on purpose
so that code does not decide DEC-002 by accident (`CLAUDE.md`). The
implementation reviewed here lives outside the repo. No code in this repo
changed.

---

## 1. What a cipher suite is

A cipher suite is an object that defines all processing choices for a
cryptographic protocol. When instantiated it may enable digital signatures,
key exchanges, hashing, and may define the encoding formats and processing.
Key sizes for each key type and hash sizes are included.

That is the whole definition used here. A suite is the choices. It is not the
act of signing, and it is not a menu the signer may narrow at statement time.

One suite is one immutable record. It has an identifier a statement can cite,
one signature scheme, one hash, the key sizes, the hash size, the encoding of
a signature and of a public key, and the exact bytes that are signed (or a
pointer to that rule). Key exchange is a slot in that record. For this
product the slot is optional and empty: the product is signatures and
delegation, not a session protocol. Leaving the slot empty is not a
key-exchange design.

The suite itself needs few functions: identify itself, report sizes, and name
the encoding. Functions that *use* a suite — generate, sign, verify, encode,
decode — sit next to it and take the suite as an argument, so two suites
cannot be mixed inside one operation.

---

## 2. Where the code is

Searched this repo, including `origin/main` at `0ea374c`, for `cipher_suite`.
Nothing. The copies on disk, same filename:

| path | what it is |
|---|---|
| `/Users/paul/cb/projects/hpke/cipher_suite.py` | The copy that imports and runs. Git remote `https://github.com/nymble/hpke.git`, branch `master`. Identical bytes to `/Users/paul/code/pl code/git_repo/hpke/cipher_suite.py`. |
| `/Users/paul/code/Code2019/hpke/cipher_suite.py` | Same HPKE class family, later text of `derive_csi` and `all_supported_suites`. Not the checkout the tests import. |
| `/Users/paul/code/pl code/git_repo/TIP/tip/cipher_suite.py` | Older ECC suite (`Sweetpea`, `Bitcoin_Suite`). Hash, group, AEAD, compressed points. No `sign`. |
| `/Users/paul/code/pl code/excess------------/persona/cipher_suite.py` | 2015 bundle. Public-key encodings as separate classes. `hashUaid` slices to 16 bytes. |
| `/Users/paul/code/pl code/work area/ecc/cipher_suite.py` | 2013 stub. `sign` returns the literal `'asd'`. Does not parse (`PublicKeyPair =` has no value). |

The critique below is of the HPKE module, because that is the only copy that
is a real suite table and that still runs. The runnable file is
`/Users/paul/cb/projects/hpke/cipher_suite.py`. The TIP and persona files are
cited only to show that signature, encoding, and identity never landed on
that object. They are not a second design to adopt.

Checked on 2026-10-02 by importing the runnable module. `derive_csi` and
`all_supported_suites` were called. One key pair was generated per suite so
the public-key lengths in §7 are measured, not assumed. The HPKE unit tests
were not run: they are not part of this repo, and this change does not touch
them.

---

## 3. What the implementation actually is

The module's own header says it is "loosely based on draft-barnes-cfrg-hpke-01".
The base class is a table of eight suites, not a signature suite:

```text
class Cipher_Suite:
    """ Base class for the following variations in cryptographic algorithms:
    | csi    | KEM   | DH_Group   | Hash   |  KDF | AEAD             |
    | 0x0001 | DHKEM | P_256      | SHA256 | HKDF | AES_GCM_128      |
    ...
    | 0x0005 | DHKEM | P_521      | SHA512 | HKDF | AES_GCM_128      |
    | 0x0007 | DHKEM | Curve448   | SHA512 | HKDF | AES_GCM_128      |
    """
```

Each concrete suite is a subclass that stores class attributes and does the
work itself. The first one:

```text
class HPKE_P256_AES_GCM_128(HPKE_Cipher_Suite):
    csi = b'\x00\x01'
    DH_Group = P_256
    Hash = SHA256
    AEAD = AES_GCM_128
    KDF = HKDF(Hash)
    name = 'P1'
```

`HPKE_Cipher_Suite` adds `KEM = DHKEM`, where `class DHKEM: pass`, and
`HPKE = HPKE_draft_01ish`, one protocol class shared by every suite. It also
sets `sci_size = 4` with the comment "four byte security context identifier".
Every concrete `csi` is two bytes.

The methods on `Cipher_Suite` are `generateKeyPair`, `derive_csi`, and
`all_supported_suites`. Public-key encode and decode, and Diffie-Hellman,
live on `DH_Group` in `dh_group.py`. AEAD seal/open live on `AEAD` in
`aead.py`. There is no `sign` and no `verify` anywhere in this module.

RFC 9180, fetched 2026-10-02, defines an HPKE ciphersuite as the triple
(KEM, KDF, AEAD), with separate two-byte identifiers and explicit lengths
`Npk`, `Nsk`, `Nh`, `Nk`, `Nn`, `Nt`. For P-256, `Npk` is 65 and
`SerializePublicKey` is the uncompressed SEC1 encoding, type byte included.
This code is not that triple, and it does not store those lengths.

---

## 4. Critique

### 4.1 One object does not own the choices

Signature, key exchange, hash, sizes, and encoding are not fields of one
record.

- **Signature.** Absent. The 2013 stub is the only file that names a
  signature algorithm, and it names two (`ECDSA_NIST_P256` and
  `ECDSA_NIST_P384`) on one suite, then returns `'asd'` from `sign`.
- **Key exchange.** Present, and it is the whole object: `DH_Group`, a stub
  `DHKEM`, and `HPKE_draft_01ish`. The KEM class has no methods.
- **Hash.** Present as `Hash = SHA256` or `SHA512`, a cryptography class
  object, not a name plus a size stored on the suite.
- **Sizes.** Not on the suite. `AEAD.key_length` and `Hash.digest_size`
  exist on other classes. Public-key length is whatever `marshal` returns.
  `sci_size = 4` disagrees with `len(csi) == 2`.
- **Encoding.** Not on the suite. `ECC_DH_Group.marshal` does
  `public_bytes(..., UncompressedPoint)[1:]` and the comment says the X9.62
  type byte is dropped. X25519 and X448 use raw public bytes. Which of those
  a verifier must apply is implied by `DH_Group`, not named.

The runnable module does group KEM, group, hash, KDF, and AEAD onto one
class. That is closer to one object than the older files. It still is not
the definition in §1: no signature, no signature encoding, no statement of
the bytes that are signed, no sizes.

### 4.2 It is behavior, and the behavior is the wrong layer

A suite should be a frozen description. Doing the crypto should be a separate
engine that takes a suite. This code does the opposite.

`generateKeyPair` is a classmethod on the suite:

```text
@classmethod
def generateKeyPair(cls):
    return cls.DH_Group().generateKeyPair()
```

`Persona.__init__` then does `self.cipher_suite = C_suite()` and immediately
`self.cipher_suite.generateKeyPair()`. The instance has no `__init__` and no
per-instance fields. The "object" is the class, and the class both names the
algorithms and generates keys.

That split is worse than a frozen record plus an engine, for three reasons.
A class attribute can be reassigned (`HPKE_P256_AES_GCM_128.Hash = SHA512`)
and every later caller silently changes hash. The suite cannot be cited as
data in a statement file; the citation would be a Python class. And the
operation does not take a suite argument distinct from the receiver, so
nothing stops a caller from marshalling with one group and hashing with
another. `DH_Group.marshal` never sees the suite.

`generate_private_key` is called as `generate_private_key(cls.Curve, default_backend())`.
On 2026-10-02 the cryptography library warned that a curve class was passed
where an instance is required, and that this will become an exception. The
suite's key generation depends on that call.

### 4.3 A relying party cannot verify without guessing

What is missing, checked against the classes and against one generated key
per suite:

| a verifier needs | what the code has |
|---|---|
| An algorithm identifier | `csi` is a private two-byte value (`b'\x00\x01'` … `b'\x00\x08'`). It is not an RFC 9180 `kem_id`/`kdf_id`/`aead_id`. RFC 9180's P-256 KEM is `0x0010`, not `0x0001`. Only the first class sets `name = 'P1'`. The other seven have no `name`. |
| Hash size | `SHA256.digest_size` is 32 and `SHA512.digest_size` is 64, on the hash class. The suite does not store it. |
| Public-key size | Not stored. Measured from `generateKeyPair`: P-256 **64**, P-521 **132**, Curve25519 **32**, Curve448 **56**. RFC 9180's `Npk` for P-256 is 65 and for P-521 is 133. The difference is the stripped type byte. X25519 and X448 match the RFC length because those encodings are already raw. |
| Signature size | No signature. |
| Canonical encoding of the signed bytes, as distinct from the envelope | No signed-bytes rule. `Persona.addPeer` calls `self.cipher_suite.readable_pk_id(peer_pk)`, which is not defined on `Cipher_Suite`, and `peer_pk` is not defined in that function. The wallet code already expects an identifier function the suite does not have. |

The base-class table and the classes disagree. Rows `0x0005` and `0x0007`
in the `Cipher_Suite` docstring say `AES_GCM_128`. The classes are
`HPKE_P521_AES_GCM_256` and `HPKE_C448_AES_GCM_256`, and their `AEAD` is
`AES_GCM_256` (`key_length` 32). Confirmed by import, not only by reading.
A verifier who trusts the table and a verifier who trusts the class will
not check the same ciphertext.

`derive_csi` does not fix the identifier. On the runnable copy:

```text
@classmethod
def derive_csi(cls, mask=None):
    return self.KDF( self.__doc__, mask )
```

Called on `HPKE_P256_AES_GCM_128` it raises `NameError: name 'self' is not
defined`. `all_supported_suites` has a docstring and no body; the call
returns `None`. The module-level list `supported_cipher_suites` is what
`test_hpke.py` imports. The tests never call `derive_csi` or
`all_supported_suites`, so both defects are invisible to the test module.

The Code2019 copy replaces the body with `cls.KDF.extract(mask, bytes(cls.__doc__, 'utf8'))`.
That no longer raises `NameError`. It derives an identifier from the class
docstring, which is a second name beside the hardcoded `csi`, and editing
the comment changes it. `HKDF.extract` does not bind a suite id into the
KDF label the way RFC 9180's `LabeledExtract` does. Two suites that share
SHA-256 can be mixed inside one derivation. That copy also drops the
module-level list, so `from cipher_suite import supported_cipher_suites`
would fail there. Neither version is an identifier a statement can cite.

### 4.4 Key exchange

This module is a key-exchange and AEAD suite. The product is not. APP-0001
and PLAN-0004 are signatures, delegation, and reduction over files. A
session KEM does not answer "did this key have standing to say this."

Key exchange does not belong in v1 of the suite this product will cite.
The record defined in §5 keeps an optional slot so a later protocol can
fill it without pretending v1 already has a KEM. The slot stays empty.
This memo does not choose a KEM, a group, or an AEAD, and it does not
repair `DHKEM`.

The example in §7 is the existing HPKE suite written as data, so the
critique has something to point at. It is not a proposal to adopt that
suite for statements.

### 4.5 Dangerous or premature choices

- **Agility inside the suite list.** Eight suites, and nothing says the
  verifier's policy picks one. A statement that carried `csi` could ask a
  verifier to accept P-256 with AES-128-GCM (`0x0001`) where the verifier
  wanted a stronger suite. The table's P-521 rows claim AES-128-GCM while
  the classes use AES-256-GCM, so the weak combination is even written down
  in the place a reader would copy from.
- **Not citable.** `csi` is not a registered identifier, disagrees with
  `sci_size`, and on the runnable copy cannot be derived. Seven of eight
  suites have no `name`. A statement file cannot name the suite without
  naming a Python class.
- **Mutable.** Suites are classes. Attributes are writable. `KDF = HKDF(Hash)`
  builds one shared instance at class-definition time. There is no frozen
  record.
- **Silent change of hash or curve.** There is no default hash on the base
  class, which is the right absence. The hazard is the opposite of a
  default argument: rebinding `Hash` or `DH_Group` on the class changes
  every caller and no statement notices, because the statement never cited
  a value.
- **Two algorithms in one suite,** on the 2013 stub only: `signatureAlgorithm`
  is a pair. One suite, one signature scheme. A pair is agility hiding
  inside the object that was supposed to end agility.
- **Private-key modulo the field prime,** on the TIP suite's
  `newPrivateKey`: the random integer is reduced modulo `group.p`, not the
  group order. That is a key-generation defect in an older file. It is not
  fixed here. It is named so it is not copied forward.

The statement prototype in this repo (`prototype/statements/statement.py`)
is a truncated SHA-256 over `b"rcbor/statement/v0" + secret + payload`. It
says it is a stand-in. It is not a suite, and it must not become one by
being the only signer the engine calls.

---

## 5. Suggested structure

One suite is an immutable record. Proposed fields, none of them a wire
encoding:

| field | v1 |
|---|---|
| `id` | a string the statement cites. Not a Python class name. Not a private integer the class happens to hold. |
| `signature` | one scheme. Required for a statement suite. Not chosen in this memo. |
| `hash` | one hash, by name. |
| `sizes` | hash size, public-key size, signature size, each in bytes. Private-key size only if a key file must record it. |
| `encoding` | a name for the public-key encoding and a name for the signature encoding. Names, not the bytes of a format. DEC-002 still chooses how a statement file carries those bytes. |
| `signed_bytes` | a name of the rule that produces the exact bytes under the signature, distinct from the envelope those bytes are carried in. |
| `key_exchange` | optional. **Empty in v1.** No KEM, no group, no AEAD until a session protocol exists. |

Functions on the suite:

- `identify()` — return `id`.
- `sizes()` — return the size record.
- `encodings()` — return the encoding names and the signed-bytes rule name.

Functions beside the suite, each taking the suite as an argument:

- `generate(suite)` — one key pair for that suite's signature scheme.
- `sign(suite, secret, message)` — `message` is already the bytes
  `signed_bytes` names. The function does not re-encode.
- `verify(suite, public, message, signature)` — same bytes the signer
  signed. No second suite argument.
- `encode_public_key(suite, public)` / `decode_public_key(suite, octets)`.
- `encode_signature(suite, signature)` / `decode_signature(suite, octets)`.

`generate`, `sign`, and `verify` refuse to run if the key's suite id is not
the suite argument's id. That is how two suites stay unmixed. No
`key_exchange` function in v1.

This shape is a proposal for a later engine change. It is not implemented
in this pull request. Implementing `encode_*` would choose the bytes on the
wire, and that is DEC-002.

---

## 6. Critical review

Verdicts are against the definition in §1 and the runnable HPKE module.
"Present but wrong" means the name exists and does not do the job.

| function | verdict | why |
|---|---|---|
| Identify the suite (`csi`, class name, `name`) | **present but wrong** | Private two-byte `csi`, not an algorithm id a statement can cite. `sci_size` says 4. `name` is set only on `HPKE_P256_AES_GCM_128`. |
| `derive_csi` | **present but wrong** | Runnable copy raises `NameError` (`self` inside a classmethod). Code2019 copy hashes the docstring and does not bind the suite into the KDF. |
| `all_supported_suites` | **present but wrong** | Runnable copy returns `None`. The real list is a module global the method does not return. Code2019 returns a list, duplicated, and still not a policy. |
| Report hash size | **missing** on the suite | `Hash.digest_size` is on the cryptography class (32 or 64). |
| Report public-key size | **missing** | Lengths measured in §4.3 are not stored. NIST lengths disagree with RFC 9180 by the stripped type byte. |
| Report signature size | **missing** | No signature scheme. |
| Name the public-key encoding | **present but wrong** | `DH_Group.marshal` / `unmarshal`. Not a named field. NIST curves drop the SEC1 type byte; X25519 does not use that encoding. The suite is not an argument. |
| Name the signature encoding | **missing** | |
| Name the signed bytes, distinct from the envelope | **missing** | |
| `generateKeyPair` | **present but wrong** | Behavior on the suite class. Calls `generate_private_key` with a curve class; cryptography warns that will become an exception. |
| `sign` | **missing** | The 2013 stub's `sign` is not this module, and it returns `'asd'`. |
| `verify` | **missing** | |
| Encode / decode a public key, taking the suite | **present but wrong** | Same `marshal` / `unmarshal`. A caller can pass another group's bytes. No length check against a size stored on the suite. |
| Encode / decode a signature, taking the suite | **missing** | |
| `DH_Group.dh`, `AEAD.seal` / `open`, `HPKE.wrap` | **present but wrong** for v1 | They are the session protocol. They do not belong on the statement suite. Not a design for the empty key-exchange slot. |
| `readable_pk_id` | **missing** | `Persona.addPeer` calls it. It is not defined. The undefined name `peer_pk` is in the caller. |

Nothing in that table was added or "fixed" in this repo. The `NameError` is
a defect, and so is the empty `all_supported_suites`, and so is the table
that says AES-128-GCM where the class says AES-256-GCM. Repairing them
inside `nymble/hpke` is a different repository. Copying that module into
`src/` would put an HPKE engine in the product and would choose encodings
(the stripped public key, the two-byte `csi`) that DEC-002 has not
accepted. A missing `sign` that does not pick an algorithm cannot be added
without picking one.

---

## 7. Example

`example.yaml` is `HPKE_P256_AES_GCM_128` written as data, from the class
body and from the key generated on 2026-10-02. Null fields are what the
class does not have. This is not the v1 statement suite. A second suite,
`HPKE_Curve25519_ChaCha20Poly1305`, changes `csi` to `0004`, the group to
Curve25519, the AEAD to ChaCha20Poly1305 (key length 32), and the measured
public-key length to 32; the hash stays SHA-256.

---

## 8. What later schemas will need from a suite

**Not designed here.** The wallet, attestation, and delegation documents
will need, from a suite, and only these, until someone designs them:

- the suite id, so a statement can cite the suite the verifier must use
- the signature algorithm
- the hash
- the key sizes and the hash size
- the encoding of a signature
- the encoding of a public key

They will not embed a KEM. Trust roots stay unsigned local files, so a root
does not carry a signature algorithm of its own. Short expiry stays the
revocation story; a suite does not grow a revocation algorithm.

---

## 9. What this report does not decide

- **DEC-002.** Encoding names inside a suite are candidates. They are not a
  choice of statement wire format. The prototype's reduced CBOR is not
  adopted by being mentioned.
- **Key exchange.** The slot is empty on purpose. No KEM is specified.
- **The signature algorithm** the product will use. The example is the
  HPKE suite the code already has, which has no signature algorithm.
- **Wallet, attestation, and delegation schemas.** §8 lists fields they
  will have to read. It does not define those documents.
- **Repair of `nymble/hpke`.** Defects are recorded in §6. They were not
  patched.
