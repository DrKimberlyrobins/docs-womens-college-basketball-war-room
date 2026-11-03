from sportradar import convert,fetch_day
from datetime import date
import pytest
def test_converts_provider_schedule():
    raw={"games":[{"id":"abc","scheduled":"2026-11-03T23:00:00Z","status":"scheduled",
    "home":{"name":"Host","id":"h"},"away":{"name":"Visitor","id":"a"}}]}
    r=convert(raw,"2026-11-03T12:00:00Z")
    assert r[0]["home"]=="Host" and r[0]["away"]=="Visitor"
    assert r[0]["home_score"] is None
def test_requires_key(monkeypatch):
    monkeypatch.delenv("SPORTRADAR_API_KEY",raising=False)
    with pytest.raises(RuntimeError,match="SPORTRADAR_API_KEY"):fetch_day(date(2026,11,3))
