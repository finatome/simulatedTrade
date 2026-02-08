# Indicator Reference

All candles—synthetic and real—are enriched with a consistent pandas-ta indicator deck so the UI can toggle overlays without recomputing. The following studies are appended by `engine/indicators.py`.

## Trend & Moving Averages

| Indicator | Columns | Notes |
| --------- | ------- | ----- |
| Simple Moving Averages | `SMA_20`, `SMA_50`, `SMA_200` | Baseline trend context from short to long horizon. |
| Exponential Moving Averages | `EMA_9`, `EMA_21`, `EMA_50` | Emphasize recent data for faster reaction during momentum bursts. |
| Weighted & Hull MAs | `WMA_21`, `HMA_21` | Alternative smoothing techniques for traders who prefer reduced lag. |
| VWAP | `VWAP_D` (pandas-ta naming) | Combines price and volume; requires a datetime index. |
| Supertrend | `SUPERT_7_3.0`, `SUPERTd_7_3.0`, etc. | Directional bias built from ATR bands. |

## Volatility & Channels

| Indicator | Columns | Usage |
| --------- | ------- | ----- |
| Bollinger Bands | `BBL_20_2.0`, `BBM_20_2.0`, `BBU_20_2.0` | 20-period SMA envelope with 2σ offsets; used for mean reversion cues. |
| Keltner Channels | `KCL_20_2`, `KCM_20_2`, `KCU_20_2` | ATR-based channel, tighter than Bollinger for breakout spotting. |
| Donchian Channels | `DCL_20_20`, `DCM_20_20`, `DCU_20_20` | High/low breakout bands for range detection. |
| Parabolic SAR | `PSARl_0.02_0.2`, `PSARs_0.02_0.2` | Trailing stop candidates; plotted as dots in the UI. |

## Momentum & Oscillators

| Indicator | Columns | Notes |
| --------- | ------- | ----- |
| RSI | `RSI_14` | 14-period momentum oscillator for overbought/oversold signals. |
| MACD | `MACD_12_26_9`, `MACDh_12_26_9`, `MACDs_12_26_9` | Trend-momentum combo; histogram highlights shifts. |
| Stochastic | `STOCHk_14_3_3`, `STOCHd_14_3_3` | Fast oscillator measuring closes relative to recent ranges. |
| ADX & DI | `ADX_14`, `DMP_14`, `DMN_14` | Directional strength via Average Directional Index. |
| CCI | `CCI_14_0.015` | Commodity Channel Index for pullback detection. |
| ROC | `ROC_10` | Percent rate of change over ten bars, useful for velocity screening. |

## Volume

| Indicator | Columns | Notes |
| --------- | ------- | ----- |
| On-Balance Volume | `OBV` | Cumulative volume flow aligned with direction of closes. |

### Naming Conventions

- pandas-ta appends parameter values to each column (`RSI_14`, `BBL_20_2.0`, etc.), so the UI can map user selections back to exact series.
- Many channel-based studies emit multiple columns (lower/mid/upper); the Dash viewport picks the subset requested by the indicator selector.
- If you extend `add_technical_indicators()`, keep names descriptive and unique so downstream components can reference them unambiguously.

This comprehensive catalog provides a technical breakdown of all **85 indicators** organized by their mathematical complexity.


## Indicator Groups

### I. First-Order Primitives (Base Data Discretization)
*Simplest transforms of raw Open, High, Low, Close, and Volume (OHLCV) data.*

1. **[Average Price (AP)](indicators/Average_Price.md):** An arithmetic mean of the High, Low, and Close for a single period.
   * **Equation:** $(H + L + C) / 3$
   * **Category:** Trend/Benchmark
   * **Use Case:** Provides a simplified representation of a single bar's price action.
2. **[Median Price (MP)](indicators/Median_Price.md):** The exact middle point between the High and Low of a specific time period.
   * **Equation:** $(H + L) / 2$
   * **Category:** Trend/Benchmark
   * **Use Case:** Identifies the midpoint of a bar's range, often used as an input for oscillators.
