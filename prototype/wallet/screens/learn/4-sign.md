# Sign

<!-- go: sign -->
*Sign* makes one **attestation**: your key says one value of one claim about
one file. For example, as a reviewer you can say DV-1's `outcome` is
`approve` for `artifact.bin`.

What is signed holds no names and no file contents:

| field | what it is |
|---|---|
| `says` | your key id, the SHA-256 of your public key |
| `this` | the file, by its SHA-256 |
| `body.has` | the claim, named by the vocabulary's id and the type's label, and its value |
| `valid` | when it holds: from now, for 30 days unless you say otherwise |

**Comparing a file without mofn's help.** *hash* prints a file's SHA-256,
exactly as a statement's `this` names it. Two people can read the hash to
each other, and a verdict's sentence shows its first 16 digits.

**What you send** is the statement file, the file it is about, and, if they
do not have it yet, your `NAME.pub.stmt`. The person who checks it still has
to decide to trust you, as you decided about Alice. A statement that has run
out of time fails authorization, whoever signed it.
