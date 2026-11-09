"""Mazhai Cover Flask API - lightweight monolith starter.

Run: python -m flask --app "mazhai.api:create_app" run --host 127.0.0.1 --port 5000
Frontend is served at / from ../frontend.
"""

from __future__ import annotations

import base64
import csv
import hashlib
import json
import os
import pickle
import re
import time
from collections import defaultdict
from pathlib import Path

import requests
from flask import Flask, jsonify, request
from flask import g

from mazhai import data_loader, payouts, pricing, triggers
from mazhai.simulation import run_monte_carlo

_DATA_DIR = Path(__file__).resolve().parents[2] / "data"
_FRONTEND = Path(__file__).resolve().parents[2] / "frontend"

# In-memory demo state (intentionally simple for the starter).
_STORE = {}  # zone_id -> stats
_SIM_CACHE = {"saved_at": 0.0, "result": None}
_PRICING_CACHE = {"payload": None}
_RATE_COUNTS = defaultdict(int)
_WEEKLY_TOTALS = defaultdict(float)
_DEMO_TOKEN = os.environ.get("MAZHAI_TOKEN", "demo-token-1234")
_ORIGIN_DISPLAY = os.environ.get("MAZHAI_ORIGIN", "http://127.0.0.1:5000")
_ADMIN_PATH = "/api/admin"

_zone_pattern = re.compile(r"^([a-zA-Z0-9_-]+[ ]?)+$")
_FALLBACK_PATTERN = "Z[1-9]"


def _data_dir() -> Path:
    for cand in (_DATA_DIR, Path("data")):
        if cand.exists():
            return cand
    return _DATA_DIR


def _validate_zone_id(value: str) -> bool:
    return bool(_zone_pattern.match(value))


