# SimTrade Overview

SimTrade is a micro-futures training ground that replays five-minute market slices so traders can practice scaling in and out of positions at high velocity. Each session stitches together synthetic or historical candles, augments them with a large technical-indicator stack, and wraps the flow inside a Dash web interface with game-like controls.

## Platform Highlights

- **Scenario Engine**: Generates 400-candle windows via Geometric Brownian Motion (GBM) or pulls matching spans from cached CME micro contracts.
- **Full Indicator Deck**: Over twenty pandas-ta indicators are pre-computed so users can toggle overlays from the UI without recomputation.
- **Trade Loop**: Every round begins with a 50-candle history, invites a LONG/SHORT/SKIP decision, and then fast-forwards until a take-profit, stop-loss, or timeout event.
- **Performance Analytics**: Win rate, profit factor, and cumulative PnL are tracked across the session using the shared `FuturesSimulator` ledger.

## Key Modules

| Area | File | Responsibilities |
| ---- | ---- | ---------------- |
| Synthetic data | `engine/gbm_engine.py` | Builds GBM candles with volatility clustering, realistic OHLC/volume synthesis, and indicator warm-up trimming. |
| Real data | `engine/real_data_engine.py` | Streams random slices from `assets/*_data.csv`, caching per ticker and falling back to synthetic data on errors. |
| Indicators | `engine/indicators.py` | Applies trend, volatility, momentum, and volume studies through pandas-ta. |
| Trading engine | `engine/simulator.py` | Handles trade entry/exit math, leverage application, and scenario bookkeeping. |
| Analytics | `engine/analytics.py` | Converts history into win rate, profit factor, total PnL, and trade count. |
| Data ingestion | `download_data.py` | Downloads 5-minute bars from Yahoo Finance and enriches them with the indicator deck for later replay. |

## Running the Simulator

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the Dash app:
   ```bash
   python app.py
   ```
3. (Optional) Launch via Docker:
   ```bash
   docker build -t simtrade .
   docker run --rm -p 8050:8050 simtrade
   ```
