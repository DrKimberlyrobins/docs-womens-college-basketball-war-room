from data_pipeline import normalize_games
import pytest
def test_central_timezone_and_order():
    data={"source":"authorized export","retrieved_utc":"2026-11-03T12:00:00Z","games":[
      {"id":"1","home":"A","away":"B","tipoff_utc":"2026-11-04T01:00:00Z"}]}
    result=normalize_games(data)
    assert result[0]["tipoff_central"].startswith("2026-11-03T19:00:00")
def test_duplicates_rejected():
    raw={"source":"test","retrieved_utc":"2026-11-03T12:00:00Z","games":[
    {"id":"1","home":"A","away":"B","tipoff_utc":"2026-11-04T01:00:00Z"}]*2}
    with pytest.raises(ValueError):normalize_games(raw)
