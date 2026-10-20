"""mofn#13 sample 3 — a *real* SLSA v1 provenance, kept byte for byte.

Two sources, in the order #13 asks for:

  --github OWNER/REPO FILE   `gh attestation download` on a release asset you
                             have downloaded. Needs an authenticated `gh`, so
                             run this one on your own machine.
  --npm NAME@VERSION         the npm registry's public attestation endpoint —
                             no auth, and the provenance there is produced by
                             GitHub Actions with the SLSA v1 predicate. Use it
                             when `gh` is not authenticated.

Either way the result is a Sigstore bundle wrapping a DSSE envelope wrapping an
in-toto Statement. We unwrap all three and keep every layer.

What is checked here is narrow, and the script says so rather than implying
more: when the bundle carries a certificate, the DSSE signature is checked
against that leaf's public key over the PAE we rebuilt. That proves the .pae
file is the exact signed input. It does NOT check the Fulcio chain, the
certificate identity, or the Rekor entry — use `gh attestation verify` or
`slsa-verifier` for that and keep the output beside the bytes.
"""

import argparse
import base64
import hashlib
import json
import pathlib
import subprocess
import sys
import urllib.parse
import urllib.request

from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.asymmetric import ec

from common import OUT, emit, pae

NPM_ATTESTATIONS = "https://registry.npmjs.org/-/npm/v1/attestations/{}"


def fetch_npm(spec: str) -> list:
    # A scoped name's "/" must be escaped; the "@" separators must not.
    url = NPM_ATTESTATIONS.format(urllib.parse.quote(spec, safe="@"))
    print(f"  GET {url}")
    with urllib.request.urlopen(url, timeout=30) as r:
        raw = r.read()
    # The registry nests each bundle inside its own JSON document, so the
    # response body is the only thing here that is really "as received".
    emit("slsa_provenance.npm_response", raw, pretty_json=True)
    return [a["bundle"] for a in json.loads(raw).get("attestations", [])]


def fetch_github(repo: str, path: str) -> list:
    path = pathlib.Path(path).resolve()  # gh runs in OUT, not in our cwd
    if not path.is_file():
        sys.exit(f"{path}: no such file — download the release asset first")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    OUT.mkdir(exist_ok=True)
    cmd = ["gh", "attestation", "download", str(path), "-R", repo]
    print("  $ " + " ".join(cmd))
    out = subprocess.run(cmd, capture_output=True, text=True, cwd=OUT)
    if out.returncode != 0:
        hint = (
            f"needs an authenticated gh with access to {repo}, and an "
            f"attestation for this exact file; fall back to --npm"
        )
        if 'unknown command "attestation"' in out.stderr:
            hint = "gh is too old: `gh attestation` needs gh >= 2.49; upgrade gh"
        sys.exit(f"gh failed: {out.stderr.strip()}\n({hint})")
    # gh writes sha256:<digest>.jsonl (":" becomes "-" on Windows), one
    # bundle per line, each line exactly as the attestation API returned it.
    jsonl = next(OUT.glob(f"sha256?{digest}.jsonl"))
    return [json.loads(line) for line in jsonl.read_text().splitlines() if line.strip()]


def leaf_certificate(bundle: dict):
    vm = bundle.get("verificationMaterial", {})
    if "certificate" in vm:  # bundle v0.3
        der = vm["certificate"]["rawBytes"]
    elif "x509CertificateChain" in vm:  # bundle v0.1 / v0.2
        der = vm["x509CertificateChain"]["certificates"][0]["rawBytes"]
    else:
        return None
    return x509.load_der_x509_certificate(base64.b64decode(der))


def unwrap(bundle: dict, tag: str):
    env = bundle["dsseEnvelope"]
    body = base64.b64decode(env["payload"])
    stmt = json.loads(body)

    emit(
        tag + ".bundle", json.dumps(bundle, indent=2).encode() + b"\n", pretty_json=True
    )
    emit(
        tag + ".envelope", json.dumps(env, indent=2).encode() + b"\n", pretty_json=True
    )
    emit(tag + ".statement", body, pretty_json=True)  # the signed octets
    emit(tag + ".pae", pae(env["payloadType"], body))

    print(f"  _type         {stmt.get('_type')}")
    print(f"  predicateType {stmt.get('predicateType')}")
    print(f"  subject       {[s.get('name') for s in stmt.get('subject', [])]}")

    cert = leaf_certificate(bundle)
    if cert is None:
        hint = bundle.get("verificationMaterial", {}).get("publicKey", {})
        print(
            f"  signed by a bare key {hint.get('hint', '?')!r}, not a "
            "certificate; not checked"
        )
        return

    emit(tag + ".leaf_cert", cert.public_bytes(Encoding.DER))
    sig = base64.b64decode(env["signatures"][0]["sig"])
    try:
        cert.public_key().verify(
            sig, pae(env["payloadType"], body), ec.ECDSA(hashes.SHA256())
        )
        print("  signature matches the leaf certificate over the rebuilt PAE: yes")
    except InvalidSignature:
        sys.exit("  signature does NOT match the leaf certificate")
    print(
        "  chain / identity / Rekor NOT verified here — run "
        "`gh attestation verify` or `slsa-verifier` and keep the output"
    )


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--npm", metavar="NAME@VERSION", default="sigstore@2.3.1")
    g.add_argument("--github", nargs=2, metavar=("OWNER/REPO", "FILE"))
    args = ap.parse_args()

    print("sample 3 — real SLSA v1 provenance")
    if args.github:
        bundles = fetch_github(*args.github)
        src = args.github[0]
    else:
        bundles = fetch_npm(args.npm)
        src = "npm:" + args.npm
    if not bundles:
        sys.exit("no attestations found")

    print(f"  {len(bundles)} attestation(s) from {src}")
    for i, b in enumerate(bundles):
        if "dsseEnvelope" not in b:
            print(f" [{i}] not a DSSE bundle (messageSignature); skipped")
            continue
        stmt = json.loads(base64.b64decode(b["dsseEnvelope"]["payload"]))
        pt = stmt.get("predicateType", "")
        slug = "slsa" if "slsa.dev/provenance" in pt else f"other{i}"
        print(f" [{i}] {pt}")
        unwrap(b, f"slsa_provenance_{slug}")


if __name__ == "__main__":
    main()
