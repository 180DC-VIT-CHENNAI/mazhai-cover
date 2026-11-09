"""Generate deterministic synthetic data in data/ (seed 42).

Run: python tools/generate_synthetic_data.py
Produces rainfall.csv, zones.csv, riders.csv used by the starter pipeline.
"""

from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ZONES = [
    ("Z1", "North Chennai", "Chennai", 0.40, 150.0, 50000.0, 1200),
    ("Z2", "South Chennai", "Chennai", 0.70, 220.0, 80000.0, 2000),
    ("Z3", "East Chennai", "Chennai", 0.90, 180.0, 60000.0, 1500),
    ("Z4", "Tambaram", "Chennai", 0.30, 120.0, 40000.0, 800),
]


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)

    with open(DATA / "zones.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["zone_id", "zone_name", "city", "risk_score",
                    "base_premium_monthly", "weekly_payout_cap", "members"])
        w.writerows(ZONES)

    rng = random.Random(42)
    riders = []
    platforms = ["Swiggy", "Zomato", "Dunzo", "AmazonFlex"]
    for i in range(1, 25):
        zone = ZONES[(i - 1) % len(ZONES)][0]
        riders.append([
            f"R{i:03d}", zone, rng.choice(platforms),
            rng.choice([True, False]),
            round(rng.uniform(600, 1500), 2),
        ])
    with open(DATA / "riders.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["rider_id", "zone_id", "platform", "subsidy_eligible", "earnings_daily"])
        w.writerows(riders)

    start = datetime(2026, 1, 1, 0, 0)
    rows: dict[tuple[str, str], list] = {}
    for zone_id, _name, _city, risk, *_rest in ZONES:
        for h in range(7 * 24):
            ts = start + timedelta(hours=h)
            # Mostly dry, occasional rain scaled by zone risk.
            if rng.random() < 0.65:
                mm = round(rng.uniform(0, 8), 1)
            else:
                mm = round(8 + rng.uniform(0, 20) * risk * 2, 1)
            rows[(ts.isoformat(), zone_id)] = [ts.isoformat(), zone_id, mm, "mm"]

    def set_row(ts: str, zone: str, mm, unit: str = "mm"):
        rows[(ts, zone)] = [ts, zone, mm, unit]

    # Issue #3 seed — midnight-crossing 2-hour spell in Z1.
    set_row("2026-01-01T23:00:00", "Z1", 25.0)
    set_row("2026-01-02T00:00:00", "Z1", 25.0)
    # Issue #4 seed — isolated single-hour spike in Z2 (must NOT trigger).
    set_row("2026-01-03T14:00:00", "Z2", 35.0)
    set_row("2026-01-03T13:00:00", "Z2", 5.0)
    set_row("2026-01-03T15:00:00", "Z2", 5.0)
    # Issue #1 seed — cm readings in Z3 (2.5 cm = 25 mm; buggy read = 2.5 mm).
    set_row("2026-01-04T10:00:00", "Z3", 2.5, "cm")
    set_row("2026-01-04T11:00:00", "Z3", 2.5, "cm")
    # A normal same-day 2-hour event in Z4 (should trigger).
    set_row("2026-01-05T09:00:00", "Z4", 28.0)
    set_row("2026-01-05T10:00:00", "Z4", 24.0)
    # Issue #2 seeds — missing observations (empty rainfall_mm).
    for ts, zone in [
        ("2026-01-02T06:00:00", "Z2"),
        ("2026-01-02T07:00:00", "Z2"),
        ("2026-01-06T12:00:00", "Z3"),
        ("2026-01-06T13:00:00", "Z1"),
    ]:
        set_row(ts, zone, "")

    ordered = sorted(rows.values(), key=lambda r: (r[0], r[1]))
    with open(DATA / "rainfall.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["timestamp", "zone_id", "rainfall_mm", "rainfall_unit"])
        w.writerows(ordered)

    print(f"Wrote {len(ordered)} rainfall rows, {len(riders)} riders, {len(ZONES)} zones to {DATA}")


if __name__ == "__main__":
    main()
