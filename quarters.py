"""Evidence-based period model: requires actual period-level historical priors."""
import random, math
PERIODS=("Q1","Q2","Q3","Q4")
def project_periods(away,home,seed=42,runs=10000):
    # Inputs are period-specific expected points, independently estimated from historical data.
    for team in (away,home):
        if not isinstance(team,dict) or any(not isinstance(team.get(p),(int,float)) or team[p]<0 for p in PERIODS):
            raise ValueError("Verified period-level point expectations required for every quarter")
    rng=random.Random(seed)
    draws=[]
    for _ in range(runs):
        common=rng.gauss(0,.04)
        row={}
        for p in PERIODS:
            # Dispersion is provisional until trained on historical quarter outcomes.
            row[p]=(max(0,round(rng.gauss(away[p]*(1+common),max(1,math.sqrt(away[p])*1.5)))),
                    max(0,round(rng.gauss(home[p]*(1+common),max(1,math.sqrt(home[p])*1.5)))))
        draws.append(row)
    means={p:{"away":sum(d[p][0] for d in draws)/runs,"home":sum(d[p][1] for d in draws)/runs} for p in PERIODS}
    def combine(keys):
        return {"away":sum(means[k]["away"] for k in keys),"home":sum(means[k]["home"] for k in keys)}
    return {"quarters":means,"first_half":combine(("Q1","Q2")),"second_half":combine(("Q3","Q4")),
            "full_game":combine(PERIODS),"runs":runs,"seed":seed,
            "status":"PROVISIONAL_NOT_CALIBRATED"}
