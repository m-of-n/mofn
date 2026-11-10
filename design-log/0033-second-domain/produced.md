---
schema: "design-log/v1"
id: DL-0033
part: produced
date: "2026-11-09"
---

# DL-0033 — produced

Spec-adjacent documents, a vocabulary, engine code for one flag, tooling,
tests. No primitive: signing and hashing are PyNaCl and hashlib, called
through the engine's existing `suite.py`.

**Commit 1: engine (`--lang`)**

| file | change |
|---|---|
| `engine/render.py` | `lang(m, want)`: RFC 4647 §3.4 lookup, then `en`, then the first tag; `want` threaded through `type_name`, `value_text`, `sentence` |
| `engine/check.py` | `run(..., lang=None)` passes it to the authorization and acceptance lines and the sentences. No result depends on it |
| `engine/definition.py` | exposes the existing language-tag pattern as `LANG_TAG` |
| `cli.py` | global `--lang TAG`, checked against `LANG_TAG` (canonical case); used by `make` and `check` |
| `engine/__init__.py`, `CHANGELOG.md` | 0.3.0 → **0.4.0** (0.3.0 was taken by mofn#152) (MINOR: behaviour added) |
| `tests/test_lang.py` | lookup, fallback, refusal of `ES`, DV-1's Spanish sentence and its English fallback for `attested` |

**Commit 2: the second domain (no file under `engine/` or `cli.py`)**

| file | change |
|---|---|
| `prototype/wallet/domains/archives/generate.py` | writes `archives.def` (definition `archives` v1, type `record-review`, template `record-attestation`, en + es throughout) and the archivist's key-publish and define statements, from a fixed published seed, in both codecs; `--check` for reproducibility |
| `…/archives/record.yaml` | library record `w3c-prov-dm` at library@6dcbdb0, frozen |
| `…/archives/golden/` | `reviewed`, `agent-not-entitled`, `agent-not-entitled-es` |
| `tests/test_archives.py` | the APP-0003 run, under both codecs, against the goldens |
| `.gitattributes` | `domains/**` byte-exact, as `fixtures/**` already is |
| wallet `README.md`, `CHANGELOG.md` | pointer to the second domain; `--lang` sentence |

**Commit 3: documents**

| file | change |
|---|---|
| `project/APP-0002-scenario-supply-chain.md` | new: roles, archetypes, setup, steps, the fail case (golden `unauthorized`, slice ②′), Spanish, gaps |
| `project/APP-0003-scenario-archives.md` | new: the same headings; the agent anchored only for `summarized · unverified` signs `reviewed` → authorization fails on the value; findings F-1…F-5 |
| `project/APP-0004-five-views.md` | new: Wallet, Domain, Make, Present, Verdict, each drawn for both domains, each element bound to a source; what changed from PLAN-0002 §6.5 |
| `project/PLAN-0002-product-spec.md` 0.3.0 → **0.4.0** | §2.2 scenarios point at APP-0002/0003; §6.5 placeholders replaced by a five-view summary and the rule |
| `project/BACKLOG-0001.md` 0.12.15 → 0.12.16 | W-2 → review |

Test run: `pytest -q` in `prototype/wallet`: 314 passed (298 before).
