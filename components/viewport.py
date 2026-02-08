import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_viewport(df, show_indicators=True, trade_state=None, theme='dark', history=None):
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
            'down_candle': '#D50000',
            'vol_up': 'rgba(0, 200, 83, 0.5)',   # Transparent Green
            'vol_down': 'rgba(213, 0, 0, 0.5)'   # Transparent Red
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
            'down_candle': '#FF1744',
            'vol_up': 'rgba(0, 230, 118, 0.5)',  # Transparent Green
            'vol_down': 'rgba(255, 23, 68, 0.5)' # Transparent Red
        }

    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.08, row_heights=[0.55, 0.15, 0.3],
                        subplot_titles=("Price Action", "Volume", "Indicators"))

    # Candlestick
    fig.add_trace(go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'], name="Market",
        increasing_line_color=palette['up_candle'], decreasing_line_color=palette['down_candle']
    ), row=1, col=1)

    # Volume Chart (Row 2)
    # Determine colors based on Close >= Open
    vol_colors = [palette['vol_up'] if c >= o else palette['vol_down'] for c, o in zip(df['Close'], df['Open'])]
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
    
    # Trade Lines (Active)
    if trade_state:
        if trade_state.get('entry'):
            fig.add_hline(y=trade_state['entry'], line_dash="solid", line_color="gray", line_width=1, annotation_text="ENTRY", row=1, col=1)
        if trade_state.get('tp'):
            fig.add_hline(y=trade_state['tp'], line_dash="dash", line_color="#00E676", line_width=1.5, annotation_text="TP", row=1, col=1)
        if trade_state.get('sl'):
            fig.add_hline(y=trade_state['sl'], line_dash="dash", line_color="#FF1744", line_width=1.5, annotation_text="SL", row=1, col=1)

    # Historical Trades (Markers & Lines)
    if history:
        for trade in history:
            # Check if entry/exit times are within the current view?
            # Plotly handles out-of-view points gracefully (just doesn't show or auto-ranges if allowed).
            # We assume df index covers the trade times if we are sliding a window, 
            # OR we just add them and let Plotly decide (might mess up auto-range if very old).
            # But the user specifically wants to see them.
            
            entry_t = trade.get('entry_time')
            exit_t = trade.get('exit_time')
            entry_p = trade.get('entry_price')
            exit_p = trade.get('exit_price')
            side = trade.get('side')
            
            if entry_t is not None:
                # Vertical Line Entry
                fig.add_vline(x=entry_t, line_width=1, line_dash="dot", line_color="gray", row=1, col=1)
                
                # Entry Marker
                # Long Entry: Green Up Triangle
                # Short Entry: Red Down Triangle
                symbol = 'triangle-up' if side == 'LONG' else 'triangle-down'
                color = '#00E676' if side == 'LONG' else '#FF1744'
                
                fig.add_trace(go.Scatter(
                    x=[entry_t], y=[entry_p],
                    mode='markers',
                    marker=dict(symbol=symbol, size=12, color=color, line=dict(color='white', width=1)),
                    name=f"{side} Entry",
                    hoverinfo='text',
                    hovertext=f"{side} Entry @ {entry_p:.2f}"
                ), row=1, col=1)

            if exit_t is not None:
                # Vertical Line Exit
                fig.add_vline(x=exit_t, line_width=1, line_dash="dot", line_color="gray", row=1, col=1)
                
                # Exit Marker
                # Exit Long (Sell): Red Down Triangle? Or Green/Red based on PnL?
                # User asked for "red or green triangle at the point of trade entry and exit".
                # Standard convention:
                # Long Exit: You are Selling. Red Triangle Down.
                # Short Exit: You are Buying. Green Triangle Up.
                # BUT maybe easy distinction is:
                # Entry = Filled Triangle
                # Exit = Open Triangle? Or just simple Up/Down.
                
                # Let's use Side logic for simplicity:
                # Closing Long -> Sell -> Red Down
                # Closing Short -> Buy -> Green Up
                
                exit_symbol = 'triangle-down' if side == 'LONG' else 'triangle-up'
                exit_color = '#FF1744' if side == 'LONG' else '#00E676'
                
                fig.add_trace(go.Scatter(
                    x=[exit_t], y=[exit_p],
                    mode='markers',
                    marker=dict(symbol=exit_symbol, size=12, color=exit_color, line=dict(color='white', width=1)),
                    name=f"{side} Exit",
                    hoverinfo='text',
                    hovertext=f"{side} Exit @ {exit_p:.2f} ({trade.get('reason')})"
                ), row=1, col=1)

    # Define subplots (Oscillators) vs Overlays
    subplots_list = ['RSI_14', 'MACD_12_26_9', 'STOCHk_14_3_3', 'ADX_14', 'CCI_14_0.015', 'ROC_10', 'OBV',
                     'STDDEV_20', 'HISTVOL_20', 'VOL_CC_20', 'VOL_OHLC_20', 'VOL_ZTC_20', 'MOM_10', 'SPREAD', 'RATIO_SMA50',
                     'MA_CROSS', 'EMA_CROSS', 'PO_20_50', 'BB_PCT_B', 'BB_WIDTH', 'DPO_20', 'ATR_14', 'SLOPE_20', 'STD_ERR',
                     'STOCHRSIk_14_14_3_3', 'SMI_5_20_5_1.0', 'TSI_13_25_13', 'AROONOSC_14', 'AO_5_34', 'AC_5_34', 'TRIX_30_9',
                     'COPC_11_14_10', 'FISHERT_9_1', 'RVI_14', 'RVI_VOL', 'CMO_14', 'UO_7_14_28', 'VTXP_14',
                     'MFI_14', 'CMF_20', 'ADOSC_3_10', 'EFI_13', 'EOM_14_100000000', 'KVO_34_55_13', 'PVO_12_26_9',
                     'CHOP_14_1_100.0', 'CHAIKIN_VOL', 'MASSI_9_25']
    
    # Hardcoded color cycle for variety
    colors = ['#00E676', '#FF1744', '#2979FF', '#FFea00', '#AA00FF', '#00B8D9']
    
    # NOTE: Oscillators are now in Row 3 (was Row 2)
    # Overlays remain in Row 1
    
    color_idx = 0
    
    for ind in selected_indicators:
        
        # --- SPECIAL HANDLERS (Bands & Channels) ---
        # STANDARD ERROR BANDS
        if ind == 'SEB':
             if 'SEB_U' in df.columns and 'SEB_L' in df.columns:
                fig.add_trace(go.Scatter(x=df.index, y=df['SEB_U'], line=dict(color='gray', width=1, dash='dash'), name='SEB Upper'), row=1, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=df['SEB_L'], line=dict(color='gray', width=1, dash='dash'), fill='tonexty', fillcolor='rgba(128,128,128,0.1)', name='SEB Lower'), row=1, col=1)
             continue

        # MA CHANNEL
        if ind == 'MACH_U':
             if 'MACH_U' in df.columns and 'MACH_L' in df.columns:
                fig.add_trace(go.Scatter(x=df.index, y=df['MACH_U'], line=dict(color='cyan', width=1), name='MA Channel Upper'), row=1, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=df['MACH_L'], line=dict(color='cyan', width=1), fill='tonexty', fillcolor='rgba(0,255,255,0.05)', name='MA Channel Lower'), row=1, col=1)
             continue

        # ENVELOPES
        if ind == 'ENV_U':
             if 'ENV_U' in df.columns and 'ENV_L' in df.columns:
                fig.add_trace(go.Scatter(x=df.index, y=df['ENV_U'], line=dict(color='orange', width=1), name='Envelope Upper'), row=1, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=df['ENV_L'], line=dict(color='orange', width=1), fill='tonexty', fillcolor='rgba(255,165,0,0.05)', name='Envelope Lower'), row=1, col=1)
             continue

        # KELTNER CHANNELS
        if 'KC' in ind: 
             # Plot KC_..._U, KC_..._L
             kc_cols = [c for c in df.columns if c.startswith('KC') and ('_U' in c or '_L' in c)]
             for c in kc_cols:
                 fig.add_trace(go.Scatter(x=df.index, y=df[c], mode='lines', line=dict(width=1, dash='dot'), name=c), row=1, col=1)
             if not kc_cols and ind in df.columns: # Fallback if just one column
                 fig.add_trace(go.Scatter(x=df.index, y=df[ind], mode='lines', line=dict(width=1), name=ind), row=1, col=1)
             if kc_cols: continue

        # DONCHIAN CHANNELS
        if 'DCL' in ind:
             # Look for DCU and DCL
             dcols = [c for c in df.columns if ('DCU' in c or 'DCL' in c) and c.split('_')[1:] == ind.split('_')[1:]]
             for c in dcols:
                 fig.add_trace(go.Scatter(x=df.index, y=df[c], mode='lines', line=dict(width=1, dash='dot'), name=c), row=1, col=1)
             if dcols: continue

        # GMMA (Guppy)
        if ind == 'GMMA':
             # Plot 12 EMAs
             short_periods = [3, 5, 8, 10, 12, 15]
             long_periods = [30, 35, 40, 45, 50, 60]
             for p in short_periods:
                 col = f"EMA_{p}"
                 if col in df.columns:
                     fig.add_trace(go.Scatter(x=df.index, y=df[col], line=dict(color='blue', width=1), opacity=0.5, name=col), row=1, col=1)
             for p in long_periods:
                 col = f"EMA_{p}"
                 if col in df.columns:
                     fig.add_trace(go.Scatter(x=df.index, y=df[col], line=dict(color='red', width=1), opacity=0.5, name=col), row=1, col=1)
             continue

        # ICHIMOKU
        if 'ISA_' in ind:
             # Find actual column names
             isa_col = next((c for c in df.columns if c.startswith('ISA_')), None)
             isb_col = next((c for c in df.columns if c.startswith('ISB_')), None)
             its_col = next((c for c in df.columns if c.startswith('ITS_')), None)
             iks_col = next((c for c in df.columns if c.startswith('IKS_')), None)
             ics_col = next((c for c in df.columns if c.startswith('ICS_')), None)
             
             if isa_col and isb_col:
                 # Cloud
                 fig.add_trace(go.Scatter(x=df.index, y=df[isa_col], line=dict(color='green', width=0), showlegend=False, hoverinfo='skip'), row=1, col=1)
                 fig.add_trace(go.Scatter(x=df.index, y=df[isb_col], line=dict(color='red', width=0), fill='tonexty', fillcolor='rgba(0, 255, 0, 0.1)', name='Ichimoku Cloud'), row=1, col=1)
                 
             if its_col: fig.add_trace(go.Scatter(x=df.index, y=df[its_col], line=dict(color='blue', width=1), name='Tenkan'), row=1, col=1)
             if iks_col: fig.add_trace(go.Scatter(x=df.index, y=df[iks_col], line=dict(color='red', width=1), name='Kijun'), row=1, col=1)
             if ics_col: fig.add_trace(go.Scatter(x=df.index, y=df[ics_col], line=dict(color='green', width=1, dash='dot'), name='Chikou'), row=1, col=1)
             continue

        # ALLIGATOR
        if 'AG_' in ind:
            # Look for AGj (Jaw), AGt (Teeth), AGl (Lips)
            jaw_col = next((c for c in df.columns if c.startswith('AGj_')), None)
            teeth_col = next((c for c in df.columns if c.startswith('AGt_')), None)
            lips_col = next((c for c in df.columns if c.startswith('AGl_')), None)
            
            if jaw_col: fig.add_trace(go.Scatter(x=df.index, y=df[jaw_col], line=dict(color='blue', width=1), name='Jaw'), row=1, col=1)
            if teeth_col: fig.add_trace(go.Scatter(x=df.index, y=df[teeth_col], line=dict(color='red', width=1), name='Teeth'), row=1, col=1)
            if lips_col: fig.add_trace(go.Scatter(x=df.index, y=df[lips_col], line=dict(color='green', width=1), name='Lips'), row=1, col=1)
            continue


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
            else:
                # If we really can't find it, skip
                print(f"WARNING: Indicator {ind} not found in columns. Skipping.")
                continue


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
            
        # NET VOLUME (Bar Chart on Row 3)
        if ind == 'NETVOL':
            # Color by sign
            nv_colors = [palette['vol_up'] if v >= 0 else palette['vol_down'] for v in df[ind]]
            fig.add_trace(go.Bar(
                x=df.index, y=df[ind],
                marker_color=nv_colors,
                name="Net Volume"
            ), row=3, col=1)
            continue

        # WILLIAMS FRACTAL (Markers on Row 1)
        if 'FRACTALS' in ind:
            # We assume df has random fractal columns. 
            # pandas_ta fractals typically adds 'FRACTAL_H_5', 'FRACTAL_L_5' etc.
            # We look for columns starting with FRACTAL
            fractal_cols = [c for c in df.columns if 'FRACTAL' in c]
            
            for fcol in fractal_cols:
                # Filter out NaNs to plot markers only where they exist
                # High Fract (Upper markers)
                if 'H' in fcol or 'Bull' in fcol or 'Up' in fcol: # Heuristic naming check
                    # Actually standard pandas_ta is `FRACTALS_5_H` or similar
                    # Let's plot ANY fractal column found.
                    # If it's effectively a High fractal, it will be near Highs.
                    
                    # Create series with only non-NaN values
                    f_series = df[fcol].dropna()
                    if not f_series.empty:
                        # Determine if it is high or low based on value relative to Close?
                        # Or just plot generic markers.
                        # Let's use Triangle Up for Highs, Triangle Down for Lows if we can distinguish.
                        
                        symbol = 'triangle-up' if ('_L' in fcol) else 'triangle-down' # Inverted logic? Low fractal marks a low (support) -> Up Arrow? High fractal marks high (resistance) -> Down arrow?
                        # Usually High Fractal is above candle (Down Arrow pointing to it)
                        # Low Fractal is below candle (Up Arrow pointing to it)
                        
                        # pandas_ta: FRACTALS_5_L, FRACTALS_5_H
                        if '_L' in fcol: 
                            symbol = 'triangle-up'
                            color = '#00E676'
                            offset = -5 # shift annotation? No, just plot at value.
                            # Value is likely NaN where no fractal. 
                        else:
                            symbol = 'triangle-down'
                            color = '#FF1744'
                        
                        fig.add_trace(go.Scatter(
                            x=f_series.index, y=f_series,
                            mode='markers',
                            marker=dict(symbol=symbol, size=10, color=color),
                            name="Fractal"
                        ), row=1, col=1)
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
    
    # Update subplot titles to look like "strips"
    fig.update_annotations(
        font=dict(size=12, color=palette['text']),
        bgcolor="#1e2329" if theme == 'dark' else "#e0e4e8",
        bordercolor="#333" if theme == 'dark' else "#ccc",
        borderwidth=1,
        borderpad=4,
        width=400, # Fixed width to make it look like a strip/badge
    )
    
    # Update axes to match terminal feel (or light theme feel)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=palette['grid'])
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=palette['grid'])
    
    return fig
