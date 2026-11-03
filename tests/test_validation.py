from validation import summarize
import pytest
def test_metrics():
    rows=[{"created_utc":"2026-01-01T00:00:00Z","tipoff_utc":"2026-01-02T00:00:00Z",
      "forecast":{"total":130,"home_margin":10,"home_win_probability":.8},
      "actual":{"status":"final","away_score":60,"home_score":75}}]
    s=summarize(rows)
    assert s["total_mae"]==5 and s["margin_mae"]==5
def test_no_leakage():
    with pytest.raises(ValueError):
        summarize([{"created_utc":"2026-01-03","tipoff_utc":"2026-01-02"}])
