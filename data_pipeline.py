"""Provider-neutral, fail-closed schedule ingestion from permitted JSON exports."""
import json
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pathlib import Path

def normalize_games(payload):
    if not isinstance(payload,dict) or not isinstance(payload.get("games"),list):
        raise ValueError("Expected games array")
    if not payload.get("source") or not payload.get("retrieved_utc"):
        raise ValueError("Source provenance required")
    seen=set(); out=[]
    for raw in payload["games"]:
        gid=str(raw["id"])
        if gid in seen: raise ValueError("Duplicate game id "+gid)
        seen.add(gid)
        tip=datetime.fromisoformat(raw["tipoff_utc"].replace("Z","+00:00"))
        if tip.tzinfo is None: raise ValueError("Tipoff must be timezone aware")
        if not raw.get("home") or not raw.get("away"): raise ValueError("Team identity missing")
        out.append({"id":gid,"home":raw["home"],"away":raw["away"],
                    "tipoff_utc":tip.astimezone(timezone.utc).isoformat(),
                    "tipoff_central":tip.astimezone(ZoneInfo("America/Chicago")).isoformat(),
                    "status":raw.get("status","scheduled"),
                    "home_score":raw.get("home_score"),"away_score":raw.get("away_score"),
                    "quarters":raw.get("quarters"),"venue":raw.get("venue"),
                    "neutral":raw.get("neutral"),"conference":raw.get("conference"),
                    "source":payload["source"],"retrieved_utc":payload["retrieved_utc"]})
    return sorted(out,key=lambda g:g["tipoff_utc"])

def publish(source_path, output_path):
    payload=json.loads(Path(source_path).read_text(encoding="utf-8"))
    games=normalize_games(payload)
    result={"status":"SCHEDULE_ONLY","source":payload["source"],
            "retrieved_utc":payload["retrieved_utc"],"games":games,
            "forecasts":[],"message":"Schedule loaded from source-labeled export. Forecast ratings not verified."}
    Path(output_path).parent.mkdir(parents=True,exist_ok=True)
    Path(output_path).write_text(json.dumps(result,indent=2),encoding="utf-8")
    return len(games)

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser();p.add_argument("input");p.add_argument("--output",default="data/dashboard.json")
    a=p.parse_args();print("Published",publish(a.input,a.output),"games")
