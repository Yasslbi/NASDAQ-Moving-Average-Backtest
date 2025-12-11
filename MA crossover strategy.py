import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import yfinance as yf

# Load historical NASDAQ Composite data (symbol ^IXIC).
# This index is widely used as a benchmark for large-cap tech and growth stocks.
start = datetime.datetime(2019, 1, 1)
end   = datetime.datetime(2025, 1, 1)
nasdaq = yf.download("^IXIC", start=start, end=end)

# We focus on the closing price because most technical strategies
# operate on end-of-day data for trend detection.
close = nasdaq["Close"]

# Moving-average strategy: compare a fast trend (20 days)
# vs a slower one (100 days). When the fast MA rises above the slow MA,
# it signals a potential uptrend; otherwise, we stay out.
fast_window = 20
slow_window = 100

signals = pd.DataFrame(index=nasdaq.index)
signals["close"] = close
signals["fast_ma"] = close.rolling(fast_window).mean()
signals["slow_ma"] = close.rolling(slow_window).mean()

# Position = 1 means fully invested in the index.
# Position = 0 means no exposure. This is a basic trend-following rule.
signals["position"] = np.where(
    signals["fast_ma"] > signals["slow_ma"],
    1.0,
    0.0
)

# Ensure position is always a clean 1-dimensional Series.
if isinstance(signals["position"], pd.DataFrame):
    signals["position"] = signals["position"].iloc[:, 0]

signals["position"] = signals["position"].astype(float)

# Remove duplicated columns that sometimes appear in VSCode.
signals = signals.loc[:, ~signals.columns.duplicated()].copy()

# Trading signal: +1 = buy, -1 = sell. We look at changes in position.
signals["signal"] = signals["position"].diff()

# Plot price, moving averages, and buy/sell points.
plt.figure(figsize=(12, 6))
plt.plot(signals.index, signals["close"], label="NASDAQ Close", color="black")
plt.plot(signals.index, signals["fast_ma"], label="Fast MA (20d)", color="blue")
plt.plot(signals.index, signals["slow_ma"], label="Slow MA (100d)", color="orange")

# Arrows appear exactly on the turning points of the moving-average crossover.
plt.scatter(
    signals.index[signals["signal"] == 1],
    signals["close"][signals["signal"] == 1],
    color="green", marker="^", s=90, label="Buy"
)

plt.scatter(
    signals.index[signals["signal"] == -1],
    signals["close"][signals["signal"] == -1],
    color="red", marker="v", s=90, label="Sell"
)

plt.title("NASDAQ – Moving Average Strategy")
plt.legend()
plt.grid(True)
plt.show()

# Portfolio simulation:
# When position = 1 we are exposed to the index, when 0 we hold cash.
initial_capital = 10000
portfolio = pd.DataFrame(index=signals.index)

# Value of our NASDAQ exposure through time.
portfolio["holdings"] = signals["position"].squeeze() * signals["close"]

# Small safety check in case holdings becomes 2-dimensional.
if isinstance(portfolio["holdings"], pd.DataFrame):
    portfolio["holdings"] = portfolio["holdings"].iloc[:, 0]

# Cash evolves based on buy/sell signals. A buy decreases cash,
# a sell increases it. diff() highlights when a position changes.
pos_diff = signals["position"].diff()
portfolio["cash"] = initial_capital + (-pos_diff * signals["close"]).cumsum()

# Total portfolio value = invested part + cash.
portfolio["total"] = portfolio["cash"] + portfolio["holdings"]

# Daily returns of the strategy.
portfolio["returns"] = portfolio["total"].pct_change()

# Performance metrics:
returns = portfolio["returns"]

# Sharpe ratio: risk-adjusted return normalized to a yearly basis (252 trading days).
sharpe = np.sqrt(252) * returns.mean() / returns.std()

# Maximum drawdown: worst peak-to-trough drop in the portfolio.
rolling_max = portfolio["total"].cummax()
drawdown = portfolio["total"] / rolling_max - 1
max_dd = drawdown.min()

# CAGR: annualized compound growth rate of the strategy.
days = (signals.index[-1] - signals.index[0]).days
cagr = (portfolio["total"].iloc[-1] / portfolio["total"].iloc[1]) ** (365 / days) - 1

print("Sharpe ratio:", sharpe)
print("Max Drawdown:", max_dd)
print("CAGR:", cagr)



