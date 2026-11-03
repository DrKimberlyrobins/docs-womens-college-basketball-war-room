import json
from team_stats import canonical,attach
def test_joins_every_game_without_fabrication(tmp_path):
    d={"games":[{"away":"Alpha U","home":"Beta U"},{"away":"Gamma","home":"Beta U"}]}
    schedule=tmp_path/"schedule.json";schedule.write_text(json.dumps(d))
    ratings=tmp_path/"ratings.csv";ratings.write_text("team,adj_off,adj_def,tempo\nAlpha U,99,100,70\nBeta U,102,97,72\n")
    out=tmp_path/"out.json"
    coverage=attach(schedule,ratings,out,"authorized export","2026-11-03")
    result=json.loads(out.read_text())
    assert coverage["games_with_both_ratings"]==1
    assert "Gamma" in coverage["missing_teams"]
    assert result["games"][0]["forecast"]["runs"]==10000
    assert "forecast" not in result["games"][1]
def test_normalization():
    assert canonical("Cal-Baker.")=="calbaker"
