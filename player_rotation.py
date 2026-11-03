"""Attach verified top five rotation players for each team, sorted by minutes.
CSV columns: team,name,height,position,minutes_per_game,points_per_game,role.
No fabricated heights or players. Partial coverage explicitly reported.
"""
import csv,json,re,sys
from pathlib import Path
from team_stats import canonical
def attach_players(dashboard_path,players_csv,output_path,source,season,aliases_path=None):
    if not source or not season:raise ValueError("Source and season required")
    d=json.loads(Path(dashboard_path).read_text())
    aliases=json.loads(Path(aliases_path).read_text()) if aliases_path else {}
    aliases={canonical(k):canonical(v) for k,v in aliases.items()}
    groups={}
    with open(players_csv,newline="",encoding="utf-8") as f:
        reader=csv.DictReader(f)
        required={"team","name","height","position","minutes_per_game","points_per_game","role"}
        if not required.issubset(reader.fieldnames or []):raise ValueError("Missing columns "+str(required-set(reader.fieldnames or [])))
        for row in reader:
            key=canonical(row["team"])
            if not key or not row["name"].strip():continue
            mins=float(row["minutes_per_game"])
            pts=float(row["points_per_game"])
            if not 0<=mins<=45 or not 0<=pts<=60:raise ValueError("Invalid player stats "+row["name"])
            height=row["height"].strip()
            if height and not re.fullmatch(r"(?:[4-7])[-'][0-9]{1,2}(?:\\\"|\")?|(?:1[4-9][0-9]|2[0-2][0-9])\\s?cm",height):
                raise ValueError("Invalid height format "+height)
            groups.setdefault(key,[]).append({"name":row["name"],"height":height or None,
               "position":row["position"] or None,"minutes_per_game":mins,
               "points_per_game":pts,"role":row["role"] or None})
    covered=0
    for game in d["games"]:
        block={"source":source,"season":season}
        for side in ("away","home"):
            key=canonical(game[side]);key=aliases.get(key,key)
            players=sorted(groups.get(key,[]),key=lambda x:-x["minutes_per_game"])[:5]
            block[side]=players
            if len(players)==5:covered+=1
        game["top_players"]=block
        game.setdefault("data_coverage",{})["top_five_players"]="verified" if len(block["away"])==5 and len(block["home"])==5 else "incomplete"
    d["player_coverage"]={"teams_with_five":covered,"teams_expected":len(d["games"])*2,"source":source,"season":season}
    Path(output_path).write_text(json.dumps(d,indent=2),encoding="utf-8")
    return d["player_coverage"]
if __name__=="__main__":
    attach_players(sys.argv[1],sys.argv[2],sys.argv[1],sys.argv[3],sys.argv[4],sys.argv[5] if len(sys.argv)>5 else None)
