"""Odds comparison only. This module never modifies the underlying forecast."""
def compare(home_margin,projected_total,market_home_spread=None,market_total=None):
    # Market home spread uses sportsbook convention: negative is favorite.
    out={"model_home_margin":home_margin,"model_total":projected_total}
    if market_home_spread is not None:
        out["market_home_spread"]=market_home_spread
        out["home_spread_edge"]=home_margin+market_home_spread
    if market_total is not None:
        out["market_total"]=market_total
        out["total_edge"]=projected_total-market_total
    return out

def american_implied_probability(odds):
    if odds==0:raise ValueError("Invalid American odds")
    return (-odds)/(-odds+100) if odds<0 else 100/(odds+100)

def no_vig_two_way(odds_a,odds_b):
    a=american_implied_probability(odds_a)
    b=american_implied_probability(odds_b)
    return a/(a+b),b/(a+b)
