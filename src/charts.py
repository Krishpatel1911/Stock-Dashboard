"""
charts.py — All Plotly figure construction lives here.
ChartBuilder is initialized with a dataframe and produces
Plotly Figure objects — completely decoupled from Streamlit.
"""

from __future__ import annotations
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from src.config import (
    CHART_TEMPLATE, CHART_BG, CHART_PAPER_BG, GRID_COLOR,
    BULL_COLOR, BEAR_COLOR, MA20_COLOR, MA50_COLOR,
    BB_COLOR, VWAP_COLOR, MACD_COLOR, SIGNAL_COLOR
)


_LAYOUT_BASE = dict(
    template=CHART_TEMPLATE,
    plot_bgcolor=CHART_BG,
    paper_bgcolor=CHART_PAPER_BG,
    font=dict(family="Inter, sans-serif", size=12, color="#c9d1d9"),
    xaxis=dict(
        showgrid=True, gridcolor=GRID_COLOR,
        zeroline=False, showspikes=True, spikecolor="#555",
        spikemode="across", spikesnap="cursor", spikedash="dot",
    ),
    yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, zeroline=False),
    margin=dict(l=10, r=10, t=44, b=10),
    legend=dict(
        orientation="h", yanchor="bottom", y=1.01,
        xanchor="right", x=1, bgcolor="rgba(0,0,0,0)"
    ),
    hovermode="x unified",
)


