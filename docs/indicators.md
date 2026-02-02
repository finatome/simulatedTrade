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
