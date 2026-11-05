# When a check fails

<!-- go: check -->
Every result prints all six lines. The line that decides is the first that
fails. These are the outputs the tests and `demo/slice.sh` compare against,
exactly as `check` prints them.

<!-- readme: The cases -->

**① All six pass.**

<!-- golden: green -->

**② Not trusted.** The key is known, and nothing anchors it.

<!-- golden: unauthorized -->

**②b The key was never received.**

<!-- golden: unknown-key -->

**③ The file changed.** The statement is valid, but it is not about this file.

<!-- golden: tampered -->

**④ The statement changed.** It is thrown out at once, so authorization is not
evaluated, and the exit code is 3.

<!-- golden: statement-changed -->

**Expired.** Checked after the statement's time ran out.

<!-- golden: expired -->
