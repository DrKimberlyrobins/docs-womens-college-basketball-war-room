import csv,pytest
from scripts.normalize_wehoop import normalize
def test_normalization(tmp_path):
    raw=tmp_path/"in.csv";out=tmp_path/"out.csv"
    raw.write_text("team_name,adj_o,adj_d,adj_tempo\nEast Carolina,101,98,69\n")
    normalize(raw,out)
    assert next(csv.DictReader(out.open()))=={"team":"East Carolina","adj_off":"101","adj_def":"98","tempo":"69"}
def test_ambiguous_mapping_fails(tmp_path):
    raw=tmp_path/"in.csv";out=tmp_path/"out.csv"
    raw.write_text("team,team_name,adj_o,adj_d,tempo\nA,B,101,98,69\n")
    with pytest.raises(ValueError):normalize(raw,out)