3. **[Typical Price (TP)](indicators/Typical_Price.md):** A standard price calculation used as a more accurate representation of the average price than just the close.
   * **Equation:** $(H + L + C) / 3$
   * **Category:** Trend/Benchmark
   * **Use Case:** Serves as the base input for more complex indicators like CCI and VWAP.
4. **[Volume (V)](indicators/Volume.md):** The total number of shares or contracts traded during a specific time interval.
   * **Equation:** $\sum \text{Trades}$
   * **Category:** Volume
   * **Use Case:** Gauges market activity and validates the strength of price moves.
5. **[Standard Deviation (StdDev)](indicators/Standard_Deviation.md):** A statistical measure of how much price deviates from its mean.
   * **Equation:** $\sqrt{\frac{1}{N} \sum_{i=1}^{N} (x_i - \bar{x})^2}$
   * **Category:** Volatility
   * **Use Case:** Quantifies market risk and serves as the backbone for Bollinger Bands.
6. **[Historical Volatility (HV)](indicators/Historical_Volatility.md):** The realized variance of an asset based on past price changes.
   * **Equation:** $\text{Annualized StdDev of Log Returns}$
   * **Category:** Volatility
   * **Use Case:** Assesses the historical risk profile and prices options.
7. **[Volatility Close-to-Close (C-C Vol)](indicators/Volatility_Close_To_Close.md):** A volatility estimate calculated using only the closing prices of consecutive bars.
   * **Equation:** $\sqrt{\frac{1}{n-1} \sum (\ln(\frac{C_t}{C_{t-1}}) - \mu)^2}$
   * **Category:** Volatility
   * **Use Case:** Measures price dispersion specifically focused on settlement prices.
8. **[Volatility O-H-L-C (OHLC Vol)](indicators/Volatility_OHLC.md):** A more efficient volatility estimator that incorporates the intrabar range.
   * **Equation:** Uses Parkinson or Garman-Klass formulas (e.g., $0.511(H-L)^2 - \dots$)
   * **Category:** Volatility
   * **Use Case:** Provides a more granular risk assessment than close-only models.
9. **[Volatility Zero-Trend C-C (Z-Trend Vol)](indicators/Volatility_Zero_Trend_Close_To_Close.md):** A variance calculation that assumes the mean return (drift) is zero.
   * **Equation:** $\sqrt{\frac{1}{n} \sum (\ln(\frac{C_t}{C_{t-1}}))^2}$
   * **Category:** Volatility
   * **Use Case:** Useful for high-frequency data where drift is negligible.
10. **[Rate of Change (ROC)](indicators/ROC.md):** Measures the percentage change in price between the current period and a period $n$ days ago.
    * **Equation:** $(\frac{C_t - C_{t-n}}{C_{t-n}}) \times 100$
    * **Category:** Momentum
    * **Use Case:** Identifies price velocity and potential trend exhaustion.
11. **[Momentum (MOM)](indicators/Momentum.md):** The absolute difference in price over a fixed lookback period.
    * **Equation:** $C_t - C_{t-n}$
    * **Category:** Momentum
    * **Use Case:** Simplest measure of trend strength and direction.
12. **[Spread (SPD)](indicators/Spread.md):** The price difference between two distinct correlated assets.
    * **Equation:** $Asset_A - Asset_B$
    * **Category:** Relative Value
    * **Use Case:** Pairs trading and identifying inter-market arbitrage.
13. **[Ratio (RAT)](indicators/Ratio.md):** The relative value of one asset expressed in terms of another.
    * **Equation:** $Asset_A / Asset_B$
    * **Category:** Relative Value
    * **Use Case:** Inter-market analysis (e.g., Gold/Silver ratio) to find relative outperformance.
14. **[Net Volume (NV)](indicators/Net_Volume.md):** The sum of volume where up-volume is positive and down-volume is negative.
    * **Equation:** $\sum (\text{if } C > C_{-1} \text{ then } V \text{ else } -V)$
    * **Category:** Volume
    * **Use Case:** Visualizes net capital flow into or out of an asset.
