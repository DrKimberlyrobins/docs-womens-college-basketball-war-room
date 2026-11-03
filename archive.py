"""Immutable pregame snapshot persistence. Store on durable disk; never overwrite."""
import json, os, hashlib
from datetime import datetime, timezone

def save_snapshot(root, game_id, tipoff_utc, forecast, inputs, model_version):
    now=datetime.now(timezone.utc)
    tip=datetime.fromisoformat(tipoff_utc.replace("Z","+00:00"))
    if tip.tzinfo is None or now >= tip:
        raise ValueError("Cannot archive forecast at or after tipoff")
    if not game_id or not model_version: raise ValueError("Missing identity or version")
    payload={"game_id":str(game_id),"created_utc":now.isoformat(),"tipoff_utc":tip.isoformat(),
             "model_version":model_version,"forecast":forecast,"inputs":inputs}
    encoded=json.dumps(payload,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
    digest=hashlib.sha256(encoded).hexdigest()
    directory=os.path.join(root,str(game_id))
    os.makedirs(directory,exist_ok=True)
    path=os.path.join(directory,digest+".json")
    with open(path,"xb") as f: f.write(encoded)
    return path

def grade(snapshot, result):
    if result.get("status")!="final": raise ValueError("Only verified final results may be graded")
    f=snapshot["forecast"]
    a,h=result["away_score"],result["home_score"]
    if any(not isinstance(x,(int,float)) for x in (a,h)): raise ValueError("Missing final scores")
    return {"away_score_absolute_error":abs(f["away_score"]-a),
            "home_score_absolute_error":abs(f["home_score"]-h),
            "total_absolute_error":abs(f["total"]-(a+h)),
            "margin_absolute_error":abs(f["home_margin"]-(h-a)),
            "brier_home_win":(f["home_win_probability"]-int(h>a))**2 if h!=a else None}
