# Trading & Scoring Engine

The trading core lives in `engine/simulator.py` and powers every scenario shown in the Dash UI. It emulates a single-position futures account with leverage, configurable take-profit/stop-loss brackets, and persistent performance tracking.

## Trade Lifecycle

1. **Entry**
    - Triggered via the LONG or SHORT buttons once the initial 50-candle history is displayed.
    - `enter_trade()` records the side, sets the entry price, and converts user-specified TP/SL *points* into absolute price levels. For example, entering long at 4,000 with a 15-point target produces a 4,015 TP and 3,985 SL.

2. **Reveal Loop**
    - The UI advances one candle per timer tick (100 ms by default). Each new candle flows through `check_exit()`.
    - Exit order of operations favors risk management: stop-loss detection runs before take-profit to mirror worst-case execution within a volatile candle.

3. **Exit Conditions**
    - **TP Hit**: Candle reaches or crosses the TP level.
    - **SL Hit**: Candle reaches or crosses the SL level (evaluated first).
    - **Manual Exit**: User presses EXIT, closing at the most recent close.
    - **Timeout**: Scenario reaches the final candle without other triggers.

4. **PnL Calculation**
    - `close_trade()` computes raw percent return `(exit - entry) / entry`, scales it by account balance and leverage, and updates the running balance.
    - Each trade appends a record to `scenario_history`, including side, realized PnL, percent return, and close reason.

5. **Reset for Next Scenario**
    - Clicking SKIP (or switching data source/ticker) calls `sim.reset()` and loads a fresh dataframe—either synthetic (GBM) or real (asset cache).

## Real-Time Stats & Scoreboard

`engine/analytics.calculate_metrics()` consumes `scenario_history` to produce the metrics displayed on the right panel:

- **Win Rate**: Percent of trades with PnL > 0.
- **Profit Factor**: Gross profits divided by gross losses (falls back to gross profits when no losses exist).
- **Total PnL**: Sum of realized PnL across the session.
- **Trade Count**: Number of completed trades.

During an active trade, the UI also computes unrealized PnL via `get_unrealized_pnl()` so traders can monitor floating gains relative to leverage and entry price.

## Risk & Configuration

- **Leverage**: Default is 10x and can be changed by instantiating `FuturesSimulator(leverage=...)`.
- **TP/SL Units**: The input fields in the right panel accept point distances (not percentages), ensuring consistency across tickers.
- **Balance Persistence**: Balance and performance history persist across scenarios until the app is restarted, encouraging longer practice sessions.

## Extending the Engine

- Add support for partial exits or multiple contracts by extending the simulator with position sizing fields.
- Plug in alternative scoring metrics (Sharpe, expectancy, drawdown) by expanding `calculate_metrics()` and the scoreboard component.
- Introduce new exit logic (trail stops, time-based exits) by updating `check_exit()` or adding auxiliary state in the simulator.
