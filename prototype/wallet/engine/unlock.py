"""Get the passphrase that opens a persona's private key.

v0 prompts on the terminal, or with `--passphrase-stdin` reads the first line
of standard input (#65-c2 A3). A caller in the same process, such as
`mofn run`, may hand it over directly. The passphrase is never a command-line
argument or an environment variable, and is never printed or logged.
"""

import getpass
import sys

from .errors import WalletError


def passphrase(
    from_stdin: bool, confirm: bool = False, given: bytes | None = None
) -> bytes:
    if given is not None:
        if not given:
            raise WalletError("the passphrase is empty")
        return bytes(given)
    if from_stdin:
        line = sys.stdin.readline()
        value = line[:-1] if line.endswith("\n") else line
        value = value[:-1] if value.endswith("\r") else value
    else:
        value = getpass.getpass("passphrase: ")
        if confirm and getpass.getpass("passphrase again: ") != value:
            raise WalletError("the passphrases differ")
    if not value:
        raise WalletError("the passphrase is empty")
    return value.encode("utf-8")
