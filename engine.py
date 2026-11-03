"""Independent women's basketball forecast math. No market lines enter projections."""
import hashlib, math, random

def forecast(away, home, n=10000, seed=None):
    required=("adj_off","adj_def","tempo")
    for team in (away,home):
        if any(not isinstance(team.get(k),(int,float)) or team[k]<=0 for k in required):
            raise ValueError("Verified positive adj_off, adj_def and tempo required")
    # These are provisional model specifications, not empirically calibrated coefficients.
    possessions=2/(1/away["tempo"]+1/home["tempo"])
    away_ppp=(away["adj_off"]*home["adj_def"]/100)/100
    home_ppp=(home["adj_off"]*away["adj_def"]/100)/100
    if seed is None:
        seed=int(hashlib.sha256(repr((away,home)).encode()).hexdigest()[:8],16)
    rng=random.Random(seed)
    trials=[]
    for _ in range(n):
        p=max(1,rng.gauss(possessions,math.sqrt(possessions)*0.7))
        shared=rng.gauss(0,0.045)
        a=max(0,round(p*max(0,rng.gauss(away_ppp+shared,0.10))))
        h=max(0,round(p*max(0,rng.gauss(home_ppp+shared,0.10))))
        trials.append((a,h))
    def quant(v,q): return sorted(v)[min(len(v)-1,int((len(v)-1)*q))]
    aa=[x[0] for x in trials]; hh=[x[1] for x in trials]
    totals=[a+h for a,h in trials]; margins=[h-a for a,h in trials]
    return {"seed":seed,"runs":n,"expected_possessions":possessions,
            "away_score":sum(aa)/n,"home_score":sum(hh)/n,
            "total":sum(totals)/n,"home_margin":sum(margins)/n,
            "home_win_probability":sum(h>a for a,h in trials)/n,
            "tie_probability":sum(h==a for a,h in trials)/n,
            "total_p10":quant(totals,.1),"total_p90":quant(totals,.9),
            "status":"EXPERIMENTAL_UNCALIBRATED"}
