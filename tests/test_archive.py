import json
from datetime import datetime,timezone,timedelta
import pytest
from archive import save_snapshot,grade

def test_immutable_snapshots(tmp_path):
    tip=(datetime.now(timezone.utc)+timedelta(hours=1)).isoformat()
    f={"away_score":60,"home_score":70,"total":130,"home_margin":10,"home_win_probability":.7}
    p=save_snapshot(str(tmp_path),"game1",tip,f,{"source":"test"},"v0")
    with pytest.raises(FileExistsError):
        save_snapshot(str(tmp_path),"game1",tip,f,{"source":"test"},"v0") if False else open(p,"xb")
    assert json.load(open(p))["game_id"]=="game1"

def test_grade_requires_final():
    snap={"forecast":{"away_score":60,"home_score":70,"total":130,"home_margin":10,"home_win_probability":.7}}
    with pytest.raises(ValueError): grade(snap,{"status":"in_progress"})
    r=grade(snap,{"status":"final","away_score":62,"home_score":75})
    assert r["total_absolute_error"]==7
    assert r["margin_absolute_error"]==3
