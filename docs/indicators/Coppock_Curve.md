# Coppock Curve

| Name | Type | Prerequisite | Use Cases |
| :--- | :--- | :--- | :--- |
| Coppock Curve (CC) | Momentum | WMA | Long-term investment timing in broad indices. |

## Definition

The Coppock Curve is a long-term price momentum indicator used primarily to identify major bottoms in the stock market. It is calculated as a 10-month weighted moving average of the sum of the 14-month rate of change and the 11-month rate of change for the index. Although designed for monthly data, it can be applied to other timeframes.

## Mathematical Equation

$$
ROC_{14} = \frac{Price_t - Price_{t-14}}{Price_{t-14}} \times 100
$$

$$
ROC_{11} = \frac{Price_t - Price_{t-11}}{Price_{t-11}} \times 100
$$

$$
\text{Coppock} = WMA_{10}(ROC_{14} + ROC_{11})
$$

## Visualization

![Coppock Curve](plots/Coppock_Curve.png)

## Trading Significance

1.  **Trend Signal**: The primary signal is generated when the Coppock Curve rises from below zero into positive territory. This is interpreted as a "buy" signal for a new long-term bull market.

2.  **Zero Line**: While crossing above zero is the main signal, remaining above zero generally confirms a bullish trend, and falling below zero indicates a bearish phase.

3.  **Divergence**: Though less common, divergence analyses can also be applied.

