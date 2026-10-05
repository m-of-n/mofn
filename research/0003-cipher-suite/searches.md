# Searches for R-0003

2026-10-02. Not a literature snowball. The question was where the existing
implementation is.

| query | where | yield |
|---|---|---|
| `git grep cipher_suite origin/main` excluding `library/` | mofn | no matches |
| `git ls-tree -r origin/main` filtered for cipher, suite, wallet | mofn | `research/0002-wallets/` only. No Python suite. |
| `find` name `cipher_suite.py` under `/Users/paul/cb/projects` and `/Users/paul/code` | local disk | seven copies. The runnable one is `/Users/paul/cb/projects/hpke/cipher_suite.py`. |
| `git -C library grep hpke` and `9180` | library submodule, read-only | no record paths. RFC cited by URL instead. |
| import `cipher_suite` and call `derive_csi`, `all_supported_suites`, `generateKeyPair` | projects/hpke, system python3 | `NameError` on `derive_csi`; `all_supported_suites` is `None`; public-key lengths 64, 64, 32, 32, 132, 132, 56, 56 in suite-list order; cryptography `CryptographyDeprecationWarning` on `generate_private_key(cls.Curve, ...)`. |