15. **[Williams Fractal (FRAC)](indicators/Fractal.md):** Identifies local high and low points based on a 5-bar sequence.
    * **Equation:** High is Fractal if $H_t > H_{t \pm 1, 2}$
    * **Category:** Structure
    * **Use Case:** Defines support and resistance levels based on local price reversals.

---

### II. Second-Order Smoothing (Moving Averages)
*Temporal filters used to isolate the signal from price noise.*

16. **[Simple Moving Average (SMA)](indicators/SMA.md):** The unweighted average of price over a specific number of periods.
    * **Equation:** $\frac{1}{n} \sum_{i=0}^{n-1} C_{t-i}$
    * **Category:** Trend
    * **Use Case:** Baseline trend identification and institutional support/resistance.
17. **[Exponential Moving Average (EMA)](indicators/EMA.md):** A moving average that applies more weight to recent prices for faster reaction.
    * **Equation:** $EMA_t = C_t \times \alpha + EMA_{t-1} \times (1 - \alpha)$
    * **Category:** Trend
    * **Use Case:** Reduces lag in trend following compared to SMA.
18. **[Weighted Moving Average (WMA)](indicators/WMA.md):** A moving average where each data point is weighted by its position in the sequence.
    * **Equation:** $\frac{\sum (C_{t-i} \times (n-i))}{\sum (n-i)}$
    * **Category:** Trend
    * **Use Case:** Provides a faster response than SMA while being less volatile than EMA.
19. **[Smoothed Moving Average (SMMA)](indicators/SMMA.md):** A hybrid average similar to EMA but with a longer-term memory.
    * **Equation:** $SMMA_t = \frac{\text{Sum}_{t-1} - SMMA_{t-1} + C_t}{n}$
    * **Category:** Trend
    * **Use Case:** Long-term trend smoothing for position trading.
20. **[Arnaud Legoux MA (ALMA)](indicators/ALMA.md):** Uses a Gaussian distribution to provide extreme smoothness with minimal lag.
    * **Equation:** $\sum (C_{t-i} \times w_i) \text{ where } w_i \text{ is Gaussian offset}$
    * **Category:** Trend
    * **Use Case:** Superior trend tracking that filters "noise" without sacrificing timing.
21. **[Hull Moving Average (HMA)](indicators/HMA.md):** A moving average designed to be extremely fast and eliminate lag almost entirely.
    * **Equation:** $WMA(2 \times WMA_{n/2} - WMA_n, \sqrt{n})$
    * **Category:** Trend
    * **Use Case:** Catching fast reversals and short-term trend changes.
22. **[Least Squares MA (LSMA)](indicators/LSMA.md):** Calculates a linear regression line over the period and plots the endpoint.
    * **Equation:** $\text{End point of Linear Regression line}$
    * **Category:** Trend
    * **Use Case:** Anticipating where price should be if the current trend continues linearly.
23. **[Volume-Weighted MA (VWMA)](indicators/VWMA.md):** A moving average that weighs price based on the volume of each period.
    * **Equation:** $\sum (C_i \times V_i) / \sum V_i$
    * **Category:** Trend/Volume
    * **Use Case:** Confirms price trends with high-volume conviction.
24. **[Moving Average Hamming (MAH)](indicators/Hamming_Moving_Average.md):** Applies a Hamming window function to the moving average for signal processing.
    * **Equation:** $\sum (C_{t-i} \times \text{Hamming Weight}_i)$
    * **Category:** Trend
    * **Use Case:** Used in cycles and spectral analysis to minimize signal "leakage."
25. **[MA Weighted by Volatility (V-WMA)](indicators/VAMA.md):** An adaptive MA that slows down during low volatility and speeds up during high volatility.
    * **Equation:** $MA \text{ where period } n \text{ is a function of } \sigma$
    * **Category:** Trend/Volatility
    * **Use Case:** Stays closer to price during breakouts and ignores "chop."

---

### III. Third-Order Oscillators & Bands (Derived from MAs)
*Derived from the averages in Section II to create boundaries and relative signals.*

