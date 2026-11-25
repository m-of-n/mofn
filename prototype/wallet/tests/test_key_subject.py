"""`make` and `check` about a key (W-8, mofn#180).

A statement's subject may be a key: `this = [1, kid]`, SPEC-0002 §7.2 target
type 1. The wire form is not new — `KIND_TARGETS[4]` is every target type, and
TV-13's own note in the published vectors reads *"attestation about a KEY"*.
What was missing was a way to make or check one, which is how a persona's
received tags are written.

The cases run over TV-12 (Alice defines DV-2, `names 1`) and TV-13 (Alice says
Bob's key has the name "fred"). Neither carries `not-on-or-after`, so the
goldens never expire, and every key in them is a vector key, so they are
stable (the rule `test_associations.py` states).

SPEC-0004 §10.4 conditions integrity's comparison clause on a digest target:
with a key subject there is no copy of the relying party's to compare, so the
line reports verification alone. Whether any statement is about that key is
authorization's and acceptance's question, which §10.4 assigns to them.
"""

import json

import pytest

from conftest import FIXTURES, VECTORS, run_mofn

PASS = "key-subject test passphrase, not a secret"
GOLDEN = FIXTURES / "golden"
BOB = VECTORS["keys"]["bob"]["kid"]
ALICE = VECTORS["keys"]["alice"]["kid"]


def ok(p):
    assert p.returncode == 0, p.stderr + p.stdout
    return p


@pytest.fixture(scope="module", params=["ksa-cbor", "review-yaml"])
def rp(request, tmp_path_factory):
    """A relying party that knows Alice and trusts her about `name`."""
    codec = request.param
    suffix = ".stmt" if codec == "ksa-cbor" else ".stmt.yaml"
    root = tmp_path_factory.mktemp("key-subject-" + codec)

    def m(*args, stdin=""):
        return run_mofn("--wallet", root, "--codec", codec, *args, stdin=stdin)

    ok(m("init"))
    ok(m("key", "gen", "me", "--passphrase-stdin", stdin=PASS + "\n"))
    ok(m("key", "import", FIXTURES / f"tv-1-alice.pub{suffix}", "--label", "Alice"))
    ok(m("root", "add", "Alice", "--as", "me", "--def", FIXTURES / "dv-2.def",
         "--type", "name"))

    handed = [FIXTURES / f"tv-13-name{suffix}", FIXTURES / f"tv-12-define-names{suffix}"]

    def check(*extra):
        p = m("check", *handed, "--def", FIXTURES / "dv-2.def", *extra)
        return p.returncode, p.stdout

    return {
        "m": m,
        "suffix": suffix,
        "root": root,
        "key-subject": check("--subject-key", BOB),
        "key-subject-other": check("--subject-key", ALICE),
        "json": m("check", *handed, "--def", FIXTURES / "dv-2.def",
                  "--subject-key", BOB, "--format", "json"),
    }


@pytest.mark.parametrize("case,code", [("key-subject", 0), ("key-subject-other", 1)])
def test_golden_verdicts(rp, case, code):
    got, out = rp[case]
    assert out == (GOLDEN / f"{case}.txt").read_text(encoding="utf-8")
    assert got == code


def test_integrity_reports_verification_only(rp):
    _, out = rp["key-subject"]
    line = next(l for l in out.splitlines() if l.startswith("integrity"))
    assert "pass" in line and "no copy of yours to compare" in line
    # The digest wording must never reach a key ask.
    assert "your file" not in out


def test_a_statement_about_another_key_is_not_evaluated(rp):
    code, out = rp["key-subject-other"]
    for name in ("authorization", "acceptance"):
        line = next(l for l in out.splitlines() if l.startswith(name))
        assert "not evaluated" in line and "is about that key" in line
    assert "not the key you named" in out
    assert code == 1


