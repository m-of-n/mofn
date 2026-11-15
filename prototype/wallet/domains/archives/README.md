# domains/archives — the second domain (mofn#66, W-2, W-2b)

The archives / library vocabulary of PLAN-0004 §3, as the wallet runs it.
Scenario: `project/APP-0003-scenario-archives.md`. Design record:
`design-log/0033-second-domain/` (v0) and `design-log/0046-archives-converge/`
(W-2b).

**The claim it tests:** one engine, two unrelated domains. This directory
runs through the same `mofn make`, `mofn delegate` and `mofn check` as DV-1,
and **no engine code changed** for it.

**Since W-2b there is one archives vocabulary:** the published DV-5
`library-review` v2 (`spec/vectors/ksa-core`). Every vocabulary file here is a
byte-for-byte copy of a vector, as `fixtures/` is for DV-1. The demo's own
`archives` v1 and its archivist key are retired.

| file | what it is |
|---|---|
| `library-review.def` | DV-5: type `record-review` (`reviewed`, `summarized`, `unverified`), plus `work`, `title`, `locator`, template `record-reviewed`. Every word of `record-review` in English and Spanish |
| `dave.pub.stmt` | TV-38, the definer's key-publish. Dave's seed is published in the vectors: an example key only |
| `dave-define.stmt` | TV-39, the define statement that says DV-5 is Dave's. `check` needs it, or semantics fails |
| `record.yaml` | the subject: library record `w3c-prov-dm`, copied byte for byte from library@6dcbdb0 and frozen |
| `golden/` | `check` outputs pinned by `tests/test_archives.py` |
| `generate.py` | copies the first three out of `vectors.json`; `--check` fails if any byte differs |

`.stmt.yaml` files are the same statements in the review codec.

## Renderings

| | en | es |
|---|---|---|
| type | Record review | Revisión del registro |
| `reviewed` | read against its source and confirmed | cotejado con su fuente y confirmado |
| `summarized` | summarized, but not read against its source | resumido, pero no cotejado con su fuente |
| `unverified` | not checked against its source | no cotejado con su fuente |
| sentence | {says} attests that {this} was {record-review}. | {says} atestigua que {this} fue {record-review}. |

## Run it

From `prototype/wallet`, in a scratch folder. The researcher anchors only the
library lead, who delegates for 30 days: the reviewer for every value, the
ingest agent for `summarized` and `unverified` only. Both issuers sign
`reviewed`.

```sh
M="$PWD/.venv/bin/python $PWD/mofn"; D=$PWD/domains/archives; DEF=$D/library-review.def
mkdir -p /tmp/mofn-archives && cd /tmp/mofn-archives && cp $D/record.yaml .
$M --wallet w/lead init && $M --wallet w/lead key gen lead -o lead.pub.stmt
$M --wallet w/reviewer init && $M --wallet w/reviewer key gen reviewer -o reviewer.pub.stmt
$M --wallet w/agent init && $M --wallet w/agent key gen agent --controller service -o agent.pub.stmt
for who in reviewer agent; do
  $M --wallet w/$who make --as $who --subject record.yaml --def $DEF \
     --type record-review --value reviewed -o $who.stmt
done
$M --wallet w/lead key import reviewer.pub.stmt --label Reviewer
$M --wallet w/lead key import agent.pub.stmt --label "ingest agent"
$M --wallet w/lead delegate Reviewer --as lead --def $DEF --type record-review \
   --values reviewed,summarized,unverified --valid-days 30 -o lead-reviewer.stmt
$M --wallet w/lead delegate "ingest agent" --as lead --def $DEF --type record-review \
   --values summarized,unverified --valid-days 30 -o lead-agent.stmt
$M --wallet w/rp init && $M --wallet w/rp key gen researcher -o rp.pub.stmt
$M --wallet w/rp key import $D/dave.pub.stmt --label "Dave (definer)"
$M --wallet w/rp key import lead.pub.stmt --label "Library lead"
$M --wallet w/rp key import reviewer.pub.stmt --label Reviewer
$M --wallet w/rp key import agent.pub.stmt --label "ingest agent"
$M --wallet w/rp root add "Library lead" --as researcher --def $DEF --type record-review \
   --values reviewed,summarized,unverified --depth 1 --context library
C="$D/dave-define.stmt --artifact record.yaml --def $DEF --context library"
$M --wallet w/rp check reviewer.stmt lead-reviewer.stmt $C          # yes                 golden/reviewed.txt
$M --wallet w/rp check agent.stmt lead-agent.stmt $C                # authorization fail  golden/agent-not-entitled.txt
$M --wallet w/rp --lang es check agent.stmt lead-agent.stmt $C      # the same, Spanish   golden/agent-not-entitled-es.txt
```

`tests/test_archives.py` also pins the agent signing `summarized` (yes,
`golden/agent-summarized.txt`) and the reviewer's chain checked 31 days on
(the delegation has expired, `golden/reviewer-expired.txt`).

The deciding lines:

```
authorization  pass           Reviewer is trusted in context library about record review (reviewed, summarized, unverified), through Library lead → Reviewer
authorization  fail           ingest agent is trusted in context library, but not about record review = reviewed
authorization  fail           the delegation Library lead → Reviewer is broken: the delegation has expired (not-valid-at-time)
```
