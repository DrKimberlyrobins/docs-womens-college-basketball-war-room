"""Strict import and integrity checks for authorized historical results."""
import csv,json
from pathlib import Path
def read_historical_csv(path):
    required={"game_id","tipoff_utc","home_id","away_id","home_final","away_final","home_q1","home_q2","home_q3","home_q4","away_q1","away_q2","away_q3","away_q4"}
    with open(path,newline="",encoding="utf-8") as f:
        reader=csv.DictReader(f)
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("Missing historical columns: "+",".join(sorted(required-set(reader.fieldnames or []))))
        games=[];ids=set()
        for row in reader:
            if row["game_id"] in ids:raise ValueError("Duplicate historical game")
            ids.add(row["game_id"])
            for team in ("home","away"):
                quarter=sum(int(row[f"{team}_q{i}"]) for i in range(1,5))
                final=int(row[f"{team}_final"])
                if quarter>final:raise ValueError("Quarter totals exceed final")
                row[f"{team}_regulation"]=quarter
                row[f"{team}_overtime"]=final-quarter
            games.append(row)
    return games
