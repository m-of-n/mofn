"""Fixtures for the rejecting decoders — the evidence for #73.

SPIKE. Run it:  python3 prototype/statements/test_decode.py

Three things are tested, in order of what they are worth:

 1. EVERY non-canonical input is REJECTED, one fixture per rule, each naming
    the rule it exercises. A decoder that accepts quietly is the failure mode
    condition (2) exists to prevent, so the negative fixtures are the point
    and the positive ones are the control.
 2. The decoders are SINGLE-PASS: bytes consumed == len(input) on every
    success. Read each byte once, never twice, never seek back.
 3. The decoders DO NOT RE-ENCODE: neither module imports an encoder. This is
    checked against the source text AND in a fresh interpreter, because the
    claim "no re-encoding" is the one the falsifier turns on and an assertion
    in prose is not evidence.
"""
from __future__ import annotations
import os, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import csexp
import rcbor                      # the ENCODER, used only to build positives
import rcbor_decode as rc

fails: list[str] = []


def reject(mod, name, buf, rule):
    try:
        mod.loads(buf)
    except mod.NotCanonical as e:
        print(f"  reject  {name:<34} {rule}")
        print(f"          └─ {str(e)[:96]}")
        return
    except RecursionError:
        print(f"  reject  {name:<34} {rule} (RecursionError)")
        fails.append(f"{name}: rejected via RecursionError, not NotCanonical")
        return
    fails.append(f"{name}: ACCEPTED non-canonical input ({rule})")
    print(f"  ACCEPT! {name:<34} {rule}   <-- FAILURE")


def accept(mod, name, buf, want=None):
    try:
        got = mod.loads(buf)
    except mod.NotCanonical as e:
        fails.append(f"{name}: rejected a canonical input: {e}")
        print(f"  REJECT! {name:<34} <-- FAILURE: {e}")
        return
    if want is not None and got != want:
        fails.append(f"{name}: decoded to {got!r}, wanted {want!r}")
        print(f"  WRONG!  {name:<34} {got!r} != {want!r}")
        return
    n = mod.passes(buf)
    if n != len(buf):
        fails.append(f"{name}: read {n} bytes of {len(buf)} — not single-pass")
        print(f"  PASSES! {name:<34} read {n} of {len(buf)}  <-- FAILURE")
        return
    print(f"  accept  {name:<34} {len(buf):>3}B, read once")


# ======================================================================
print("\ncanonical S-expressions (RFC 9804 §7.2) — DEC-002 option 1")
print("accepted:")
accept(csexp, "atom", b"3:abc", csexp.Atom(b"abc"))
accept(csexp, "empty atom", b"0:", csexp.Atom(b""))
accept(csexp, "list", b"(1:a1:b)", [csexp.Atom(b"a"), csexp.Atom(b"b")])
accept(csexp, "empty list", b"()", [])
accept(csexp, "nested", b"(1:a(1:b1:c))")
accept(csexp, "display hint", b"[10:text/plain]5:hello",
       csexp.Atom(b"hello", b"text/plain"))
# §6.2's own example: the payload holds ) ] } > and needs no escaping.
accept(csexp, "RFC §6.2 no-escape case", b"10:foo)]}>bar")
accept(csexp, "length 2 digits", b"10:0123456789")

print("rejected:")
reject(csexp, "leading zero in length", b"03:abc",
       "decimal = %x30 / (%x31-39 *DIGIT) — ungrammatical, not merely non-canonical")
reject(csexp, "token form", b"abc", "advanced-only: §7.1 token")
reject(csexp, "quoted-string form", b'"abc"', "advanced-only: §7.1 quoted-string")
reject(csexp, "hexadecimal form", b"#616263#", "advanced-only: §7.1 hexadecimal")
reject(csexp, "base-64 form", b"|YWJj|", "advanced-only: §7.1 base-64")
reject(csexp, "base-64 brace wrapper", b"{KDE6YTE6YjE6Yyk=}",
       "§6.3 basic transport — a SECOND spelling of one value; rejected so (1) holds")
reject(csexp, "whitespace between items", b"(1:a 1:b)",
       "canonical grammar has no whitespace production")
reject(csexp, "leading whitespace", b" 3:abc", "ditto")
reject(csexp, "length runs past end", b"9:abc", "truncated")
reject(csexp, "truncated length", b"3", "truncated")
reject(csexp, "missing colon", b"3abc", "verbatim = decimal ':' *OCTET")
reject(csexp, "unterminated list", b"(1:a", "no ')'")
reject(csexp, "trailing bytes", b"3:abcX", "exactly one S-expression")
reject(csexp, "stray close paren", b")", "not a c-sexp")
reject(csexp, "hint not closed", b"[4:text5:hello", "expected ']'")
reject(csexp, "deep nesting", b"(" * 300 + b")" * 300, "depth guard")

