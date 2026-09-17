# Test vectors

**Published artifacts, not test fixtures.** They are the interoperability
contract: another implementation should be able to consume this directory and
nothing else.

```
NNN-name/
  input.<ext>      the logical object, in the authored form
  canonical.<ext>  its canonical encoding, byte-exact
  digest.txt       sha-256 of canonical
  notes.md         what this vector exercises and why it exists
```

Empty until **DEC-002** is accepted (`T-031`). Vectors before an encoding
decision would encode the guess.

Each vector names the requirement it exercises — `R-O-05`, `R-M-06`, and so on —
so a reader can tell coverage from decoration.
