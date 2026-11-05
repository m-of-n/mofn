"""The CLI end to end: one wallet per role, and only the files
handed over move between them (#65). Runs under both codecs and compares
`check` with the golden verdicts in fixtures/golden/."""

import json
import os
import stat
import subprocess
import sys

import pytest

from conftest import FIXTURES, VECTORS, WALLET, run_mofn

PASS = "correct horse battery staple"
DV1 = FIXTURES / "dv-1.def"
GOLDEN = FIXTURES / "golden"
ARTIFACT = (FIXTURES / "artifact.bin").read_bytes()


def ok(p):
    assert p.returncode == 0, p.stderr + p.stdout
    return p


@pytest.fixture(scope="module", params=["ksa-cbor", "review-yaml"])
def world(request, tmp_path_factory):
    codec = request.param
    suffix = ".stmt" if codec == "ksa-cbor" else ".stmt.yaml"
    root = tmp_path_factory.mktemp(codec)
    hand = root / "handover"
    hand.mkdir()
    (root / "app.pyz").write_bytes(ARTIFACT)

    def m(wallet, *args, stdin="", cwd=root):
        return run_mofn(
            "--wallet", root / wallet, "--codec", codec, *args, stdin=stdin, cwd=cwd
        )

    out = {"codec": codec, "root": root, "m": m, "logs": []}
    ok(m("issuer", "init"))
    out["logs"].append(
        ok(
            m(
                "issuer",
                "key",
                "gen",
                "build",
                "--controller",
                "service",
                "--passphrase-stdin",
                "-o",
                hand / "build.pub.stmt",
                stdin=PASS + "\n",
            )
        )
    )
    out["logs"].append(
        ok(
            m(
                "issuer",
                "make",
                "--as",
                "build",
                "--subject",
                "app.pyz",
                "--def",
                DV1,
                "--type",
                "build-provenance",
                "--value",
                "reproducible",
                "-o",
                hand / "prov.stmt",
                "--passphrase-stdin",
                stdin=PASS + "\n",
            )
        )
    )
    (hand / "app.pyz").write_bytes(ARTIFACT)

    for wallet in ("rp", "rp-unknown"):
        ok(m(wallet, "init"))
        ok(
            m(
                wallet,
                "key",
                "gen",
                "rp",
                "--passphrase-stdin",
                "-o",
                root / f"{wallet}.pub",
                stdin=PASS + "\n",
            )
        )
        ok(
            m(
                wallet,
                "key",
                "import",
                FIXTURES / f"tv-1-alice.pub{suffix}",
                "--label",
                "Alice (definer)",
            )
        )
    out["logs"].append(
        ok(
            m(
                "rp",
                "key",
                "import",
                hand / "build.pub.stmt",
                "--label",
                "release machine",
            )
        )
    )

    def chk(wallet, artifact="app.pyz", *extra):
        return m(
            wallet,
            "check",
            "prov.stmt",
            FIXTURES / f"tv-3-define{suffix}",
            "--artifact",
            artifact,
            "--def",
            DV1,
            *extra,
            cwd=hand,
        )

    out["unauthorized"] = chk("rp")
    out["unknown-key"] = chk("rp-unknown")
    ok(
        m(
            "rp",
            "root",
            "add",
            "release machine",
            "--as",
            "rp",
            "--def",
            DV1,
            "--type",
            "build-provenance",
            "--values",
            "reproducible,attested",
        )
    )
    out["green"] = chk("rp")
    out["json"] = chk("rp", "app.pyz", "--format", "json")
    (hand / "bad.pyz").write_bytes(b"X" + ARTIFACT[1:])
    out["tampered"] = chk("rp", "bad.pyz")
    out["expired"] = chk("rp", "app.pyz", "--at", "2099-01-01T00:00:00Z")
    data = (hand / "prov.stmt").read_bytes()
    if codec == "ksa-cbor":
        data = data[:-1] + bytes([data[-1] ^ 0x01])
    else:
        data = data.replace(b"value: reproducible", b"value: attested")
    (hand / "changed.stmt").write_bytes(data)
    out["statement-changed"] = m(
        "rp",
        "check",
        "changed.stmt",
        FIXTURES / f"tv-3-define{suffix}",
        "--artifact",
        "app.pyz",
        "--def",
        DV1,
        cwd=hand,
    )
    return out