def test_json_names_the_key_subject(rp):
    j = json.loads(rp["json"].stdout)
    assert j["answer"] == "yes"
    assert j["subject-target"] == "key"
    assert j["subject-key"] == BOB
    s = j["associations"][0]["subject"]
    assert s["target"] == "key" and s["kid"] == BOB and s["yours"] == BOB
    assert s["matches"] is True and s["digest"] is None
    want = json.loads((GOLDEN / "associations-key-subject.json").read_text(encoding="utf-8"))
    assert [{k: v for k, v in a.items() if k != "file"} for a in j["associations"]] == want


def test_a_digest_ask_keeps_the_shape_w5_fixed(rp):
    """The key form is additive: `target` is absent for a digest subject, so
    W-5's goldens and W-7's renderer do not move (DL-0049)."""
    m, suffix = rp["m"], rp["suffix"]
    artifact = rp["root"] / "app.bin"
    artifact.write_bytes((FIXTURES / "artifact.bin").read_bytes())
    p = m("check", FIXTURES / f"tv-4-attestation{suffix}", FIXTURES / f"tv-3-define{suffix}",
          "--artifact", artifact, "--def", FIXTURES / "dv-1.def", "--format", "json")
    j = json.loads(p.stdout)
    assert j["subject-target"] == "digest" and j["subject-key"] is None
    assert set(j["associations"][0]["subject"]) == {"digest", "yours", "matches"}


def test_make_signs_a_key_subject(rp):
    """A tag given to a key this wallet owns, then checked back."""
    m, suffix = rp["m"], rp["suffix"]
    ok(m("key", "gen", "bot", "--controller", "service", "--passphrase-stdin",
         stdin=PASS + "\n"))
    out = rp["root"] / f"tag{suffix}"
    ok(m("make", "--as", "me", "--subject-key", "bot", "--def", FIXTURES / "dv-2.def",
         "--type", "name", "--value", "buildbot", "--passphrase-stdin", "-o", out,
         stdin=PASS + "\n"))
    shown = ok(m("show", out)).stdout
    assert "this: {key:" in shown

    handed = [out, FIXTURES / f"tv-12-define-names{suffix}"]
    args = ["--subject-key", "bot", "--def", FIXTURES / "dv-2.def"]
    # Nobody is trusted about `name` by `me` yet for its own statements.
    assert m("check", *handed, *args, "--as", "me").returncode == 1
    ok(m("root", "add", "me", "--as", "me", "--def", FIXTURES / "dv-2.def", "--type", "name"))
    p = ok(m("check", *handed, *args, "--as", "me"))
    assert "answer: yes" in p.stdout


def test_subject_key_takes_a_label_a_prefix_or_a_full_kid(rp):
    m, suffix = rp["m"], rp["suffix"]
    handed = [FIXTURES / f"tv-13-name{suffix}", FIXTURES / f"tv-12-define-names{suffix}"]

    def answer(ref):
        p = m("check", *handed, "--def", FIXTURES / "dv-2.def", "--subject-key", ref)
        return p.returncode

    # Bob has no key-publish vector, so he can never be a persona here: only
    # the full-kid fallback can name him at all.
    assert answer(BOB) == 0 and answer(BOB[:8]) != 0
    assert answer("Alice") == answer(ALICE) == answer(ALICE[:8]) == 1


def test_an_unknown_reference_keeps_the_wallet_s_own_message(rp):
    p = rp["m"]("check", FIXTURES / "tv-13-name.stmt", "--def", FIXTURES / "dv-2.def",
                "--subject-key", "nobody")
    assert p.returncode == 2 and "no persona 'nobody' in this wallet" in p.stderr


def test_artifact_and_subject_key_are_exclusive(rp):
    m = rp["m"]
    both = m("check", FIXTURES / "tv-13-name.stmt", "--artifact", FIXTURES / "artifact.bin",
             "--subject-key", BOB, "--def", FIXTURES / "dv-2.def")
    assert both.returncode == 2 and "not allowed with" in both.stderr
    neither = m("check", FIXTURES / "tv-13-name.stmt", "--def", FIXTURES / "dv-2.def")
    assert neither.returncode == 2 and "one of the arguments" in neither.stderr
