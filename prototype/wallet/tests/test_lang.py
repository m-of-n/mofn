"""`--lang` (mofn#66): the vocabulary's words in the language asked for.

It changes only text the definition supplies. It never changes a result, an
exit code, or the engine's own words.
"""

import pytest

from conftest import FIXTURES, run_mofn
from engine import render

M = {"en": "Reviewed", "es": "Revisado", "pt-BR": "Revisado (BR)"}


@pytest.mark.parametrize(
    "want,text",
    [
        (None, "Reviewed"),
        ("es", "Revisado"),
        ("es-MX", "Revisado"),          # RFC 4647 §3.4: drop the last subtag
        ("pt-BR", "Revisado (BR)"),
        ("pt", "Reviewed"),             # lookup never widens pt to pt-BR
        ("fr", "Reviewed"),             # absent: English
    ],
)
def test_lookup(want, text):
    assert render.lang(M, want) == text


def test_without_english_the_first_tag():
    assert render.lang({"fr": "Revu", "de": "Geprüft"}, "es") == "Geprüft"


def test_a_tag_not_in_canonical_case_is_refused():
    p = run_mofn("--lang", "ES", "hash", FIXTURES / "artifact.bin")
    assert p.returncode == 2
    assert "not a language tag in canonical case" in p.stderr


def test_dv1_sentence_in_spanish_and_its_fallback():
    from engine import definition as defs
    from engine.verifier import verify
    from conftest import envelope, keystore

    d = defs.load((FIXTURES / "dv-1.def").read_bytes())
    s = verify(envelope("TV-4"), keystore()).statement
    assert render.sentence(d, s, {}, "es").endswith(
        "fue compilado de forma reproducible desde fuentes publicadas."
    )
    # DV-1 gives `attested` no Spanish: its words fall back to English.
    assert render.value_text(d, "build-provenance", "attested", 3, "es") == (
        "built by an attested pipeline"
    )
