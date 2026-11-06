# Keys

<!-- go: keys -->
**Your own key** is made by *key gen*. Its private half is encrypted in your
wallet under a passphrase you choose. The passphrase is asked for in a masked
field, and is never put on a command line or in the environment. Signing
asks for it again. *key gen* also writes your **key-publish statement**,
`NAME.pub.stmt`: that file is what you send to anyone who should be able to
check what you sign.

**A key you were sent** is imported with *key import*, under a name you give
it. From then on the wallet shows that key by your name, never by a name the
sender chose: a statement holds no names, only key ids and hashes.

**Knowing a key is not trusting it.** An imported key lets mofn check that a
signature is that key's. It says nothing about whether the key may say what
it said. That is the next page.

**Seeing and sending your keys.** *key list* prints every key in your
wallet, yours and the ones you know, with your name for each, its kind and
its fingerprint, and for a key you were sent, the file and the date you
imported it. It changes nothing. *key export* writes your key-publish
statement again, from the copy *key gen* kept, so you can send your key to
someone you meet later. It signs nothing and asks for no passphrase. It
exports only your own keys: of a key you were sent, mofn keeps the key, not
the statement it came in.

A key has a **kind**: person, organisation, service, agent, software or
device. Only a person or an organisation may decide to trust another key.
