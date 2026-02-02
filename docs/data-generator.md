# Synthetic Scenario Generator

The synthetic path generator in `engine/gbm_engine.py` fabricates realistic intraday candles whenever you need endless practice data. Each call to `generate_scenario_data()` returns a 400-candle `pandas.DataFrame` with OHLCV fields and a full set of technical indicators.

## Generation Pipeline

1. **Volatility-Aware GBM**
   - Uses a discrete Geometric Brownian Motion (GBM) update with `mu = 0.0001` and a time step of one five-minute bar.
   - Applies *volatility clustering*: the instantaneous sigma follows a bounded random walk between 0.1% and 0.5% to emulate news shocks and quiet periods.
   - Prices evolve via $S_t = S_{t-1} \cdot e^{(\mu - 0.5\sigma^2)\Delta t + \sigma \sqrt{\Delta t} \cdot \epsilon_t}$ with fresh Gaussian noise per bar.

2. **Timestamp Fabrication**
   - Builds a synthetic `DatetimeIndex` ending at the current wall-clock time and stepping backwards in five-minute intervals. This ensures pandas-ta studies that rely on index metadata (such as VWAP) operate correctly.

3. **OHLC Reconstruction**
   - `Open` is the previous close, while `High`/`Low` expand around the max/min of `(Open, Close)` using volatility-scaled noise.
   - `Volume` is sampled from an integer range and scaled by the current sigma so that turbulent regimes naturally produce larger prints.

4. **Indicator Enrichment**
   - Delegates to `engine.indicators.add_technical_indicators()` to append the full indicator suite (moving averages, oscillators, channels, etc.).
   - After indicators are computed, the first 210 rows are dropped to remove initialization artifacts from long lookbacks such as the 200-period SMA.

## Practical Notes

- **Determinism**: The engine intentionally uses NumPy randomness without seeds so that each "Skip" action yields a unique scenario.
- **Performance**: All calculations are vectorized; even with the indicator stack, generating a fresh scenario typically takes <50 ms on modern hardware.
- **Extensibility**: You can add custom indicators by editing `add_technical_indicators()`—the synthetic generator will pick them up automatically.
