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
        html.H1("SimTrade: Simulated Trading", style={
            'textAlign': 'center', 
            'color': '#28a745', 
            'fontFamily': 'sans-serif', 
            'fontSize': '24px',
            'margin': '0', 
            'flex': '1', # Take up available space to center it roughly (or we can center absolutely)
        }),
        
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
    ], style={
        'position': 'relative', # For absolute positioning of button
        'textAlign': 'center', 
        'padding': '15px 0', 
        'backgroundColor': '#0e1117', 
        'borderBottom': '1px solid #333',
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center'
    }),

    html.Div([
        # Left Panel (Data & Theme)
        html.Div(id='left-panel', className='left-panel', style={'flex': '0 0 250px', 'padding': '10px', 'borderRight': '1px solid #333', 'overflowY': 'auto'}, children=[
            left_panel_settings(),
            # Placeholder for future left panel items
        ]),

        # Middle Panel (Chart & Controls)
        html.Div(id='middle-panel', className='middle-panel', style={'flex': '1', 'display': 'flex', 'flexDirection': 'column', 'padding': '10px', 'gap': '20px'}, children=[
            dcc.Graph(id='main-viewport', figure=create_viewport(current_df.iloc[:50], show_indicators=['SMA_20', 'SMA_50', 'BBM_20_2.0_2.0', 'SUPERT_7_3.0', 'MACD_12_26_9']), style={'flex': '1'}),
            controls_layout()
        ]),
        
        # Right Panel (Scoreboard & Config)
        html.Div(id='right-panel-container', className='right-panel', 
                 style={'flex': '0 0 350px', 'display': 'flex', 'flexDirection': 'column', 'height': '100%', 'overflow': 'hidden', 'padding': '10px', 'borderLeft': '1px solid #333'},
                 children=[
                     html.Div(id='scoreboard-wrapper', children=scoreboard_layout(calculate_metrics(sim.scenario_history), sim.balance)),
                     html.Div(id='right-settings-wrapper', style={'flex': '1', 'overflowY': 'auto'}, children=right_panel_settings())
                 ])
    ], className='container', style={'display': 'flex', 'flex': '1', 'width': '100vw', 'backgroundColor': '#0e1117', 'color': '#e6e6e6', 'overflow': 'hidden'}),
    
    # Interval for the "fast forward" animation
    dcc.Interval(id='reveal-clock', interval=100, disabled=True),
    
    # Store to track current scenario state
    dcc.Store(id='scenario-store', data={'idx': 50, 'active': False, 'scenario_count': 0})
], style={'display': 'flex', 'flexDirection': 'column', 'height': '100vh', 'margin': '0', 'padding': '0'})