# ======================================================================
print("\nreduced CBOR (RFC 8949 §4.2 + ARCH-0002 P1) — DEC-002 option 5")
print("accepted:")
for label, value in [
    ("int small", 23), ("int 1-byte head", 24), ("int 2-byte head", 256),
    ("negative", -1), ("bytes", b"\x01\x02"), ("text", "hello"),
    ("empty text", ""), ("array", [1, 2, 3]), ("empty array", []),
    ("map", {"a": 1, "b": 2}), ("empty map", {}),
    ("false", False), ("true", True), ("null", None),
    ("nested", {"z": [1, {"a": b"\xff"}], "a": "x"}),
    ("unicode text", "Ünïcødé ✓"),
]:
    accept(rc, label, rcbor.encode(value), value)

print("rejected:")
# Built by hand: these are precisely the things rcbor.py cannot emit.
reject(rc, "map keys out of order", bytes([0xA2]) + rcbor.encode("b") + rcbor.encode(2)
       + rcbor.encode("a") + rcbor.encode(1),
       "THE CRUX — ascending by ENCODED key bytes, checked against the input slices")
reject(rc, "duplicate map key", bytes([0xA2]) + rcbor.encode("a") + rcbor.encode(1)
       + rcbor.encode("a") + rcbor.encode(2),
       "same check: strictly ascending subsumes duplicates")
reject(rc, "non-smallest head (24 in 2B)", bytes([0x19, 0x00, 0x18]),
       "smallest-form integer head — local, no encoder")
reject(rc, "non-smallest head (0 in 1B)", bytes([0x18, 0x00]), "ditto")
reject(rc, "non-smallest head (2^16-1 in 4B)", bytes([0x1A, 0x00, 0x00, 0xFF, 0xFF]), "ditto")
reject(rc, "non-smallest bstr length", bytes([0x58, 0x01, 0x41]), "heads are checked everywhere")
reject(rc, "indefinite-length array", bytes([0x9F, 0x01, 0xFF]), "definite lengths only")
reject(rc, "indefinite-length bstr", bytes([0x5F, 0x41, 0x41, 0xFF]), "ditto")
reject(rc, "tag", bytes([0xC0]) + rcbor.encode("x"), "major type 6 excluded — R-M-12")
reject(rc, "float16", bytes([0xF9, 0x00, 0x00]), "no floats")
reject(rc, "float32", bytes([0xFA, 0, 0, 0, 0]), "no floats")
reject(rc, "float64", bytes([0xFB, 0, 0, 0, 0, 0, 0, 0, 0]), "no floats")
reject(rc, "undefined", bytes([0xF7]), "outside the profile")
reject(rc, "simple value 0", bytes([0xE0]), "outside the profile")
reject(rc, "reserved ai 28", bytes([0x1C]), "reserved")
reject(rc, "invalid UTF-8 in text", bytes([0x62, 0xFF, 0xFE]), "tstr must be UTF-8")
reject(rc, "truncated array", bytes([0x83, 0x01]), "truncated")
reject(rc, "trailing bytes", rcbor.encode(1) + b"\x01", "exactly one item")
reject(rc, "array as map key", bytes([0xA1, 0x80, 0x01]), "key must be int/bytes/str")
reject(rc, "deep nesting", bytes([0x81]) * 300 + bytes([0x01]), "depth guard")

# ======================================================================
print("\nno re-encoding — the claim the falsifier turns on")
# Parsed with `ast`, not grepped. An earlier draft scanned lines for a leading
# "import", and csexp.py's own docstring — which explains that it does not
# import an encoder — tripped it. A test that reads prose as code is a test
# that will eventually lie in the other direction too.
import ast
for mod in ("csexp.py", "rcbor_decode.py"):
    tree = ast.parse((HERE / mod).read_text())
    bad = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            bad += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module != "__future__":
            bad.append(node.module or "?")
    if bad:
        fails.append(f"{mod} imports {bad}")
        print(f"  FAIL    {mod} imports {bad}")
    else:
        print(f"  ok      {mod:<20} imports no module at all")

probe = ("import sys; sys.path.insert(0, %r); import rcbor_decode, csexp; "
         "print('rcbor' in sys.modules)" % str(HERE))
out = subprocess.run([sys.executable, "-I", "-c", probe],
                     capture_output=True, text=True).stdout.strip()
if out != "False":
    fails.append(f"encoder reachable from the decoders: probe said {out!r}")
    print(f"  FAIL    encoder module loaded transitively ({out!r})")
else:
    print("  ok      fresh interpreter: decoders load without the encoder")

# ======================================================================
print()
if fails:
    print(f"FAILED — {len(fails)}")
    for f in fails:
        print(f"  - {f}")
    sys.exit(1)
print("All fixtures behaved. Canonicality was decided by parsing alone:")
print("  - no re-encoding, no second validation pass, no normalisation")
print("  - every accepted input read exactly once, front to back")
sys.exit(0)
