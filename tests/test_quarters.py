import pytest
from quarters import project_periods
def test_quarters_sum_to_halves():
    t={"Q1":15,"Q2":16,"Q3":18,"Q4":17}
    a=project_periods(t,t,seed=2,runs=10000)
    assert a["first_half"]["away"]==pytest.approx(a["quarters"]["Q1"]["away"]+a["quarters"]["Q2"]["away"])
    assert a["full_game"]["home"]==pytest.approx(a["first_half"]["home"]+a["second_half"]["home"])
    assert a==project_periods(t,t,seed=2,runs=10000)
def test_missing_periods_rejected():
    with pytest.raises(ValueError):project_periods({"Q1":15},{})
