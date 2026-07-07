"""
╔══════════════════════════════════════════════════════════════════╗
║         STOCK MARKET INTELLIGENCE DASHBOARD                      ║
║         Production-Ready | Python + Streamlit + Plotly           ║
║         UI: Terminal / Exchange-board redesign                   ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import numpy as np
import pandas as pd
from src.data_fetcher import DataFetcher
from src.indicators import TechnicalIndicators
from src.charts import ChartBuilder
from src.config import WATCHLIST, PAGE_CONFIG, PERIODS

# ─── Page Config (must be first Streamlit call) ───────────────────────────────
st.set_page_config(**PAGE_CONFIG)

# ─── Inject Custom CSS ────────────────────────────────────────────────────────
with open("assets/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ─── Sidebar ("control rail") ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="rail-logo">STOCKER</div>', unsafe_allow_html=True)
    st.markdown('<p class="rail-sub">Market Intelligence Terminal</p>', unsafe_allow_html=True)

    st.markdown('<div class="rail-section">Instrument</div>', unsafe_allow_html=True)
    ticker_label = st.selectbox(
        "Ticker",
        options=list(WATCHLIST.keys()),
        label_visibility="collapsed"
    )
    symbol = WATCHLIST[ticker_label]

    st.markdown('<div class="rail-section">Time Window</div>', unsafe_allow_html=True)
    period_label = st.select_slider(
        "Period",
        options=list(PERIODS.keys()),
        value="3 Months",
        label_visibility="collapsed"
    )
    days = PERIODS[period_label]

    st.markdown('<div class="rail-section">Chart Style</div>', unsafe_allow_html=True)
    chart_type = st.radio(
        "Chart Type",
        ["Candlestick", "Line", "OHLC Bar"],
        label_visibility="collapsed",
        horizontal=False
    )

    st.markdown('<div class="rail-section">Overlays</div>', unsafe_allow_html=True)
    show_ma   = st.toggle("Moving Averages (MA20/MA50)", value=True)
    show_bb   = st.toggle("Bollinger Bands", value=True)
    show_vwap = st.toggle("VWAP", value=False)

    st.markdown('<div class="rail-section">Sub-Charts</div>', unsafe_allow_html=True)
    show_volume = st.toggle("Volume", value=True)
    show_rsi    = st.toggle("RSI (14)", value=True)
    show_macd   = st.toggle("MACD", value=True)

    st.markdown('<div class="rail-section">System</div>', unsafe_allow_html=True)
    if st.button("↻  Refresh Feed", use_container_width=True):
        st.cache_data.clear()

    st.caption("Data via Yahoo Finance · Updates on refresh")

# ─── Fetch Data ───────────────────────────────────────────────────────────────
fetcher = DataFetcher()

with st.spinner(f"Loading {ticker_label}..."):
    df, meta = fetcher.get_stock_data(symbol, days)

if df is None or df.empty:
    st.error(f"⚠️ Could not load data for **{symbol}**. Check your internet connection and try again.")
    st.stop()

# Add technical indicators
df = TechnicalIndicators.add_all(df)

# ─── Derived values ─────────────────────────────────────────────────────────
latest  = df["Close"].iloc[-1]
prev    = df["Close"].iloc[-2]
change  = latest - prev
pct     = (change / prev) * 100
high52  = df["High"].max()
low52   = df["Low"].min()
rsi_val = df["RSI"].iloc[-1]
vol_avg = df["Volume"].mean()
mkt_cap = meta.get("marketCap", 0)

arrow   = "▲" if change >= 0 else "▼"
clr_cls = "positive" if change >= 0 else "negative"

# ─── Scrolling tape (decorative, built from the current watchlist) ───────────
tape_items = []
for label, sym in WATCHLIST.items():
    cls = "up" if sym == symbol and change >= 0 else ("down" if sym == symbol and change < 0 else "")
    marker = f"{arrow} {abs(pct):.2f}%" if sym == symbol else "—"
    tape_items.append(f'<span class="{cls}">{sym}  {marker}</span>')
tape_html = "".join(tape_items) * 2  # doubled for seamless scroll loop
st.markdown(f'<div class="tape-wrap"><div class="tape-track">{tape_html}</div></div>', unsafe_allow_html=True)

# ─── Header Readout ─────────────────────────────────────────────────────────
st.markdown(
    f'<div class="header-block">'
    f'<div class="ticker-name">{ticker_label}</div>'
    f'<div class="ticker-symbol">{symbol}</div>'
    f'<div class="price-row">'
    f'<span class="price">${latest:,.2f}</span>'
    f'<span class="change {clr_cls}">{arrow} {abs(change):.2f} ({abs(pct):.2f}%)</span>'
    f'</div></div>',
    unsafe_allow_html=True
)

# ─── Metric Board Strip ───────────────────────────────────────────────────────
cards_data = [
    ("52W High",   f"${high52:,.2f}",   None),
    ("52W Low",    f"${low52:,.2f}",    None),
    ("RSI (14)",   f"{rsi_val:.1f}",    "OVERBOUGHT" if rsi_val > 70 else ("OVERSOLD" if rsi_val < 30 else "NEUTRAL")),
    ("Avg Volume", f"{vol_avg/1e6:.2f}M", None),
    ("Day High",   f"${df['High'].iloc[-1]:,.2f}", None),
    ("Mkt Cap",    f"${mkt_cap/1e9:.1f}B" if mkt_cap else "N/A", None),
]
cells = "".join([
    f'<div class="metric-card"><div class="metric-label">{label}</div>'
    f'<div class="metric-value">{val}</div>'
    f'{"<div class=\'metric-note\'>" + note + "</div>" if note else ""}</div>'
    for label, val, note in cards_data
])
st.markdown(f'<div class="board-strip">{cells}</div>', unsafe_allow_html=True)

# ─── Main Price Chart ─────────────────────────────────────────────────────────
builder = ChartBuilder(df, symbol, ticker_label)
price_fig = builder.price_chart(
    chart_type=chart_type,
    show_ma=show_ma,
    show_bb=show_bb,
    show_vwap=show_vwap
)
st.plotly_chart(price_fig, use_container_width=True, config={"displayModeBar": True, "scrollZoom": True})

# ─── Sub-charts ───────────────────────────────────────────────────────────────
active_sub = [s for s, flag in [("Volume", show_volume), ("RSI", show_rsi), ("MACD", show_macd)] if flag]
if active_sub:
    cols = st.columns(len(active_sub))
    for col, sub in zip(cols, active_sub):
        with col:
            if sub == "Volume":
                st.plotly_chart(builder.volume_chart(), use_container_width=True)
            elif sub == "RSI":
                st.plotly_chart(builder.rsi_chart(), use_container_width=True)
            elif sub == "MACD":
                st.plotly_chart(builder.macd_chart(), use_container_width=True)

# ─── Data Table + Statistics ──────────────────────────────────────────────────
st.divider()
tab1, tab2, tab3 = st.tabs(["RECENT DATA", "STATISTICS", "EXPORT"])

with tab1:
    display = df[["Open","High","Low","Close","Volume"]].tail(15).copy()
    display.index = display.index.strftime("%Y-%m-%d")
    display["Change%"] = display["Close"].pct_change().mul(100).round(2)
    display = display.round(2)
    display["Volume"] = display["Volume"].apply(lambda x: f"{int(x):,}")
    st.dataframe(display, use_container_width=True)

with tab2:
    s = df["Close"]
    stats = {
        "Mean Price":     f"${s.mean():.2f}",
        "Std Deviation":  f"${s.std():.2f}",
        "Variance":       f"{s.var():.2f}",
        "Skewness":       f"{s.skew():.4f}",
        "Kurtosis":       f"{s.kurtosis():.4f}",
        "Daily Return μ": f"{s.pct_change().mean()*100:.3f}%",
        "Daily Return σ": f"{s.pct_change().std()*100:.3f}%",
        "Sharpe Ratio":   f"{(s.pct_change().mean()/s.pct_change().std()*np.sqrt(252)):.3f}",
        "Max Drawdown":   f"{((s/s.cummax()-1).min()*100):.2f}%",
    }
    stats_df = pd.DataFrame(stats.items(), columns=["Metric", "Value"]).set_index("Metric")
    st.dataframe(stats_df, use_container_width=True)

with tab3:
    csv = df.to_csv().encode("utf-8")
    st.download_button(
        "⬇  Download CSV",
        data=csv,
        file_name=f"{symbol}_{period_label.replace(' ','_')}.csv",
        mime="text/csv",
        use_container_width=True
    )
    st.caption(f"Exports last {len(df)} trading days of OHLCV + indicator data for **{symbol}**")

st.markdown('<p class="footer">FOR EDUCATIONAL PURPOSES ONLY · NOT FINANCIAL ADVICE · DATA VIA YAHOO FINANCE</p>', unsafe_allow_html=True)