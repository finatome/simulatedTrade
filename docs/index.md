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
