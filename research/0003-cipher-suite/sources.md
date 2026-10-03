# Sources for R-0003

Retrieved or read on 2026-10-02. `library/` was not modified and these were
not ingested as records.

## Code

- `/Users/paul/cb/projects/hpke/cipher_suite.py` — imported. `derive_csi` raised `NameError`. `all_supported_suites` returned `None`. One key pair generated per class in `supported_cipher_suites`.
- Same checkout: `dh_group.py`, `aead.py`, `kdf.py`, `persona.py`, `test_hpke.py`, `README.md`.
- `/Users/paul/code/Code2019/hpke/cipher_suite.py` — read. Later `derive_csi` / `all_supported_suites`. Not imported.
- `/Users/paul/code/pl code/git_repo/hpke/cipher_suite.py` — same SHA-256 as the projects checkout (`2f1607c0a43b…`).
- `/Users/paul/code/pl code/git_repo/TIP/tip/cipher_suite.py` and `test_cipher_suite.py` — read.
- `/Users/paul/code/pl code/excess------------/persona/cipher_suite.py` — read.
- `/Users/paul/code/pl code/work area/ecc/cipher_suite.py` — read. Does not parse.
- This repo, `origin/main` at `0ea374c`: `project/APP-0001-application-design.md`, `project/PLAN-0004-application-plan.md`, `project/DECISIONS-0001.md` (DEC-002 still open), `prototype/statements/statement.py`, `CLAUDE.md`. No `cipher_suite.py`.

## Standards

- RFC 9180, Hybrid Public Key Encryption. https://www.rfc-editor.org/rfc/rfc9180.html — fetched 2026-10-02. Used for the definition of a ciphersuite as (KEM, KDF, AEAD), Table 2 KEM ids and `Npk` (P-256: `0x0010`, `Npk` 65; P-521: `0x0012`, `Npk` 133; X25519: `0x0020`, `Npk` 32; X448: `0x0021`, `Npk` 56), Table 3 HKDF ids, Table 5 AEAD ids, and `SerializePublicKey` for NIST curves (uncompressed SEC1, type byte included).

The code's header cites draft-barnes-cfrg-hpke-01. That draft was not fetched. The comparison above is to the published RFC, not to a claim that draft-01 required the same bytes.
