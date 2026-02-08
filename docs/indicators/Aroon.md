# Aroon Indicator

| Name | Type | Prerequisite | Use Cases |
| :--- | :--- | :--- | :--- |
| Aroon (ARN) | Trend | OHLC Data | Identifying the start of a new trend. |

## Definition

The Aroon indicator is used to identify trend changes in the price of an asset, as well as the strength of that trend. It measures the time between highs and the time between lows over a time period. The indicator consists of the "Aroon Up" line, which measures the strength of the uptrend, and the "Aroon Down" line, which measures the strength of the downtrend.

## Mathematical Equation

The indicator is calculated over $N$ periods (typically 25):

$$
\text{Aroon Up} = \frac{N - \text{Periods Since Last High}}{N} \times 100
$$

$$
\text{Aroon Down} = \frac{N - \text{Periods Since Last Low}}{N} \times 100
$$

## Visualization

![Aroon](plots/Aroon.png)

## Trading Significance

1.  **Trend Identification**:

    *   **Uptrend**: Aroon Up is above 70 and Aroon Down is below 30.

    *   **Downtrend**: Aroon Down is above 70 and Aroon Up is below 30.

2.  **Crossovers**:

    *   When Aroon Up crosses above Aroon Down, it is a potential buy signal (trend change to bullish).

    *   When Aroon Down crosses above Aroon Up, it is a potential sell signal (trend change to bearish).

3.  **Consolidation**: If both lines are below 50 or moving parallel to each other, it suggests a consolidation phase or lack of a strong trend.

