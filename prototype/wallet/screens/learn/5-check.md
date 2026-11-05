# Check

<!-- go: check -->
*Check* takes the statements you were handed, the file, and the vocabulary,
and answers one question: **was this said, about this file, by someone you
trusted to say it?** It always prints six lines, the answer, what was said,
and the limit of what that proves.

<!-- readme: What the six lines mean -->

Here is a check that passes every line. The sender is a build machine its
receiver labelled *release machine*:

<!-- golden: green -->

Hand over the vocabulary's `define` statement as well
(`example/alice-define.stmt` for DV-1), or semantics fails: nothing would say
who published the vocabulary.
