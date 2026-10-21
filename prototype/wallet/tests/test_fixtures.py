"""The fixtures are copies of the published vectors, never edited by hand."""

import subprocess
import sys

from conftest import FIXTURES


def test_fixtures_match_vectors_json():
    p = subprocess.run(
        [sys.executable, str(FIXTURES / "sync.py"), "--check"],
        capture_output=True,
        text=True,
    )
    assert p.returncode == 0, p.stdout
