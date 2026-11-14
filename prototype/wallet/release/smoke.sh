#!/usr/bin/env bash
# smoke.sh MOFN DIR — the release smoke test for one built mofn (DL-0043).
#
# release.yml runs it on a fresh runner that has the build and this folder
# but no checkout and no Python packages. DIR holds the fixtures it needs:
# artifact.bin, dv-1.def, tv-1-alice.pub.stmt, tv-3-define.stmt,
# tv-4-attestation.stmt and golden/green.txt.
#
# 1. `mofn --version` and a bare `mofn` exit 0 (#127 acceptance).
# 2. A fresh wallet makes a key (PyNaCl inside the build), knows Alice's
#    key, trusts her about build provenance, and checks her TV-4 attestation:
#    exit 0, and the verdict is golden/green.txt with Alice in place of the
#    release machine.
# 3. Where there is a pty: `mofn run` opens, opens Learn (README.md and
#    fixtures/golden/ inside the build), and quits on ctrl+q.
#
# The passphrase is for this test only.

set -euo pipefail
unset MOFN_WALLET

MOFN=$1
DIR=$(cd "$2" && pwd)
WORK=$(mktemp -d)
cd "$WORK"
PASSPHRASE="release smoke passphrase, not a secret"
LABEL="Alice (definer)"

echo "--- mofn --version"
"$MOFN" --version
echo "--- mofn (the menu)"
"$MOFN" >menu.txt
head -3 menu.txt

echo "--- a fresh wallet checks TV-4"
"$MOFN" --wallet w init
printf '%s\n' "$PASSPHRASE" | "$MOFN" --wallet w key gen me --passphrase-stdin -o me.pub.stmt
"$MOFN" --wallet w key import "$DIR/tv-1-alice.pub.stmt" --label "$LABEL"
"$MOFN" --wallet w root add "$LABEL" --as me --def "$DIR/dv-1.def" \
  --type build-provenance --values reproducible,attested
got=0
"$MOFN" --wallet w check "$DIR/tv-4-attestation.stmt" "$DIR/tv-3-define.stmt" \
  --artifact "$DIR/artifact.bin" --def "$DIR/dv-1.def" \
  --at 2026-10-15T00:00:00Z >verdict.txt || got=$?
cat verdict.txt
sed "s/release machine/$LABEL/g" "$DIR/golden/green.txt" >wanted.txt
if [ "$got" != 0 ] || ! diff --strip-trailing-cr wanted.txt verdict.txt; then
  echo "smoke: wanted golden green.txt and exit 0, got exit $got" >&2
  exit 1
fi
echo "[ok] matches golden green.txt, exit 0"

if python3 -c 'import pty' 2>/dev/null; then
  echo "--- mofn run, in a pty"
  python3 "$DIR/pty_run.py" "$MOFN" w
else
  echo "--- mofn run: no pty on this runner; skipped"
fi
