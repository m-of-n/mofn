# Trust

<!-- go: trust -->
An **anchor** is your decision to trust one key about one kind of claim:

> In context `default`, I trust **Alice** to say **build-provenance** is
> **reproducible** or **attested**, about any file.

| part | what it means |
|---|---|
| whose key | the key you trust, from the keys you know |
| as which of your keys | the one of your own keys that decides: a person or an organisation |
| vocabulary, claim | the type, named by the vocabulary's id and the type's label |
| values | the values the key may say; any other value fails authorization |
| context | where the decision applies; trust in one context counts for nothing in another |

An anchor is signed by nobody and sent to nobody (SPEC-0004 §4.2). It is
written in your wallet, and it is what the **authorization** line looks for.
Trust is about one kind of claim: the same key saying anything else still
fails.
