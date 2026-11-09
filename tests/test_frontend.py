"""Frontend static checks (React)."""

from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]


def test_frontend_files_exist():
    assert (_ROOT / "frontend" / "index.html").exists()
    assert (_ROOT / "frontend" / "app.js").exists()
    assert (_ROOT / "frontend" / "style.css").exists()


def test_frontend_calls_report_api():
    text = (_ROOT / "frontend" / "app.js").read_text(encoding="utf-8")
    assert "/api/report" in text


def test_frontend_is_react():
    html = (_ROOT / "frontend" / "index.html").read_text(encoding="utf-8")
    js = (_ROOT / "frontend" / "app.js").read_text(encoding="utf-8")
    assert 'id="root"' in html
    assert "react" in html.lower()
    assert "React" in js and "createRoot" in js
