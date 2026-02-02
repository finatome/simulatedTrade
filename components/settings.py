from dash import html, dcc

def left_panel_settings(current_theme='dark', current_source='synthetic', current_ticker='MES'):
    """
    Returns the layout for the Left Panel: Data Source and Theme Selection.
    """
    return html.Div([
        html.H3("CONFIG", className="panel-title", style={'marginBottom': '15px'}),

        # Data Source
        html.Div([
            html.Label("DATA SOURCE", className="stat-label"),
            dcc.RadioItems(
                id='data-source-selector',
                options=[
                    {'label': ' Synthetic', 'value': 'synthetic'},
                    {'label': ' Real (Futures)', 'value': 'real'}
                ],
                value=current_source,
                labelStyle={'display': 'block', 'marginBottom': '10px', 'color': '#ccc', 'cursor': 'pointer'},
                inputStyle={'marginRight': '10px', 'cursor': 'pointer'}
            )
        ], style={'marginBottom': '15px'}),

        # Ticker Selection (Only active if Real is selected, but we will handle visibility/disabled in app, or just leave it)
        html.Div([
            html.Label("TICKER (Real Data)", className="stat-label"),
            dcc.Dropdown(
                id='ticker-selector',
                options=[
                    {'label': 'Micro E-mini S&P 500 (MES)', 'value': 'MES'},
                    {'label': 'Micro Gold (MGC)', 'value': 'MGC'},
                    {'label': 'Micro Silver (SIL)', 'value': 'SIL'},
                    {'label': 'Micro Nasdaq 100 (MNQ)', 'value': 'MNQ'},
                    {'label': 'Micro Bitcoin (MBT)', 'value': 'MBT'},
                ],
                value=current_ticker,
                clearable=False,
                style={'backgroundColor': '#1e2329', 'color': '#333'}
            )
        ], style={'marginBottom': '25px'}),

        # Theme
        html.Div([
            html.Label("THEME", className="stat-label"),
            dcc.RadioItems(
                id='theme-selector',
                options=[
                    {'label': ' Dark', 'value': 'dark'},
                    {'label': ' Light', 'value': 'light'}
                ],
                value=current_theme,
                labelStyle={'display': 'block', 'marginBottom': '10px', 'color': '#ccc', 'cursor': 'pointer'},
                inputStyle={'marginRight': '10px', 'cursor': 'pointer'}
            )
        ], style={'marginBottom': '20px'}),
        
    ], className="settings-panel left-settings", style={'padding': '20px'})


def right_panel_settings(current_indicators=None, current_tp=None, current_sl=None):
    """
    Returns the layout for the Right Panel: Trade Config and Indicators.
    """
    if current_indicators is None:
        current_indicators = ['SMA_20', 'SMA_50', 'BBM_20_2.0_2.0', 'SUPERT_7_3.0', 'MACD_12_26_9']
    
    tp_val = current_tp if current_tp is not None else 15
    sl_val = current_sl if current_sl is not None else 15

    return html.Div([
        html.H3("TRADE CONFIG", className="panel-title", style={'marginTop': '0px'}),
        
        # Trade Controls in a Row
        html.Div([
            html.Div([
                html.Label("TP (Pts)", className="stat-label"),
                dcc.Input(
                    id='tp-input',
                    type='number',
                    value=tp_val,
                    min=1,
                    max=5000,
                    step=1,
                    style={'width': '80px', 'backgroundColor': '#1e2329', 'border': '2px solid #28a745', 'color': 'white', 'textAlign': 'center', 'outline': 'none'}
                )
            ], style={'display': 'inline-block', 'marginRight': '20px'}),
            
            html.Div([
                html.Label("SL (Pts)", className="stat-label"),
                dcc.Input(
                    id='sl-input',
                    type='number',
                    value=sl_val,
                    min=1,
                    max=5000,
                    step=1,
                    style={'width': '80px', 'backgroundColor': '#1e2329', 'border': '2px solid #dc3545', 'color': 'white', 'textAlign': 'center', 'outline': 'none'}
                )
            ], style={'display': 'inline-block'}),
            
        ], style={'textAlign': 'center', 'marginBottom': '20px'}),

        html.Div([
            html.Label("INDICATORS (Max 5)", className="stat-label", style={'marginBottom': '10px', 'display': 'block'}),
            html.Div([
                dcc.Checklist(
                    id='indicator-selector',
                    options=[
                        {'label': ' SMA 20', 'value': 'SMA_20'},
                        {'label': ' SMA 50', 'value': 'SMA_50'},
                        {'label': ' SMA 200', 'value': 'SMA_200'},
                        {'label': ' EMA 9', 'value': 'EMA_9'},
                        {'label': ' EMA 21', 'value': 'EMA_21'},
                        {'label': ' Bollinger Bands', 'value': 'BBM_20_2.0_2.0'},
                        {'label': ' Keltner Channels', 'value': 'KC_20_2'},
                        {'label': ' Donchian Channels', 'value': 'DCL_20_20'},
                        {'label': ' VWAP', 'value': 'VWAP_D'},
                        {'label': ' Supertrend', 'value': 'SUPERT_7_3.0'},
                        {'label': ' RSI', 'value': 'RSI_14'},
                        {'label': ' MACD', 'value': 'MACD_12_26_9'},
                        {'label': ' Stochastic', 'value': 'STOCHk_14_3_3'},
                        {'label': ' ADX', 'value': 'ADX_14'},
                        {'label': ' CCI', 'value': 'CCI_14_0.015'},
                        {'label': ' ROC', 'value': 'ROC_10'},
                        {'label': ' OBV', 'value': 'OBV'},
                        {'label': ' Parabolic SAR', 'value': 'PSARl_0.02_0.2'}
                    ],
                    value=current_indicators,
                    labelStyle={'display': 'block', 'padding': '8px', 'borderBottom': '1px solid #333', 'cursor': 'pointer'},
                    inputStyle={'marginRight': '10px', 'cursor': 'pointer'}
                )
            ], style={'textAlign': 'left', 'height': '400px', 'overflowY': 'auto', 'border': '1px solid #333', 'borderRadius': '5px', 'padding': '5px'})
        ], style={'display': 'block', 'marginTop': '10px'}),
            
    ], className="settings-panel", style={'flex': '1', 'overflowY': 'auto', 'display': 'flex', 'flexDirection': 'column'})
