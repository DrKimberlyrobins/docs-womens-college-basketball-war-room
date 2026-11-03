from market import compare,no_vig_two_way
def test_comparison_not_calibration():
    p=compare(8,140,-6.5,136.5)
    assert p["home_spread_edge"]==1.5 and p["total_edge"]==3.5
    assert p["model_total"]==140
def test_vig_removal():
    a,b=no_vig_two_way(-110,-110)
    assert a==.5 and b==.5
