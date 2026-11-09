"""Trigger tests — Issues #3 (midnight) and #4 (single-hour)."""

from mazhai.triggers import detect_events


def test_normal_two_hour_event_triggers(make_record):
    # PASSING baseline: two consecutive rainy hours on the same day
    # must trigger (fixed code emits exactly 1; see Issue #4 for count).
    rows = [
        make_record("2026-01-01T10:00:00", mm=25.0),
        make_record("2026-01-01T11:00:00", mm=25.0),
    ]
    assert len(detect_events(rows)) >= 1


def test_no_trigger_below_threshold(make_record):
    rows = [
        make_record("2026-01-01T10:00:00", mm=5.0),
        make_record("2026-01-01T11:00:00", mm=5.0),
    ]
    assert len(detect_events(rows)) == 0


def test_single_hour_must_not_trigger_two_hour_policy(make_record):
    # Issue #4: one rainy hour followed by a dry hour must NOT fire.
    rows = [
        make_record("2026-01-01T14:00:00", mm=35.0),
        make_record("2026-01-01T15:00:00", mm=5.0),
    ]
    assert len(detect_events(rows)) == 0


def test_midnight_crossing_counts_as_consecutive(make_record):
    # Issue #3: 23:00 + 00:00 next day is a valid 2-hour spell.
    rows = [
        make_record("2026-01-01T23:00:00", mm=25.0),
        make_record("2026-01-02T00:00:00", mm=25.0),
    ]
    events = detect_events(rows)
    assert len(events) == 1
    assert events[0]["start_time"].isoformat() == "2026-01-01T23:00:00"
    assert events[0]["end_time"].isoformat() == "2026-01-02T00:00:00"