@pytest.mark.parametrize(
    "case,code",
    [
        ("green", 0),
        ("unauthorized", 1),
        ("unknown-key", 1),
        ("tampered", 1),
        ("statement-changed", 3),
        ("expired", 1),
    ],
)
def test_golden_verdicts(world, case, code):
    p = world[case]
    assert p.stdout == (GOLDEN / f"{case}.txt").read_text(encoding="utf-8")
    assert p.returncode == code, p.stderr


def test_json_verdict(world):
    j = json.loads(world["json"].stdout)
    assert j["answer"] == "yes"
    assert j["verdict"]["acceptance"] == {
        "result": "pass",
        "sentence": "no template is named",
    }
    assert j["because"][0]["path"][0]["key"] == "release machine"


def test_handover_file_is_in_the_codec_form(world):
    data = (world["root"] / "handover" / "prov.stmt").read_bytes()
    assert data.startswith(b"kind: attestation\n") == (world["codec"] == "review-yaml")


def test_tampered_statement_exits_3(world):
    hand = world["root"] / "handover"
    data = bytearray((hand / "prov.stmt").read_bytes())
    if world["codec"] == "ksa-cbor":
        data[-1] ^= 0x01
    else:
        data = bytearray(
            bytes(data).replace(b"value: reproducible", b"value: attested")
        )
    (hand / "forged.stmt").write_bytes(bytes(data))
    p = world["m"](
        "rp",
        "check",
        "forged.stmt",
        FIXTURES / "dv-1.def",
        "--artifact",
        "app.pyz",
        "--def",
        DV1,
        cwd=hand,
    )
    assert p.returncode == 3
    assert p.stdout.startswith(
        "integrity      fail           forged.stmt is invalid at V4 (signature)"
    )


def test_passphrase_never_leaves_the_prompt(world):
    for p in world["logs"]:
        assert PASS not in p.stdout + p.stderr
    for f in world["root"].rglob("*"):
        if f.is_file():
            assert PASS.encode() not in f.read_bytes()


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="NTFS has no POSIX mode bits; on Windows the key is protected by "
    "Argon2id + SecretBox at rest and by the profile's ACL",
)
def test_key_permissions(world):
    keys = list((world["root"] / "issuer" / "personas").glob("*/keys"))
    assert len(keys) == 1
    assert stat.S_IMODE(keys[0].stat().st_mode) == 0o700
    (key,) = keys[0].glob("*.key")
    assert stat.S_IMODE(key.stat().st_mode) == 0o600


@pytest.fixture
def wallet(tmp_path):
    w = tmp_path / "w"
    ok(run_mofn("--wallet", w, "init"))
    ok(
        run_mofn(
            "--wallet",
            w,
            "key",
            "gen",
            "me",
            "--passphrase-stdin",
            "-o",
            tmp_path / "me.pub",
            stdin=PASS + "\n",
        )
    )
    (tmp_path / "file").write_bytes(ARTIFACT)
    return tmp_path, w


def test_init_never_overwrites(wallet):
    _, w = wallet
    p = run_mofn("--wallet", w, "init")
    assert p.returncode == 2 and "already holds a wallet" in p.stderr


def test_wallet_from_environment(wallet):
    _, w = wallet
    env = dict(os.environ, MOFN_WALLET=str(w))
    p = subprocess.run(
        [sys.executable, str(WALLET / "mofn"), "init"],
        env=env,
        capture_output=True,
        text=True,
    )
    assert p.returncode == 2 and str(w) in p.stderr