@app.callback(
    [Output('main-viewport', 'figure'),
     Output('scoreboard-wrapper', 'children'),
     Output('right-settings-wrapper', 'children'),
     Output('scenario-store', 'data'),
     Output('reveal-clock', 'disabled'),
     Output('trade-status', 'children'),
     Output('left-panel', 'children')],
    [Input('btn-long', 'n_clicks'), Input('btn-short', 'n_clicks'), Input('btn-exit', 'n_clicks'),
     Input('btn-skip', 'n_clicks'), Input('reveal-clock', 'n_intervals'),
     Input('indicator-selector', 'value'),
     Input('theme-selector', 'value'),
     Input('data-source-selector', 'value'),
     Input('ticker-selector', 'value')],
    [State('scenario-store', 'data'),
     State('tp-input', 'value'),
     State('sl-input', 'value')]
)
def orchestrate(long_clicks, short_clicks, exit_clicks, skip_clicks, n_intervals, selected_indicators, theme_value, source_value, ticker_value, state, tp_input, sl_input):
    ctx = callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    
    # Default values validation (Points)
    tp_points = tp_input if tp_input is not None else 20
    sl_points = sl_input if sl_input is not None else 20
    theme = theme_value or 'dark'
    data_source = source_value or 'synthetic'
    ticker = ticker_value or 'MES'
    
    # Limit indicators to 5
    if selected_indicators and len(selected_indicators) > 5:
        selected_indicators = selected_indicators[:5]

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
        
        state = {'idx': 50, 'active': False, 'scenario_count': state['scenario_count']}
        
        fig = create_viewport(current_df.iloc[:50], show_indicators=selected_indicators, theme=theme)
        metrics = calculate_metrics(sim.scenario_history)
        
        scoreboard_content = scoreboard_layout(metrics, sim.balance)
        right_settings_content = right_panel_settings(
            current_indicators=selected_indicators, 
            current_tp=tp_points,
            current_sl=sl_points
        )
        
        # We need to maintain the left panel state (and pass back the selected ticker/source)
        # Note: We need to update left_panel_settings signature in components/settings.py if we want to pass back current_ticker
        # But for now, we will simply NOT update the specific arguments of the function if it doesn't support it, 
        # OR we assume the replacement above didn't change the signature yet.
        # WAIT: I did not update the `left_panel_settings` signature in previous step, only the content inside.
        # I need to update the signature to accept `current_ticker`. 
        # I will do that in a separate replacement or assume I can do it here if I edit components/settings.py again.
        # For this step, let's assume I'll fix the signature in settings.py shortly or it defaults.
        # Actually I can't pass `current_ticker` if the function doesn't take it.
        # I will update settings.py signature in the next tool call properly. 
        # For now, I'll pass it assuming I will fix it, or just pass kwargs if it was flexible (it's not).
        
        # Let's check `components/settings.py` signature again.
        # def left_panel_settings(current_theme='dark', current_source='synthetic'):
        # I need to update that signature.
        
        # For now, I will NOT pass it, and accept that it resets to default 'MES' on re-render, 
        # WHICH IS BAD UX.
        # So I MUST update settings.py signature.
        
        # I will defer this tool call's logic slightly or fix settings.py first.
        # Since I am in `replace_file_content` for `app.py`, I will write the code intending for `left_panel_settings` to accept it.
        
        left_panel_content = left_panel_settings(current_theme=theme, current_source=data_source, current_ticker=ticker)
        
        status_msg = f"New {data_source.upper()} Scenario ({ticker if data_source=='real' else 'GBM'})."
        return fig, scoreboard_content, right_settings_content, state, True, status_msg, left_panel_content
    
    # Handle Indicator or Theme Change (Just Refresh View)
    if trigger in ['indicator-selector', 'theme-selector']:
        end_idx = state['idx']
        
        trade_state = {'entry': sim.entry_price, 'tp': sim.tp_price, 'sl': sim.sl_price} if state['active'] else None
        
        fig = create_viewport(current_df.iloc[:end_idx], show_indicators=selected_indicators, trade_state=trade_state, theme=theme)
        
        metrics = calculate_metrics(sim.scenario_history)
        scoreboard_content = scoreboard_layout(
            metrics, 
            sim.balance, 
            live_data={'active': state['active'], 'entry': sim.entry_price, 'tp': sim.tp_price, 'sl': sim.sl_price, 'unrealized_pnl': sim.get_unrealized_pnl(current_df.iloc[end_idx-1]['Close']) if state['active'] else 0}
        )
        
        right_settings_content = right_panel_settings(
            current_indicators=selected_indicators, 
            current_tp=tp_points,
            current_sl=sl_points
        )
        
        left_panel_content = left_panel_settings(current_theme=theme, current_source=data_source, current_ticker=ticker)
        
        return fig, scoreboard_content, right_settings_content, dash.no_update, dash.no_update, dash.no_update, left_panel_content

    # 2. Handle Entry
    if trigger in ['btn-long', 'btn-short'] and not state['active']:
        side = 'LONG' if trigger == 'btn-long' else 'SHORT'
        current_price = current_df.iloc[49]['Close']
        
        sim.enter_trade(side, current_price, tp_points=tp_points, sl_points=sl_points)
        
        state['active'] = True
        
        # Initial chart with lines
        trade_state = {'entry': sim.entry_price, 'tp': sim.tp_price, 'sl': sim.sl_price}
        fig = create_viewport(current_df.iloc[:50], show_indicators=selected_indicators, trade_state=trade_state, theme=theme)
        
        status_msg = f"Entered {side} at {current_price:.2f}. Executing..."
        return fig, dash.no_update, dash.no_update, state, False, status_msg, dash.no_update
        
    # 3. Handle Manual Exit
    if trigger == 'btn-exit' and state['active']:
        # Exit at the LAST known candle close (which is at index state['idx']-1)
        exit_price = current_df.iloc[state['idx']-1]['Close']
        pnl = sim.close_trade(exit_price, reason="MANUAL")
        
        state['active'] = False
        state['scenario_count'] += 1
        
        metrics = calculate_metrics(sim.scenario_history)
        
        fig = create_viewport(current_df.iloc[:state['idx']], show_indicators=selected_indicators, trade_state=None, theme=theme)
        
        scoreboard_content = scoreboard_layout(metrics, sim.balance)
        right_settings_content = right_panel_settings(
            current_indicators=selected_indicators, 
            current_tp=tp_points,
            current_sl=sl_points
        )
        
        status_msg = f"Trade Manually Closed. PnL: ${pnl:.2f}. Click SKIP for next."
        # IMPORTANT: Disable the clock so it stops running
        return fig, scoreboard_content, right_settings_content, state, True, status_msg, dash.no_update

    # 3. Handle Reveal
    if trigger == 'reveal-clock':
        state['idx'] += 1
        candle_to_check = current_df.iloc[state['idx']-1]
        
        triggered, reason, exit_price = sim.check_exit(candle_to_check)
        
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
            
            scoreboard_content = scoreboard_layout(metrics, sim.balance)
            right_settings_content = right_panel_settings(
                current_indicators=selected_indicators, 
                current_tp=tp_points,
                current_sl=sl_points
            )
            
            status_msg = f"Trade Closed ({msg_reason}). PnL: ${pnl:.2f}. Click SKIP for next."
            return fig, scoreboard_content, right_settings_content, state, True, status_msg, dash.no_update
        
        trade_state = {'entry': sim.entry_price, 'tp': sim.tp_price, 'sl': sim.sl_price}
        fig = create_viewport(current_df.iloc[:state['idx']], show_indicators=selected_indicators, trade_state=trade_state, theme=theme)
        
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
            current_indicators=selected_indicators, 
            current_tp=tp_points,
            current_sl=sl_points
        )
        
        return fig, scoreboard_content, right_settings_content, state, False, dash.no_update, dash.no_update

    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, "Ready.", dash.no_update

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    host = os.environ.get('HOST', '0.0.0.0')
    debug_mode = os.environ.get('DASH_DEBUG', '0').lower() in ('1', 'true', 'yes')
    app.run(debug=debug_mode, host=host, port=port)
