"""KSA time (SPEC-0002 §4.4)."""

import pytest

from engine import ksatime


def test_day_and_seconds_forms():
    assert ksatime.from_text("2026-01-01T00:00:00Z") == 1
    assert ksatime.from_text("2026-01-02T00:00:00Z") == 3
    assert ksatime.from_text("2026-01-01T00:00:01Z") == 2
    assert ksatime.to_text(ksatime.from_text("2026-10-06T10:30:00Z")) == "2026-10-06T10:30:00Z"
    assert ksatime.from_text("2025-12-31T00:00:00Z") == -1


def test_whole_day_in_seconds_form_is_rejected():
    with pytest.raises(ValueError):
        ksatime.to_seconds(2 * 86400)
    assert not ksatime.is_time(2 * 86400)


@pytest.mark.parametrize("text", ["2026-10-06T10:30:00", "2026-10-06t10:30:00Z", "2026-10-06T10:30:00.5Z",
                                  "2026-10-06T10:30:00+00:00", "2026-10-06T10:30:60Z", "2026-10-06 10:30:00Z"])
def test_text_form_is_exact(text):
    with pytest.raises(ValueError):
        ksatime.from_text(text)


def test_add_days():
    t = ksatime.from_text("2026-10-06T10:30:00Z")
    assert ksatime.to_text(ksatime.add_days(t, 30)) == "2026-11-05T10:30:00Z"
