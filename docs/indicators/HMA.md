# Hull Moving Average (HMA)

| Name | Type | Prerequisite | Use Cases |
| :--- | :--- | :--- | :--- |
| Hull Moving Average (HMA) | Trend | WMA | Catching fast reversals and short-term trend changes. |

## Definition

Developed by Alan Hull, the Hull Moving Average (HMA) makes a moving average more responsive to current price activity while maintaining curve smoothness. It effectively eliminates lag and manages to improve smoothing at the same time.

## Mathematical Equation

$$
HMA = WMA(2 \times WMA(\frac{n}{2}) - WMA(n), \sqrt{n})
$$

## Visualization

![HMA](plots/HMA.png)

## Trading Significance

1. **Trend Reversal**: Due to its speed, the turning points of the HMA are often used as entry/exit signals.

2. **Trend Filter**: If HMA is rising, trend is up; if falling, trend is down.