26. **[Moving Average Cross (MAX)](indicators/MA_Cross.md):** A signal generated when a fast SMA crosses above or below a slow SMA.
    * **Equation:** $SMA_{fast} - SMA_{slow}$
    * **Category:** Trend
    * **Use Case:** Defining broad bullish or bearish regimes (e.g., Golden Cross).
27. **[EMA Cross (EMAX)](indicators/EMA_Cross.md):** Uses exponential averages to signal trend changes with less lag.
    * **Equation:** $EMA_{fast} - EMA_{slow}$
    * **Category:** Trend
    * **Use Case:** Capturing trend shifts earlier in volatile markets.
28. **[Price Oscillator (PO)](indicators/Price_Oscillator.md):** The percentage difference between two moving averages.
    * **Equation:** $(\frac{MA_{fast} - MA_{slow}}{MA_{slow}}) \times 100$
    * **Category:** Momentum
    * **Use Case:** Comparing momentum across different assets regardless of price level.
29. **[Moving Average Convergence Divergence (MACD)](indicators/MACD.md):** A trend-following momentum indicator showing the relationship between two EMAs.
    * **Equation:** $EMA_{12} - EMA_{26}$
    * **Category:** Momentum
    * **Use Case:** Identifying momentum shifts and signal line crossovers.
30. **[Bollinger Bands (BB)](indicators/Bollinger_Bands.md):** Volatility bands placed above and below a moving average.
    * **Equation:** $SMA \pm (k \times StdDev)$
    * **Category:** Volatility
    * **Use Case:** Identifying "overextended" prices and volatility squeezes.
31. **[Bollinger %B (%B)](indicators/Bollinger_PctB.md):** Quantifies where the current price is relative to the Bollinger Bands.
    * **Equation:** $\frac{C - LowerBand}{UpperBand - LowerBand}$
    * **Category:** Momentum
    * **Use Case:** Identifying specific breakout or mean-reversion triggers.
32. **[Bollinger Bandwidth (BBW)](indicators/Bollinger_Bandwidth.md):** Measures the distance between the upper and lower Bollinger Bands.
    * **Equation:** $\frac{UpperBand - LowerBand}{SMA}$
    * **Category:** Volatility
    * **Use Case:** Detecting the beginning of volatility expansions (the "squeeze").
33. **[Standard Error Bands (SEB)](indicators/Standard_Error_Bands.md):** Similar to Bollinger Bands but uses Standard Error instead of Standard Deviation.
    * **Equation:** $SMA \pm (k \times \text{Std Error})$
    * **Category:** Volatility
    * **Use Case:** Creating tighter bands that focus on the average's reliability.
34. **[Price Channel / Donchian (DC)](indicators/Donchian_Channels.md):** Plots the highest high and lowest low over $n$ periods.
    * **Equation:** $Upper = \max(H_n), Lower = \min(L_n)$
    * **Category:** Structure/Trend
    * **Use Case:** Classic breakout trading (e.g., Turtle Trading).
35. **[Keltner Channels (KC)](indicators/Keltner_Channels.md):** Volatility bands based on Average True Range instead of Standard Deviation.
    * **Equation:** $EMA \pm (k \times ATR)$
    * **Category:** Volatility
    * **Use Case:** Filtering price noise in trending markets more effectively than BB.
36. **[Moving Average Channel (MAC)](indicators/MA_Channel.md):** Uses the High and Low prices for the averages to create a price "envelope."
    * **Equation:** $Upper = SMA(H, n), Lower = SMA(L, n)$
    * **Category:** Trend
    * **Use Case:** Identifying the "trading range" of a specific trend.
37. **[Envelopes (ENV)](indicators/Envelopes.md):** Fixed percentage bands placed above and below a moving average.
    * **Equation:** $SMA \pm (SMA \times k\%)$
    * **Category:** Volatility
    * **Use Case:** Mean reversion in stable, non-volatile instruments.
38. **[Detrended Price Oscillator (DPO)](indicators/Detrended_Price_Oscillator.md):** Removes trend from price to make it easier to identify cycles.
    * **Equation:** $C_{t} - SMA_{t-(n/2+1)}$
    * **Category:** Momentum/Cycles
    * **Use Case:** Identifying cyclical highs and lows without trend interference.
