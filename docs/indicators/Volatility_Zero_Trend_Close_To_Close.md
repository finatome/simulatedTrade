# Volatility Zero-Trend C-C

| Name | Type | Prerequisite | Use Cases |
| :--- | :--- | :--- | :--- |
| Volatility Zero-Trend C-C (Z-Trend Vol) | Volatility | OHLC Data | Useful for high-frequency data where drift is negligible. |

## Definition

A variance calculation that assumes the mean return (drift) is zero.

## Mathematical Equation

$$\n\sqrt{\frac{1}{n} \sum (\ln(\frac{C_t}{C_{t-1}}))^2}\n$$

## Visualization

![Volatility Zero-Trend C-C](plots/Volatility_Zero_Trend_Close_To_Close.png)

## Trading Significance

*   **Category**: Volatility

*   **Use Case**: Useful for high-frequency data where drift is negligible.

