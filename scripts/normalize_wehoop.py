"""Strict mapping from inspected wehoop historical ratings schema.
Never silently substitute an incompatible statistic.
"""
import csv,sys
from pathlib import Path
def normalize(source,dest):
    with open(source,encoding="utf-8",newline="") as f:
        reader=csv.DictReader(f)
        rows=list(reader);columns=set(reader.fieldnames or [])
    # Candidate names differ across released model vintages. Explicitly fail
    # when expected fields cannot be identified without ambiguity.
    options={
      "team":[("team",),("team_name",),("display_name",)],
      "adj_off":[("adj_off",),("adj_o",),("adjusted_offense",),("adj_offensive_efficiency",)],
      "adj_def":[("adj_def",),("adj_d",),("adjusted_defense",),("adj_defensive_efficiency",)],
      "tempo":[("tempo",),("adj_tempo",),("adjusted_tempo",),("pace",)]
    }
    found={}
    for target,sets in options.items():
        candidates=[x for group in sets for x in group if x in columns]
        if len(candidates)!=1:raise ValueError(f"Cannot unambiguously map {target}: candidates={candidates}; actual columns={sorted(columns)}")
        found[target]=candidates[0]
    dest=Path(dest);dest.parent.mkdir(parents=True,exist_ok=True)
    with dest.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(options));writer.writeheader()
        for row in rows:
            writer.writerow({key:row[column] for key,column in found.items()})
    print("Normalized",len(rows),"historical ratings with mapping",found)
if __name__=="__main__":normalize(sys.argv[1],sys.argv[2])
