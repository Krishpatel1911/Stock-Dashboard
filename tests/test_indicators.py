"""
tests/test_indicators.py
Run: pytest tests/ -v
"""

import pandas as pd
import numpy as np
import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.indicators import TechnicalIndicators as TI


@pytest.fixture
def sample_df():
    n = 100
    rng = np.random.default_rng(42)
    idx = pd.date_range("2024-01-01", periods=n, freq="B")
    prices = 150 + np.cumsum(rng.normal(0, 1.5, n))
    return pd.DataFrame({
        "Open":   prices * 0.999,
        "High":   prices * 1.012,
        "Low":    prices * 0.988,
        "Close":  prices,
        "Volume": rng.integers(1_000_000, 50_000_000, n).astype(float),
    }, index=idx)


def test_moving_averages(sample_df):
    df = TI.moving_averages(sample_df)
    assert "MA20" in df.columns
    assert "MA50" in df.columns
    assert not df["MA20"].iloc[19:].isna().any()


def test_bollinger_bands(sample_df):
    df = TI.bollinger_bands(sample_df)
    assert all(c in df.columns for c in ["BB_UPPER","BB_MID","BB_LOWER","BB_WIDTH"])
    # Upper must always be above lower (after warm-up period)
    valid = df.dropna(subset=["BB_UPPER", "BB_LOWER"])
    assert (valid["BB_UPPER"] >= valid["BB_LOWER"]).all()


def test_rsi_range(sample_df):
    df = TI.rsi(sample_df)
    assert "RSI" in df.columns
    rsi = df["RSI"].dropna()
    assert rsi.between(0, 100).all(), "RSI must be in [0, 100]"


def test_macd(sample_df):
    df = TI.macd(sample_df)
    for col in ["MACD", "MACD_SIGNAL", "MACD_HIST"]:
        assert col in df.columns
    # Histogram must equal MACD - Signal
    diff = (df["MACD_HIST"] - (df["MACD"] - df["MACD_SIGNAL"])).abs()
    assert diff.max() < 1e-10


def test_vwap(sample_df):
    df = TI.vwap(sample_df)
    assert "VWAP" in df.columns
    assert not df["VWAP"].isna().any()


def test_add_all_columns(sample_df):
    df = TI.add_all(sample_df)
    expected = ["MA20","MA50","BB_UPPER","BB_LOWER","VWAP","RSI","MACD","ATR","OBV"]
    for col in expected:
        assert col in df.columns, f"Missing column: {col}"