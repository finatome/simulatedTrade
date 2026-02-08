from dash import html
from components.indicator_cards import render_indicator_cards

def controls_layout():
    return html.Div([
        html.Div([
            html.Button("LONG / BUY", id="btn-long", className="control-btn long"),
            html.Button("SHORT / SELL", id="btn-short", className="control-btn short"),
            html.Button("EXIT NOW", id="btn-exit", className="control-btn exit"),
            html.Button("SKIP SCENARIO", id="btn-skip", className="control-btn skip"),
        ], className="controls-row"),
        html.Div(id="trade-status", className="status-text"),
        html.Div(id="indicator-cards-wrapper", children=render_indicator_cards(['SMA_20', 'SMA_50', 'BBM_20_2.0_2.0', 'SUPERT_7_3.0', 'MACD_12_26_9']))
    ], className="controls-panel")
