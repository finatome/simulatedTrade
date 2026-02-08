# Guppy Multiple Moving Average (GMMA)

| Name | Type | Prerequisite | Use Cases |
| :--- | :--- | :--- | :--- |
| Guppy Multiple MA (GMMA) | Trend/Regime | EMA | Spotting trend breakouts and exhaustion. |

## Definition

The Guppy Multiple Moving Average (GMMA) was developed by Daryl Guppy. It involves two groups of exponential moving averages (EMAs): a short-term group and a long-term group. It is designed to capture the interaction between traders (short-term) and investors (long-term).

## Mathematical Equation

*   **Short-term EMAs**: 3, 5, 8, 10, 12, 15 periods.

*   **Long-term EMAs**: 30, 35, 40, 45, 50, 60 periods.

## Visualization

![Guppy Multiple Moving Average](plots/GMMA.png)

## Trading Significance

1.  **Compression**: When the EMAs in a group compress (come close together), it indicates agreement on price and potential for a breakout.

2.  **Crossover**: When the short-term group crosses the long-term group, it signals a major trend change.

3.  **Separation**: Wide separation between the groups indicates a strong trend.

