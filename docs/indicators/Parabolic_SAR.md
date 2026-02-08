# Parabolic SAR (Stop and Reverse)

| Name | Type | Prerequisite | Use Cases |
| :--- | :--- | :--- | :--- |
| Parabolic SAR (PSAR) | Trend/Regime | OHLC Data | Trailing stops in strong trending markets. |

## Definition

The Parabolic SAR is a price-and-time-based trading system designed to find potential reversals in the market price direction. It uses a trailing stop and reverse method called 'SAR', or 'Stop and Reverse'.

## Mathematical Equation

$$
SAR_{n+1} = SAR_n + \alpha (EP - SAR_n)
$$

 

Where:

*   $\alpha$ is the acceleration factor (starts at 0.02, increases by 0.02 to max 0.2)

*   $EP$ is the Extreme Point (highest high in uptrend, lowest low in downtrend)

## Visualization

![Parabolic_SAR](plots/Parabolic_SAR.png)

## Trading Significance

1. **Trailing Stop**: The primary use is as a trailing stop loss.

2. **Trend Reversal**: When price crosses the dots, a reversal is signaled.

