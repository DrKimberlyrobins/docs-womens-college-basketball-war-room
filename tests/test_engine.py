import pytest
from engine import forecast
def test_reproducible():
    a={"adj_off":100,"adj_def":100,"tempo":70}
    assert forecast(a,a,10000,42)==forecast(a,a,10000,42)
def test_real_simulations():
    a={"adj_off":100,"adj_def":100,"tempo":70}
    r=forecast(a,a,10000,42)
    assert r["runs"]==10000 and r["total_p90"]>r["total_p10"]
def test_missing_data_rejected():
    with pytest.raises(ValueError): forecast({}, {})
