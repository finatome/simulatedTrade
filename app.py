import dash
from dash import dcc, html, Input, Output, State, callback_context
from engine.gbm_engine import generate_scenario_data
from engine.simulator import FuturesSimulator
from engine.analytics import calculate_metrics
from components.viewport import create_viewport
from components.scoreboard import scoreboard_layout
from components.settings import settings_layout
from components.controls import controls_layout

# Initialize Simulator global instance
sim = FuturesSimulator()
current_df = generate_scenario_data()

app = dash.Dash(__name__, title="TradeSim Pro")
app._favicon = None

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Graph(id='main-viewport', figure=create_viewport(current_df.iloc[:50], show_indicators=['SMA_20', 'SMA_50', 'BBM_20_2.0_2.0', 'SUPERT_7_3.0', 'MACD_12_26_9'])),
            controls_layout()
        ], className='main-chart-area'),
        
        html.Div(id='scoreboard-container', className='right-panel', 
                 children=[
                     scoreboard_layout(calculate_metrics(sim.scenario_history), sim.balance),
                     settings_layout()
                 ])
    ], className='container'),
    
    # Interval for the "fast forward" animation
    dcc.Interval(id='reveal-clock', interval=100, disabled=True),
    
    # Store to track current scenario state
    dcc.Store(id='scenario-store', data={'idx': 50, 'active': False, 'scenario_count': 0})
])

@app.callback(
    [Output('main-viewport', 'figure'),
     Output('scoreboard-container', 'children'),
     Output('scenario-store', 'data'),
     Output('reveal-clock', 'disabled'),
     Output('trade-status', 'children')],
    [Input('btn-long', 'n_clicks'), Input('btn-short', 'n_clicks'), 
     Input('btn-skip', 'n_clicks'), Input('reveal-clock', 'n_intervals'),
     Input('indicator-dropdown', 'value'),
     Input('theme-selector', 'value')],
    [State('scenario-store', 'data'),
     State('tp-input', 'value'),
     State('sl-input', 'value')]
)
def orchestrate(long_clicks, short_clicks, skip_clicks, n_intervals, selected_indicators, theme_value, state, tp_input, sl_input):
    ctx = callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    
    # Default values validation
    tp_pct = (tp_input or 1) / 100.0
    sl_pct = (sl_input or 1) / 100.0
    theme = theme_value or 'dark'
    
    # Limit indicators to 5
    if selected_indicators and len(selected_indicators) > 5:
        selected_indicators = selected_indicators[:5]

    global current_df
    
    # Check if we are mid-run
    if state['active']:
        pass

    # 1. Start New Scenario if Skip (or initial load handled by layout)
    if trigger == 'btn-skip':
        # Reset scene
        current_df = generate_scenario_data()
        state = {'idx': 50, 'active': False, 'scenario_count': state['scenario_count']}
        
        fig = create_viewport(current_df.iloc[:50], show_indicators=selected_indicators, theme=theme)
        metrics = calculate_metrics(sim.scenario_history)
        
        right_panel_content = [
            scoreboard_layout(metrics, sim.balance),
            settings_layout(current_theme=theme, current_indicators=selected_indicators)
        ]
        
        status_msg = "Scenario skipped. New market loaded."
        return fig, right_panel_content, state, True, status_msg
    
    # Handle Indicator or Theme Change (Just Refresh View)
    if trigger in ['indicator-dropdown', 'theme-selector']:
        start_idx = 0 if state['active'] else 0 # actually we show from start? 
        # Logic: if active, show up to current idx.
        end_idx = state['idx']
        
        trade_state = {'entry': sim.entry_price, 'tp': sim.tp_price, 'sl': sim.sl_price} if state['active'] else None
        
        fig = create_viewport(current_df.iloc[:end_idx], show_indicators=selected_indicators, trade_state=trade_state, theme=theme)
        return fig, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    # 2. Handle Entry
    if trigger in ['btn-long', 'btn-short'] and not state['active']:
        side = 'LONG' if trigger == 'btn-long' else 'SHORT'
        current_price = current_df.iloc[49]['Close']
        
        sim.enter_trade(side, current_price, tp_pct=tp_pct, sl_pct=sl_pct)
        
        state['active'] = True
        
        # Initial chart with lines
        trade_state = {'entry': sim.entry_price, 'tp': sim.tp_price, 'sl': sim.sl_price}
        fig = create_viewport(current_df.iloc[:50], show_indicators=selected_indicators, trade_state=trade_state, theme=theme)
        
        status_msg = f"Entered {side} at {current_price:.2f}. Executing..."
        return fig, dash.no_update, state, False, status_msg

    # 3. Handle Reveal (The "Full Show")
    if trigger == 'reveal-clock':
        state['idx'] += 1
        candle_to_check = current_df.iloc[state['idx']-1]
        
        # Check Exit Trigger
        triggered, reason, exit_price = sim.check_exit(candle_to_check)
        
        # End of scenario check or Triggered
        if triggered or state['idx'] >= len(current_df):
            
            if triggered:
                pnl = sim.close_trade(exit_price, reason=reason)
                msg_reason = reason
            else:
                exit_price = current_df.iloc[-1]['Close']
                pnl = sim.close_trade(exit_price, reason="TIMEOUT")
                msg_reason = "TIMEOUT"
            
            state['active'] = False
            state['scenario_count'] += 1
            
            metrics = calculate_metrics(sim.scenario_history)
            
            fig = create_viewport(current_df.iloc[:state['idx']], show_indicators=selected_indicators, trade_state=None, theme=theme) 
            
            right_panel_content = [
                scoreboard_layout(metrics, sim.balance),
                settings_layout(current_theme=theme, current_indicators=selected_indicators)
            ]
            
            status_msg = f"Trade Closed ({msg_reason}). PnL: ${pnl:.2f}. Click SKIP for next."
            return fig, right_panel_content, state, True, status_msg
        
        # Incremental update
        trade_state = {'entry': sim.entry_price, 'tp': sim.tp_price, 'sl': sim.sl_price}
        fig = create_viewport(current_df.iloc[:state['idx']], show_indicators=selected_indicators, trade_state=trade_state, theme=theme)
        
        # Live Stats
        unrealized_pnl = sim.get_unrealized_pnl(candle_to_check['Close'])
        live_data = {
            'active': True,
            'entry': sim.entry_price,
            'tp': sim.tp_price,
            'sl': sim.sl_price,
            'unrealized_pnl': unrealized_pnl
        }
        
        metrics = calculate_metrics(sim.scenario_history)
        
        right_panel_content = [
            scoreboard_layout(metrics, sim.balance, live_data),
            settings_layout(current_theme=theme, current_indicators=selected_indicators)
        ]
        
        return fig, right_panel_content, state, False, dash.no_update

    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, "Ready."

if __name__ == '__main__':
    app.run(debug=True, port=8050)
