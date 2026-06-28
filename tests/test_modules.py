import math
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from modules.decibels import db_to_linear, linear_to_db, dbm_to_mw, mw_to_dbm
from modules.shannon import shannon_capacity, nyquist_capacity, snr_db_to_linear
from modules.fibre import calc_pout, calc_pin, calc_length, calc_marge
from modules.cellulaire import calc_N


# --- Tests décibels ---

def test_db_to_linear():
    assert abs(db_to_linear(0) - 1.0) < 1e-9
    assert abs(db_to_linear(10) - 10.0) < 1e-9
    assert abs(db_to_linear(3) - 10 ** 0.3) < 1e-9

def test_linear_to_db():
    assert abs(linear_to_db(1.0) - 0.0) < 1e-9
    assert abs(linear_to_db(10.0) - 10.0) < 1e-9

def test_dbm_to_mw():
    assert abs(dbm_to_mw(0) - 1.0) < 1e-9
    assert abs(dbm_to_mw(30) - 1000.0) < 1e-6

def test_mw_to_dbm():
    assert abs(mw_to_dbm(1.0) - 0.0) < 1e-9
    assert abs(mw_to_dbm(1000.0) - 30.0) < 1e-6


# --- Tests Shannon / Nyquist ---

def test_shannon():
    # B=1Hz, S/B=1 (0dB) -> C = log2(2) = 1 bit/s
    C = shannon_capacity(1, 1)
    assert abs(C - 1.0) < 1e-9

def test_nyquist():
    # B=1Hz, M=2 -> C = 2*1*log2(2) = 2 bit/s
    C = nyquist_capacity(1, 2)
    assert abs(C - 2.0) < 1e-9

def test_snr_db_to_linear():
    assert abs(snr_db_to_linear(0) - 1.0) < 1e-9
    assert abs(snr_db_to_linear(10) - 10.0) < 1e-9


# --- Tests fibre optique ---

def test_calc_pout():
    # Pin=0dBm, alpha=0.2dB/km, L=10km, pas de connecteurs/épissures
    pout = calc_pout(0, 0.2, 10, 0, 0, 0, 0)
    assert abs(pout - (-2.0)) < 1e-9

def test_calc_pin():
    pin = calc_pin(-2.0, 0.2, 10, 0, 0, 0, 0)
    assert abs(pin - 0.0) < 1e-9

def test_calc_length():
    L = calc_length(0, -2.0, 0.2, 0, 0, 0, 0)
    assert abs(L - 10.0) < 1e-9

def test_calc_marge():
    assert abs(calc_marge(-10, -30) - 20.0) < 1e-9


# --- Tests cellulaire ---

def test_calc_N():
    assert calc_N(1, 0) == 1
    assert calc_N(1, 1) == 3
    assert calc_N(2, 0) == 4
    assert calc_N(2, 1) == 7
    assert calc_N(3, 0) == 9
    assert calc_N(2, 2) == 12


if __name__ == "__main__":
    tests = [
        test_db_to_linear, test_linear_to_db, test_dbm_to_mw, test_mw_to_dbm,
        test_shannon, test_nyquist, test_snr_db_to_linear,
        test_calc_pout, test_calc_pin, test_calc_length, test_calc_marge,
        test_calc_N,
    ]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL  {t.__name__}: {e}")

    print(f"\n{passed}/{len(tests)} tests passés.")
