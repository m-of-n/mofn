#!/usr/bin/env bash

set -euo pipefail
cd "$(dirname "$0")"

[ -d .venv ] || python3 -m venv .venv
# always sync: idempotent and fast, and a venv left half-installed by a failed run, or made before requirements.txt changed, is not silently reused.
.venv/bin/pip install -q -r requirements.txt

rm -rf out && mkdir -p out
for s in 01_cose_sign1.py 02_dsse_intoto.py 04_key_relative.py; do
  .venv/bin/python "$s"
  echo
done
.venv/bin/python 03_slsa_provenance.py "$@"
echo

# record what produced these bytes, so the library record can cite it.
{
  .venv/bin/python --version
  .venv/bin/pip freeze
} >out/ENVIRONMENT.txt
(cd out && sha256sum -- *.bin *.json >SHA256SUMS)
echo "wrote out/ENVIRONMENT.txt and out/SHA256SUMS"
