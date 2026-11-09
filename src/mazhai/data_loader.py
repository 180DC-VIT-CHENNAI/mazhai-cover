"""CSV loading, unit conversion, and missing-data handling.

Product rules:
- Rainfall is recorded in ``mm`` or ``cm`` (``rainfall_unit`` column).
- Missing rainfall must surface as ``None`` (unknown), never as 0 mm.
  A true 0 mm row is an explicit dry hour.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class RainfallRecord:
    timestamp: datetime
    zone_id: str
    rainfall_mm: float | None  # None means missing/unknown
    raw_value: float | None
    unit: str


@dataclass
class Zone:
    zone_id: str
    zone_name: str
    city: str
    risk_score: float
    base_premium_monthly: float
    weekly_payout_cap: float
    members: int


@dataclass
class Rider:
    rider_id: str
    zone_id: str
    platform: str
    subsidy_eligible: bool
    earnings_daily: float


def _parse_bool(value: str) -> bool:
    return value.strip().lower() in ("true", "1", "yes", "y")


def _to_mm(value: float, unit: str) -> float:
    unit = (unit or "mm").strip().lower()
    # TODO(Issue #1): cm values must be converted (1 cm = 10 mm).
    # Currently cm is read as if it were mm, under-reporting rainfall 10x.
    if unit == "cm":
        return value  # BUG: should be value * 10
    return value


def parse_rainfall_row(row: dict) -> RainfallRecord:
    ts = datetime.fromisoformat(row["timestamp"].strip())
    zone_id = row["zone_id"].strip()
    unit = (row.get("rainfall_unit") or "mm").strip()
    raw = (row.get("rainfall_mm") or "").strip()
    if raw == "":
        # TODO(Issue #2): missing observations must stay None.
        # Currently missing is coerced to 0.0 (dry hour), hiding triggers.
        rainfall_mm: float | None = 0.0  # BUG: should be None
        raw_value: float | None = None
    else:
        raw_value = float(raw)
        rainfall_mm = _to_mm(raw_value, unit)
    return RainfallRecord(ts, zone_id, rainfall_mm, raw_value, unit)


def load_rainfall(path: str | Path) -> list[RainfallRecord]:
    with open(path, newline="", encoding="utf-8") as f:
        return [parse_rainfall_row(r) for r in csv.DictReader(f)]


def load_zones(path: str | Path) -> list[Zone]:
    zones = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            zones.append(
                Zone(
                    zone_id=r["zone_id"].strip(),
                    zone_name=r["zone_name"].strip(),
                    city=r["city"].strip(),
                    risk_score=float(r["risk_score"]),
                    base_premium_monthly=float(r["base_premium_monthly"]),
                    weekly_payout_cap=float(r["weekly_payout_cap"]),
                    members=int(r["members"]),
                )
            )
    return zones


def load_riders(path: str | Path) -> list[Rider]:
    riders = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            riders.append(
                Rider(
                    rider_id=r["rider_id"].strip(),
                    zone_id=r["zone_id"].strip(),
                    platform=r["platform"].strip(),
                    subsidy_eligible=_parse_bool(r["subsidy_eligible"]),
                    earnings_daily=float(r["earnings_daily"]),
                )
            )
    return riders
