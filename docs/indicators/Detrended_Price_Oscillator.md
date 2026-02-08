# Detrended Price Oscillator (DPO)

| Name | Type | Prerequisite | Use Cases |
| :--- | :--- | :--- | :--- |
| Detrended Price Oscillator (DPO) | Momentum/Cycles | SMA | Identifying cyclical highs and lows without trend interference. |

## Definition

The Detrended Price Oscillator (DPO) is an indicator designed to remove the long-term trend from prices, making it easier to identify potential cycles and overbought/oversold levels. Unlike other oscillators, DPO is not a momentum indicator but rather a price oscillator that highlights peaks and troughs in price relative to a displaced moving average.

## Mathematical Equation

$$
DPO = \text{Price close} - SMA_n(\frac{n}{2} + 1 \text{ periods ago})
$$

Usually, $n=20$. The specific displacement allows the indicator to compare the current price to a past average, effectively removing the trend influence up to that timeframe.

## Visualization

![Detrended Price Oscillator](plots/Detrended_Price_Oscillator.png)

## Trading Significance

1.  **Cycle Identification**: DPO is helpful for identifying the length of price cycles. The distance between peaks or troughs on the DPO can correspond to the cycle length.

2.  **Overbought/Oversold**: Peaks and troughs in the DPO often align with reaction highs and lows in price.

3.  **Trend Confirmation**: Since it compares price to a past average, determining if the price is significantly deviated from its "norm" can signal reversions.

