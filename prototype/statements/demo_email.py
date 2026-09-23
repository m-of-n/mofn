#!/usr/bin/env python3
"""Alice, Bob, Carol, Dave — the sponsor's worked example, executable.

    python3 prototype/statements/demo_email.py

From the 2026-09-22 email. This is the canonical test of whether reduction
does what it is supposed to do, and it is deliberately the SMALLEST example
that needs every part: a trust root, a delegation of a different type, an
attestation, and a range that must still cover the value at the end.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from reduce import TrustRoot, Delegation, Attestation, reduce_chain, covers

Pa, Pb, Pc, Pd = "Pa(alice)", "Pb(bob)", "Pc(carol)", "Pd(dave)"


def rule(t):
    print(f"\n{'─' * 68}\n{t}\n{'─' * 68}")


rule("The setup")
print("""    Alice  Pa/Sa      trusted by the group for email in *@foo.com
    Bob    Pb/Sb      delegated by Alice
    Carol  Pc/Sc      introduces herself
    Dave   Pd/Sd      has to decide whether to believe her""")

# Dave's own policy. Unsigned — it is a decision he made, not a statement
# anyone made to him. This is why AclEntry has no speaker.
daves_roots = [TrustRoot(key=Pa, topic="email", range="*@foo.com")]

# Alice delegates. NOTE: a DIFFERENT TYPE from the email attestation itself.
alice_delegates = Delegation(speaker=Pa, subject=Pb, topic="email", range="*@foo.com")

# Bob attests. Carol carries this plus Alice's delegation when she introduces herself.
bob_attests = Attestation(speaker=Pb, subject=Pc, topic="email", value="c@foo.com")

rule("Dave's trust management — what a wallet holds")
for r in daves_roots:
    print(f"    I trust {r.key} for statements about {r.topic} in range '{r.range}'")
print("\n    Unsigned. Nobody said this TO Dave — he decided it.")
print("    That is the fixed floor: if a key could define its own trustworthiness,")
print("    there would be no floor at all.")

rule("What Carol presents when she introduces herself")
print(f"    I {Pb} say that {Pc} has name Carol and email c@foo.com      (created by Bob)")
print(f"    I {Pa} say that {Pb} can speak about email in '*@foo.com'    (created by Alice)")
print("\n    Two statements, two TYPES. The delegation is not an email attestation —")
print("    if it were, holding one would be indistinguishable from holding a claim,")
print("    and anyone could promote themselves.")

rule("Reduction — does Dave believe it?")
v = reduce_chain(bob_attests, [alice_delegates], daves_roots)
print(v.explain())

rule("Now the cases that must FAIL")

print("\n  1. Bob attests outside the delegated range")
bad = Attestation(speaker=Pb, subject=Pc, topic="email", value="carol@bar.com")
print(reduce_chain(bad, [alice_delegates], daves_roots).explain())

print("\n  2. Carol attests about herself — nobody delegated to her")
selfie = Attestation(speaker=Pc, subject=Pc, topic="email", value="c@foo.com")
print(reduce_chain(selfie, [alice_delegates], daves_roots).explain())

print("\n  3. Alice delegated only a narrower range than Bob then sub-delegates")
narrow_root = [TrustRoot(key=Pa, topic="email", range="*@eng.foo.com")]
print(reduce_chain(bob_attests, [alice_delegates], narrow_root).explain())

rule("And a chain two deep — Bob sub-delegates to Carol, narrowing")
bob_delegates = Delegation(speaker=Pb, subject=Pc, topic="email", range="*@foo.com")
carol_attests = Attestation(speaker=Pc, subject="Pe(erin)", topic="email", value="erin@foo.com")
print(reduce_chain(carol_attests, [alice_delegates, bob_delegates], daves_roots).explain())

rule("What this shows, and what it does not")
print("""    SHOWS
      - reduction is following signed statements back to a root you chose
      - the range must still cover the value after every narrowing
      - delegation is a DIFFERENT TYPE from the thing delegated
      - the trust root is unsigned, and that is load-bearing

    DOES NOT
      - signatures are not checked here; reduce.py takes statements as given
      - no revocation, no validity windows, no thresholds
      - ranges are globs. Real ranges need the tag language DEC-004 picks
      - this is the email topic only. The PICS-like part - what a topic MEANS,
        its human-readable names and processing constraints - is labeltype.py""")
