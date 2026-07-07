"""
indicators.py — Pure-pandas technical indicator calculations.
No TA-Lib dependency; fully portable.

Indicators implemented:
  • MA20, MA50  (Simple Moving Average)
  • Bollinger Bands (20-period, ±2σ)
  • VWAP  (Volume-Weighted Average Price)
  • RSI   (14-period Relative Strength Index)
  • MACD  (12/26/9 EMA)
  • ATR   (14-period Average True Range)
  • OBV   (On-Balance Volume)
"""

from __future__ import annotations
import pandas as pd
import numpy as np


class TechnicalIndicators:
    """Stateless utility class — all methods are static."""

    @staticmethod
    def add_all(df: pd.DataFrame) -> pd.DataFrame:
        """Convenience wrapper: apply every indicator at once."""
        df = TechnicalIndicators.moving_averages(df)
        df = TechnicalIndicators.bollinger_bands(df)
        df = TechnicalIndicators.vwap(df)
        df = TechnicalIndicators.rsi(df)
        df = TechnicalIndicators.macd(df)
        df = TechnicalIndicators.atr(df)
        df = TechnicalIndicators.obv(df)
        return df

    # ── Moving Averages ───────────────────────────────────────────────────────
    @staticmethod
    def moving_averages(df: pd.DataFrame,
                        windows: list[int] | None = None) -> pd.DataFrame:
        windows = windows or [20, 50]
        for w in windows:
            df[f"MA{w}"] = df["Close"].rolling(w, min_periods=1).mean()
        return df

    # ── Bollinger Bands ───────────────────────────────────────────────────────
    @staticmethod
    def bollinger_bands(df: pd.DataFrame, window: int = 20, n_std: float = 2.0) -> pd.DataFrame:
        mid        = df["Close"].rolling(window, min_periods=1).mean()
        std        = df["Close"].rolling(window, min_periods=1).std()
        df["BB_MID"]   = mid
        df["BB_UPPER"] = mid + n_std * std
        df["BB_LOWER"] = mid - n_std * std
        df["BB_WIDTH"] = (df["BB_UPPER"] - df["BB_LOWER"]) / mid   # squeeze indicator
        return df

    # ── VWAP ─────────────────────────────────────────────────────────────────
    @staticmethod
    def vwap(df: pd.DataFrame) -> pd.DataFrame:
        typical = (df["High"] + df["Low"] + df["Close"]) / 3
        cum_vol = df["Volume"].cumsum()
        cum_tp  = (typical * df["Volume"]).cumsum()
        df["VWAP"] = cum_tp / cum_vol
        return df

    # ── RSI ───────────────────────────────────────────────────────────────────
    @staticmethod
    def rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        delta  = df["Close"].diff()
        gain   = delta.clip(lower=0)
        loss   = -delta.clip(upper=0)
        avg_g  = gain.ewm(alpha=1/period, min_periods=period).mean()
        avg_l  = loss.ewm(alpha=1/period, min_periods=period).mean()
        rs     = avg_g / avg_l.replace(0, np.nan)
        df["RSI"] = (100 - 100 / (1 + rs)).fillna(50)
        return df

    # ── MACD ──────────────────────────────────────────────────────────────────
    @staticmethod
    def macd(df: pd.DataFrame,
             fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        ema_fast      = df["Close"].ewm(span=fast, adjust=False).mean()
        ema_slow      = df["Close"].ewm(span=slow, adjust=False).mean()
        df["MACD"]    = ema_fast - ema_slow
        df["MACD_SIGNAL"] = df["MACD"].ewm(span=signal, adjust=False).mean()
        df["MACD_HIST"]   = df["MACD"] - df["MACD_SIGNAL"]
        return df

    # ── ATR ───────────────────────────────────────────────────────────────────
    @staticmethod
    def atr(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        prev_close = df["Close"].shift(1)
        tr = pd.concat([
            df["High"] - df["Low"],
            (df["High"] - prev_close).abs(),
            (df["Low"]  - prev_close).abs(),
        ], axis=1).max(axis=1)
        df["ATR"] = tr.ewm(span=period, adjust=False).mean()
        return df

    # ── OBV ───────────────────────────────────────────────────────────────────
    @staticmethod
    def obv(df: pd.DataFrame) -> pd.DataFrame:
        direction = np.sign(df["Close"].diff()).fillna(0)
        df["OBV"]  = (direction * df["Volume"]).cumsum()
        return df