class ChartBuilder:
    def __init__(self, df: pd.DataFrame, symbol: str, name: str):
        self.df     = df
        self.symbol = symbol
        self.name   = name

    # ── Price Chart ───────────────────────────────────────────────────────────
    def price_chart(
        self,
        chart_type: str = "Candlestick",
        show_ma:    bool = True,
        show_bb:    bool = True,
        show_vwap:  bool = False,
    ) -> go.Figure:
        df  = self.df
        fig = go.Figure()

        # ── Core price trace ──
        if chart_type == "Candlestick":
            fig.add_trace(go.Candlestick(
                x=df.index, open=df["Open"], high=df["High"],
                low=df["Low"], close=df["Close"],
                increasing=dict(line=dict(color=BULL_COLOR), fillcolor=BULL_COLOR),
                decreasing=dict(line=dict(color=BEAR_COLOR), fillcolor=BEAR_COLOR),
                name="OHLC", showlegend=False,
                whiskerwidth=0.3,
            ))
        elif chart_type == "Line":
            fig.add_trace(go.Scatter(
                x=df.index, y=df["Close"],
                mode="lines", name="Close",
                line=dict(color=BULL_COLOR, width=2),
                fill="tozeroy",
                fillcolor="rgba(38,166,154,0.08)",
            ))
        else:  # OHLC Bar
            fig.add_trace(go.Ohlc(
                x=df.index, open=df["Open"], high=df["High"],
                low=df["Low"], close=df["Close"],
                increasing_line_color=BULL_COLOR,
                decreasing_line_color=BEAR_COLOR,
                name="OHLC", showlegend=False,
            ))

        # ── Bollinger Bands ──
        if show_bb and "BB_UPPER" in df:
            fig.add_trace(go.Scatter(
                x=df.index, y=df["BB_UPPER"],
                line=dict(color=BB_COLOR, width=1, dash="dot"),
                name="BB Upper", showlegend=True,
            ))
            fig.add_trace(go.Scatter(
                x=df.index, y=df["BB_LOWER"],
                line=dict(color=BB_COLOR, width=1, dash="dot"),
                name="BB Lower",
                fill="tonexty",
                fillcolor="rgba(167,139,250,0.06)",
                showlegend=True,
            ))

        # ── Moving Averages ──
        if show_ma:
            if "MA20" in df:
                fig.add_trace(go.Scatter(
                    x=df.index, y=df["MA20"],
                    line=dict(color=MA20_COLOR, width=1.5),
                    name="MA 20",
                ))
            if "MA50" in df:
                fig.add_trace(go.Scatter(
                    x=df.index, y=df["MA50"],
                    line=dict(color=MA50_COLOR, width=1.5),
                    name="MA 50",
                ))

        # ── VWAP ──
        if show_vwap and "VWAP" in df:
            fig.add_trace(go.Scatter(
                x=df.index, y=df["VWAP"],
                line=dict(color=VWAP_COLOR, width=1.5, dash="dash"),
                name="VWAP",
            ))

        fig.update_layout(
            **_LAYOUT_BASE,
            title=dict(text=f"<b>{self.symbol}</b> — Price", font=dict(size=15)),
            height=480,
            xaxis_rangeslider_visible=False,
        )
        return fig

    # ── Volume Chart ──────────────────────────────────────────────────────────
    def volume_chart(self) -> go.Figure:
        df     = self.df
        colors = [BULL_COLOR if c >= o else BEAR_COLOR
                  for c, o in zip(df["Close"], df["Open"])]
        fig = go.Figure(go.Bar(
            x=df.index, y=df["Volume"],
            marker_color=colors,
            name="Volume",
        ))
        # OBV overlay on secondary axis
        if "OBV" in df:
            fig.add_trace(go.Scatter(
                x=df.index, y=df["OBV"],
                line=dict(color="#80cbc4", width=1.2),
                name="OBV",
                yaxis="y2",
            ))
        fig.update_layout(
            **_LAYOUT_BASE,
            title=dict(text="<b>Volume</b> + OBV", font=dict(size=13)),
            height=240,
            showlegend=True,
            yaxis2=dict(overlaying="y", side="right", showgrid=False, zeroline=False),
        )
        return fig

    # ── RSI Chart ─────────────────────────────────────────────────────────────
    def rsi_chart(self) -> go.Figure:
        df  = self.df
        rsi = df["RSI"].dropna()

        # Color gradient based on zone
        colors = [
            BEAR_COLOR if v > 70 else (BULL_COLOR if v < 30 else "#42a5f5")
            for v in rsi
        ]
        fig = go.Figure()
        fig.add_hrect(y0=70, y1=100, fillcolor="rgba(239,83,80,0.08)", line_width=0)
        fig.add_hrect(y0=0,  y1=30,  fillcolor="rgba(38,166,154,0.08)", line_width=0)
        fig.add_hline(y=70, line_dash="dot", line_color=BEAR_COLOR, line_width=1,
                      annotation_text="Overbought", annotation_position="top left",
                      annotation_font_color=BEAR_COLOR, annotation_font_size=10)
        fig.add_hline(y=30, line_dash="dot", line_color=BULL_COLOR, line_width=1,
                      annotation_text="Oversold", annotation_position="bottom left",
                      annotation_font_color=BULL_COLOR, annotation_font_size=10)
        fig.add_trace(go.Scatter(
            x=rsi.index, y=rsi,
            mode="lines",
            line=dict(color="#ab47bc", width=2),
            name="RSI (14)",
            fill="tozeroy",
            fillcolor="rgba(171,71,188,0.07)",
        ))
        fig.update_layout(
            **_LAYOUT_BASE,
            title=dict(text="<b>RSI</b> (14-period)", font=dict(size=13)),
            height=240,
        )
        fig.update_yaxes(range=[0, 100])
        return fig

    # ── MACD Chart ────────────────────────────────────────────────────────────
    def macd_chart(self) -> go.Figure:
        df   = self.df.dropna(subset=["MACD"])
        hist = df["MACD_HIST"]
        hist_colors = [BULL_COLOR if v >= 0 else BEAR_COLOR for v in hist]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df.index, y=hist,
            marker_color=hist_colors,
            name="Histogram",
            opacity=0.7,
        ))
        fig.add_trace(go.Scatter(
            x=df.index, y=df["MACD"],
            line=dict(color=MACD_COLOR, width=1.8),
            name="MACD",
        ))
        fig.add_trace(go.Scatter(
            x=df.index, y=df["MACD_SIGNAL"],
            line=dict(color=SIGNAL_COLOR, width=1.8, dash="dash"),
            name="Signal",
        ))
        fig.add_hline(y=0, line_color="rgba(255,255,255,0.15)", line_width=1)
        fig.update_layout(
            **_LAYOUT_BASE,
            title=dict(text="<b>MACD</b> (12 / 26 / 9)", font=dict(size=13)),
            height=240,
        )
        return fig