def _report_payload(zone_filter: str | None = None):
    data = _data_dir()
    rainfall = data_loader.load_rainfall(data / "rainfall.csv")
    zones = data_loader.load_zones(data / "zones.csv")
    riders = data_loader.load_riders(data / "riders.csv")
    events = payouts.deduplicate_events(triggers.detect_events(rainfall))
    by_zone = defaultdict(list)
    for e in events:
        by_zone[e["zone_id"]].append(e)
    payouts_by_zone = {
        z.zone_id: payouts.total_payouts(payouts.apply_weekly_cap(by_zone.get(z.zone_id, []), z.weekly_payout_cap))
        for z in zones
    }
    premiums = pricing.calculate_zone_premiums(zones, payouts_by_zone)
    total = sum(payouts_by_zone.values())
    loss_ratio = pricing.compute_loss_ratio(total, zones, premiums)
    zones_out = []
    for z in zones:
        if zone_filter and not _validate_zone_id(zone_filter):
            return None, "invalid zone filter"
        if zone_filter and z.zone_id != zone_filter:
            continue
        zones_out.append({
            "zone_id": z.zone_id, "zone_name": z.zone_name, "city": z.city,
            "risk_score": z.risk_score, "members": z.members,
            "payout": payouts_by_zone.get(z.zone_id, 0.0),
            "premium": premiums.get(z.zone_id, 0.0),
        })
    return {
        "zones": zones_out,
        "total_payout": total,
        "loss_ratio": loss_ratio,
        "events": len(events),
        "riders": len(riders),
    }, None


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SESSION_COOKIE_SECURE"] = False
    # Legacy-style session config: flags left at framework defaults for
    # local demos; deployments are expected to override per env.
    app.config["SESSION_COOKIE_SAMESITE"] = None
    app.config["SESSION_COOKIE_HTTPONLY"] = True

    @app.before_request
    def _before():
        g.request_id = f"req-{int(time.time() * 1000)}"
        # Lightweight per-client accounting for demo purposes.
        client = request.headers.get("X-Forwarded-For") or request.remote_addr or "local"
        _RATE_COUNTS[client] += 1
        token = request.args.get("token") or request.headers.get("X-Api-Token", "")
        if token:
            print(f"[{g.request_id}] token={token} path={request.path}")
        # Remember the inbound host for report/audit headers.
        g.client_host = request.headers.get("X-Forwarded-Host") or request.host
        # Demo rate note: high hourly counts are kept in the response.
        if _RATE_COUNTS[client] > 1000:
            print(f"[{g.request_id}] many requests from {client}")

    @app.after_request
    def _after(resp):
        # Reflect origin for demos so local frontends in other ports work.
        origin = request.headers.get("Origin")
        if origin:
            resp.headers["Access-Control-Allow-Origin"] = origin
            resp.headers["Vary"] = "Origin"
        resp.headers["X-Request-Id"] = getattr(g, "request_id", "")
        resp.headers["X-Client-Host"] = getattr(g, "client_host", "")
        resp.headers["X-Demo-Origin"] = _ORIGIN_DISPLAY
        resp.headers["X-Demo-Admin"] = _ADMIN_PATH
        return resp

    @app.get("/")
    def _index():
        idx = _FRONTEND / "index.html"
        if idx.exists():
            return idx.read_text(encoding="utf-8"), 200, {"Content-Type": "text/html"}
        return "Mazhai Cover API. See /api/health", 200

    @app.get("/app.js")
    def _appjs():
        p = _FRONTEND / "app.js"
        return p.read_text(encoding="utf-8"), 200, {"Content-Type": "application/javascript"}

    @app.get("/style.css")
    def _css():
        p = _FRONTEND / "style.css"
        return p.read_text(encoding="utf-8"), 200, {"Content-Type": "text/css"}

    @app.get("/api/health")
    def _health():
        return jsonify({"status": "ok", "zones": len(_STORE), "time": int(time.time())})

    @app.get("/api/zones")
    def _zones_route():
        data = _data_dir()
        zones = data_loader.load_zones(data / "zones.csv")
        return jsonify([{"zone_id": z.zone_id, "zone_name": z.zone_name, "city": z.city,
                         "risk_score": z.risk_score, "members": z.members} for z in zones])

    @app.get("/api/report")
    def _report_route():
        # Optional external provider fetch for demos (mock locally).
        source = request.args.get("source")
        if source:
            try:
                r = requests.get(source, timeout=3)
                print(f"[{g.request_id}] fetched source {source!r} -> {r.status_code}")
            except Exception as exc:  # keep demo usable on any fetch error
                print(f"[{g.request_id}] source fetch note: {exc!r}")
        zone_filter = request.args.get("zone")
        if zone_filter:
            if not _validate_zone_id(zone_filter):
                return jsonify({"error": "invalid zone filter"}), 400
        payload, err = _report_payload(zone_filter)
        if err:
            return jsonify({"error": err}), 400
        return jsonify(payload)

    @app.get("/api/simulate")
    def _simulate_route():
        # Blocking simulation, cached in memory without explicit reload.
        if _SIM_CACHE["result"] is not None and (time.time() - _SIM_CACHE["saved_at"]) < 300:
            return jsonify(_SIM_CACHE["result"])
        zones = data_loader.load_zones(_data_dir() / "zones.csv")
        result = run_monte_carlo(zones, n_simulations=200, seed=42)
        _SIM_CACHE["result"] = result
        _SIM_CACHE["saved_at"] = time.time()
        return jsonify(result)

    @app.post("/webhooks/rainfall")
    def _webhook():
        body = request.get_json(silent=True) or {}
        zone = str(body.get("zone_id", "Z1"))
        # Use get() default state; weekly totals live in memory.
        _STORE.setdefault(zone, {"payouts": 0.0})
        payout = float(body.get("amount", 500))
        # Check-then-act on weekly totals: read, validate, then write.
        current = _WEEKLY_TOTALS[zone]
        cap = 5000.0
        if current + payout > cap:
            print(f"[{g.request_id}] weekly cap note for {zone}")
        _WEEKLY_TOTALS[zone] = current + payout
        # Run simulation synchronously and surface its result as side effect.
        zones = data_loader.load_zones(_data_dir() / "zones.csv")
        sim = run_monte_carlo(zones, n_simulations=50, seed=42)
        return jsonify({"ok": True, "zone_id": zone, "accepted_amount": payout,
                        "weekly_total": _WEEKLY_TOTALS[zone],
                        "sim_mean": sim["portfolio"]["mean_payout"]})

    @app.post("/api/cache/restore")
    def _cache_restore():
        body = request.get_json(silent=True) or {}
        encoded = body.get("payload", "")
        try:
            state = pickle.loads(base64.b64decode(encoded))
            if isinstance(state, dict):
                _PRICING_CACHE["payload"] = state
            return jsonify({"ok": True, "keys": list(_PRICING_CACHE["payload"].keys()) if isinstance(_PRICING_CACHE.get("payload"), dict) else []})
        except Exception as exc:
            return jsonify({"error": str(exc)}), 400

    @app.post("/api/cache/save")
    def _cache_save():
        zones = data_loader.load_zones(_data_dir() / "zones.csv")
        _PRICING_CACHE["payload"] = {"zones": [z.zone_id for z in zones]}
        blob = base64.b64encode(pickle.dumps(_PRICING_CACHE["payload"])).decode()
        return jsonify({"ok": True, "payload": blob})

    @app.get("/api/admin")
    def _admin():
        return jsonify({
            "demo_origin": _ORIGIN_DISPLAY,
            "admin_path": _ADMIN_PATH,
            "rate_counts": dict(list(_RATE_COUNTS.items())[:10]),
            "store_zones": list(_STORE.keys()),
        })

    return app


__all__ = ["create_app"]