4. Open the UI at [http://127.0.0.1:8050](http://127.0.0.1:8050) and start trading scenarios.

## Working With This Documentation

1. Install MkDocs locally (one-time):
   ```bash
   pip install mkdocs
   ```
2. Serve the docs with live reload:
   ```bash
   mkdocs serve
   ```
   Visit the printed URL (defaults to [http://127.0.0.1:8000](http://127.0.0.1:8000)).
3. Build the static site for deployment:
   ```bash
   mkdocs build
   ```
   The generated site will be placed in the `site/` folder.

Use the navigation to dive into data generation, historical downloads, indicator references, and the trading/scoring engine internals.

---

## Comprehensive Indicator Suite

This consolidated list organizes all **85 indicators** analyzed in our sequence into a structural hierarchy. The list moves from **First-Order Primitives** (simple price/volume statistics) to **Higher-Order Derivatives** (indicators that use other indicators as inputs) and finally to **Complex Systems**.

### I. First-Order Primitives (Base Data Discretization)
*These indicators are the simplest mathematical transforms of raw OHLCV data.*

1. **[Average Price](indicators/Average_Price.md):** $(H+L+C)/3$
2. **[Median Price](indicators/Median_Price.md):** $(H+L)/2$
3. **[Typical Price](indicators/Typical_Price.md):** $(H+L+C)/3$ (Commonly used as the base for CCI/VWAP)
4. **[Volume](indicators/Volume.md):** Raw activity count ($V_t$)
5. **[Standard Deviation](indicators/Standard_Deviation.md):** Basic dispersion measure ($\sigma$)
6. **[Historical Volatility](indicators/Historical_Volatility.md):** Realized variance estimate
7. **[Volatility Close-to-Close](indicators/Volatility_Close_To_Close.md):** Precise realized $\sigma$ estimator
8. **[Volatility O-H-L-C](indicators/Volatility_OHLC.md):** Parkinson/Garman-Klass efficiency estimators
9. **[Volatility Zero-Trend C-C](indicators/Volatility_Zero_Trend_Close_To_Close.md):** Detrended variance
10. **[Rate of Change (ROC)](indicators/ROC.md):** Simple percentage momentum
11. **[Momentum](indicators/Momentum.md):** Absolute price change ($P_t - P_{t-n}$)
12. **[Spread](indicators/Spread.md):** $X - Y$ price difference
13. **[Ratio](indicators/Ratio.md):** $X / Y$ relative valuation
14. **[Net Volume](indicators/Net_Volume.md):** Aggregated buying/selling pressure
15. **[Williams Fractal](indicators/Fractal.md):** Local extrema detection (Highs/Lows)

### II. Second-Order Smoothing (Moving Averages)
*Indicators that apply a single-layer temporal filter to First-Order Primitives.*

16. **[Moving Average (SMA)](indicators/SMA.md):** The fundamental arithmetic mean.
17. **[Exponential Moving Average (EMA)](indicators/EMA.md):** Recursive weighted smoothing.
18. **[Weighted Moving Average (WMA)](indicators/WMA.md):** Linear temporal weighting.
19. **[Smoothed Moving Average (SMMA)](indicators/SMMA.md):** Long-memory recursive filter.
20. **[Arnaud Legoux MA (ALMA)](indicators/ALMA.md):** Gaussian-weighted low-lag filter.
21. **[Hull Moving Average (HMA)](indicators/HMA.md):** Weighted smoothing to reduce lag.
22. **[Least Squares MA (LSMA)](indicators/LSMA.md):** Linear regression-based smoothing.
23. **[VWMA](indicators/VWMA.md):** Volume-Weighted Moving Average.
24. **[Moving Average Hamming](indicators/Hamming_Moving_Average.md):** Spectral-window smoothing.
25. **[Moving Average weighted by Volatility](indicators/VAMA.md):** Adaptive smoothing based on $\sigma$.

### III. Third-Order Oscillators & Bands (Derived from MAs)
*These indicators use the averages in Section II as their primary inputs.*

26. **[Moving Average Cross](indicators/MA_Cross.md):** Logic based on $MA_f > MA_s$.
27. **[EMA Cross](indicators/EMA_Cross.md):** Logic based on $EMA_f > EMA_s$.
28. **[Price Oscillator (PO)](indicators/Price_Oscillator.md):** Percentage difference between two MAs.
29. **[MACD](indicators/MACD.md):** Convergence/Divergence of $EMA_{12}$ and $EMA_{26}$.
30. **[Bollinger Bands](indicators/Bollinger_Bands.md):** $\text{SMA} \pm k\sigma$.
31. **[Bollinger %B](indicators/Bollinger_PctB.md):** Position relative to Bollinger Bands.
32. **[Bollinger Bandwidth](indicators/Bollinger_Bandwidth.md):** Spread of the Bollinger Bands.
33. **[Standard Error Bands](indicators/Standard_Error_Bands.md):** Confidence intervals around a mean.
34. **[Price Channel / Donchian](indicators/Donchian_Channels.md):** Range based on $\max(H)$ and $\min(L)$.
35. **[Keltner Channels](indicators/Keltner_Channels.md):** $EMA \pm k \cdot ATR$.
36. **[Moving Average Channel](indicators/MA_Channel.md):** $MA \pm k\sigma$.
37. **[Envelopes](indicators/Envelopes.md):** $MA$ shifted by a fixed percentage.
38. **[DPO (Detrended Price Oscillator)](indicators/Detrended_Price_Oscillator.md):** Price compared to a shifted SMA.
39. **[Average True Range (ATR)](indicators/ATR.md):** EMA of the True Range.
40. **[CCI (Commodity Channel Index)](indicators/CCI.md):** Typical Price deviation from its SMA.
41. **[Standard Error](indicators/Standard_Error.md):** Statistical uncertainty of the mean.
42. **[Linear Regression Curve](indicators/Linear_Regression_Curve.md):** Time-series of regression intercepts.
43. **[Linear Regression Slope](indicators/Linear_Regression_Slope.md):** The $\beta$ coefficient of price vs. time.

### IV. Fourth-Order Complex Momentum & Volume
*Indicators that integrate multiple transformations (e.g., smoothing an oscillator).*

44. **[RSI (Relative Strength Index)](indicators/RSI.md):** Smoothed ratio of gains vs. losses.
45. **[Stochastic Oscillator](indicators/Stochastic.md):** Normalized position within a lookback range.
46. **[Stochastic RSI](indicators/Stochastic_RSI.md):** Stochastic formula applied to RSI values.
47. **[SMI Ergodic Indicator](indicators/SMI_Ergodic.md):** Double-smoothed price momentum.
48. **[True Strength Index (TSI)](indicators/True_Strength_Index.md):** Double-smoothed rate of change.
49. **[Trend Strength Index](indicators/Trend_Strength_Index.md):** EMA-based directional persistence.
50. **[ADX (Average Directional Index)](indicators/ADX.md):** Smoothed strength of DM+ and DM-.
51. **[Directional Movement (DM)](indicators/Directional_Movement.md):** Foundation for ADX.
52. **[Aroon](indicators/Aroon.md):** Time-based measure of recent Highs vs. Lows.
53. **[Awesome Oscillator (AO)](indicators/Awesome_Oscillator.md):** Difference between 5 and 34-period SMAs of Median Price.
54. **[Accelerator Oscillator (AC)](indicators/Accelerator_Oscillator.md):** AO minus its 5-period SMA.
55. **[TRIX](indicators/TRIX.md):** Rate of change of a Triple-EMA.
56. **[Coppock Curve](indicators/Coppock_Curve.md):** WMA of two summed ROCs.
57. **[Fisher Transform](indicators/Fisher_Transform.md):** Gaussianizing an oscillator (like RSI or Stochastic).
58. **[Relative Vigor Index (RVI)](indicators/Relative_Vigor_Index.md):** Conviction based on Close-Open vs. High-Low.
59. **[Relative Volatility Index](indicators/Relative_Volatility_Index.md):** Volatility asymmetry (Up- $\sigma$ vs. Down- $\sigma$).
60. **[Chande Momentum Oscillator (CMO)](indicators/CMO.md):** Pure momentum using $U-D / U+D$.
61. **[Ultimate Oscillator](indicators/Ultimate_Oscillator.md):** Weighted average of three different timeframes.
62. **[Vortex Indicator](indicators/Vortex_Indicator.md):** Difference between upward and downward "vortex" flows.

### V. Microstructure & Flow Dynamics
*Indicators integrating Volume with Price or Direction.*

63. **[VWAP](indicators/VWAP.md):** Cumulative volume-weighted average price.
64. **[OBV (On-Balance Volume)](indicators/OBV.md):** Cumulative volume based on price direction.
65. **[MFI (Money Flow Index)](indicators/MFI.md):** Volume-weighted RSI.
66. **[CMF (Chaikin Money Flow)](indicators/CMF.md):** Volume-weighted accumulation over time.
67. **[A/D Indicator (Accumulation/Distribution)](indicators/Accumulation_Distribution.md):** Multiplier-based volume flow.
68. **[Chaikin Oscillator](indicators/Chaikin_Oscillator.md):** MACD-style logic applied to the A/D line.
69. **[Price Volume Trend (PVT)](indicators/PVT.md):** Cumulative volume scaled by % price change.
70. **[Elder’s Force Index](indicators/EFI.md):** $\Delta P \times V$.
71. **[Ease of Movement (EOM)](indicators/Ease_of_Movement.md):** Price movement per unit of volume.
72. **[Klinger Oscillator](indicators/Klinger_Oscillator.md):** Volume force based on high-low-close relationships.
73. **[Volume Oscillator](indicators/Percentage_Volume_Oscillator.md):** Difference between two volume EMAs.
74. **[Volume Profile](indicators/Volume_Profile.md):** Price-level volume distribution.

### VI. Adaptive & Regime-Switching Systems
*The highest-order indicators that change their own parameters based on market state.*

75. **[KAMA (Kaufman Adaptive MA)](indicators/KAMA.md):** Changes smoothing based on efficiency.
76. **[McGinley Dynamic](indicators/McGinley_Dynamic.md):** MA that adjusts its speed to avoid price separation.
77. **[SuperTrend](indicators/SuperTrend.md):** ATR-based trailing stop system.
78. **[Parabolic SAR](indicators/Parabolic_SAR.md):** Time/Price-based acceleration stop.
79. **[Choppiness Index](indicators/Choppiness_Index.md):** Measures if price is "fractal" or "linear."
80. **[Chaikin Volatility](indicators/Chaikin_Volatility.md):** Rate of change of the ATR.
81. **[Chande Kroll Stop](indicators/Chande_Kroll_Stop.md):** Path-dependent volatility exit.
82. **[Ichimoku Cloud](indicators/Ichimoku_Cloud.md):** Multi-line equilibrium and regime system.
83. **[GMMA (Guppy Multiple MA)](indicators/GMMA.md):** Behavior analysis through EMA clusters.
84. **[Williams Alligator](indicators/Williams_Alligator.md):** Three shifted SMAs defining "hunger" (regimes).
85. **[Mass Index](indicators/Mass_Index.md):** Uses EMA ratios to predict volatility reversals.
