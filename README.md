<div align="center">

# 📊 Stoker — Real-Time Stock Market Intelligence Dashboard

**A production-ready market analysis platform built with Python, Streamlit & Plotly**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-5.22+-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)
[![CI](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/Bansaripatel02/StockIQ-Market-Intelligence-Dashboard/actions)

<br/>

*Live candlestick charts · 8 technical indicators · 17 stocks · 6 time periods*

<br/>

[🚀 Quick Start](#-quick-start) · [✨ Features](#-features) · [🛠 Tech Stack](#-tech-stack) · [📖 Docs](#-architecture)

</div>

---

## 🎯 Problem Statement

Retail investors and finance students need professional-grade market analysis tools — but Bloomberg Terminal costs **$24,000/year** and most free tools lack technical depth.

**Stoker** solves this by delivering:
- ✅ **Live OHLCV data** via Yahoo Finance — completely free, no API key needed
- ✅ **8 technical indicators** calculated in pure NumPy/Pandas — no TA-Lib dependency issues
- ✅ **3 interactive chart types** with zoom, pan, and crosshair — publication-quality Plotly charts
- ✅ **Statistical analysis** — Sharpe Ratio, Max Drawdown, Skewness, Kurtosis
- ✅ **CSV export** of full OHLCV + indicator data for further analysis
- ✅ **Smart fallback** — GBM synthetic data when Yahoo Finance rate-limits

---

## ✨ Features

### 📈 Interactive Price Charts
| Chart Type | Description |
|---|---|
| **Candlestick** | Classic OHLC with bull/bear color coding |
| **Line Chart** | Gradient area fill for trend visualization |
| **OHLC Bar** | Traditional bar chart for active traders |

### 🔬 Technical Indicators (8 built-in)

| Indicator | Parameters | Trading Signal |
|---|---|---|
| **MA 20** | 20-day Simple Moving Average | Short-term trend direction |
| **MA 50** | 50-day Simple Moving Average | Medium-term trend direction |
| **Bollinger Bands** | 20-period · ±2σ | Volatility & overbought/oversold zones |
| **VWAP** | Volume-Weighted Average Price | Institutional fair value level |
| **RSI** | 14-period Relative Strength Index | >70 overbought · <30 oversold |
| **MACD** | 12 / 26 / 9 EMA | Momentum & signal line crossovers |
| **ATR** | 14-period Average True Range | Volatility for stop-loss sizing |
| **OBV** | On-Balance Volume | Volume trend confirmation |

### 📊 Sub-Charts
- **Volume** — bull/bear color-coded bars with OBV overlay on secondary axis
- **RSI** — shaded overbought (>70) and oversold (<30) zones with gradient fill
- **MACD** — histogram + signal line + MACD line with zero-cross marker

### 📋 Data & Analytics
- **Metric cards** — Live price, % change, 52W High/Low, RSI reading, Avg Volume, Market Cap
- **Statistics tab** — Mean, Std Dev, Variance, Skewness, Kurtosis, Sharpe Ratio, Max Drawdown, Daily Return σ
- **CSV export** — Download complete OHLCV + all calculated indicator columns
- **Recent data table** — Last 15 trading days with daily % change column

### 🗂 Watchlist (17 instruments)
```
US Stocks  →  AAPL · GOOGL · TSLA · MSFT · AMZN · META · NFLX · NVDA · V · JPM
Indian NSE →  RELIANCE · TCS · HDFCBANK · INFY · WIPRO
ETFs       →  SPY (S&P 500 Index) · GLD (Gold)
```

---

## 🛠 Tech Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| **UI Framework** | Streamlit | 1.35+ | Python-native dashboard — zero JavaScript required |
| **Charting** | Plotly | 5.22+ | Interactive, zoomable financial-grade charts |
| **Data Source** | yfinance | 0.2.40+ | Yahoo Finance wrapper — no API key required |
| **Data Processing** | Pandas | 2.2+ | DataFrame operations & rolling window indicators |
| **Numerics** | NumPy | 1.26+ | Vectorised EWM & cumulative calculations |
| **Styling** | Custom CSS | — | Dark finance theme (`.streamlit/config.toml`) |
| **Testing** | pytest | 8.2+ | Unit tests for all 7 indicator calculations |
| **CI/CD** | GitHub Actions | — | Auto-runs full test suite on every push to main |

---

## 📁 Project Structure

```
Stoker-Market-Intelligence-Dashboard/
│
├── 📄 app.py                    # Streamlit entry point — complete dashboard UI
│
├── 📂 src/
│   ├── __init__.py
│   ├── config.py                # Watchlist, time periods, Plotly color tokens
│   ├── data_fetcher.py          # yfinance fetch + GBM synthetic data fallback
│   ├── indicators.py            # MA, BB, VWAP, RSI, MACD, ATR, OBV (pure Pandas)
│   └── charts.py                # ChartBuilder class — all Plotly figure builders
│
├── 📂 assets/
│   └── style.css                # Custom dark theme stylesheet
│
├── 📂 tests/
│   └── test_indicators.py       # 6 pytest unit tests — one per indicator
│
├── 📂 .streamlit/
│   └── config.toml              # Streamlit theme & server config
│
├── 📂 .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI pipeline
│
├── 📄 requirements.txt          # Pinned production dependencies
├── 📄 .gitignore
└── 📄 README.md
```

---

## ⚡ Quick Start

### Prerequisites
- **Python 3.12** (64-bit) — [Download](https://www.python.org/downloads/release/python-31210/)
- **Git** — [Download](https://git-scm.com)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Bansaripatel02/StockIQ-Market-Intelligence-Dashboard.git
cd StockIQ-Market-Intelligence-Dashboard

# 2. Create a virtual environment
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — Mac / Linux
source venv/bin/activate

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Launch the dashboard
streamlit run app.py
```

**Open your browser → [http://localhost:8501](http://localhost:8501)** 🎉

> **Note:** On first run, yfinance fetches live data from Yahoo Finance.
> If rate-limited, the app automatically serves realistic simulated data — no crash, no error message.

---

## 🖥 Usage Guide

| What you want | How to do it |
|---|---|
| Switch stock | Sidebar → **Select Stock** dropdown |
| Change date range | Sidebar → **Time Period** slider (1W → 1Y) |
| Toggle MA / Bollinger Bands | Sidebar → **Overlays** section |
| Toggle Volume / RSI / MACD | Sidebar → **Sub-Charts** section |
| Change chart style | Sidebar → Candlestick / Line / OHLC Bar |
| Refresh live data | Sidebar → **🔄 Refresh Data** button |
| Download data as CSV | **Export tab** → ⬇️ Download CSV |
| View Sharpe Ratio etc. | **Statistics tab** |

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

```
tests/test_indicators.py::test_moving_averages   PASSED  [ 16%]
tests/test_indicators.py::test_bollinger_bands   PASSED  [ 33%]
tests/test_indicators.py::test_rsi_range         PASSED  [ 50%]
tests/test_indicators.py::test_macd              PASSED  [ 66%]
tests/test_indicators.py::test_vwap              PASSED  [ 83%]
tests/test_indicators.py::test_add_all_columns   PASSED  [100%]

========================= 6 passed in 0.83s =========================
```

---

## 🏗 Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        app.py  (Streamlit UI)                    │
│   Sidebar → Metric Cards → Price Chart → Sub-charts → Data Tabs  │
└──────────┬───────────────────┬─────────────────┬────────────────┘
           │                   │                 │
  ┌────────▼────────┐  ┌───────▼──────┐  ┌──────▼──────────────┐
  │  data_fetcher   │  │  indicators  │  │     charts.py        │
  │                 │  │              │  │                      │
  │  yfinance API   │  │  MA20 / MA50 │  │  price_chart()       │
  │       +         │  │  Bollinger   │  │  volume_chart()      │
  │  GBM Fallback   │  │  VWAP / RSI  │  │  rsi_chart()        │
  │  (offline mode) │  │  MACD / ATR  │  │  macd_chart()       │
  │                 │  │  OBV         │  │                      │
  └─────────────────┘  └──────────────┘  └──────────────────────┘
```

### Design Decisions

**Why pure-Pandas indicators instead of TA-Lib?**
> TA-Lib requires a C compiler — notoriously hard to install on Windows and breaks on Python 3.12+. Pure NumPy/Pandas gives mathematically identical results with zero setup friction on any platform.

**Why a GBM synthetic data fallback?**
> Yahoo Finance rate-limits API calls aggressively. Geometric Brownian Motion simulation keeps the dashboard fully functional for demos, interviews, and offline use — with realistic price behaviour.

**Why Streamlit over Flask/Dash?**
> For a single-page data dashboard, Streamlit cuts the codebase in half. Flask/Dash would be the right choice if we needed multi-page routing, user login, or a custom REST API.

---

## 📐 Indicator Formulas

```
MA(n)     = (1/n) × Σ Close[t]          for the last n periods

BB_upper  = MA20 + 2σ₂₀
BB_lower  = MA20 − 2σ₂₀

VWAP      = Σ(Typical × Volume) / Σ(Volume)
            Typical = (High + Low + Close) / 3

RSI       = 100 − [100 / (1 + RS)]
            RS = EWM_avg(gains, 14) / EWM_avg(losses, 14)

MACD      = EMA(Close, 12) − EMA(Close, 26)
Signal    = EMA(MACD, 9)
Histogram = MACD − Signal

ATR       = EWM[ max(H−L, |H−C_prev|, |L−C_prev|), α=1/14 ]

OBV       = Σ [ sign(ΔClose) × Volume ]
```

---

## 🗺 Roadmap

- [ ] **Portfolio tracker** — compare multiple tickers on one chart
- [ ] **Price alerts** — email/Telegram notification on RSI or MA crossover
- [ ] **Stock comparison** — overlay two symbols on the same axis
- [ ] **Options chain viewer** — implied volatility surface
- [ ] **ML price prediction** — LSTM trained on historical OHLCV + indicators
- [ ] **Docker support** — single `docker compose up` deployment

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

```bash
# Fork → branch → commit → PR
git checkout -b feature/your-feature-name
git commit -m "feat: add Stochastic Oscillator"
git push origin feature/your-feature-name
```

Before submitting, make sure:
- [ ] `pytest tests/ -v` — all 6 tests pass
- [ ] Code follows existing style in `src/`
- [ ] New indicators have a matching unit test

---

## 📜 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 👤 Author

**Krish Patel**

---

<div align="center">

**If this project helped you, please consider giving it a ⭐ — it really helps!**

*Built as part of a Data Science & Python portfolio · Data from Yahoo Finance*

*⚠️ For educational purposes only · Not financial advice*

</div>