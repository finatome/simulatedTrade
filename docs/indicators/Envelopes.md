# Moving Average Envelopes

| Name | Type | Prerequisite | Use Cases |
| :--- | :--- | :--- | :--- |
| Envelopes (ENV) | Volatility | SMA | Mean reversion in stable, non-volatile instruments. |

## Definition

Moving Average Envelopes consist of a Moving Average and two outer bands (envelopes) set at a fixed percentage above and below the moving average. They help identify deviations from the trend and potential overbought/oversold conditions.

## Mathematical Equation

*   **Upper Envelope**: $SMA_{20} + (SMA_{20} \times k\%)$

*   **Lower Envelope**: $SMA_{20} - (SMA_{20} \times k\%)$

*   **Middle**: $SMA_{20}$

Where $k$ is a user-defined percentage (e.g., 2.5% or 5%).

## Visualization

![Moving Average Envelopes](plots/Envelopes.png)

## Trading Significance

1.  **Trend Following**: In a strong trend, price tends to stay between the MA and one of the envelopes.

2.  **Reversion to Mean**: When price touches or breaches the outer envelopes, it is often considered overextended and likely to revert towards the central moving average.

