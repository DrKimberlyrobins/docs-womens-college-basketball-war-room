"""Import permitted season team statistics and join EVERY game by normalized team ID.
Fail closed on missing or ambiguous identities. No invented team ratings.
"""
import csv,json,re
from datetime import datetime,timezone
from pathlib import Path
from engine import forecast

def canonical(s):
    return re.sub(r"[^a-z0-9]","",str(s).casefold())

def read_ratings(path):
    required={"team","adj_off","adj_def","tempo"}
    with open(path,newline="",encoding="utf-8") as f:
        reader=csv.DictReader(f)
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("Missing rating columns: "+", ".join(sorted(required-set(reader.fieldnames or []))))
        ratings={}
        for row in reader:
            key=canonical(row["team"])
            if not key or key in ratings: raise ValueError("Empty or duplicate team identity: "+row["team"])
            item={"team":row["team"]}
            for stat in ("adj_off","adj_def","tempo"):
                value=float(row[stat])
                if not 0<value<250:raise ValueError("Invalid rating: "+row["team"]+" "+stat)
                item[stat]=value
            ratings[key]=item
        return ratings

def attach(schedule_path,ratings_path,output_path,source,as_of,aliases_path=None):
    if not source or not as_of:raise ValueError("Rating provenance required")
    dashboard=json.loads(Path(schedule_path).read_text(encoding="utf-8"))
    ratings=read_ratings(ratings_path)
    aliases=json.loads(Path(aliases_path).read_text()) if aliases_path else {}
    aliases={canonical(k):canonical(v) for k,v in aliases.items()}
    count=0;missing=set()
    for game in dashboard["games"]:
        teams=[]
        for side in ("away","home"):
            key=canonical(game[side]);key=aliases.get(key,key)
            rating=ratings.get(key)
            if rating is None:missing.add(game[side])
            teams.append(rating)
        if any(x is None for x in teams):
            game.pop("forecast",None)
            game["rating_status"]="MISSING_VERIFIED_TEAM_RATING"
            continue
        a,h=teams
        result=forecast(a,h,n=10000)
        game["forecast"]=result
        game["rating_status"]="EXPERIMENTAL_UNCALIBRATED"
        game["rating_provenance"]={"source":source,"as_of":as_of,
          "away_team":a["team"],"home_team":h["team"]}
        count+=1
    dashboard["ratings_coverage"]={"games_with_both_ratings":count,
      "total_games":len(dashboard["games"]),"missing_teams":sorted(missing),
      "source":source,"as_of":as_of}
    dashboard["message"]=f"{count}/{len(dashboard['games'])} matchups have both sourced ratings. Projections are experimental, NOT calibrated."
    dashboard["status"]="EXPERIMENTAL_RATINGS" if count else "SCHEDULE_ONLY"
    output=Path(output_path);output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(dashboard,indent=2),encoding="utf-8")
    return dashboard["ratings_coverage"]

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--ratings",required=True)
    p.add_argument("--source",required=True)
    p.add_argument("--as-of",required=True)
    p.add_argument("--aliases")
    p.add_argument("--schedule",default="data/dashboard.json")
    p.add_argument("--output",default="data/dashboard.json")
    args=p.parse_args()
    print(json.dumps(attach(args.schedule,args.ratings,args.output,args.source,args.as_of,args.aliases),indent=2))
