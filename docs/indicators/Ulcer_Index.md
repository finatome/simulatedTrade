# Ulcer Index

## Definition

The Ulcer Index is a technical indicator that measures downside risk. It was designed by Peter Martin to measure the depth and duration of price drawdowns from recent highs. It is an indicator of volatility, but only downside volatility (stress).

## Mathematical Equation

1.  Calculate Percentage Drawdown: $R_i = \frac{Price_i - \max(Price_{last N})}{\max(Price_{last N})} \times 100$.

2.  Calculate Square Average: $Avg = \frac{\sum R_i^2}{N}$.

3.  $UI = \sqrt{Avg}$.

## Visualization

![Ulcer Index](plots/Ulcer_Index.png)

## Trading Significance

1.  **Risk Measure**: High values indicate high drawdown risk/stress (an "ulcer" causing market). Low values indicate a smooth uptrend.

2.  **Trend Quality**: Can be used to find stocks with smooth, low-volatility uptrends.

