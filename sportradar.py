"""Licensed Sportradar NCAA women's basketball daily schedule connector.

Requires explicit subscription/API key via SPORTRADAR_API_KEY GitHub Secret.
No undocumented scraping or public-website extraction.
"""
import os, json, argparse
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from pathlib import Path
import time

BASE="https://api.sportradar.com/ncaawb/trial/v8/en"
def fetch_day(day, api_key=None, base=None):
    key=api_key or os.environ.get("SPORTRADAR_API_KEY")
    if not key: raise RuntimeError("SPORTRADAR_API_KEY missing: licensed schedule feed not connected")
    endpoint=(base or os.environ.get("SPORTRADAR_BASE_URL") or BASE).rstrip("/")
    url=f"{endpoint}/games/{day.year:04d}/{day.month:02d}/{day.day:02d}/schedule.json"
    req=Request(url,headers={"accept":"application/json","x-api-key":key,"user-agent":"DocsWomensWarRoom/0.1"})
    for attempt in range(3):
        try:
            with urlopen(req,timeout=25) as response:
                return json.load(response)
        except HTTPError as exc:
            if exc.code in (401,403): raise RuntimeError("Provider credentials rejected or subscription not authorized") from exc
            if exc.code not in (429,500,502,503,504) or attempt==2: raise
        except (TimeoutError,URLError):
            if attempt==2: raise
        time.sleep(2**attempt)
    raise RuntimeError("Provider unavailable")

def convert(raw, retrieved):
    out=[]
    for g in raw.get("games",[]):
        home=g.get("home") or {};away=g.get("away") or {}
        if not g.get("id") or not home.get("name") or not away.get("name") or not g.get("scheduled"):
            raise ValueError("Provider returned incomplete game record")
        state=str(g.get("status","scheduled")).lower()
        is_final=state in ("closed","complete","final")
        score=lambda team:team.get("points") if is_final and isinstance(team.get("points"),int) else None
        quarters=None
        if is_final:
            quarters={"home":home.get("scoring"),"away":away.get("scoring")}
        out.append({"id":str(g["id"]),"home":home["name"],"away":away["name"],
          "home_id":home.get("id"),"away_id":away.get("id"),"tipoff_utc":g["scheduled"],
          "status":"final" if is_final else state,"home_score":score(home),"away_score":score(away),
          "quarters":quarters,"venue":(g.get("venue") or {}).get("name"),
          "neutral":g.get("neutral_site"),"conference":None,
          "source":"Sportradar NCAAWB v8 (licensed)","retrieved_utc":retrieved})
    return out

def run():
    p=argparse.ArgumentParser()
    p.add_argument("--days",type=int,default=8)
    p.add_argument("--output",default="data/dashboard.json")
    args=p.parse_args()
    if not 1<=args.days<=15: raise ValueError("days must be 1..15")
    now=datetime.now(timezone.utc)
    local=now.astimezone(ZoneInfo("America/Chicago")).date()
    games=[];errors=[]
    for delta in range(-2,args.days-2):
        day=local+timedelta(days=delta)
        try: games.extend(convert(fetch_day(day),now.isoformat()))
        except Exception as e: errors.append({"date":day.isoformat(),"error":str(e)})
    if errors:
        # Never publish a partial schedule as if it were complete.
        raise RuntimeError("Incomplete schedule: "+json.dumps(errors))
    ids=set()
    for game in games:
        if game["id"] in ids: raise RuntimeError("Duplicate provider game ID")
        ids.add(game["id"])
    path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps({"status":"SCHEDULE_VERIFIED_FORECASTS_PENDING",
      "source":"Sportradar NCAAWB v8 (licensed)","retrieved_utc":now.isoformat(),
      "games":games,"forecasts":[],"message":f"Loaded {len(games)} provider schedule records; forecast model awaiting validated ratings."},indent=2))
    print(f"Published {len(games)} verified provider records")
if __name__=="__main__":run()
