from dash import html

def controls_layout():
    return html.Div([
        html.Button("LONG / BUY", id="btn-long", className="control-btn long"),
        html.Button("SHORT / SELL", id="btn-short", className="control-btn short"),
        html.Button("SKIP SCENARIO", id="btn-skip", className="control-btn skip"),
        html.Hr(style={'borderColor': '#333'}),
        html.Div(id="trade-status", className="status-text")
    ], className="controls-panel")
