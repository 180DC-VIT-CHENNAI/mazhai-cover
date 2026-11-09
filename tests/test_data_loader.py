"""Data loader tests — Issues #1 (unit) and #2 (missing)."""

from mazhai.data_loader import parse_rainfall_row


def test_mm_passthrough():
    # PASSING baseline: mm rows convert 1:1.
    r = parse_rainfall_row({"timestamp": "2026-01-01T10:00:00", "zone_id": "Z1", "rainfall_mm": "25.0", "rainfall_unit": "mm"})
    assert r.rainfall_mm == 25.0


def test_cm_converted_to_mm():
    # Issue #1: 2.5 cm == 25 mm.
    r = parse_rainfall_row({"timestamp": "2026-01-01T10:00:00", "zone_id": "Z3", "rainfall_mm": "2.5", "rainfall_unit": "cm"})
    assert r.rainfall_mm == 25.0


def test_missing_rainfall_is_none_not_zero():
    # Issue #2: empty rainfall is unknown (None), not a dry hour.
    r = parse_rainfall_row({"timestamp": "2026-01-01T10:00:00", "zone_id": "Z1", "rainfall_mm": "", "rainfall_unit": "mm"})
    assert r.rainfall_mm is None


def test_zero_is_explicit_dry_hour():
    r = parse_rainfall_row({"timestamp": "2026-01-01T10:00:00", "zone_id": "Z1", "rainfall_mm": "0.0", "rainfall_unit": "mm"})
    assert r.rainfall_mm == 0.0
