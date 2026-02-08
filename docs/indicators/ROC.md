# Rate of Change (ROC)

| Name | Type | Prerequisite | Use Cases |
| :--- | :--- | :--- | :--- |
| Rate of Change (ROC) | Momentum | OHLC Data | Identifies price velocity and potential trend exhaustion. |

## Definition

The Price Rate of Change (ROC) is a momentum-based technical indicator that measures the percentage change in price between the current price and the price a certain number of periods ago.

## Mathematical Equation

$$
ROC = \frac{\text{Close}_t - \text{Close}_{t-n}}{\text{Close}_{t-n}} \times 100
$$

## Visualization

![ROC](plots/ROC.png)

## Trading Significance

1. **Momentum**: Rising ROC indicates increasing bullish momentum. Falling ROC (even if positive) indicates waning momentum.

2. **Zero Line Cross**: Crossing above zero is a buy signal; below zero is a sell signal.

