import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_viewport(df, show_indicators=True, trade_state=None):
    # trade_state: dict with keys 'entry', 'tp', 'sl'
    
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.03, row_heights=[0.7, 0.3])

    # Candlestick
    fig.add_trace(go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'], name="Market"
    ), row=1, col=1)

    # Selected Indicators Plotting
    # Lists of indicators that go on the main chart (Overlays)
    # Check pandas_ta names or our internal mapping. 
    # Actually, pandas_ta appends columns like 'SMA_20', 'BBM_20_2.0', etc.
    # The value passed from dropdown matches the column name.
    
    selected_indicators = show_indicators if isinstance(show_indicators, list) else []
    
    # Trade Lines (Re-inserted)
    if trade_state:
        if trade_state.get('entry'):
            fig.add_hline(y=trade_state['entry'], line_dash="solid", line_color="gray", line_width=1, annotation_text="ENTRY", row=1, col=1)
        if trade_state.get('tp'):
            fig.add_hline(y=trade_state['tp'], line_dash="dash", line_color="#00E676", line_width=1.5, annotation_text="TP", row=1, col=1)
        if trade_state.get('sl'):
            fig.add_hline(y=trade_state['sl'], line_dash="dash", line_color="#FF1744", line_width=1.5, annotation_text="SL", row=1, col=1)

    
    # Define subplots (Oscillators) vs Overlays
    subplots_list = ['RSI_14', 'MACD_12_26_9', 'STOCHk_14_3_3', 'ADX_14', 'CCI_14_0.015', 'ROC_10', 'OBV']
    
    # Hardcoded color cycle for variety
    colors = ['#00E676', '#FF1744', '#2979FF', '#FFea00', '#AA00FF', '#00B8D9']
    
    color_idx = 0
    
    for ind in selected_indicators:
        if ind not in df.columns:
            # Maybe it's a multi-column indicator?
            # e.g., BBands produces BBL, BBM, BBU.
            # Handle specific cases
            if 'BBM' in ind: # Bollinger Bands
                # Draw Upper and Lower
                upper = ind.replace('BBM', 'BBU')
                lower = ind.replace('BBM', 'BBL')
                if upper in df.columns and lower in df.columns:
                    fig.add_trace(go.Scatter(x=df.index, y=df[upper], line=dict(color='rgba(255, 255, 255, 0.3)', width=1), name="BB Upper"), row=1, col=1)
                    fig.add_trace(go.Scatter(x=df.index, y=df[lower], line=dict(color='rgba(255, 255, 255, 0.3)', width=1), name="BB Lower"), row=1, col=1)
            
            if 'MACD' in ind: # MACD
                # Draw MACD and Signal
                macd = df['MACD_12_26_9']
                signal = df['MACDs_12_26_9']
                hist = df['MACDh_12_26_9']
                fig.add_trace(go.Scatter(x=df.index, y=macd, line=dict(color='#2979FF', width=1.5), name="MACD"), row=2, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=signal, line=dict(color='#FF1744', width=1.5), name="Signal"), row=2, col=1)
                fig.add_bar(x=df.index, y=hist, name="Hist", row=2, col=1)
                continue

            if 'STOCH' in ind:
                k = df['STOCHk_14_3_3']
                d = df['STOCHd_14_3_3']
                fig.add_trace(go.Scatter(x=df.index, y=k, line=dict(color='#2979FF', width=1.5), name="Stoch %K"), row=2, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=d, line=dict(color='#FF1744', width=1.5), name="Stoch %D"), row=2, col=1)
                fig.add_hline(y=80, line_dash="dot", line_color="gray", row=2, col=1)
                fig.add_hline(y=20, line_dash="dot", line_color="gray", row=2, col=1)
                continue
                
            continue

        # Color assignment
        c = colors[color_idx % len(colors)]
        color_idx += 1
        
        if ind in subplots_list or (ind == 'OBV'):
            # Plot on Row 2
            fig.add_trace(go.Scatter(x=df.index, y=df[ind], line=dict(color=c, width=1.5), name=ind), row=2, col=1)
            # Add reference lines for Oscillators
            if 'RSI' in ind:
                fig.add_hline(y=70, line_dash="dot", line_color="gray", row=2, col=1)
                fig.add_hline(y=30, line_dash="dot", line_color="gray", row=2, col=1)
        else:
            # Overlays on Row 1
            fig.add_trace(go.Scatter(x=df.index, y=df[ind], line=dict(color=c, width=1.5), name=ind), row=1, col=1)

    fig.update_layout(
        template='plotly_dark',
        xaxis_rangeslider_visible=False,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='#0b0e11',
        paper_bgcolor='#0b0e11',
        font=dict(color='#e0e0e0')
    )
    
    # Update axes to match terminal feel
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#333333')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#333333')
    
    return fig