def test_wrong_passphrase(wallet):
    tmp, w = wallet
    p = run_mofn(
        "--wallet",
        w,
        "make",
        "--as",
        "me",
        "--subject",
        tmp / "file",
        "--def",
        DV1,
        "--type",
        "build-provenance",
        "--value",
        "reproducible",
        "--passphrase-stdin",
        stdin="nope\n",
    )
    assert p.returncode == 2 and "wrong passphrase" in p.stderr


def test_make_refuses_a_typo(wallet):
    tmp, w = wallet
    p = run_mofn(
        "--wallet",
        w,
        "make",
        "--as",
        "me",
        "--subject",
        tmp / "file",
        "--def",
        DV1,
        "--type",
        "build-provenance",
        "--value",
        "reproducable",
        "--passphrase-stdin",
        stdin=PASS + "\n",
    )
    assert (
        p.returncode == 2 and "allowed: reproducible, attested, unverified" in p.stderr
    )
    assert len(list((w / "statements").glob("*.stmt"))) == 1


def test_empty_passphrase_is_refused(tmp_path):
    w = tmp_path / "w"
    ok(run_mofn("--wallet", w, "init"))
    p = run_mofn("--wallet", w, "key", "gen", "me", "--passphrase-stdin", stdin="\n")
    assert p.returncode == 2 and "empty" in p.stderr


def test_duplicate_label_is_refused(wallet):
    tmp, w = wallet
    p = run_mofn(
        "--wallet",
        w,
        "key",
        "gen",
        "me",
        "--passphrase-stdin",
        "-o",
        tmp / "x",
        stdin=PASS + "\n",
    )
    assert p.returncode == 2 and "already exists" in p.stderr


def test_only_a_person_or_organisation_accepts_an_anchor(wallet):
    tmp, w = wallet
    ok(
        run_mofn(
            "--wallet",
            w,
            "key",
            "gen",
            "bot",
            "--controller",
            "agent",
            "--passphrase-stdin",
            "-o",
            tmp / "bot.pub",
            stdin=PASS + "\n",
        )
    )
    ok(
        run_mofn(
            "--wallet",
            w,
            "key",
            "import",
            FIXTURES / "tv-1-alice.pub.stmt",
            "--label",
            "Alice",
        )
    )
    p = run_mofn(
        "--wallet",
        w,
        "root",
        "add",
        "Alice",
        "--as",
        "bot",
        "--def",
        DV1,
        "--type",
        "build-provenance",
    )
    assert p.returncode == 2 and "only a person or an organisation" in p.stderr
    ok(
        run_mofn(
            "--wallet",
            w,
            "root",
            "add",
            "Alice",
            "--as",
            "me",
            "--def",
            DV1,
            "--type",
            "build-provenance",
        )
    )


def test_root_add_needs_a_known_key_and_a_real_value(wallet):
    _, w = wallet
    p = run_mofn(
        "--wallet",
        w,
        "root",
        "add",
        "nobody",
        "--as",
        "me",
        "--def",
        DV1,
        "--type",
        "build-provenance",
    )
    assert p.returncode == 2 and "no persona" in p.stderr
    ok(
        run_mofn(
            "--wallet",
            w,
            "key",
            "import",
            FIXTURES / "tv-1-alice.pub.stmt",
            "--label",
            "Alice",
        )
    )
    p = run_mofn(
        "--wallet",
        w,
        "root",
        "add",
        "Alice",
        "--as",
        "me",
        "--def",
        DV1,
        "--type",
        "build-provenance",
        "--values",
        "reproducible,maybe",
    )
    assert p.returncode == 2 and "'maybe' is not a value" in p.stderr


def test_key_import_refuses_other_kinds(wallet):
    _, w = wallet
    p = run_mofn("--wallet", w, "key", "import", FIXTURES / "tv-3-define.stmt")
    assert p.returncode == 2


