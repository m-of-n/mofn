"""The example vocabulary shipped with mofn: DV-1, its author Alice's key
and define statement, and one statement of hers with the file it is about.

They are the published fixtures. `install` copies them into `example/`
next to the wallet, so the commands the forms show name files that exist
after mofn exits.
"""

import shutil
from pathlib import Path

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
ALICE = "Alice (definer)"


def names(suffix: str) -> dict[str, str]:
    return {
        "dv-1.def": "dv-1.def",
        f"alice.pub{suffix}": f"tv-1-alice.pub{suffix}",
        f"alice-define{suffix}": f"tv-3-define{suffix}",
        f"alice{suffix}": f"tv-4-attestation{suffix}",
        "artifact.bin": "artifact.bin",
    }


def folder(wallet: Path) -> Path:
    return wallet.parent / "example"


def path(wallet: Path, name: str) -> Path:
    return folder(wallet) / name


def installed(wallet: Path) -> bool:
    return path(wallet, "dv-1.def").is_file()


def install(wallet: Path, suffix: str) -> Path:
    dest = folder(wallet)
    dest.mkdir(parents=True, exist_ok=True)
    for mine, theirs in names(suffix).items():
        if not (dest / mine).exists():
            shutil.copyfile(FIXTURES / theirs, dest / mine)
    return dest


def is_example(wallet: Path, vocabulary: str) -> bool:
    try:
        return Path(vocabulary).resolve() == path(wallet, "dv-1.def").resolve()
    except OSError:
        return False
