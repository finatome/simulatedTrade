from dash import html, dcc

def settings_layout():
    return html.Div([
        html.H3("TRADE SETTINGS", className="panel-title", style={'marginTop': '20px'}),
        
        html.Div([
            html.Div([
                html.Label("Take Profit (%)", className="stat-label"),
                dcc.Input(
                    id='tp-input',
                    type='number',
                    value=1,
                    min=0.1,
                    max=100,
                    step=0.1,
                    className="input-field"
                )
            ], className="stat-mini"),
            
            html.Div([
                html.Label("Stop Loss (%)", className="stat-label"),
                dcc.Input(
                    id='sl-input',
                    type='number',
                    value=1,
                    min=0.1,
                    max=100,
                    step=0.1,
                    className="input-field"
                )
            ], className="stat-mini"),
        ], className="stat-grid"),
        
        html.Div([
            html.Label("Top Indicators (Max 5)", className="stat-label"),
            dcc.Dropdown(
                id='indicator-dropdown',
                options=[
                    {'label': 'Simple Moving Average (20)', 'value': 'SMA_20'},
                    {'label': 'Simple Moving Average (50)', 'value': 'SMA_50'},
                    {'label': 'Simple Moving Average (200)', 'value': 'SMA_200'},
                    {'label': 'Exponential Moving Average (9)', 'value': 'EMA_9'},
                    {'label': 'Exponential Moving Average (21)', 'value': 'EMA_21'},
                    {'label': 'Exponential Moving Average (50)', 'value': 'EMA_50'},
                    {'label': 'Weighted Moving Average (21)', 'value': 'WMA_21'},
                    {'label': 'Hull Moving Average (21)', 'value': 'HMA_21'},
                    {'label': 'Volume Weighted Average Price (VWAP)', 'value': 'VWAP_D'},
                    {'label': 'Supertrend', 'value': 'SUPERT_7_3.0'},
                    {'label': 'Bollinger Bands', 'value': 'BBM_20_2.0'},
                    {'label': 'Keltner Channels', 'value': 'KC_20_2'},
                    {'label': 'Donchian Channels', 'value': 'DCM_20_20'},
                    {'label': 'Relative Strength Index (RSI)', 'value': 'RSI_14'},
                    {'label': 'MACD', 'value': 'MACD_12_26_9'},
                    {'label': 'Stochastic Oscillator', 'value': 'STOCHk_14_3_3'},
                    {'label': 'Average Directional Index (ADX)', 'value': 'ADX_14'},
                    {'label': 'Commodity Channel Index (CCI)', 'value': 'CCI_14_0.015'},
                    {'label': 'Rate of Change (ROC)', 'value': 'ROC_10'},
                    {'label': 'On-Balance Volume (OBV)', 'value': 'OBV'},
                    {'label': 'Parabolic SAR', 'value': 'PSARl_0.02_0.2'}
                ],
                value=['SMA_20', 'SMA_50', 'BBM_20_2.0', 'SUPERT_7_3.0', 'MACD_12_26_9'],
                multi=True,
                placeholder="Select indicators...",
                style={'color': '#000'}
            )
        ], style={'marginTop': '10px'})
    ], className="settings-panel")
