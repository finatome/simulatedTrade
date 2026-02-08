# Price Volume Trend (PVT)

| Name | Type | Prerequisite | Use Cases |
| :--- | :--- | :--- | :--- |
| Price Volume Trend (PVT) | Volume | Price & Volume | Provides a more granular view of volume flow than OBV. |

## Definition

The Price Volume Trend (PVT) indicator, similar to On-Balance Volume (OBV), is a momentum cumulative volume indicator used to measure money flow. However, unlike OBV which adds all volume if price is up, PVT adds only a portion of the volume proportional to the percentage price change.

## Mathematical Equation

$$
PVT_t = PVT_{t-1} + \left( Volume_t \times \frac{Close_t - Close_{t-1}}{Close_{t-1}} \right)
$$

## Visualization

![Price Volume Trend](plots/PVT.png)

## Trading Significance

1.  **More Accurate than OBV**: Because it weights volume by the magnitude of the price move, PVT often provides a more accurate reflection of market flow than OBV.

2.  **Divergence**: Divergence between price and PVT can signal a market reversal.

3.  **Trend Confirmation**: Rising PVT confirms an uptrend; falling PVT confirms a downtrend.