def test_key_import_refuses_a_small_order_key(wallet, tmp_path):
    bad = tmp_path / "n4.stmt"
    bad.write_bytes(bytes.fromhex(VECTORS["negative"]["N-4"]["envelope"]))
    p = run_mofn("--wallet", wallet[1], "key", "import", bad)
    assert p.returncode == 2 and "V3" in p.stderr


@pytest.mark.parametrize(
    "codec,suffix", [("ksa-cbor", ".stmt"), ("review-yaml", ".stmt.yaml")]
)
def test_show_a_statement(codec, suffix):
    p = ok(run_mofn("--codec", codec, "show", FIXTURES / f"tv-4-attestation{suffix}"))
    head, statement = p.stdout.split("\n\nstatement")
    assert "suite  ksa-ed25519-sha256" in head and "pub    absent" in head
    assert f"says   0x{VECTORS['keys']['alice']['kid']}" in head
    assert f"sig    0x{VECTORS['positive']['TV-4']['sig']}" in head
    assert "kind: attestation" in statement and "value: reproducible" in statement


def test_show_a_definition():
    p = ok(run_mofn("show", DV1))
    assert p.stdout.startswith(f"definition {VECTORS['definitions']['DV-1']['id']}\n")
    assert "base: enum" in p.stdout and "function: attestation" in p.stdout


def test_show_refuses_what_is_not_a_statement():
    p = run_mofn("show", FIXTURES / "artifact.bin")
    assert p.returncode == 2 and "mofn: error:" in p.stderr


def test_root_list_prints_what_root_add_wrote(wallet):
    _, w = wallet
    p = ok(run_mofn("--wallet", w, "root", "list"))
    assert "no anchors in context default" in p.stdout
    ok(
        run_mofn(
            "--wallet",
            w,
            "key",
            "import",
            FIXTURES / "tv-1-alice.pub.stmt",
            "--label",
            "Alice",
        )
    )
    added = ok(
        run_mofn(
            "--wallet",
            w,
            "root",
            "add",
            "Alice",
            "--as",
            "me",
            "--def",
            DV1,
            "--type",
            "build-provenance",
            "--values",
            "reproducible",
            "--note",
            "release builds only",
        )
    )
    p = ok(run_mofn("--wallet", w, "root", "list"))
    line, note = p.stdout.splitlines()
    assert line.startswith(added.stdout.strip() + " on ")
    assert "build-provenance ∈ {reproducible}" in line
    assert note == "  note: release builds only"
    p = ok(run_mofn("--wallet", w, "root", "list", "--context", "other"))
    assert "no anchors in context other" in p.stdout


@pytest.mark.parametrize("context", ["../../../escaped", "a/b", "Default", ""])
def test_context_must_be_a_name(wallet, context):
    _, w = wallet
    ok(
        run_mofn(
            "--wallet",
            w,
            "key",
            "import",
            FIXTURES / "tv-1-alice.pub.stmt",
            "--label",
            "Alice",
        )
    )
    p = run_mofn(
        "--wallet",
        w,
        "root",
        "add",
        "Alice",
        "--as",
        "me",
        "--def",
        DV1,
        "--type",
        "build-provenance",
        "--context",
        context,
    )
    assert p.returncode == 2 and "is not a name" in p.stderr
    assert not list(w.parent.rglob("escaped*"))
    assert not list(w.rglob("trusts/*"))
    p = run_mofn("--wallet", w, "root", "list", "--context", context)
    assert p.returncode == 2 and "is not a name" in p.stderr


def test_check_refuses_a_context_that_is_not_a_name(tmp_path):
    w = tmp_path / "w"
    ok(run_mofn("--wallet", w, "init"))
    p = run_mofn(
        "--wallet",
        w,
        "check",
        FIXTURES / "tv-3-define.stmt",
        "--artifact",
        FIXTURES / "artifact.bin",
        "--def",
        DV1,
        "--context",
        "../x",
    )
    assert p.returncode == 2 and "is not a name" in p.stderr
