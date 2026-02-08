# Moving Average weighted by Volatility (VAMA)

| Name | Type | Prerequisite | Use Cases |
| :--- | :--- | :--- | :--- |
| MA Weighted by Volatility (V-WMA) | Trend/Volatility | StdDev | Stays closer to price during breakouts and ignores "chop." |

## Definition

Volatility Adaptive Moving Average (VAMA) adapts its smoothing period based on the volatility of the price. When volatility is high, it can react faster (or slower depending on design), effectively filtering out noise during consolidation while catching trends.

## Trading Significance

1.  **Adaptability**: Reduces lag during trends and avoids whipsaws during sideways markets better than static MAs.

