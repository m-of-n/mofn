#!/usr/bin/env bash
# R-0007 unverified.md §1 and §2: does GnuPG narrow trust-signature scope
# along a chain, and does a command-line domain scope over-match?
#
# NOT YET RUN. Needs gpg (2.2+) on PATH. Uses throwaway GNUPGHOMEs under a
# temp dir and touches nothing else. Record `gpg --version` with the output.
#
#   Dave --tsig 2,full,foo.com--> Alice --tsig 1,full,$SCOPE--> Bob --sig--> Carol <$ADDR>
#
# Each persona has its own keyring: a key generated in Dave's home would be
# ultimately trusted and short-circuit the chain.
set -euo pipefail

T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
gpg --version | head -1

H() { local who=$1; shift
      gpg --homedir "$T/$who" --batch --yes --quiet --pinentry-mode loopback \
          --passphrase '' --trust-model pgp "$@"; }
fpr() { H "$1" --list-keys --with-colons "$2" | awk -F: '/^fpr/{print $10; exit}'; }
move() { H "$1" --export "$3" | H "$2" --import 2>/dev/null; }

run() {
  local scope=$1 addr=$2 expect=$3
  rm -rf "$T"/{dave,alice,bob,carol}
  for p in dave alice bob carol; do mkdir -m 700 "$T/$p"; done
  H dave  --quick-gen-key 'Dave <dave@dave.example>' default default never
  H alice --quick-gen-key 'Alice <alice@foo.com>'    default default never
  H bob   --quick-gen-key 'Bob <bob@eng.foo.com>'    default default never
  H carol --quick-gen-key "Carol <$addr>"            default default never
  local A B C; A=$(fpr alice alice@foo.com); B=$(fpr bob bob@eng.foo.com); C=$(fpr carol "$addr")

  move alice dave "$A";  H dave  --quick-tsign-key "$A" 2,full,foo.com
  move bob alice "$B";   H alice --quick-tsign-key "$B" "1,full,$scope"
  move carol bob "$C";   H bob   --quick-sign-key  "$C"

  # Dave already holds Alice with his own tsig on her.
  H dave --import < <(H alice --export "$B") 2>/dev/null   # Bob, with Alice's tsig
  H dave --import < <(H bob --export "$C") 2>/dev/null     # Bob's sig on Carol
  H dave --check-trustdb 2>/dev/null || true

  local v; v=$(H dave --list-keys --with-colons "$C" | awk -F: '/^uid/{print $2; exit}')
  printf '%-34s scope=%-12s carol validity=%s  (expect %s)\n' "$addr" "$scope" "$v" "$expect"
}

echo "validity: f=full m=marginal u=ultimate -/q=unknown n=never"
# Controls
run eng.foo.com carol@eng.foo.com  "f: in scope"
run eng.foo.com carol@bar.com      "-: out of Alice's scope"
# §1: Alice widens Bob to bar.com. f here means Dave's foo.com scope did not carry.
run bar.com     carol@bar.com      "- if scope narrows along the chain; f if it does not"
# §2: unescaped '.' — eng.foo.com regex vs a look-alike domain
run eng.foo.com carol@eng-foo.com  "- if '.' is literal; f if it over-matches"
