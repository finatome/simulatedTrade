import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_viewport(df, show_indicators=True, trade_state=None, theme='dark'):
    # trade_state: dict with keys 'entry', 'tp', 'sl'
    
    # Theme Configuration
    if theme == 'light':
        palette = {
            'bg': '#F0F4F8',       # Bluish White
            'paper': '#F0F4F8',
            'grid': '#E4E7EB',     # Light Grey
            'text': '#0b0e11',     # Dark Text
            'st_base': 'black',    # Supertrend Base
            'template': 'plotly_white',
            'up_candle': '#00C853',
            'down_candle': '#D50000'
        }
    else: # Default to Dark
        palette = {
            'bg': '#0b0e11',       # Bloomberg Black
            'paper': '#0b0e11',
            'grid': '#333333',     # Dark Grey
            'text': '#e0e0e0',     # Light Text
            'st_base': 'white',    # Supertrend Base
            'template': 'plotly_dark',
            'up_candle': '#00E676',
            'down_candle': '#FF1744'
        }

    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.03, row_heights=[0.6, 0.15, 0.25])

    # Candlestick
    fig.add_trace(go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'], name="Market",
        increasing_line_color=palette['up_candle'], decreasing_line_color=palette['down_candle']
    ), row=1, col=1)

    # Volume Chart (Row 2)
    # Determine colors based on Close >= Open
    vol_colors = [palette['up_candle'] if c >= o else palette['down_candle'] for c, o in zip(df['Close'], df['Open'])]
    fig.add_trace(go.Bar(
        x=df.index, y=df['Volume'],
        marker_color=vol_colors,
        name="Volume",
        marker_line_width=0
    ), row=2, col=1)

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
    
    # NOTE: Oscillators are now in Row 3 (was Row 2)
    # Overlays remain in Row 1
    
    color_idx = 0
    
    for ind in selected_indicators:

        # --- SPECIAL INDICATOR HANDLERS ---
        
        # MACD (Line, Signal, Histogram)
        if 'MACD' in ind: 
            # We assume df has MACD_..., MACDs_..., MACDh_...
            # The dropdown value matches the main MACD column.
            # We can find the others by prefix matching or assumption.
            # Step 450 showed columns: MACD_12_26_9, MACDh_12_26_9, MACDs_12_26_9
            
            # Construct names based on standard suffix if needed, 
            # or just rely on the columns existing.
            # Since ind IS 'MACD_12_26_9', we can guess others.
            
            macd_col = ind
            signal_col = ind.replace('MACD_', 'MACDs_')
            hist_col = ind.replace('MACD_', 'MACDh_')
            
            # Verify they exist (or try to find them if naming is different)
            if macd_col in df.columns and signal_col in df.columns and hist_col in df.columns:
                macd = df[macd_col]
                signal = df[signal_col]
                hist = df[hist_col]
                
                # Dynamic Histogram Colors
                hist_colors = ['#00E676' if v >= 0 else '#FF1744' for v in hist]
                
                fig.add_trace(go.Bar(
                    x=df.index, y=hist,
                    marker_color=hist_colors,
                    opacity=0.4,
                    name="MACD Hist"
                ), row=3, col=1)
                
                fig.add_trace(go.Scatter(
                    x=df.index, y=macd, 
                    line=dict(color='#2979FF', width=2), 
                    name="MACD Line"
                ), row=3, col=1)
                
                fig.add_trace(go.Scatter(
                    x=df.index, y=signal, 
                    line=dict(color='#FF9100', width=2), 
                    name="Signal Line"
                ), row=3, col=1)
                
                # Add Zero Line
                fig.add_hline(y=0, line_color="gray", line_width=1, line_dash="solid", row=3, col=1)
            continue

        # Stochastic (K, D)
        if 'STOCH' in ind:
            # ind is typically STOCHk_...
            if 'STOCHk' in ind:
                k_col = ind
                d_col = ind.replace('STOCHk', 'STOCHd')
            else:
                # If they selected STOCHd? unlikely given settings.
                k_col = ind.replace('STOCHd', 'STOCHk')
                d_col = ind
            
            if k_col in df.columns and d_col in df.columns:
                k = df[k_col]
                d = df[d_col]
                fig.add_trace(go.Scatter(x=df.index, y=k, line=dict(color='#2979FF', width=1.5), name="Stoch %K"), row=3, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=d, line=dict(color='#FF1744', width=1.5), name="Stoch %D"), row=3, col=1)
                fig.add_hline(y=80, line_dash="dot", line_color="gray", row=3, col=1)
                fig.add_hline(y=20, line_dash="dot", line_color="gray", row=3, col=1)
            continue

        if ind not in df.columns:
            # Handle multi-column indicators that might NOT be in columns by their exact name
            # e.g. Bollinger Bands if ind was 'Bollinger Bands' (but it is BBM_...)
            
            # Bollinger Bands (handled below explicitly now, so this might be redundant but safe)
            if 'BBM' in ind: 
                # This block was moving, so I'll leave the logic to the main BB handler below 
                # or just let it pass through to the BB handler.
                pass 
                
            # If we really can't find it, skip
            pass


        # Indicator IS in columns (or we corrected the name mapping)
        
        # SUPERTREND Handling
        if 'SUPERT' in ind and 'SUPERTd' in ind.replace('SUPERT', 'SUPERTd'): # Check if direction column exists
            # ind is e.g. 'SUPERT_7_3.0'
            dir_col = ind.replace('SUPERT_', 'SUPERTd_') # e.g. SUPERTd_7_3.0
            if dir_col in df.columns:
                # Plot separate traces for Up (Green) and Down (Red)
                # Create masks
                up_mask = df[dir_col] > 0
                down_mask = df[dir_col] < 0
                
                # 1. Plot the connectors (Thin White Line or Black for Light Mode)
                # We plot the entire line first. The colored segments will cover it, 
                # but the gaps (jumps) will remain visible as the base color.
                fig.add_trace(go.Scatter(
                    x=df.index, y=df[ind],
                    mode='lines',
                    line=dict(color=palette['st_base'], width=1),
                    showlegend=False,
                    hoverinfo='skip',
                    name="Supertrend Base"
                ), row=1, col=1)
                
                # Up Trend (Green)
                # To prevent Plotly from connecting separate green segments across a red gap,
                # we must provide the FULL index but set Y-values to None (or NaN) where it's not green.
                # Plotly breaks lines at None/NaN.
                
                up_series = df[ind].copy()
                up_series[~up_mask] = None
                
                fig.add_trace(go.Scatter(
                    x=df.index, y=up_series, 
                    mode='lines',
                    line=dict(color='#00E676', width=3), 
                    name="Supertrend Up"
                ), row=1, col=1)
                
                # Down Trend (Red)
                down_series = df[ind].copy()
                down_series[~down_mask] = None
                
                fig.add_trace(go.Scatter(
                    x=df.index, y=down_series, 
                    mode='lines',
                    line=dict(color='#FF1744', width=3), 
                    name="Supertrend Down"
                ), row=1, col=1)
                continue

        # Bollinger Bands Handling (if ind IS in columns, which it is now)
        if 'BBM' in ind:
             # Draw Upper and Lower bounds
            upper = ind.replace('BBM', 'BBU')
            lower = ind.replace('BBM', 'BBL')
            
            if upper in df.columns and lower in df.columns:
                # Lower (invisible for fill)
                fig.add_trace(go.Scatter(
                    x=df.index, y=df[lower], 
                    line=dict(width=0), 
                    showlegend=False,
                    hoverinfo='skip',
                    mode='lines'
                ), row=1, col=1)
                
                # Upper (fill, colored)
                fig.add_trace(go.Scatter(
                    x=df.index, y=df[upper], 
                    fill='tonexty', 
                    fillcolor='rgba(0, 184, 217, 0.15)',
                    line=dict(color='rgba(0, 184, 217, 0.3)', width=1), 
                    name="Bollinger Bands"
                ), row=1, col=1)
                 # Lower (visible line)
                fig.add_trace(go.Scatter(
                    x=df.index, y=df[lower], 
                    line=dict(color='rgba(0, 184, 217, 0.3)', width=1), 
                    showlegend=False,
                    mode='lines'
                ), row=1, col=1)
            
            # Draw the Middle Band (the indicator itself)
            fig.add_trace(go.Scatter(x=df.index, y=df[ind], line=dict(color='#00B8D9', width=1, dash='dash'), name="BB Mid"), row=1, col=1)
            continue
            
        # Standard Plotting for others
        c = colors[color_idx % len(colors)]
        color_idx += 1
        
        if ind in subplots_list or (ind == 'OBV'):
            # Plot on Row 3 (Oscillators)
            fig.add_trace(go.Scatter(x=df.index, y=df[ind], line=dict(color=c, width=1.5), name=ind), row=3, col=1)
            # Add reference lines for Oscillators
            if 'RSI' in ind:
                fig.add_hline(y=70, line_dash="dot", line_color="gray", row=3, col=1)
                fig.add_hline(y=30, line_dash="dot", line_color="gray", row=3, col=1)
        else:
            # Overlays on Row 1
            fig.add_trace(go.Scatter(x=df.index, y=df[ind], line=dict(color=c, width=1.5), name=ind), row=1, col=1)

    fig.update_layout(
        template=palette['template'],
        xaxis_rangeslider_visible=False,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color=palette['text'])),
        plot_bgcolor=palette['bg'],
        paper_bgcolor=palette['paper'],
        font=dict(color=palette['text'])
    )
    
    # Update axes to match terminal feel (or light theme feel)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=palette['grid'])
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=palette['grid'])
    
    return fig
