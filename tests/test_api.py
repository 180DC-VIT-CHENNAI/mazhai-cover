"""Public API behaviour tests (contributor verification)."""

def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_zones_lists_four(client):
    r = client.get("/api/zones")
    assert r.status_code == 200
    assert len(r.get_json()) == 4


def test_report_shape(client):
    r = client.get("/api/report")
    assert r.status_code == 200
    body = r.get_json()
    assert "zones" in body and "total_payout" in body
    assert len(body["zones"]) == 4


def test_report_zone_filter(client):
    r = client.get("/api/report?zone=Z1")
    assert r.status_code == 200
    zones = r.get_json()["zones"]
    assert len(zones) == 1 and zones[0]["zone_id"] == "Z1"


def test_simulate_returns_portfolio(client):
    r = client.get("/api/simulate")
    assert r.status_code == 200
    assert "portfolio" in r.get_json()


def test_webhook_accepts_fixture(client):
    r = client.post("/webhooks/rainfall", json={"zone_id": "Z1", "amount": 500})
    assert r.status_code == 200
    assert r.get_json()["ok"] is True


def test_frontend_served(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"Mazhai Cover" in r.data
    assert b'/style.css' in r.data
    assert b'/app.js' in r.data


def test_static_assets_served(client):
    assert client.get("/style.css").status_code == 200
    assert client.get("/style.css").mimetype == "text/css"
    assert client.get("/app.js").status_code == 200
    assert "javascript" in (client.get("/app.js").mimetype or "")