39. **[Average True Range (ATR)](indicators/ATR.md):** Measures market volatility by decomposing the entire range of an asset.
    * **Equation:** $EMA(\max(H-L, |H-C_1|, |L-C_1|))$
    * **Category:** Volatility
    * **Use Case:** Setting volatility-based stop losses.
40. **[Commodity Channel Index (CCI)](indicators/CCI.md):** Measures the current price level relative to an average price level over a given time period.
    * **Equation:** $\frac{TP - SMA(TP)}{0.015 \times \text{Mean Deviation}}$
    * **Category:** Momentum
    * **Use Case:** Spotting new trends or extreme overbought/oversold conditions.
41. **[Standard Error (SE)](indicators/Standard_Error.md):** Estimates the precision of the mean price.
    * **Equation:** $\sigma / \sqrt{n}$
    * **Category:** Volatility/Statistics
    * **Use Case:** Gauging the consistency of a trend.
42. **[Linear Regression Curve (LRC)](indicators/Linear_Regression_Curve.md):** A series of linear regression endpoints plotted as a curve.
    * **Equation:** $\text{Series of LSMA values}$
    * **Category:** Trend
    * **Use Case:** Identifying the "fair value" path of a trend.
43. **[Linear Regression Slope (LRS)](indicators/Linear_Regression_Slope.md):** Measures the rate of change of the linear regression line.
    * **Equation:** $\frac{n \sum (xy) - \sum x \sum y}{n \sum x^2 - (\sum x)^2}$
    * **Category:** Momentum
    * **Use Case:** Identifying trend strength and potential exhaustion.

---

### IV. Fourth-Order Complex Momentum & Volume
*Highly processed indicators that often use other oscillators as inputs.*

44. **[Relative Strength Index (RSI)](indicators/RSI.md):** A speed and change of price movements oscillator.
    * **Equation:** $100 - [100 / (1 + \text{Avg Gain} / \text{Avg Loss})]$
    * **Category:** Momentum
    * **Use Case:** Identifying overbought (>70) and oversold (<30) conditions.
45. **[Stochastic Oscillator (STOCH)](indicators/Stochastic.md):** Compares a specific closing price to a range of its prices over a certain period.
    * **Equation:** $\frac{C - L_n}{H_n - L_n} \times 100$
    * **Category:** Momentum
    * **Use Case:** Mean reversion and divergence trading.
46. **[Stochastic RSI (StochRSI)](indicators/Stochastic_RSI.md):** Applies the Stochastic formula to RSI values instead of price.
    * **Equation:** $\frac{RSI - RSI_{min}}{RSI_{max} - RSI_{min}}$
    * **Category:** Momentum
    * **Use Case:** Identifying RSI reversals with high sensitivity.
47. **[SMI Ergodic Indicator (SMI)](indicators/SMI_Ergodic.md):** A double-smoothed version of the Stochastic Oscillator.
    * **Equation:** Double EMA of price relative to range.
    * **Category:** Momentum
    * **Use Case:** Providing smoother, more reliable signals than standard Stochastics.
48. **[True Strength Index (TSI)](indicators/True_Strength_Index.md):** A double-smoothed momentum oscillator.
    * **Equation:** $\frac{EMA(EMA(C-C_1))}{EMA(EMA|C-C_1|)} \times 100$
    * **Category:** Momentum
    * **Use Case:** Identifying trend direction and overbought/oversold levels.
49. **[Trend Strength Index (TRSI)](indicators/Trend_Strength_Index.md):** Measures the persistence of a trend using smoothed price changes.
    * **Equation:** $EMA(\Delta P) / EMA(|\Delta P|)$
    * **Category:** Momentum/Trend
    * **Use Case:** Distinguishing between strong trends and "noise."
50. **[Average Directional Index (ADX)](indicators/ADX.md):** Measures the overall strength of a trend.
    * **Equation:** $EMA(\frac{|+DI - -DI|}{+DI + -DI}) \times 100$
    * **Category:** Trend
    * **Use Case:** Determining if a market is trending or ranging (values > 25).
