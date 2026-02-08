# Volume Weighted Moving Average (VWMA)

| Name | Type | Prerequisite | Use Cases |
| :--- | :--- | :--- | :--- |
| Volume-Weighted MA (VWMA) | Trend/Volume | Price & Volume | Confirms price trends with high-volume conviction. |

## Definition

The Volume Weighted Moving Average (VWMA) averages price data with an emphasis on volume. Unlike a Simple Moving Average (SMA), which treats each day's closing price equally, the VWMA gives more weight to days with higher volume.

## Mathematical Equation

$$
VWMA = \frac{\sum (\text{Price} \times \text{Volume})}{\sum \text{Volume}}
$$

Calculated over a rolling window of $N$ periods.

## Visualization

![Volume Weighted Moving Average](plots/VWMA.png)

## Trading Significance

1.  **Trend Confirmation**: When VWMA is above the SMA, it implies that higher volume is accompanying rising prices (validating the uptrend).

2.  **Divergence**: If prices are rising but the VWMA is falling or flat, it suggests the move is not supported by strong volume.

3.  **Support/Resistance**: Like other MAs, it acts as dynamic support and resistance.

