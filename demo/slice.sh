#!/usr/bin/env bash
# demo/slice.sh — the demo slice (mofn#65 acceptance, mofn#68).
#
# Three roles, one wallet each, under both codecs. Only the files in
# handover/ cross between roles; the issuer's and the key-holder's wallets are
# locked before the relying party starts, so a check cannot pass by reaching
# into them. Every `check` is compared byte for byte with
# prototype/wallet/fixtures/golden/, and its exit code with the one expected.
#
#   ②b unknown key    the speaker's key has not been handed over   authenticity fail
#   ②  no root        key known, nothing anchors it                authorization fail
#   ①  authorized     the relying party anchors the issuer's key   all six pass
#   ③  tampered       first byte of the artifact becomes X         integrity fail
#   ②′ other key      valid signature, a different unanchored key  authorization fail
#
# Prerequisites: Python 3.12 or later with prototype/wallet/requirements.txt
# installed, in prototype/wallet/.venv (see prototype/wallet/README.md "Run"),
# or in the interpreter named by $MOFN_PYTHON, or in `python3` on the PATH.
# This script installs nothing, and uses no network and no keychain.
#
# Wallets land in demo/wallets/, ignored by git and rebuilt on every run. The
# passphrase below is for this demo only; it goes to `mofn` on stdin.

set -euo pipefail
unset MOFN_WALLET

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
ENGINE=$ROOT/prototype/wallet
FIXTURES=$ENGINE/fixtures
GOLDEN=$FIXTURES/golden
WALLETS=$ROOT/demo/wallets
PASSPHRASE="slice demo passphrase, not a secret"

PY=${MOFN_PYTHON:-}
if [ -z "$PY" ]; then
  if [ -x "$ENGINE/.venv/bin/python" ]; then PY=$ENGINE/.venv/bin/python; else PY=python3; fi
fi
if ! "$PY" -c 'import nacl, yaml' 2>/dev/null; then
  echo "slice: $PY cannot import nacl and yaml." >&2
  echo "slice: install the prerequisites first; see prototype/wallet/README.md, Run." >&2
  exit 2
fi

unlock_wallets() { chmod -R u+rwx "$WALLETS" 2>/dev/null || true; }
trap unlock_wallets EXIT

failures=0

# mofn WALLET ARGS... — one party acting on its own wallet.
mofn() {
  local wallet=$1
  shift
  "$PY" "$ENGINE/mofn" --wallet "$wallet" --codec "$CODEC" "$@"
}

# signing WALLET ARGS... — the same, with the passphrase on stdin.
signing() {
  printf '%s\n' "$PASSPHRASE" | mofn "$@" --passphrase-stdin
}

# expect CASE GOLDEN CODE [LABEL] — the relying party checks STATEMENT against
# FILE, from what is in handover/ only. LABEL replaces the golden's label for
# the speaker, because the relying party names a second key differently.
expect() {
  local title=$1 golden=$2 code=$3 label=${4:-release machine}
  local actual=$BASE/$golden.$STATEMENT.out wanted=$BASE/$golden.$STATEMENT.golden got=0

  (
    cd "$HANDOVER"
    mofn "$RP" check "$STATEMENT" "tv-3-define$SUFFIX" \
      --artifact "$FILE" --def dv-1.def
  ) >"$actual" 2>&1 || got=$?
  sed "s/release machine/$label/g" "$GOLDEN/$golden.txt" >"$wanted"

  echo "--- $title"
  cat "$actual"
  if cmp -s "$actual" "$wanted" && [ "$got" = "$code" ]; then
    echo "[ok] matches golden $golden.txt, exit $got"
  else
    echo "[FAILED] wanted golden $golden.txt and exit $code, got exit $got:"
    diff -u "$wanted" "$actual" || true
    failures=$((failures + 1))
  fi
  echo
}

slice() {
  CODEC=$1
  SUFFIX=$2
  BASE=$WALLETS/$CODEC
  HANDOVER=$BASE/handover
  ISSUER=$BASE/issuer
  HOLDER=$BASE/key-holder
  RP=$BASE/relying-party
  mkdir -p "$HANDOVER"

  echo "=== codec $CODEC"

  # The issuer signs the file. What it hands over: its public key, the
  # statement and the file.
  mofn "$ISSUER" init >/dev/null
  signing "$ISSUER" key gen build --controller service -o "$HANDOVER/build.pub.stmt" >/dev/null
  signing "$ISSUER" make --as build --subject "$FIXTURES/artifact.bin" \
    --def "$FIXTURES/dv-1.def" --type build-provenance --value reproducible \
    -o "$HANDOVER/prov.stmt" >/dev/null
  cp "$FIXTURES/artifact.bin" "$HANDOVER/release.bin"

  # The key-holder signs the same file with its own key, which nobody anchors.
  mofn "$HOLDER" init >/dev/null
  signing "$HOLDER" key gen holder -o "$HANDOVER/holder.pub.stmt" >/dev/null
  signing "$HOLDER" make --as holder --subject "$FIXTURES/artifact.bin" \
    --def "$FIXTURES/dv-1.def" --type build-provenance --value reproducible \
    -o "$HANDOVER/holder.stmt" >/dev/null

  # Published vocabulary: the definition, its author's key and `define`.
  cp "$FIXTURES/dv-1.def" "$FIXTURES/tv-1-alice.pub$SUFFIX" \
    "$FIXTURES/tv-3-define$SUFFIX" "$HANDOVER/"

  # From here on the relying party has its own wallet and handover/, and
  # the other two wallets cannot be read.
  chmod 000 "$ISSUER" "$HOLDER"

  mofn "$RP" init >/dev/null
  signing "$RP" key gen me -o "$RP.pub.stmt" >/dev/null
  mofn "$RP" key import "$HANDOVER/tv-1-alice.pub$SUFFIX" --label "Alice (definer)" >/dev/null

  STATEMENT=prov.stmt
  FILE=release.bin
  expect "②b speaker's key not handed over → authenticity fail" unknown-key 1

  mofn "$RP" key import "$HANDOVER/build.pub.stmt" --label "release machine" >/dev/null
  expect "② valid signature, no root or delegation → authorization fail" unauthorized 1

  mofn "$RP" root add "release machine" --as me --def "$HANDOVER/dv-1.def" \
    --type build-provenance --values reproducible,attested >/dev/null
  expect "① authorized key → all six pass" green 0

  { printf X; tail -c +2 "$HANDOVER/release.bin"; } >"$HANDOVER/tampered.bin"
  FILE=tampered.bin
  expect "③ first byte of the artifact flipped → integrity fail" tampered 1

  mofn "$RP" key import "$HANDOVER/holder.pub.stmt" --label "key holder" >/dev/null
  STATEMENT=holder.stmt
  FILE=release.bin
  expect "②′ valid signature, a different key with no root → authorization fail" \
    unauthorized 1 "key holder"

  chmod 700 "$ISSUER" "$HOLDER"
}

unlock_wallets
rm -rf "$WALLETS"

slice ksa-cbor .stmt
slice review-yaml .stmt.yaml

if [ "$failures" -ne 0 ]; then
  echo "slice: $failures case(s) FAILED"
  exit 1
fi
echo "slice: 5 cases passed under each of 2 codecs"