51. **[Directional Movement (DM)](indicators/Directional_Movement.md):** The component used to calculate the ADX.
    * **Equation:** Difference between current and previous highs/lows.
    * **Category:** Momentum
    * **Use Case:** Building block for trend-strength indicators.
52. **[Aroon (ARN)](indicators/Aroon.md):** Measures the time between highs and lows over each period.
    * **Equation:** $\frac{n - \text{periods since High}}{n} \times 100$
    * **Category:** Trend
    * **Use Case:** Identifying the start of a new trend.
53. **[Awesome Oscillator (AO)](indicators/Awesome_Oscillator.md):** The difference between a 5-period and 34-period SMA of median price.
    * **Equation:** $SMA_5(MP) - SMA_{34}(MP)$
    * **Category:** Momentum
    * **Use Case:** Confirming trends and spotting "Twin Peaks" signals.
54. **[Accelerator Oscillator (AC)](indicators/Accelerator_Oscillator.md):** Measures the acceleration/deceleration of the Awesome Oscillator.
    * **Equation:** $AO - SMA_5(AO)$
    * **Category:** Momentum
    * **Use Case:** Spotting momentum shifts before they appear in price.
55. **[TRIX (TRX)](indicators/TRIX.md):** The rate of change of a triple-exponentially smoothed moving average.
    * **Equation:** $\%$ Change of $EMA(EMA(EMA(C)))$
    * **Category:** Trend/Momentum
    * **Use Case:** Filtering out insignificant cycles and noise.
56. **[Coppock Curve (CC)](indicators/Coppock_Curve.md):** A long-term price momentum indicator used to identify major market bottoms.
    * **Equation:** $WMA_{10}(ROC_{14} + ROC_{11})$
    * **Category:** Momentum
    * **Use Case:** Long-term investment timing in broad indices.
57. **[Fisher Transform (FT)](indicators/Fisher_Transform.md):** Transforms prices into a Gaussian normal distribution.
    * **Equation:** $0.5 \times \ln(\frac{1+X}{1-X})$
    * **Category:** Momentum
    * **Use Case:** Pinpointing turning points with extreme clarity.
58. **[Relative Vigor Index (RVI)](indicators/Relative_Vigor_Index.md):** Measures the conviction of a trend by comparing close to open.
    * **Equation:** $\frac{EMA(C-O)}{EMA(H-L)}$
    * **Category:** Momentum
    * **Use Case:** Trend confirmation in volatile markets.
59. **[Relative Volatility Index (RVI-V)](indicators/Relative_Volatility_Index.md):** An RSI-style oscillator that uses standard deviation of price changes.
    * **Equation:** RSI formula applied to StdDev.
    * **Category:** Volatility/Momentum
    * **Use Case:** Confirming breakout signals.
60. **[Chande Momentum Oscillator (CMO)](indicators/CMO.md):** A momentum oscillator that uses price data in both the numerator and denominator.
    * **Equation:** $100 \times \frac{SumUp - SumDn}{SumUp + SumDn}$
    * **Category:** Momentum
    * **Use Case:** Capturing momentum changes without the smoothing lag of RSI.
61. **[Ultimate Oscillator (UO)](indicators/Ultimate_Oscillator.md):** A momentum oscillator that uses three different timeframes.
    * **Equation:** Weighted average of three different cycles.
    * **Category:** Momentum
    * **Use Case:** Reducing false overbought/oversold signals.
62. **[Vortex Indicator (VI)](indicators/Vortex_Indicator.md):** Two lines that capture positive and negative trend movement.
    * **Equation:** $\sum |H - L_{-1}| / \sum TR$
    * **Category:** Trend
    * **Use Case:** Spotting trend reversals and identifying current trend direction.

---

### V. Microstructure & Flow Dynamics
*Incorporates Volume to gauge the "force" or "liquidity" behind price.*

