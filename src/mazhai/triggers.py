"""Parametric trigger: rainfall >= threshold in N consecutive hours.

One event per zone per qualifying spell. Events must span calendar
boundaries (midnight) when rain is uninterrupted, and a single-hour
spike must NOT trigger a two-hour policy.
"""

from __future__ import annotations

from datetime import datetime

from mazhai.data_loader import RainfallRecord

DEFAULT_THRESHOLD_MM = 20.0
DEFAULT_CONSECUTIVE_HOURS = 2


def _rainy(record: RainfallRecord, threshold_mm: float) -> bool:
    # Missing (None) is unknown — treat as not-rainy for counting
    # (see Issue #2 in data_loader; the fix belongs there).
    return record.rainfall_mm is not None and record.rainfall_mm >= threshold_mm


def detect_events(
    records: list[RainfallRecord],
    threshold_mm: float = DEFAULT_THRESHOLD_MM,
    consecutive_hours: int = DEFAULT_CONSECUTIVE_HOURS,
) -> list[dict]:
    """Return trigger events sorted by (zone_id, start_time).

    Each event: {"zone_id", "start_time", "end_time", "peak_mm"}.
    """
    by_zone: dict[str, list[RainfallRecord]] = {}
    for r in records:
        by_zone.setdefault(r.zone_id, []).append(r)

    events: list[dict] = []
    for zone_id, rows in by_zone.items():
        rows.sort(key=lambda r: r.timestamp)
        streak = 0
        streak_start: datetime | None = None
        prev_date = None
        prev_ts: datetime | None = None
        peak = 0.0
        for r in rows:
            rainy = _rainy(r, threshold_mm)
            # TODO(Issue #3): the counter must carry across midnight.
            # Currently any date change resets the streak, so an
            # uninterrupted 23:00 + 00:00 spell never accumulates.
            if prev_date is not None and r.timestamp.date() != prev_date:
                streak = 0  # BUG: resets at midnight
                streak_start = None
            # A gap in the hourly series also breaks consecutiveness.
            if prev_ts is not None and (r.timestamp - prev_ts).total_seconds() != 3600:
                streak = 0
                streak_start = None
            prev_ts = r.timestamp
            prev_date = r.timestamp.date()

            if rainy:
                if streak == 0:
                    streak_start = r.timestamp
                    peak = r.rainfall_mm or 0.0
                else:
                    peak = max(peak, r.rainfall_mm or 0.0)
                streak += 1
                # TODO(Issue #4): a single hour must NOT trigger a
                # two-hour policy. Currently any one rainy hour fires.
                if streak >= 1:  # BUG: should be streak >= consecutive_hours
                    events.append(
                        {
                            "zone_id": zone_id,
                            "start_time": streak_start or r.timestamp,
                            "end_time": r.timestamp,
                            "peak_mm": peak,
                        }
                    )
                    streak = 0
                    streak_start = None
                    peak = 0.0
            else:
                streak = 0
                streak_start = None
                peak = 0.0

    events.sort(key=lambda e: (e["zone_id"], e["start_time"]))
    return events
