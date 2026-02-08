# Average True Range (ATR)

| Name | Type | Prerequisite | Use Cases |
| :--- | :--- | :--- | :--- |
| Average True Range (ATR) | Volatility | EMA | Setting volatility-based stop losses. |

## Definition

The Average True Range (ATR) is a technical analysis indicator that measures market volatility. It is typically derived from the 14-day simple moving average of a series of true range indicators.

## Mathematical Equation

$$
\begin{align}
TR &= \max[(H - L), |H - C_{prev}|, |L - C_{prev}|] \\
ATR &= \text{SMA}(TR, n)
\end{align}
$$

## Visualization

![ATR](plots/ATR.png)

## Trading Significance

1. **Volatility Measurement**: High ATR = High Volatility. Low ATR = Ranges.

2. **Stop Loss**: A multiple of ATR is often used to set stop-loss levels (e.g., 2x ATR).

