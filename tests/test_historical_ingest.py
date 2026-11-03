from historical_ingest import read_historical_csv
import pytest
def test_missing_headers_rejected(tmp_path):
    p=tmp_path/"games.csv";p.write_text("game_id,score\na,3\n")
    with pytest.raises(ValueError):read_historical_csv(p)