63. **[Volume Weighted Average Price (VWAP)](indicators/VWAP.md):** The average price an asset has traded at throughout the day, based on both volume and price.
    * **Equation:** $\sum (P \times V) / \sum V$
    * **Category:** Volume/Benchmark
    * **Use Case:** Determining institutional fair value for the day.
64. **[On-Balance Volume (OBV)](indicators/OBV.md):** A cumulative total of volume that adds volume on up days and subtracts it on down days.
    * **Equation:** $OBV_{prev} \pm V$
    * **Category:** Volume
    * **Use Case:** Identifying divergence between price and volume.
65. **[Money Flow Index (MFI)](indicators/MFI.md):** A volume-weighted version of the RSI.
    * **Equation:** $100 - [100 / (1 + \text{Money Ratio})]$
    * **Category:** Volume/Momentum
    * **Use Case:** Spotting reversals when volume and price are out of sync.
66. **[Chaikin Money Flow (CMF)](indicators/CMF.md):** Measures the amount of Money Flow Volume over a specific period.
    * **Equation:** $\sum \text{Money Flow Volume} / \sum \text{Volume}$
    * **Category:** Volume
    * **Use Case:** Gauging institutional accumulation or distribution.
67. **[Accumulation/Distribution (A/D)](indicators/Accumulation_Distribution.md):** Uses price and volume to show how strongly an asset is being accumulated.
    * **Equation:** $\sum [(\frac{(C-L)-(H-C)}{H-L}) \times V]$
    * **Category:** Volume
    * **Use Case:** Confirming a trend or spotting potential reversals.
68. **[Chaikin Oscillator (CO)](indicators/Chaikin_Oscillator.md):** Applies the MACD formula to the Accumulation/Distribution line.
    * **Equation:** $EMA_3(A/D) - EMA_{10}(A/D)$
    * **Category:** Volume/Momentum
    * **Use Case:** Identifying momentum in volume flow.
69. **[Price Volume Trend (PVT)](indicators/PVT.md):** Similar to OBV but adds only a percentage of volume based on price change.
    * **Equation:** $PVT_{prev} + V \times (\frac{C - C_1}{C_1})$
    * **Category:** Volume
    * **Use Case:** Provides a more granular view of volume flow than OBV.
70. **[Elder’s Force Index (EFI)](indicators/EFI.md):** Uses price and volume to measure the power behind a move.
    * **Equation:** $(C - C_1) \times V$
    * **Category:** Volume/Momentum
    * **Use Case:** Identifying the end of corrections within a trend.
71. **[Ease of Movement (EOM)](indicators/Ease_of_Movement.md):** Relates price change to volume to show how easily a price can move.
    * **Equation:** $\frac{\text{Midpoint Move}}{\text{Box Ratio}}$
    * **Category:** Volume
    * **Use Case:** Identifying trends that require very little volume to persist.
72. **[Klinger Oscillator (KO)](indicators/Klinger_Oscillator.md):** High-volume force indicator that compares volume to price range.
    * **Equation:** $EMA_{fast}(VF) - EMA_{slow}(VF)$
    * **Category:** Volume
    * **Use Case:** Long-term trend confirmation and short-term timing.
73. **[Volume Oscillator (VO)](indicators/Percentage_Volume_Oscillator.md):** Measures the difference between two volume moving averages.
    * **Equation:** $EMA_{fast}(V) - EMA_{slow}(V)$
    * **Category:** Volume
    * **Use Case:** Identifying when volume is expanding or contracting.
74. **[Volume Profile (VP)](indicators/Volume_Profile.md):** An advanced charting study that displays trading activity over a specified time period at specified price levels.
    * **Equation:** $\sum V \text{ at each Price } P$
    * **Category:** Volume/Structure
    * **Use Case:** Identifying High Volume Nodes (HVN) as support/resistance.

---

### VI. Adaptive & Regime-Switching Systems
*Sophisticated systems that adjust their sensitivity based on market conditions.*

75. **[Kaufman Adaptive MA (KAMA)](indicators/KAMA.md):** A moving average that adjusts its speed based on the efficiency of price movement.
    * **Equation:** $AMA_t = AMA_{t-1} + SC^2 \times (C_t - AMA_{t-1})$
    * **Category:** Trend/Adaptive
    * **Use Case:** Following trends in noisy markets without getting whipsawed.
