import os

import dash
from dash import dcc, html, Input, Output, State, callback_context
from flask import send_from_directory
from engine.gbm_engine import generate_scenario_data
from engine.real_data_engine import get_random_scenario as get_real_scenario
from engine.simulator import FuturesSimulator
from engine.analytics import calculate_metrics
from components.viewport import create_viewport
from components.scoreboard import scoreboard_layout
from components.settings import left_panel_settings, right_panel_settings
from components.controls import controls_layout
from components.indicator_cards import render_indicator_cards

# Initialize Simulator global instance
sim = FuturesSimulator()
current_df = generate_scenario_data()

app = dash.Dash(__name__, title="TradeSim Pro")
app._favicon = None

# Documentation Server
DOCS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site')

@app.server.route('/docs/')
@app.server.route('/docs/<path:path>')
def serve_docs(path='index.html'):
    if not os.path.exists(DOCS_DIR):
        return "Documentation not found. Run 'mkdocs build' first.", 404
    return send_from_directory(DOCS_DIR, path)

app.layout = html.Div([
    # Header
    html.Div([
        html.H1("SimTrade: Simulated Trading", className='dashboard-title'),
        
        html.A(
            html.Button("Documentation", style={
                'backgroundColor': '#28a745',
                'color': 'white',
                'border': 'none',
                'padding': '8px 15px',
                'borderRadius': '5px',
                'cursor': 'pointer',
                'fontSize': '14px',
                'fontWeight': 'bold'
            }),
            href='/docs/index.html',
            target='_blank',
            style={'position': 'absolute', 'right': '20px', 'top': '15px', 'textDecoration': 'none'}
        )
    ], className='app-header'),

    html.Div([
        # Left Panel (Data & Theme)
        html.Div(id='left-panel', className='left-panel', children=[
            left_panel_settings(),
            # Placeholder for future left panel items
        ]),

        # Middle Panel (Chart & Controls)
        html.Div(id='middle-panel', className='middle-panel', children=[
            dcc.Graph(id='main-viewport', figure=create_viewport(current_df.iloc[:100], show_indicators=['SMA_20', 'SMA_50', 'BBM_20_2.0_2.0', 'SUPERT_7_3.0', 'MACD_12_26_9']), style={'minHeight': '75vh'}),
            controls_layout()
        ]),
        
        # Right Panel (Scoreboard & Config)
        html.Div(id='right-panel-container', className='right-panel', 
                 children=[
                     html.Div(id='scoreboard-wrapper', children=scoreboard_layout(calculate_metrics(sim.scenario_history), sim.balance)),
                     html.Div(id='right-settings-wrapper', style={'flex': '1', 'overflowY': 'auto'}, children=right_panel_settings())
                 ])
    ], className='container'),
    
    # Interval for the "fast forward" animation
    dcc.Interval(id='reveal-clock', interval=100, disabled=True),
    
    # Store to track current scenario state
    dcc.Store(id='scenario-store', data={'idx': 100, 'active': False, 'scenario_count': 0})
])

