# Volatility (Close-to-Close)

| Name | Type | Prerequisite | Use Cases |
| :--- | :--- | :--- | :--- |
| Volatility Close-to-Close (C-C Vol) | Volatility | OHLC Data | Measures price dispersion specifically focused on settlement prices. |

## Definition

Close-to-Close volatility is a standard measure of volatility, calculating the standard deviation of close-to-close returns. It is the simplest estimator of volatility.

## Mathematical Equation

Standard deviation of simple percentage returns:

$$
\text{Vol}_{CC} = \text{StdDev}\left(\frac{Close_t - Close_{t-1}}{Close_{t-1}}\right)
$$

(Often annualized).

## Visualization

![Volatility Close-to-Close](plots/Volatility_Close_To_Close.png)

## Trading Significance

1.  **Baseline Volatility**: Provides a baseline measure of asset risk based on closing prices.

2.  **Limitations**: Ignores intraday price action (High/Low).

