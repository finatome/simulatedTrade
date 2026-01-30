from dash import html, dcc

def settings_layout(current_theme='dark', current_indicators=None, current_source='synthetic', current_tp=None, current_sl=None):
    if current_indicators is None:
        current_indicators = ['SMA_20', 'SMA_50', 'BBM_20_2.0_2.0', 'SUPERT_7_3.0', 'MACD_12_26_9']
    
    tp_val = current_tp if current_tp is not None else 15
    sl_val = current_sl if current_sl is not None else 15

    return html.Div([
        html.Div([
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
                    inline=True,
                    labelStyle={'marginRight': '20px', 'color': '#888'},
                    inputStyle={'marginRight': '5px'}
                )
            ], style={'display': 'inline-block', 'marginRight': '30px'}),

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
                    inline=True,
                    labelStyle={'marginRight': '20px', 'color': '#888'},
                    inputStyle={'marginRight': '5px'}
                )
            ], style={'display': 'inline-block'}),
            
        ], style={'marginBottom': '20px', 'textAlign': 'center'}),

        html.H3("TRADE SETTINGS", className="panel-title", style={'marginTop': '0px'}),
        
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
            ], style={'display': 'inline-block', 'marginRight': '20px'}),
            
            html.Div([
                html.Label("INDICATORS", className="stat-label"),
                dcc.Dropdown(
                    id='indicator-dropdown',
                    options=[
                        {'label': 'SMA 20', 'value': 'SMA_20'},
                        {'label': 'SMA 50', 'value': 'SMA_50'},
                        {'label': 'SMA 200', 'value': 'SMA_200'},
                        {'label': 'EMA 9', 'value': 'EMA_9'},
                        {'label': 'EMA 21', 'value': 'EMA_21'},
                        {'label': 'Bollinger Bands', 'value': 'BBM_20_2.0_2.0'},
                        {'label': 'Keltner Channels', 'value': 'KC_20_2'},
                        {'label': 'Donchian Channels', 'value': 'DCL_20_20'},
                        {'label': 'VWAP', 'value': 'VWAP_D'},
                        {'label': 'Supertrend', 'value': 'SUPERT_7_3.0'},
                        {'label': 'RSI', 'value': 'RSI_14'},
                        {'label': 'MACD', 'value': 'MACD_12_26_9'},
                        {'label': 'Stochastic', 'value': 'STOCHk_14_3_3'},
                        {'label': 'ADX', 'value': 'ADX_14'},
                        {'label': 'CCI', 'value': 'CCI_14_0.015'},
                        {'label': 'ROC', 'value': 'ROC_10'},
                        {'label': 'OBV', 'value': 'OBV'},
                        {'label': 'Parabolic SAR', 'value': 'PSARl_0.02_0.2'}
                    ],
                    value=current_indicators,
                    multi=True,
                    style={'width': '300px', 'color': '#333'}
                )
            ], style={'display': 'inline-block', 'verticalAlign': 'top'}),
            
        ], style={'textAlign': 'center', 'marginBottom': '20px'}),
    ], className="settings-panel")
