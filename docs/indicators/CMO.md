# Chande Momentum Oscillator (CMO)

| Name | Type | Prerequisite | Use Cases |
| :--- | :--- | :--- | :--- |
| Chande Momentum Oscillator (CMO) | Momentum | OHLC Data | Capturing momentum changes without the smoothing lag of RSI. |

## Definition

The Chande Momentum Oscillator (CMO) was developed by Tushar Chande. It is a technical momentum indicator that attempts to capture the momentum of a security. Unlike other momentum oscillators like RSI, the CMO uses data from both up days and down days in the numerator. The values range from -100 to +100.

## Mathematical Equation

Over $N$ periods:

*   $S_u$: Sum of the difference between the current close and previous close on up days.

*   $S_d$: Sum of the absolute difference between the current close and previous close on down days.

$$
CMO = \frac{S_u - S_d}{S_u + S_d} \times 100
$$

## Visualization

![CMO](plots/CMO.png)

## Trading Significance

1.  **Overbought/Oversold**: Traditionally, levels above +50 are considered overbought, and levels below -50 are considered oversold.

2.  **Trend Strength**: Unlike RSI, CMO measures trend strength directly. High absolute values indicate a strong trend.

3.  **Divergence**: Divergence between the price and the CMO can signal potential reversals.

4.  **Crossovers**: A moving average of the CMO can be used as a signal line for crossovers.

