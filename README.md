# Overview

This project implements a simple trend-following trading strategy on the NASDAQ Composite Index (^IXIC).
The strategy compares two moving averages — a fast one (20 days) and a slow one (100 days) — and generates buy/sell signals whenever the fast MA crosses above or below the slow MA.

The goal is to evaluate how a basic technical indicator behaves across multiple market regimes between 2019 and 2025, including the COVID crash, the 2020–2021 rally, and the 2022 correction.

The backtest computes portfolio performance, Sharpe ratio, maximum drawdown, and CAGR to assess risk-adjusted returns.

# Key Features

- Downloads historical NASDAQ data using yfinance
- Computes 20-day and 100-day moving averages
- Generates trading signals based on MA crossovers
- Simulates a long-only portfolio (in-market or in-cash)
- Plots buy/sell points on the price chart
- Computes Sharpe ratio, Max Drawdown, and CAGR
- Fully commented code for reproducibility

# Strategy Logic (Simple Trend Following)

- If the fast MA > slow MA → enter long
- If the fast MA < slow MA → exit to cash

This rule attempts to follow medium-term market trends while avoiding prolonged downtrends.

# Performance Summary (2019–2025)

Your current run produced approximately:

- Sharpe ratio: 0.74
- Max Drawdown: –26%
- CAGR: ~11%

These results are consistent with a conservative trend-following system:
lower drawdown than buy-and-hold, but also lower performance during strong bull markets.
