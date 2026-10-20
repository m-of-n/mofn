"""The codec interface.

A codec chooses how a signed statement is written to a file and read back.
It does not choose what is signed: the signed bytes are always the KSA-CBOR
TBS (SPEC-0002 §4.2, §11). Every codec turns its file form into the same
envelope bytes `[suite, says, tbs, sig, ? pub]` (SPEC-0002 §5), and the
verifier only ever sees those.

Two codecs exist so that DEC-002 stays swappable (#65). Having two does not
decide DEC-002.
"""

from abc import ABC, abstractmethod


class Codec(ABC):
    name: str
    suffix: str

    @abstractmethod
    def dump(self, envelope: bytes) -> bytes:
        """Write an envelope in this codec's file form."""

    @abstractmethod
    def load(self, data: bytes) -> bytes:
        """Read this codec's file form back into envelope bytes. Raises
        `EncodingError` for anything that is not exactly that form."""
