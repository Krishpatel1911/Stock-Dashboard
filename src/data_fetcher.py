"""
data_fetcher.py — Responsible for all data retrieval.
Uses yfinance (Yahoo Finance) with Streamlit caching.
Falls back to realistic synthetic data when offline.
"""

from __future__ import annotations
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

try:
    import yfinance as yf
    YF_AVAILABLE = True
except ImportError:
    YF_AVAILABLE = False


class DataFetcher:
    """Fetch OHLCV stock data with smart caching and fallback."""

    # ── Public API ────────────────────────────────────────────────────────────
    def get_stock_data(self, symbol: str, days: int) -> tuple[pd.DataFrame | None, dict]:
        """
        Returns (df, meta) where df has DatetimeIndex + OHLCV columns.
        meta is a dict with marketCap, sector, etc.
        Caches for 5 minutes via Streamlit.
        """
        return self._cached_fetch(symbol, days)

    # ── Internal ──────────────────────────────────────────────────────────────
    @st.cache_data(ttl=300, show_spinner=False)
    def _cached_fetch(_self, symbol: str, days: int):
        if YF_AVAILABLE:
            return _self._fetch_yfinance(symbol, days)
        return _self._synthetic(symbol, days), {}

    def _fetch_yfinance(self, symbol: str, days: int):
        try:
            end   = datetime.today()
            start = end - timedelta(days=days + 30)        # extra buffer for indicators
            ticker = yf.Ticker(symbol)
            df     = ticker.history(start=start, end=end, auto_adjust=True)
            if df.empty:
                raise ValueError("Empty response")

            df.index = pd.to_datetime(df.index).tz_localize(None)
            df = df[["Open", "High", "Low", "Close", "Volume"]].dropna()
            df = df[df.index >= end - timedelta(days=days + 30)]

            meta = {}
            try:
                info = ticker.info
                meta = {
                    "marketCap": info.get("marketCap", 0),
                    "sector":    info.get("sector", "N/A"),
                    "industry":  info.get("industry", "N/A"),
                    "website":   info.get("website", ""),
                    "beta":      info.get("beta", "N/A"),
                    "peRatio":   info.get("trailingPE", "N/A"),
                }
            except Exception:
                pass

            return df, meta

        except Exception as e:
            st.warning(f"⚠️ Live data unavailable ({e}). Showing simulated data.")
            return self._synthetic(symbol, days), {}

    @staticmethod
    def _synthetic(symbol: str, days: int) -> pd.DataFrame:
        """Realistic GBM-based synthetic OHLCV data."""
        BASE = {
            "AAPL": 178, "GOOGL": 141, "TSLA": 245, "MSFT": 415,
            "AMZN": 185, "META": 480, "NFLX": 620, "NVDA": 875,
            "RELIANCE.NS": 2950, "TCS.NS": 3800, "HDFCBANK.NS": 1680,
        }
        base  = BASE.get(symbol, 200)
        rng   = np.random.default_rng(abs(hash(symbol)) % 10_000)
        total = days + 60
        dates = pd.bdate_range(end=datetime.today(), periods=total)

        # Geometric Brownian Motion
        mu    = 0.0003
        sigma = 0.015
        dt    = 1
        log_returns = rng.normal((mu - 0.5 * sigma**2) * dt, sigma * np.sqrt(dt), total)
        prices = base * np.exp(np.cumsum(log_returns))

        opens  = prices * (1 + rng.uniform(-0.008, 0.008, total))
        highs  = prices * (1 + rng.uniform(0.004, 0.022, total))
        lows   = prices * (1 - rng.uniform(0.004, 0.022, total))
        vols   = rng.integers(4_000_000, 90_000_000, total).astype(float)

        df = pd.DataFrame({
            "Open": opens, "High": highs, "Low": lows,
            "Close": prices, "Volume": vols
        }, index=dates)
        return df