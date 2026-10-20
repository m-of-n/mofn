"""KSA time (SPEC-0002 §4.4).

`s` is seconds since 2026-01-01T00:00:00Z. A whole day is written in the odd
day form `2·(s / 86400) + 1`; any other instant in the even seconds form
`2·s`. An even value whose `s` is a whole day is rejected, so every instant
has exactly one encoding. The text form is exactly `YYYY-MM-DDTHH:MM:SSZ`.
"""

import datetime
import re

EPOCH = datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc)
DAY = 86400
_TEXT = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")


def from_seconds(s: int) -> int:
    return 2 * (s // DAY) + 1 if s % DAY == 0 else 2 * s


def to_seconds(t: int) -> int:
    if t % 2:
        return (t - 1) // 2 * DAY
    if (t // 2) % DAY == 0:
        raise ValueError(f"time {t} is a whole day written in the seconds form")
    return t // 2


def is_time(t) -> bool:
    return type(t) is int and (t % 2 == 1 or (t // 2) % DAY != 0)


def from_datetime(d: datetime.datetime) -> int:
    return from_seconds(int((d - EPOCH).total_seconds()))


def to_datetime(t: int) -> datetime.datetime:
    return EPOCH + datetime.timedelta(seconds=to_seconds(t))


def from_text(text: str) -> int:
    if not isinstance(text, str) or not _TEXT.fullmatch(text) or int(text[17:19]) > 59:
        raise ValueError(f"time {text!r} is not exactly YYYY-MM-DDTHH:MM:SSZ")
    d = datetime.datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
    return from_datetime(d)


def to_text(t: int) -> str:
    return to_datetime(t).strftime("%Y-%m-%dT%H:%M:%SZ")


def now() -> int:
    return from_datetime(datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0))


def add_days(t: int, days: int) -> int:
    return from_seconds(to_seconds(t) + days * DAY)
