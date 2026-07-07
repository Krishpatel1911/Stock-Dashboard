"""
config.py — Central configuration for Stock Dashboard
All tuneable constants live here — change once, affects everywhere.
"""

PAGE_CONFIG = dict(
    page_title="Stocker Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help":    "https://github.com/yourusername/stock-dashboard",
        "Report a bug":"https://github.com/yourusername/stock-dashboard/issues",
        "About":       "**StockIQ** — Real-time Stock Market Intelligence Dashboard",
    }
)

# Watchlist: Display Name → Yahoo Finance ticker
WATCHLIST = {
    # ── US Stocks ──
    "🍎 Apple (AAPL)":       "AAPL",
    "🔍 Alphabet (GOOGL)":   "GOOGL",
    "🚗 Tesla (TSLA)":       "TSLA",
    "💻 Microsoft (MSFT)":   "MSFT",
    "📦 Amazon (AMZN)":      "AMZN",
    "📘 Meta (META)":        "META",
    "🔴 Netflix (NFLX)":     "NFLX",
    "💳 Visa (V)":           "V",
    "💰 JPMorgan (JPM)":     "JPM",
    "⚡ NVIDIA (NVDA)":      "NVDA",
    # ── Indian Stocks (NSE) ──
    "🛢  Reliance (NSE)":    "RELIANCE.NS",
    "💻 TCS (NSE)":          "TCS.NS",
    "🏦 HDFC Bank (NSE)":    "HDFCBANK.NS",
    "🔬 Infosys (NSE)":      "INFY.NS",
    "🏭 Wipro (NSE)":        "WIPRO.NS",
    # ── ETFs / Indices ──
    "📈 S&P 500 ETF (SPY)":  "SPY",
    "💎 Gold ETF (GLD)":     "GLD",
}

PERIODS = {
    "1 Week":   7,
    "2 Weeks":  14,
    "1 Month":  30,
    "3 Months": 90,
    "6 Months": 180,
    "1 Year":   365,
}

# Plotly chart base template (dark finance theme)
CHART_TEMPLATE  = "plotly_dark"
CHART_BG        = "rgba(0,0,0,0)"      # transparent → CSS controls bg
CHART_PAPER_BG  = "rgba(0,0,0,0)"
GRID_COLOR      = "rgba(255,255,255,0.06)"
BULL_COLOR      = "#26a69a"            # teal-green
BEAR_COLOR      = "#ef5350"            # red
MA20_COLOR      = "#42a5f5"            # blue
MA50_COLOR      = "#ffca28"            # amber
BB_COLOR        = "rgba(167,139,250,0.4)"  # violet
VWAP_COLOR      = "#4dd0e1"            # cyan
MACD_COLOR      = "#ab47bc"
SIGNAL_COLOR    = "#ff7043"