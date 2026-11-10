# domains/archives — the second domain (mofn#66, W-2)

The archives / library vocabulary of PLAN-0004 §3, and the files its author
publishes. Scenario: `project/APP-0003-scenario-archives.md`. Design record:
`design-log/0033-second-domain/`.

**The claim it tests:** one engine, two unrelated domains. This directory
runs through the same `mofn make` and `mofn check` as DV-1, and **no engine
code changed** for it: the commit that adds it touches nothing under
`engine/` or `cli.py`. `--lang` arrived in the commit before it, as engine
work allowed on 2026-11-09 (DL-0033), and works for every domain alike.

| file | what it is |
|---|---|
| `archives.def` | definition `archives` v1: type `record-review` (`reviewed`, `summarized`, `unverified`), template `record-attestation`. Every word in English and Spanish |
| `archivist.pub.stmt` | the definer's key-publish. The seed is published in `generate.py`: an example key only |
| `archivist-define.stmt` | the define statement that says `archives.def` is the archivist's. `check` needs it, or semantics fails |
| `record.yaml` | the subject: library record `w3c-prov-dm`, copied byte for byte from library@6dcbdb0 and frozen |
| `golden/` | `check` outputs pinned by `tests/test_archives.py` |
| `generate.py` | writes the first three; `--check` fails if any byte differs |

`.stmt.yaml` files are the same statements in the review codec.

## Renderings

| | en | es |
|---|---|---|
| type | Record review | Revisión del registro |
| `reviewed` | read against its source and confirmed | cotejado con su fuente y confirmado |
| `summarized` | summarized, but not read against its source | resumido, pero no cotejado con su fuente |
| `unverified` | not checked against its source | no cotejado con su fuente |
| sentence | {says} attests that the library record {this} was {record-review}. | {says} atestigua que el registro de la biblioteca {this} fue {record-review}. |

## Run it

From `prototype/wallet`, in a scratch folder. Two issuers sign the same
claim; the researcher trusts only the reviewer for `reviewed`.

```sh
M="$PWD/.venv/bin/python $PWD/mofn"; D=$PWD/domains/archives
mkdir -p /tmp/mofn-archives && cd /tmp/mofn-archives && cp $D/record.yaml .
$M --wallet w/reviewer init && $M --wallet w/reviewer key gen reviewer -o reviewer.pub.stmt
$M --wallet w/agent init && $M --wallet w/agent key gen agent --controller service -o agent.pub.stmt
for who in reviewer agent; do
  $M --wallet w/$who make --as $who --subject record.yaml --def $D/archives.def \
     --type record-review --value reviewed -o $who.stmt
done
$M --wallet w/rp init && $M --wallet w/rp key gen researcher -o rp.pub.stmt
$M --wallet w/rp key import $D/archivist.pub.stmt --label "Archivist (definer)"
$M --wallet w/rp key import reviewer.pub.stmt --label Reviewer
$M --wallet w/rp key import agent.pub.stmt --label "ingest agent"
A="--as researcher --def $D/archives.def --type record-review --context library"
$M --wallet w/rp root add Reviewer $A --values reviewed,summarized,unverified
$M --wallet w/rp root add "ingest agent" $A --values summarized,unverified
C="$D/archivist-define.stmt --artifact record.yaml --def $D/archives.def --context library"
$M --wallet w/rp check reviewer.stmt $C              # answer: yes         golden/reviewed.txt
$M --wallet w/rp check agent.stmt $C                 # authorization fail  golden/agent-not-entitled.txt
$M --wallet w/rp --lang es check agent.stmt $C       # the same, in Spanish golden/agent-not-entitled-es.txt
```

The deciding line of the second check:

```
authorization  fail           ingest agent is trusted in context library, but not about record review = reviewed
```
