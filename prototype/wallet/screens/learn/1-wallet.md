# Your wallet

<!-- go: wallet -->
mofn keeps **one wallet**: a folder, `./wallet` unless you name another with
`--wallet` or `$MOFN_WALLET`. `mofn run` opens the same wallet the command
line does, and every form shows the command it runs, so you can do the same
thing in a shell.

Someone else is not a second wallet in your mofn. They are a person with
their own mofn and their own wallet, and what passes between you is **files**:
a key-publish statement (`*.pub.stmt`), a statement about a file, the file.

<!-- readme: What the wallet keeps -->

The **example vocabulary** sits next to your wallet, in `example/`: DV-1, a
vocabulary for supply-chain claims, published by Alice. With it are her key,
her `define` statement, which says DV-1 is hers, one statement of hers about
`artifact.bin`, and the file itself. They are the published test vectors,
handed to you as files Alice sent.
