from dash import html

def scoreboard_layout(metrics, balance, live_data=None):
    # live_data: dict with 'entry', 'tp', 'sl', 'unrealized_pnl'
    
    # Active Trade Section
    active_trade_div = html.Div()
    if live_data and live_data.get('active'):
        pnl = live_data.get('unrealized_pnl', 0)
        pnl_color = "#00E676" if pnl >= 0 else "#FF1744"
        
        active_trade_div = html.Div([
            html.P("ACTIVE TRADE", className="panel-title", style={'marginTop': '20px', 'color': '#fff'}),
            html.Div([
                html.Div([
                    html.P("Entry", className="stat-label"),
                    html.H4(f"${live_data['entry']:.2f}", className="stat-value"),
                ], className="stat-mini"),
                html.Div([
                    html.P("Unrealized PnL", className="stat-label"),
                    html.H4(f"${pnl:.2f}", className="stat-value", style={'color': pnl_color}),
                ], className="stat-mini"),
            ], className="stat-grid"),
            html.Div([
                html.Div([
                    html.P("Target (TP)", className="stat-label"),
                    html.H4(f"${live_data['tp']:.2f}", className="stat-value"),
                ], className="stat-mini"),
                html.Div([
                    html.P("Stop (SL)", className="stat-label"),
                    html.H4(f"${live_data['sl']:.2f}", className="stat-value"),
                ], className="stat-mini"),
            ], className="stat-grid"),
        ])

    return html.Div([
        html.H3("TRADER PERFORMANCE", className="panel-title"),
        html.Div([
            html.P("Account Equity", className="stat-label"),
            html.H2(f"${balance:,.2f}", id="display-equity", className="stat-value-large"),
        ], className="stat-card primary"),
        
        html.Div([
            html.Div([
                html.P("Win Rate", className="stat-label"),
                html.H4(f"{metrics['win_rate']}%", className="stat-value")
            ], className="stat-mini"),
            html.Div([
                html.P("Profit Factor", className="stat-label"),
                html.H4(f"{metrics['profit_factor']}", className="stat-value")
            ], className="stat-mini"),
        ], className="stat-grid"),
        
        html.Div([
            html.Div([
                html.P("Total PnL", className="stat-label"),
                html.H4(f"${metrics['total_pnl']:,.2f}", className="stat-value")
            ], className="stat-mini"),
            html.Div([
                html.P("Trades", className="stat-label"),
                html.H4(f"{metrics['trade_count']}/100", className="stat-value")
            ], className="stat-mini"),
        ], className="stat-grid"),

        # Win/Loss Visualization
        html.Div([
            html.P("Win / Loss Ratio", className="stat-label", style={'marginBottom': '5px'}),
            
            # Bar Container
            html.Div([
                # Win Bar
                html.Div(style={
                    'width': f"{metrics['win_rate']}%", 
                    'height': '10px', 
                    'backgroundColor': '#00E676', 
                    'display': 'inline-block'
                }),
                # Loss Bar
                html.Div(style={
                    'width': f"{100 - float(metrics['win_rate'])}%", 
                    'height': '10px', 
                    'backgroundColor': '#FF1744', 
                    'display': 'inline-block'
                }),
            ], style={'width': '100%', 'height': '10px', 'backgroundColor': '#333', 'borderRadius': '5px', 'overflow': 'hidden', 'marginBottom': '5px'}),
            
            # Text Labels
            html.Div([
                html.Span(f"{int(metrics['trade_count'] * float(metrics['win_rate']) / 100)} Wins", style={'color': '#00E676', 'fontSize': '12px'}),
                html.Span(f"{int(metrics['trade_count'] * (100 - float(metrics['win_rate'])) / 100)} Losses", style={'color': '#FF1744', 'fontSize': '12px', 'float': 'right'})
            ])
        ], style={'marginTop': '15px', 'padding': '10px', 'backgroundColor': 'rgba(255,255,255,0.05)', 'borderRadius': '5px'}),
        
        active_trade_div,
        
        html.Div([
            html.P("Scenario Progress (100 Max)", className="stat-label"),
            html.Progress(value=str(metrics['trade_count']), max="100", style={'width': '100%', 'height': '20px', 'accentColor': '#00B8D9'})
        ], style={'marginTop': '20px'})
    ], className="scoreboard-panel")
