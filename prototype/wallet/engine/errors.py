"""Why a statement or an input was refused.

`Invalid` and `Unverifiable` are the two failure results of SPEC-0002 §9.1.
Each one carries the step that failed (V1 to V8) and a reason code from
SPEC-0002 §12.9. The codecs raise `EncodingError`; the verifier turns it into
the reason code of the step it was running.
"""


class EncodingError(ValueError):
    """Bytes or text that are not exactly the canonical form of a value.
    Rejected, never repaired."""


class StructureError(ValueError):
    """A value that does not have the shape SPEC-0002 Appendix B gives it."""


class Rejected(Exception):
    result = ""

    def __init__(self, step: str, reason: str, detail: str = ""):
        text = f"{self.result} at {step} ({reason})"
        super().__init__(f"{text}: {detail}" if detail else text)
        self.step, self.reason, self.detail = step, reason, detail


class Invalid(Rejected):
    """Malformed, or the signature does not verify. MUST NOT be used."""
    result = "invalid"


class Unverifiable(Rejected):
    """May be valid, but this verifier cannot tell: unsupported suite, or no
    key for `says`."""
    result = "unverifiable"


class DefinitionError(ValueError):
    """A definition that cannot be used. `reason` is a SPEC-0004 §14.2 code:
    `definition-unobtainable` or `definition-non-conforming`."""

    def __init__(self, reason: str, detail: str):
        super().__init__(f"{reason}: {detail}")
        self.reason, self.detail = reason, detail


class WalletError(Exception):
    """A wallet operation the user asked for cannot be done."""
