import pandas as pd
import pytest

from wet_freight_tce import tce_calc


def test_tc1():
    ds = "2021-10-08"
    dd = {
        "Freight_USDMT": 10.0,
        "MGO": 500,
        "VLSFO": 500,
    }
    data = pd.DataFrame(dd, index=[pd.to_datetime(ds)])
    res = tce_calc.calc("TC1", data)

    assert res["GrossFreight"][ds] == pytest.approx(770250.0, abs=1e-1)
    assert res["BunkerCost"][ds] == pytest.approx(952169.24, abs=1e-1)
    assert res["TCE"][ds] == pytest.approx(-5683.48, abs=1e-1)


def test_tc2():
    ds = "2021-10-08"
    dd = {
        "FlatRate": 12.31,
        "WorldScale": 100.0,
        "MGO": 500,
        "VLSFO": 500,
        # 'HSFO': 560.25,
    }
    data = pd.DataFrame(dd, index=[pd.to_datetime(ds)])
    res = tce_calc.calc("TC2_37", data)

    assert res["GrossFreight"][ds] == pytest.approx(486685.4205, abs=1e-1)
    assert res["BunkerCost"][ds] == pytest.approx(322109.18, abs=1e-1)
    assert res["TCE"][ds] == pytest.approx(939.33, abs=1e-1)


def test_tc5():
    ds = "2021-10-06"

    dd = {
        "FlatRate": 10,
        "WorldScale": 100,
        "MGO": 500,
        "VLSFO": 500,
        "HSFO": 5000,
    }

    data = pd.DataFrame(dd, index=[pd.to_datetime(ds)])
    res = tce_calc.calc("tc5", data)

    assert res["GrossFreight"][ds] == pytest.approx(564850.0, abs=1e-1)
    assert res["BunkerCost"][ds] == pytest.approx(733306.95, abs=1e-1)
    assert res["TCE"][ds] == pytest.approx(-4974.08, abs=1e-1)


def test_tc6():
    ds = "2021-10-06"

    dd = {
        "FlatRate": 10,
        "WorldScale": 100,
        "MGO": 500.00,
        "VLSFO": 500.00,
        "HSFO": 500.00,
    }

    data = pd.DataFrame(dd, index=[pd.to_datetime(ds)])
    res = tce_calc.calc("tc6", data)

    assert res["GrossFreight"][ds] == pytest.approx(300000.0, abs=1e-1)
    assert res["BunkerCost"][ds] == pytest.approx(59536.57, abs=1e-1)
    assert res["TCE"][ds] == pytest.approx(11655.80, abs=1e-1)


def test_tc7():
    ds = "2021-10-06"

    dd = {
        "FlatRate": 10,
        "WorldScale": 100,
        "MGO": 500.00,
        "VLSFO": 500.00,
        "HSFO": 500.00,
    }

    data = pd.DataFrame(dd, index=[pd.to_datetime(ds)])
    res = tce_calc.calc("tc7", data)

    assert res["GrossFreight"][ds] == pytest.approx(350000.0, abs=1e-1)
    assert res["BunkerCost"][ds] == pytest.approx(419198.51, abs=1e-1)
    assert res["TCE"][ds] == pytest.approx(-4785.61, abs=1e-1)


def test_tc12():
    ds = "2021-10-06"

    dd = {
        "FlatRate": 10,
        "WorldScale": 100,
        "MGO": 500.00,
        "VLSFO": 500.00,
        "HSFO": 500.00,
    }

    data = pd.DataFrame(dd, index=[pd.to_datetime(ds)])
    res = tce_calc.calc("tc12", data)

    assert res["GrossFreight"][ds] == pytest.approx(358400.0, abs=1e-1)
    assert res["BunkerCost"][ds] == pytest.approx(526918.41, abs=1e-1)
    assert res["TCE"][ds] == pytest.approx(-5438.01, abs=1e-1)


def test_tc14():
    ds = "2021-10-06"

    dd = {
        "FlatRate": 10,
        "WorldScale": 100,
        "MGO": 500.00,
        "VLSFO": 500.00,
        "HSFO": 500.00,
    }

    data = pd.DataFrame(dd, index=[pd.to_datetime(ds)])
    res = tce_calc.calc("tc14", data)

    assert res["GrossFreight"][ds] == pytest.approx(380000.0, abs=1e-1)
    assert res["BunkerCost"][ds] == pytest.approx(477147.06, abs=1e-1)
    assert res["TCE"][ds] == pytest.approx(-5523.27, abs=1e-1)


def test_td3c():
    ds = "2021-10-06"

    dd = {
        "FlatRate": 10,
        "WorldScale": 100,
        "MGO": 500.00,
        "VLSFO": 500.00,
        "HSFO": 500.00,
    }

    data = pd.DataFrame(dd, index=[pd.to_datetime(ds)])
    res = tce_calc.calc("td3 c", data)

    assert res["GrossFreight"][ds] == pytest.approx(2772900.0, abs=1e-1)
    assert res["BunkerCost"][ds] == pytest.approx(1381545.31, abs=1e-1)
    assert res["TCE"][ds] == pytest.approx(21420.88, abs=1e-1)


def test_td7():
    ds = "2021-10-06"

    dd = {
        "FlatRate": 10,
        "WorldScale": 100,
        "MGO": 500.00,
        "VLSFO": 500.00,
        "HSFO": 500.00,
    }

    data = pd.DataFrame(dd, index=[pd.to_datetime(ds)])
    res = tce_calc.calc("td7", data)

    assert res["GrossFreight"][ds] == pytest.approx(800000.0, abs=1e-1)
    assert res["BunkerCost"][ds] == pytest.approx(126347.96, abs=1e-1)
    assert res["TCE"][ds] == pytest.approx(45375.37, abs=1e-1)


def test_td20():
    ds = "2021-10-06"

    dd = {
        "FlatRate": 10,
        "WorldScale": 100,
        "MGO": 500.00,
        "VLSFO": 500.00,
        "HSFO": 500.00,
    }

    data = pd.DataFrame(dd, index=[pd.to_datetime(ds)])
    res = tce_calc.calc("td20", data)

    assert res["GrossFreight"][ds] == pytest.approx(1411707.98, abs=1e-1)
    assert res["BunkerCost"][ds] == pytest.approx(828578.37, abs=1e-1)
    assert res["TCE"][ds] == pytest.approx(10215.94, abs=1e-1)


def test_td22():
    ds = "2021-10-06"

    dd = {
        "FlatRate": 10,
        "WorldScale": 100,
        "MGO": 500.00,
        "VLSFO": 500.00,
        "HSFO": 500.00,
    }

    data = pd.DataFrame(dd, index=[pd.to_datetime(ds)])
    res = tce_calc.calc("td22", data)

    assert res["GrossFreight"][ds] == pytest.approx(100.0, abs=1e-1)
    assert res["BunkerCost"][ds] == pytest.approx(3348962.36, abs=1e-1)
    assert res["TCE"][ds] == pytest.approx(-32299.82, abs=1e-1)


def test_td25():
    ds = "2021-10-06"

    dd = {
        "FlatRate": 10,
        "WorldScale": 100,
        "MGO": 500.00,
        "VLSFO": 500.00,
        "HSFO": 500.00,
    }

    data = pd.DataFrame(dd, index=[pd.to_datetime(ds)])
    res = tce_calc.calc("td25", data)

    assert res["GrossFreight"][ds] == pytest.approx(773128, abs=1e-1)
    assert res["BunkerCost"][ds] == pytest.approx(758251.69, abs=1e-1)
    assert res["TCE"][ds] == pytest.approx(-4369.55, abs=1e-1)
