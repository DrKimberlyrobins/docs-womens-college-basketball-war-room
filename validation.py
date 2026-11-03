"""Chronological scoring of independently archived forecasts."""
import math
def summarize(records):
    if not records: return {"n":0,"status":"NO_VALIDATED_FORECASTS"}
    n=len(records);total=[];margin=[];brier=[]
    for r in records:
        if r["created_utc"]>=r["tipoff_utc"]: raise ValueError("Forecast leakage: not pregame")
        f=r["forecast"];a=r["actual"]
        if a["status"]!="final":continue
        total.append(f["total"]-a["away_score"]-a["home_score"])
        margin.append(f["home_margin"]-(a["home_score"]-a["away_score"]))
        if a["home_score"]!=a["away_score"]:
            brier.append((f["home_win_probability"]-int(a["home_score"]>a["away_score"]))**2)
    if not total:return {"n":0,"status":"NO_VALIDATED_FORECASTS"}
    return {"n":len(total),"total_mae":sum(map(abs,total))/len(total),
            "total_rmse":math.sqrt(sum(x*x for x in total)/len(total)),
            "margin_mae":sum(map(abs,margin))/len(margin),
            "home_win_brier":sum(brier)/len(brier) if brier else None}