76. **[McGinley Dynamic (MD)](indicators/McGinley_Dynamic.md):** An adaptive average designed to follow price more accurately than traditional MAs.
    * **Equation:** $MD_{prev} + \frac{C - MD_{prev}}{k \cdot n \cdot (C/MD_{prev})^4}$
    * **Category:** Trend/Adaptive
    * **Use Case:** Avoiding the "separation" of price and average in fast moves.
77. **[SuperTrend (ST)](indicators/SuperTrend.md):** A trend-following indicator based on Average True Range.
    * **Equation:** $\text{Median Price} \pm (k \times ATR)$
    * **Category:** Trend/Regime
    * **Use Case:** Clear buy/sell signals and trailing stops.
78. **[Parabolic SAR (PSAR)](indicators/Parabolic_SAR.md):** A trailing stop and reversal system.
    * **Equation:** $SAR_{t+1} = SAR_t + \alpha(EP - SAR_t)$
    * **Category:** Trend/Regime
    * **Use Case:** Trailing stops in strong trending markets.
79. **[Choppiness Index (CHOP)](indicators/Choppiness_Index.md):** Measures the market's tendency to trend or range.
    * **Equation:** $100 \times \log_{10}(\frac{\sum ATR}{H_n - L_n}) / \log_{10}(n)$
    * **Category:** Regime
    * **Use Case:** Avoiding trading in "sideways" or "choppy" markets (values > 61.8).
80. **[Chaikin Volatility (CV)](indicators/Chaikin_Volatility.md):** Measures the rate of change of the Average True Range.
    * **Equation:** $\%$ Change in $EMA(H-L)$
    * **Category:** Volatility
    * **Use Case:** Identifying volatility peaks that lead to reversals.
81. **[Chande Kroll Stop (CKS)](indicators/Chande_Kroll_Stop.md):** A volatility-based exit indicator.
    * **Equation:** Uses $n$-period High/Low and ATR.
    * **Category:** Volatility/Regime
    * **Use Case:** Dynamic stop losses that don't get hit by random noise.
82. **[Ichimoku Cloud (ICH)](indicators/Ichimoku_Cloud.md):** A comprehensive system identifying trend, support, and momentum.
    * **Equation:** Uses 5 different mid-point lines.
    * **Category:** Trend/Regime
    * **Use Case:** Full market-regime analysis.
83. **[Guppy Multiple MA (GMMA)](indicators/GMMA.md):** Uses two groups of moving averages to identify trend strength and investor behavior.
    * **Equation:** Clusters of 12 EMAs.
    * **Category:** Trend/Regime
    * **Use Case:** Spotting trend breakouts and exhaustion.
84. **[Williams Alligator (ALLI)](indicators/Williams_Alligator.md):** Uses three smoothed moving averages to identify trend formation.
    * **Equation:** 3 shifted SMAs (Jaw, Teeth, Lips).
    * **Category:** Trend/Regime
    * **Use Case:** Identifying "sleep" (range) and "hunger" (trend) phases.
85. **[Mass Index (MI)](indicators/Mass_Index.md):** Identifies trend reversals by measuring the widening and narrowing of the price range.
    * **Equation:** $\sum (\frac{EMA(H-L)}{EMA(EMA(H-L))})$
    * **Category:** Volatility/Momentum
    * **Use Case:** Predicting "reversal bulges" where a trend is about to turn.

---

### Hierarchy Summary
1.  **Level 1 (Data):** Basic arithmetic on OHLCV (e.g., Average Price).
2.  **Level 2 (Smoothing):** Time-filters that remove noise (e.g., EMA).
3.  **Level 3 (Derivatives):** Using averages to find relative value (e.g., Bollinger Bands).
4.  **Level 4 (Advanced):** Recursive logic, multi-factor integration, and adaptive speed (e.g., KAMA, Ichimoku).

Would you like me to create the **Python visualizer** to demonstrate how a Level 1 error (like a price spike) propagates through these levels?