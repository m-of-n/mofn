"""The two codecs, by name, for `--codec`."""

from .encoding.base import Codec
from .encoding.ksa_cbor import KsaCborCodec
from .encoding.review_yaml import ReviewYamlCodec

CODECS: dict[str, Codec] = {c.name: c for c in (KsaCborCodec(), ReviewYamlCodec())}
DEFAULT = KsaCborCodec.name