@app.callback(
    [Output('main-viewport', 'figure'),
     Output('scoreboard-wrapper', 'children'),
     Output('right-settings-wrapper', 'children'),
     Output('scenario-store', 'data'),
     Output('reveal-clock', 'disabled'),
     Output('trade-status', 'children'),
     Output('left-panel', 'children'),
     Output('indicator-cards-wrapper', 'children')],
    [Input('btn-long', 'n_clicks'), Input('btn-short', 'n_clicks'), Input('btn-exit', 'n_clicks'),
     Input('btn-skip', 'n_clicks'), Input('reveal-clock', 'n_intervals'),
     Input('indicator-selector', 'value'),
     Input('theme-selector', 'value'),
     Input('data-source-selector', 'value'),
     Input('ticker-selector', 'value'),
     Input('optional-indicator-selector', 'value'),
     Input('second-order-selector', 'value'),
     Input('third-order-selector', 'value'),
     Input('fourth-order-selector', 'value'),
     Input('fifth-order-selector', 'value'),
     Input('sixth-order-selector', 'value')],
    [State('scenario-store', 'data'),
     State('tp-input', 'value'),
     State('sl-input', 'value')]
)
def orchestrate(long_clicks, short_clicks, exit_clicks, skip_clicks, n_intervals, selected_indicators, theme_value, source_value, ticker_value, optional_indicators, second_order_indicators, third_order_indicators, fourth_order_indicators, fifth_order_indicators, sixth_order_indicators, state, tp_input, sl_input):
    ctx = callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    
    # Default values validation (Points)
    tp_points = tp_input if tp_input is not None else 20
    sl_points = sl_input if sl_input is not None else 20
    theme = theme_value or 'dark'
    data_source = source_value or 'synthetic'
    ticker = ticker_value or 'MES'
    
    # Limit indicators to 5 (Standard only for now, or total?)
    # Let's keep the limit on standard indicators as per UI, but allow optional ones freely or limit total?
    # User request didn't specify limits on optional.
    if selected_indicators and len(selected_indicators) > 5:
        selected_indicators = selected_indicators[:5]

    # Combine for viewport
    all_indicators = (selected_indicators or []) + (optional_indicators or []) + (second_order_indicators or []) + (third_order_indicators or []) + (fourth_order_indicators or []) + (fifth_order_indicators or []) + (sixth_order_indicators or [])

    global current_df
    
    # Check if we are mid-run
    if state['active']:
        pass

    # 1. Start New Scenario (Skip OR Source Change OR Ticker Change)
    if trigger == 'btn-skip' or trigger == 'data-source-selector' or trigger == 'ticker-selector':
        # Generate new scenario based on Source
        if data_source == 'real':
            # Use Real Data (CV/Download)
            # Pass ticker to engine
            possible_df = get_real_scenario(ticker=ticker, periods=400)
            if possible_df is not None and len(possible_df) > 100:
                current_df = possible_df
            else:
                 # Fallback
                 current_df = generate_scenario_data()
        else:
            # Synthetic
            current_df = generate_scenario_data()
            
        sim.load_data(current_df)
        sim.reset() 
        
        state = {'idx': 100, 'active': False, 'scenario_count': state['scenario_count']}
        
        fig = create_viewport(current_df.iloc[:100], show_indicators=all_indicators, theme=theme, history=[])
        metrics = calculate_metrics(sim.scenario_history)
        
        scoreboard_content = scoreboard_layout(metrics, sim.balance)
        right_settings_content = right_panel_settings(
            current_tp=tp_points,
            current_sl=sl_points,
            current_theme=theme
        )
        
        left_panel_content = left_panel_settings(
            current_source=data_source, 
            current_ticker=ticker,
            current_indicators=selected_indicators,
            current_optional_indicators=optional_indicators,
            current_second_order=second_order_indicators,
            current_third_order=third_order_indicators,
            current_fourth_order=fourth_order_indicators,
            current_fifth_order=fifth_order_indicators,
            current_sixth_order=sixth_order_indicators
        )
        
        status_msg = f"New {data_source.upper()} Scenario ({ticker if data_source=='real' else 'GBM'})."
        
        cards_content = render_indicator_cards(all_indicators)
        return fig, scoreboard_content, right_settings_content, state, True, status_msg, left_panel_content, cards_content
    
    # Old block removed to use optimized selector handler below
    if False and trigger in ['indicator-selector', 'theme-selector', 'optional-indicator-selector']:
        pass

    # 2. Handle Entry
    if trigger in ['btn-long', 'btn-short'] and not state['active']:
        side = 'LONG' if trigger == 'btn-long' else 'SHORT'
        current_price = current_df.iloc[49]['Close']
        entry_time = current_df.index[49] # Capture entry time
        
        sim.enter_trade(side, current_price, tp_points=tp_points, sl_points=sl_points, entry_time=entry_time)
        
        state['active'] = True
        
        # Initial chart with lines
        trade_state = {'entry': sim.entry_price, 'tp': sim.tp_price, 'sl': sim.sl_price}
        # While active, pass empty history so old trades don't show.
        fig = create_viewport(current_df.iloc[:100], show_indicators=all_indicators, trade_state=trade_state, theme=theme, history=[])
        
        status_msg = f"Entered {side} at {current_price:.2f}. Executing..."
        return fig, dash.no_update, dash.no_update, state, False, status_msg, dash.no_update, dash.no_update
        
    # 3. Handle Manual Exit
    if trigger == 'btn-exit' and state['active']:
        # Exit at the LAST known candle close (which is at index state['idx']-1)
        exit_price = current_df.iloc[state['idx']-1]['Close']
        exit_time = current_df.index[state['idx']-1]
        
        pnl = sim.close_trade(exit_price, reason="MANUAL", exit_time=exit_time)
        
        state['active'] = False
        state['scenario_count'] += 1
        
        metrics = calculate_metrics(sim.scenario_history)
        
        # Implement sliding window: show max 150 candles
        window_size = 150
        start_idx = max(0, state['idx'] - window_size)
        
        # Show ONLY the latest trade (the one just closed)
        last_trade = [sim.scenario_history[-1]] if sim.scenario_history else []
        fig = create_viewport(current_df.iloc[start_idx:state['idx']], show_indicators=all_indicators, trade_state=None, theme=theme, history=last_trade)
        
        scoreboard_content = scoreboard_layout(metrics, sim.balance)
        right_settings_content = right_panel_settings(
            current_tp=tp_points,
            current_sl=sl_points
        )
        
        status_msg = f"Trade Manually Closed. PnL: ${pnl:.2f}. Click SKIP for next."
        # IMPORTANT: Disable the clock so it stops running
        cards_content = render_indicator_cards(all_indicators)
        return fig, scoreboard_content, right_settings_content, state, True, status_msg, dash.no_update, cards_content
    
    # 4. Handle Static Updates (Selectors)
    if trigger and ('selector' in trigger):
        # Repaint chart with new settings (using recent window)
        # Identify window
        if state['active']:
             # If active, we might wait for next tick, or force update? 
             # Let's force update.
             pass
        
        window_size = 150
        start_idx = max(0, state['idx'] - window_size)
        
        # Determine trade state if active?
        trade_state = {'entry': sim.entry_price, 'tp': sim.tp_price, 'sl': sim.sl_price} if state['active'] else None
        
        # If active, history should be empty. If inactive (finished), show last trade?
        # Typically static updates happen WHILE active (user toggles indicator).
        # Or AFTER finished (user toggles indicator before skipping).
        current_history = []
        if not state['active'] and sim.scenario_history:
             # If finished, maybe show last trade? Assuming we haven't started NEW scenario yet.
             # Wait, how do we know if we are "post-trade" or "pre-trade"?
             # If active is False, and data hasn't been reset (which happens on SKIP).
             # We can't distinguish "New - Pre-Entry" vs "Finished - Post-Exit" easily just from state['active'].
             # But usually user toggles setting -> repaints.
             # A safe bet: if not active, SHOW last trade IF it exists?
             # BUT if we are "New", last trade is from PREVIOUS scenario.
             # We want to avoid showing previous scenario's trade on NEW scenario.
             # On "New Scenario" (skip), we reset simulator but History REMAINS.
             # So actually, we CANNOT rely on history existing.
             # We need to know if the CURRENT history item belongs to CURRENT data.
             # But data is replaced.
             # So safest: Default empty for static updates unless we track "scenario_id" in history vs current.
             # Let's just default empty to solve "disappear" request safely.
             current_history = []
        
        fig = create_viewport(current_df.iloc[start_idx:state['idx']], show_indicators=all_indicators, trade_state=trade_state, theme=theme, history=current_history)
        
        # Don't update other components
        cards_content = render_indicator_cards(all_indicators)
        return fig, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, cards_content

    # 3. Handle Reveal
    if trigger == 'reveal-clock':
        state['idx'] += 1
        candle_to_check = current_df.iloc[state['idx']-1]
        
        triggered, reason, exit_price = sim.check_exit(candle_to_check)
        
        if triggered or state['idx'] >= len(current_df):
            exit_time = current_df.index[state['idx']-1]
            
            if triggered:
                pnl = sim.close_trade(exit_price, reason=reason, exit_time=exit_time)
                msg_reason = reason
            else:
                exit_price = current_df.iloc[-1]['Close']
                pnl = sim.close_trade(exit_price, reason="TIMEOUT", exit_time=exit_time)
                msg_reason = "TIMEOUT"
            
            state['active'] = False
            state['scenario_count'] += 1
            
            metrics = calculate_metrics(sim.scenario_history)
            
            # Implement sliding window: show max 150 candles
            window_size = 150
            start_idx = max(0, state['idx'] - window_size)
            
            # Show ONLY the latest trade (the one just closed)
            last_trade = [sim.scenario_history[-1]] if sim.scenario_history else []
            fig = create_viewport(current_df.iloc[start_idx:state['idx']], show_indicators=all_indicators, trade_state=None, theme=theme, history=last_trade) 
            
            scoreboard_content = scoreboard_layout(metrics, sim.balance)
            right_settings_content = right_panel_settings(
                current_tp=tp_points,
                current_sl=sl_points,
                current_theme=theme
            )
            
            status_msg = f"Trade Closed ({msg_reason}). PnL: ${pnl:.2f}. Click SKIP for next."
            return fig, scoreboard_content, right_settings_content, state, True, status_msg, dash.no_update, dash.no_update
        
        trade_state = {'entry': sim.entry_price, 'tp': sim.tp_price, 'sl': sim.sl_price}
        
        # Implement sliding window: show max 150 candles
        window_size = 150
        start_idx = max(0, state['idx'] - window_size)
        
        # Reveal Mode (Active): Empty history
        fig = create_viewport(current_df.iloc[start_idx:state['idx']], show_indicators=all_indicators, trade_state=trade_state, theme=theme, history=[])
        
        unrealized_pnl = sim.get_unrealized_pnl(candle_to_check['Close'])
        live_data = {
            'active': True,
            'entry': sim.entry_price,
            'tp': sim.tp_price,
            'sl': sim.sl_price,
            'unrealized_pnl': unrealized_pnl
        }
        
        metrics = calculate_metrics(sim.scenario_history)
        
        scoreboard_content = scoreboard_layout(metrics, sim.balance, live_data)
        right_settings_content = right_panel_settings(
            current_tp=tp_points,
            current_sl=sl_points,
            current_theme=theme
        )
        
        return fig, scoreboard_content, right_settings_content, state, False, dash.no_update, dash.no_update, dash.no_update

    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, "", dash.no_update, dash.no_update

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    host = os.environ.get('HOST', '0.0.0.0')
    debug_mode = os.environ.get('DASH_DEBUG', '0').lower() in ('1', 'true', 'yes')
    app.run(debug=debug_mode, host=host, port=port)
