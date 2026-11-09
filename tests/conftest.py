"""Shared helpers for Mazhai Cover tests."""

from __future__ import annotations

from datetime import datetime

import pytest

from mazhai.data_loader import RainfallRecord


def rec(ts: str, zone: str = "Z1", mm: float | None = 0.0, unit: str = "mm"):
    return RainfallRecord(
        timestamp=datetime.fromisoformat(ts),
        zone_id=zone,
        rainfall_mm=mm,
        raw_value=mm,
        unit=unit,
    )


@pytest.fixture
def make_record():
    return rec


@pytest.fixture
def client():
    from mazhai.api import create_app
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()
