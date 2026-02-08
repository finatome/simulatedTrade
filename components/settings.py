from dash import html, dcc

def left_panel_settings(current_source='synthetic', current_ticker='MES', current_indicators=None, current_optional_indicators=None, current_second_order=None, current_third_order=None, current_fourth_order=None, current_fifth_order=None, current_sixth_order=None):
    """
    Returns the layout for the Left Panel: Data Source, Theme Selection, and Indicators.
    """
    if current_indicators is None:
        current_indicators = ['SMA_20', 'SMA_50', 'BBM_20_2.0_2.0', 'SUPERT_7_3.0', 'MACD_12_26_9']
    if current_optional_indicators is None:
        current_optional_indicators = []
    if current_second_order is None:
        current_second_order = []
    if current_third_order is None:
        current_third_order = []
    if current_fourth_order is None:
        current_fourth_order = []
    if current_fifth_order is None:
        current_fifth_order = []
    if current_sixth_order is None:
        current_sixth_order = []
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


        
        # Indicators
        html.Div([
            html.Label("DEFAULT INDICATORS (Max 5)", className="stat-label", style={'marginBottom': '10px', 'display': 'block'}),
            html.Div([
                dcc.Checklist(
                    id='indicator-selector',
                    options=[
                        {'label': ' SMA 20', 'value': 'SMA_20'},
                        {'label': ' SMA 50', 'value': 'SMA_50'},
                        {'label': ' Bollinger Bands', 'value': 'BBM_20_2.0_2.0'},
                        {'label': ' Supertrend', 'value': 'SUPERT_7_3.0'},
                        {'label': ' MACD', 'value': 'MACD_12_26_9'},
                    ],
                    value=current_indicators,
                    labelStyle={'display': 'block', 'padding': '8px', 'borderBottom': '1px solid #333', 'cursor': 'pointer'},
                    inputStyle={'marginRight': '10px', 'cursor': 'pointer'}
                )
            ], style={'textAlign': 'left', 'height': 'auto', 'maxHeight': '400px', 'overflowY': 'auto', 'border': '1px solid #333', 'borderRadius': '5px', 'padding': '5px'}),
        # Optional Indicators
        html.Div([
            html.Label("FIRST ORDER PRIMITIVES", className="stat-label", style={'marginBottom': '10px', 'display': 'block', 'marginTop': '15px'}),
            html.Div([
                dcc.Checklist(
                    id='optional-indicator-selector',
                    options=[
                        {'label': ' Average Price', 'value': 'AVGPRICE'},
                        {'label': ' Median Price', 'value': 'MEDPRICE'},
                        {'label': ' Typical Price', 'value': 'TYPPRICE'},
                        # Volume removed as it's default
                        {'label': ' Standard Deviation', 'value': 'STDDEV_20'},
                        {'label': ' Historical Volatility', 'value': 'HISTVOL_20'},
                        {'label': ' Volatility C-C', 'value': 'VOL_CC_20'},
                        {'label': ' Volatility OHLC', 'value': 'VOL_OHLC_20'},
                        {'label': ' Volatility Zero-Trend', 'value': 'VOL_ZTC_20'},
                        {'label': ' Rate of Change (ROC)', 'value': 'ROC_10'},
                        {'label': ' Momentum', 'value': 'MOM_10'},
                        {'label': ' Spread (H-L)', 'value': 'SPREAD'},
                        {'label': ' Ratio (C/SMA50)', 'value': 'RATIO_SMA50'},
                        {'label': ' Net Volume', 'value': 'NETVOL'},
                        {'label': ' Williams Fractal', 'value': 'FRACTALS'},
                    ],
                    value=current_optional_indicators,
                    labelStyle={'display': 'block', 'padding': '8px', 'borderBottom': '1px solid #333', 'cursor': 'pointer'},
                    inputStyle={'marginRight': '10px', 'cursor': 'pointer'}
                )
            ], style={'textAlign': 'left', 'height': '300px', 'overflowY': 'auto', 'border': '1px solid #333', 'borderRadius': '5px', 'padding': '5px'})
        ], style={'display': 'block', 'marginTop': '10px'}),

        # Second Order Smoothing
        html.Div([
            html.Label("SECOND ORDER SMOOTHING", className="stat-label", style={'marginBottom': '10px', 'display': 'block', 'marginTop': '15px'}),
            html.Div([
                dcc.Checklist(
                    id='second-order-selector',
                    options=[
                        {'label': ' EMA (20)', 'value': 'EMA_20'},
                        {'label': ' WMA (20)', 'value': 'WMA_20'},
                        {'label': ' SMMA (20)', 'value': 'RMA_20'},
                        {'label': ' ALMA', 'value': 'ALMA_20_6.0_0.85'},
                        {'label': ' Hull MA (20)', 'value': 'HMA_20'},
                        {'label': ' LSMA (LinReg)', 'value': 'LREG_20'},
                        {'label': ' VWMA', 'value': 'VWMA_20'},
                        {'label': ' Hamming MA', 'value': 'HAMMING_20'},
                        {'label': ' Volatility Weighted (KAMA)', 'value': 'KAMA_10_2_30'},
                    ],
                    value=current_second_order,
                    labelStyle={'display': 'block', 'padding': '8px', 'borderBottom': '1px solid #333', 'cursor': 'pointer'},
                    inputStyle={'marginRight': '10px', 'cursor': 'pointer'}
                )
            ], style={'textAlign': 'left', 'height': 'auto', 'maxHeight': '300px', 'overflowY': 'auto', 'border': '1px solid #333', 'borderRadius': '5px', 'padding': '5px'})
        ], style={'display': 'block', 'marginTop': '10px'}),

        # Third Order Oscillators & Bands
        html.Div([
            html.Label("THIRD ORDER OSCILLATORS", className="stat-label", style={'marginBottom': '10px', 'display': 'block', 'marginTop': '15px'}),
            html.Div([
                dcc.Checklist(
                    id='third-order-selector',
                    options=[
                        {'label': ' MA Cross', 'value': 'MA_CROSS'},
                        {'label': ' EMA Cross', 'value': 'EMA_CROSS'},
                        {'label': ' Price Oscillator', 'value': 'PO_20_50'},
                        {'label': ' Bollinger %B', 'value': 'BB_PCT_B'},
                        {'label': ' Bollinger Bandwidth', 'value': 'BB_WIDTH'},
                        {'label': ' Standard Error Bands', 'value': 'SEB'},
                        {'label': ' Donchian Channels', 'value': 'DCL_20_20'},
                        {'label': ' Keltner Channels', 'value': 'KC_20_2'},
                        {'label': ' MA Channel', 'value': 'MACH_U'},
                        {'label': ' Envelopes', 'value': 'ENV_U'},
                        {'label': ' DPO', 'value': 'DPO_20'},
                        {'label': ' ATR', 'value': 'ATR_14'},
                        {'label': ' CCI', 'value': 'CCI_14_0.015'},
                        {'label': ' Standard Error', 'value': 'STD_ERR'},
                        {'label': ' LinReg Curve', 'value': 'LINREG_CURVE'},
                        {'label': ' LinReg Slope', 'value': 'SLOPE_20'},
                    ],
                    value=current_third_order,
                    labelStyle={'display': 'block', 'padding': '8px', 'borderBottom': '1px solid #333', 'cursor': 'pointer'},
                    inputStyle={'marginRight': '10px', 'cursor': 'pointer'}
                )
            ], style={'textAlign': 'left', 'height': 'auto', 'maxHeight': '400px', 'overflowY': 'auto', 'border': '1px solid #333', 'borderRadius': '5px', 'padding': '5px'})
        ], style={'display': 'block', 'marginTop': '10px'}),

        # Fourth Order Complex Momentum & Volume
        html.Div([
            html.Label("IV. COMPLEX MOMENTUM", className="stat-label", style={'marginBottom': '10px', 'display': 'block', 'marginTop': '15px'}),
            html.Div([
                dcc.Checklist(
                    id='fourth-order-selector',
                    options=[
                        {'label': ' RSI', 'value': 'RSI_14'},
                        {'label': ' Stochastic', 'value': 'STOCHk_14_3_3'},
                        {'label': ' Stochastic RSI', 'value': 'STOCHRSIk_14_14_3_3'},
                        {'label': ' SMI Ergodic', 'value': 'SMI_5_20_5_1.0'},
                        {'label': ' TSI', 'value': 'TSI_13_25_13'},
                        {'label': ' ADX', 'value': 'ADX_14'},
                        {'label': ' Aroon', 'value': 'AROONOSC_14'},
                        {'label': ' Awesome Osc (AO)', 'value': 'AO_5_34'},
                        {'label': ' Accelerator Osc (AC)', 'value': 'AC_5_34'},
                        {'label': ' TRIX', 'value': 'TRIX_30_9'},
                        {'label': ' Coppock Curve', 'value': 'COPC_11_14_10'},
                        {'label': ' Fisher Transform', 'value': 'FISHERT_9_1'},
                        {'label': ' RVI (Vigor)', 'value': 'RVI_14'},
                        {'label': ' RVI (Volatility)', 'value': 'RVI_VOL'},
                        {'label': ' CMO', 'value': 'CMO_14'},
                        {'label': ' Ultimate Osc', 'value': 'UO_7_14_28'},
                        {'label': ' Vortex', 'value': 'VTXP_14'},
                    ],
                    value=current_fourth_order,
                    labelStyle={'display': 'block', 'padding': '8px', 'borderBottom': '1px solid #333', 'cursor': 'pointer'},
                    inputStyle={'marginRight': '10px', 'cursor': 'pointer'}
                )
            ], style={'textAlign': 'left', 'height': 'auto', 'maxHeight': '400px', 'overflowY': 'auto', 'border': '1px solid #333', 'borderRadius': '5px', 'padding': '5px'})
        ], style={'display': 'block', 'marginTop': '10px'}),

        # Fifth Order Microstructure & Flow
        html.Div([
            html.Label("V. FLOW DYNAMICS", className="stat-label", style={'marginBottom': '10px', 'display': 'block', 'marginTop': '15px'}),
            html.Div([
                dcc.Checklist(
                    id='fifth-order-selector',
                    options=[
                        {'label': ' VWAP', 'value': 'VWAP_D'},
                        {'label': ' OBV', 'value': 'OBV'},
                        {'label': ' MFI', 'value': 'MFI_14'},
                        {'label': ' CMF', 'value': 'CMF_20'},
                        {'label': ' A/D', 'value': 'AD'},
                        {'label': ' Chaikin Osc', 'value': 'ADOSC_3_10'},
                        {'label': ' PVT', 'value': 'PVT'},
                        {'label': ' Force Index', 'value': 'EFI_13'},
                        {'label': ' Ease of Move', 'value': 'EOM_14_100000000'},
                        {'label': ' Klinger', 'value': 'KVO_34_55_13'},
                        {'label': ' Volume Osc', 'value': 'PVO_12_26_9'},
                    ],
                    value=current_fifth_order,
                    labelStyle={'display': 'block', 'padding': '8px', 'borderBottom': '1px solid #333', 'cursor': 'pointer'},
                    inputStyle={'marginRight': '10px', 'cursor': 'pointer'}
                )
            ], style={'textAlign': 'left', 'height': 'auto', 'maxHeight': '400px', 'overflowY': 'auto', 'border': '1px solid #333', 'borderRadius': '5px', 'padding': '5px'})
        ], style={'display': 'block', 'marginTop': '10px'}),

        # Sixth Order Adaptive Systems
        html.Div([
            html.Label("VI. ADAPTIVE SYSTEMS", className="stat-label", style={'marginBottom': '10px', 'display': 'block', 'marginTop': '15px'}),
            html.Div([
                dcc.Checklist(
                    id='sixth-order-selector',
                    options=[
                        {'label': ' KAMA', 'value': 'KAMA_10_2_30'},
                        {'label': ' McGinley', 'value': 'MCGD_14'},
                        {'label': ' Parabolic SAR', 'value': 'PSARl_0.02_0.2'},
                        {'label': ' Choppiness', 'value': 'CHOP_14_1_100.0'},
                        {'label': ' Chaikin Vol', 'value': 'CHAIKIN_VOL'},
                        {'label': ' Chande Kroll', 'value': 'CKSPl_10_1_9'},
                        {'label': ' Ichimoku', 'value': 'ISA_9_26_52'},
                        {'label': ' GMMA', 'value': 'GMMA'},
                        {'label': ' Alligator', 'value': 'AG_13_8_5'},
                        {'label': ' Mass Index', 'value': 'MASSI_9_25'},
                    ],
                    value=current_sixth_order,
                    labelStyle={'display': 'block', 'padding': '8px', 'borderBottom': '1px solid #333', 'cursor': 'pointer'},
                    inputStyle={'marginRight': '10px', 'cursor': 'pointer'}
                )
            ], style={'textAlign': 'left', 'height': 'auto', 'maxHeight': '400px', 'overflowY': 'auto', 'border': '1px solid #333', 'borderRadius': '5px', 'padding': '5px'})
        ], style={'display': 'block', 'marginTop': '10px'})
    ])
        
    ], className="settings-panel left-settings", style={'padding': '15px'})


def right_panel_settings(current_tp=None, current_sl=None, current_theme='dark'):
    """
    Returns the layout for the Right Panel: Trade Config.
    """
    tp_val = current_tp if current_tp is not None else 15
    sl_val = current_sl if current_sl is not None else 15

    return html.Div([
        # Theme (Moved from Left)
        html.Div([
            html.Label("THEME", className="stat-label"),
            dcc.RadioItems(
                id='theme-selector',
                options=[
                    {'label': ' Dark', 'value': 'dark'},
                    {'label': ' Light', 'value': 'light'}
                ],
                value=current_theme,
                labelStyle={'display': 'inline-block', 'marginRight': '15px', 'color': '#ccc', 'cursor': 'pointer'},
                inputStyle={'marginRight': '5px', 'cursor': 'pointer'}
            )
        ], style={'marginBottom': '20px', 'textAlign': 'center', 'borderBottom': '1px solid #333', 'paddingBottom': '10px'}),

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
            
    ], className="settings-panel", style={'flex': '1', 'overflowY': 'auto', 'display': 'flex', 'flexDirection': 'column'})
