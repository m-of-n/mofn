"""Open `mofn run` in a pseudo-terminal, open Learn, quit (DL-0043).

    python3 pty_run.py MOFN WALLET

The smoke test for a frozen build: Learn reads README.md and
fixtures/golden/ from inside the bundle, so a build missing its data files
fails here. POSIX only (the `pty` module). The test driver uses the runner's
Python; the build under test does not.
"""

import os
import pty
import select
import sys
import time


def drain(fd, seconds, out):
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        r, _, _ = select.select([fd], [], [], 0.1)
        if r:
            try:
                chunk = os.read(fd, 65536)
            except OSError:
                return False
            if not chunk:
                return False
            out.extend(chunk)
    return True


def send(fd, data):
    try:
        os.write(fd, data)
    except OSError:
        pass  # mofn already exited; its status is read below


def main(mofn, wallet):
    pid, fd = pty.fork()
    if pid == 0:
        os.environ["TERM"] = "xterm-256color"
        os.environ["COLUMNS"], os.environ["LINES"] = "120", "40"
        os.execv(mofn, [mofn, "--wallet", wallet, "run"])
    out = bytearray()
    drain(fd, 8, out)  # one-file builds unpack before they start
    send(fd, b"?")  # Learn, from any tab
    drain(fd, 3, out)
    send(fd, b"\x11")  # ctrl+q
    drain(fd, 5, out)
    deadline = time.monotonic() + 10
    while True:
        done, status = os.waitpid(pid, os.WNOHANG)
        if done:
            break
        if time.monotonic() > deadline:
            os.kill(pid, 9)
            sys.exit("pty_run: mofn run did not quit on ctrl+q")
        drain(fd, 0.2, out)
    text = out.decode("utf-8", "replace")
    code = os.waitstatus_to_exitcode(status)
    if code != 0 or "Traceback" in text:
        sys.stdout.write(text[-4000:])
        why = " with a traceback" if "Traceback" in text else ""
        sys.exit(f"pty_run: mofn run exited {code}{why}")
    print("pty_run: mofn run opened Learn and quit, exit 0")


if __name__ == "__main__":
    main(*sys.argv[1:3])
