
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Ensure plots directory exists
plots_dir = "docs/indicators/plots"
if not os.path.exists(plots_dir):
    os.makedirs(plots_dir)

def download_data():
    print("Downloading SPY data...")
    df = yf.download("SPY", period="2y", interval="1d")
    try:
        df.columns = df.columns.droplevel('Ticker')
    except:
        pass
    return df

def save_plot(fig, filename):
    filepath = os.path.join(plots_dir, filename)
    try:
        fig.write_image(filepath, width=1000, height=800, scale=2)
        print(f"Saved {filepath}")
    except Exception as e:
        print(f"Error saving {filename}: {e}")

def create_chart(df, title, filename, overlay_traces=[], oscillator_traces=[], oscillator_hlines=[]):
    """
    Creates a standardized chart with:
    Row 1: OHLC + Overlays
    Row 2: Volume (Green/Red)
    Row 3 (Optional): Oscillators
    """
    has_oscillator = len(oscillator_traces) > 0
    
    if has_oscillator:
        rows = 3
        row_heights = [0.5, 0.2, 0.3]
    else:
        rows = 2
        row_heights = [0.7, 0.3]
        
    fig = make_subplots(rows=rows, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=row_heights)
    
    # Row 1: OHLC
    fig.add_trace(go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], 
        name='OHLC'
    ), row=1, col=1)
    
    # Row 1: Overlays
    for trace in overlay_traces:
        fig.add_trace(trace, row=1, col=1)
        
    # Row 2: Volume
    # Determine colors
    colors = ['green' if row['Close'] >= row['Open'] else 'red' for i, row in df.iterrows()]
    fig.add_trace(go.Bar(
        x=df.index, y=df['Volume'], 
        name='Volume', 
        marker_color=colors
    ), row=2, col=1)
    
    # Row 3: Oscillators
    if has_oscillator:
        for trace in oscillator_traces:
            fig.add_trace(trace, row=3, col=1)
        
        # Horizontal lines for oscillator
        for y_val, color, dash in oscillator_hlines:
             fig.add_hline(y=y_val, line_dash=dash, line_color=color, row=3, col=1)
            
    fig.update_layout(title=title, template='plotly_dark', showlegend=True)
    fig.update_xaxes(rangeslider_visible=False)
    save_plot(fig, filename)

def generate_plots(df):
    
    # --- Part 1: Basic & Overlap ---
    try:
        df.ta.sma(length=20, append=True)
        view_df = df.tail(150)
        overlay = [go.Scatter(x=view_df.index, y=view_df['SMA_20'], mode='lines', name='SMA 20', line=dict(color='blue'))]
        create_chart(view_df, 'Simple Moving Average (SMA)', "SMA.png", overlay_traces=overlay)
    except Exception as e: print(f"SMA: {e}")

    try:
        df.ta.ema(length=20, append=True)
        view_df = df.tail(150)
        overlay = [go.Scatter(x=view_df.index, y=view_df['EMA_20'], mode='lines', name='EMA 20', line=dict(color='orange'))]
        create_chart(view_df, 'Exponential Moving Average (EMA)', "EMA.png", overlay_traces=overlay)
    except Exception as e: print(f"EMA: {e}")

    try:
        df.ta.wma(length=20, append=True)
        view_df = df.tail(150)
        overlay = [go.Scatter(x=view_df.index, y=view_df['WMA_20'], mode='lines', name='WMA 20', line=dict(color='cyan'))]
        create_chart(view_df, 'Weighted Moving Average (WMA)', "WMA.png", overlay_traces=overlay)
    except Exception as e: print(f"WMA: {e}")
    
    try:
        df.ta.hma(length=20, append=True)
        view_df = df.tail(150)
        overlay = [go.Scatter(x=view_df.index, y=view_df['HMA_20'], mode='lines', name='HMA 20', line=dict(color='purple'))]
        create_chart(view_df, 'Hull Moving Average (HMA)', "HMA.png", overlay_traces=overlay)
    except Exception as e: print(f"HMA: {e}")

    try:
        if 'VWAP_D' not in df.columns:
             tp = (df['High'] + df['Low'] + df['Close']) / 3
             df['VWAP_D'] = (tp * df['Volume']).cumsum() / df['Volume'].cumsum()
        view_df = df.tail(150)
        overlay = [go.Scatter(x=view_df.index, y=view_df['VWAP_D'], mode='lines', name='VWAP', line=dict(color='gold'))]
        create_chart(view_df, 'Volume Weighted Average Price (VWAP)', "VWAP.png", overlay_traces=overlay)
    except Exception as e: print(f"VWAP: {e}")
    
    try:
        st = df.ta.supertrend(length=7, multiplier=3)
        # SUPERTl_7_3.0 (Long/Green), SUPERTs_7_3.0 (Short/Red)
        l_col = next((c for c in st.columns if c.startswith('SUPERTl')), None)
        s_col = next((c for c in st.columns if c.startswith('SUPERTs')), None)
        
        if l_col and s_col:
            view_df = df.tail(150)
            overlay = [
                go.Scatter(x=view_df.index, y=st[l_col].tail(150), mode='lines', name='SuperTrend Up', line=dict(color='green')),
                go.Scatter(x=view_df.index, y=st[s_col].tail(150), mode='lines', name='SuperTrend Down', line=dict(color='red'))
            ]
            create_chart(view_df, 'SuperTrend', "SuperTrend.png", overlay_traces=overlay)
    except Exception as e: print(f"SuperTrend: {e}")
        
    try:
        psar = df.ta.psar()
        psar_comb = psar[psar.columns[0]].combine_first(psar[psar.columns[1]])
        view_df = df.tail(150)
        overlay = [go.Scatter(x=view_df.index, y=psar_comb.tail(150), mode='markers', name='PSAR', marker=dict(color='white', size=4))]
        create_chart(view_df, 'Parabolic SAR', "Parabolic_SAR.png", overlay_traces=overlay)
    except Exception as e: print(f"PSAR: {e}")
    
    try:
        ichi, _ = df.ta.ichimoku()
        isa_col = next((c for c in ichi.columns if c.startswith('ISA')), None)
        isb_col = next((c for c in ichi.columns if c.startswith('ISB')), None)
        if isa_col and isb_col:
            view_df = df.tail(150)
            overlay = [
                go.Scatter(x=view_df.index, y=ichi[isa_col].tail(150), line=dict(width=0), showlegend=False),
                go.Scatter(x=view_df.index, y=ichi[isb_col].tail(150), fill='tonexty', fillcolor='rgba(0, 250, 0, 0.2)', line=dict(width=0), name='Cloud')
            ]
            create_chart(view_df, 'Ichimoku Cloud', "Ichimoku_Cloud.png", overlay_traces=overlay)
    except Exception as e: print(f"Ichimoku: {e}")
    
    try:
        df['SMMA_20'] = df.ta.rma(length=20)
        view_df = df.tail(150)
        overlay = [go.Scatter(x=view_df.index, y=view_df['SMMA_20'], mode='lines', name='SMMA 20', line=dict(color='magenta'))]
        create_chart(view_df, 'Smoothed Moving Average (SMMA)', "SMMA.png", overlay_traces=overlay)
    except Exception as e: print(f"SMMA: {e}")
    
    try:
        df.ta.kama(length=10, append=True)
        kama_col = next((c for c in df.columns if c.startswith('KAMA')), None)
        if kama_col:
            view_df = df.tail(150)
            overlay = [go.Scatter(x=view_df.index, y=df[kama_col].tail(150), mode='lines', name='KAMA', line=dict(color='yellow'))]
            create_chart(view_df, 'Kaufman Adaptive MA (KAMA)', "KAMA.png", overlay_traces=overlay)
    except Exception as e: print(f"KAMA: {e}")
    
    # --- Channels (Overlay) ---
    try:
        bb = df.ta.bbands()
        view_df = df.tail(150)
        overlay = [
            go.Scatter(x=view_df.index, y=bb[bb.columns[2]].tail(150), line=dict(color='gray'), name='Upper'),
            go.Scatter(x=view_df.index, y=bb[bb.columns[0]].tail(150), fill='tonexty', fillcolor='rgba(128,128,128,0.2)', line=dict(color='gray'), name='Lower'),
            go.Scatter(x=view_df.index, y=bb[bb.columns[1]].tail(150), line=dict(color='orange'), name='Middle')
        ]
        create_chart(view_df, 'Bollinger Bands', "Bollinger_Bands.png", overlay_traces=overlay)
    except Exception as e: print(f"BBands: {e}")

    try:
        kc = df.ta.kc()
        view_df = df.tail(150)
        overlay = [
            go.Scatter(x=view_df.index, y=kc[kc.columns[2]].tail(150), line=dict(color='cyan'), name='Upper'),
            go.Scatter(x=view_df.index, y=kc[kc.columns[0]].tail(150), fill='tonexty', fillcolor='rgba(0,255,255,0.1)', line=dict(color='cyan'), name='Lower'),
            go.Scatter(x=view_df.index, y=kc[kc.columns[1]].tail(150), line=dict(color='blue'), name='EMA 20')
        ]
        create_chart(view_df, 'Keltner Channels', "Keltner_Channels.png", overlay_traces=overlay)
    except Exception as e: print(f"KC: {e}")
    
    try:
        dc = df.ta.donchian()
        view_df = df.tail(150)
        overlay = [
            go.Scatter(x=view_df.index, y=dc[dc.columns[2]].tail(150), line=dict(color='green'), name='Upper'),
            go.Scatter(x=view_df.index, y=dc[dc.columns[0]].tail(150), fill='tonexty', fillcolor='rgba(0,255,0,0.1)', line=dict(color='red'), name='Lower'),
            go.Scatter(x=view_df.index, y=dc[dc.columns[1]].tail(150), line=dict(color='gray', dash='dot'), name='Middle')
        ]
        create_chart(view_df, 'Donchian Channels', "Donchian_Channels.png", overlay_traces=overlay)
    except Exception as e: print(f"Donchian: {e}")

    # --- Oscillators (3 Rows) ---
    try:
        df.ta.rsi(length=14, append=True)
        view_df = df.tail(150)
        hlines = [(70, 'red', 'dash'), (30, 'green', 'dash')]
        create_chart(view_df, 'Relative Strength Index (RSI)', "RSI.png", oscillator_traces=[go.Scatter(x=view_df.index, y=view_df['RSI_14'], mode='lines', name='RSI', line=dict(color='purple'))], oscillator_hlines=hlines)
    except Exception as e: print(f"RSI: {e}")
    
    try:
        macd = df.ta.macd()
        macd_line = next((c for c in macd.columns if c.startswith('MACD_')), None)
        signal_line = next((c for c in macd.columns if c.startswith('MACDs_')), None)
        hist_line = next((c for c in macd.columns if c.startswith('MACDh_')), None)
        if macd_line:
            view_df = df.tail(150)
            m_view = macd.tail(150)
            osc_traces = [
                go.Scatter(x=view_df.index, y=m_view[macd_line], name='MACD Line', line=dict(color='blue')),
                go.Scatter(x=view_df.index, y=m_view[signal_line], name='Signal Line', line=dict(color='orange')),
                go.Bar(x=view_df.index, y=m_view[hist_line], name='Hist', marker_color=['green' if v>=0 else 'red' for v in m_view[hist_line]])
            ]
            create_chart(view_df, 'MACD', "MACD.png", oscillator_traces=osc_traces)
    except Exception as e: print(f"MACD: {e}")
    
    try:
        stoch = df.ta.stoch()
        k_line = next((c for c in stoch.columns if c.startswith('STOCHk')), None)
        d_line = next((c for c in stoch.columns if c.startswith('STOCHd')), None)
        if k_line:
            view_df = df.tail(150)
            osc_traces = [
                go.Scatter(x=view_df.index, y=stoch[k_line].tail(150), name='%K', line=dict(color='blue')),
                go.Scatter(x=view_df.index, y=stoch[d_line].tail(150), name='%D', line=dict(color='orange', dash='dot'))
            ]
            hlines = [(80, 'red', 'dash'), (20, 'green', 'dash')]
            create_chart(view_df, 'Stochastic Oscillator', "Stochastic.png", oscillator_traces=osc_traces, oscillator_hlines=hlines)
    except Exception as e: print(f"Stochastic: {e}")
    
    try:
        adx = df.ta.adx()
        adx_col = next((c for c in adx.columns if c.startswith('ADX')), None)
        dmp_col = next((c for c in adx.columns if c.startswith('DMP')), None)
        dmn_col = next((c for c in adx.columns if c.startswith('DMN')), None)
        if adx_col:
            view_df = df.tail(150)
            osc_traces = [
                go.Scatter(x=view_df.index, y=adx[adx_col].tail(150), name='ADX', line=dict(color='white')),
                go.Scatter(x=view_df.index, y=adx[dmp_col].tail(150), name='+DI', line=dict(color='green')),
                go.Scatter(x=view_df.index, y=adx[dmn_col].tail(150), name='-DI', line=dict(color='red'))
            ]
            hlines = [(25, 'gray', 'dot')]
            create_chart(view_df, 'Average Directional Index (ADX)', "ADX.png", oscillator_traces=osc_traces, oscillator_hlines=hlines)
    except Exception as e: print(f"ADX: {e}")

    try:
        cci = df.ta.cci()
        view_df = df.tail(150)
        hlines = [(100, 'red', 'dash'), (-100, 'green', 'dash')]
        create_chart(view_df, 'Commodity Channel Index (CCI)', "CCI.png", oscillator_traces=[go.Scatter(x=view_df.index, y=cci.tail(150), name='CCI', line=dict(color='orange'))], oscillator_hlines=hlines)
    except Exception as e: print(f"CCI: {e}")
    
    try:
        roc = df.ta.roc()
        view_df = df.tail(150)
        hlines = [(0, 'white', 'solid')]
        create_chart(view_df, 'Rate of Change (ROC)', "ROC.png", oscillator_traces=[go.Scatter(x=view_df.index, y=roc.tail(150), name='ROC', line=dict(color='cyan'))], oscillator_hlines=hlines)
    except Exception as e: print(f"ROC: {e}")

    try:
        mom = df.ta.mom()
        view_df = df.tail(150)
        hlines = [(0, 'white', 'solid')]
        create_chart(view_df, 'Momentum (MOM)', "Momentum.png", oscillator_traces=[go.Scatter(x=view_df.index, y=mom.tail(150), name='MOM', line=dict(color='yellow'))], oscillator_hlines=hlines)
    except Exception as e: print(f"MOM: {e}")
    
    try:
        obv = df.ta.obv()
        view_df = df.tail(150)
        create_chart(view_df, 'On-Balance Volume (OBV)', "OBV.png", oscillator_traces=[go.Scatter(x=view_df.index, y=obv.tail(150), name='OBV', line=dict(color='yellow'))])
    except Exception as e: print(f"OBV: {e}")
    
    try:
        atr = df.ta.atr()
        view_df = df.tail(150)
        create_chart(view_df, 'Average True Range (ATR)', "ATR.png", oscillator_traces=[go.Scatter(x=view_df.index, y=atr.tail(150), name='ATR', line=dict(color='brown'))])
    except Exception as e: print(f"ATR: {e}")

    try:
        std = df['Close'].rolling(20).std()
        view_df = df.tail(150)
        create_chart(view_df, 'Standard Deviation', "Standard_Deviation.png", oscillator_traces=[go.Scatter(x=view_df.index, y=std.tail(150), name='Std Dev', line=dict(color='magenta'))])
    except Exception as e: print(f"StdDev: {e}")
    
    try:
        chop = df.ta.chop()
        view_df = df.tail(150)
        hlines = [(61.8, 'red', 'dot'), (38.2, 'green', 'dot')]
        create_chart(view_df, 'Choppiness Index', "Choppiness_Index.png", oscillator_traces=[go.Scatter(x=view_df.index, y=chop.tail(150), name='CHOP', line=dict(color='yellow'))], oscillator_hlines=hlines)
    except Exception as e: print(f"CHOP: {e}")
    
    try:
        mfi = df.ta.mfi()
        view_df = df.tail(150)
        hlines = [(80, 'red', 'dash'), (20, 'green', 'dash')]
        create_chart(view_df, 'Money Flow Index (MFI)', "MFI.png", oscillator_traces=[go.Scatter(x=view_df.index, y=mfi.tail(150), name='MFI', line=dict(color='orange'))], oscillator_hlines=hlines)
    except Exception as e: print(f"MFI: {e}")
    
    try:
        cmf = df.ta.cmf()
        view_df = df.tail(150)
        hlines = [(0, 'white', 'solid')]
        create_chart(view_df, 'Chaikin Money Flow (CMF)', "CMF.png", oscillator_traces=[go.Scatter(x=view_df.index, y=cmf.tail(150), name='CMF', line=dict(color='green'))], oscillator_hlines=hlines)
    except Exception as e: print(f"CMF: {e}")
    
    try:
        efi = df.ta.efi()
        view_df = df.tail(150)
        hlines = [(0, 'white', 'solid')]
        create_chart(view_df, "Elder's Force Index (EFI)", "EFI.png", oscillator_traces=[go.Scatter(x=view_df.index, y=efi.tail(150), name='EFI', line=dict(color='cyan'))], oscillator_hlines=hlines)
    except Exception as e: print(f"EFI: {e}")

    # --- Batch 6: Momentum & Trend ---
    
    try:
        df['ALMA_20'] = df.ta.alma(length=20)
        view_df = df.tail(150)
        overlay = [go.Scatter(x=view_df.index, y=view_df['ALMA_20'], mode='lines', name='ALMA 20', line=dict(color='magenta'))]
        create_chart(view_df, 'Arnaud Legoux Moving Average (ALMA)', "ALMA.png", overlay_traces=overlay)
    except Exception as e: print(f"ALMA: {e}")

    try:
        aroon = df.ta.aroon()
        ad_col = next((c for c in aroon.columns if c.startswith('AROOND')), None)
        au_col = next((c for c in aroon.columns if c.startswith('AROONU')), None)
        if ad_col and au_col:
            view_df = df.tail(150)
            osc_traces = [
                go.Scatter(x=view_df.index, y=aroon[au_col].tail(150), name='Aroon Up', line=dict(color='green')),
                go.Scatter(x=view_df.index, y=aroon[ad_col].tail(150), name='Aroon Down', line=dict(color='red'))
            ]
            hlines = [(70, 'gray', 'dot'), (30, 'gray', 'dot')]
            create_chart(view_df, 'Aroon Indicator', "Aroon.png", oscillator_traces=osc_traces, oscillator_hlines=hlines)
    except Exception as e: print(f"Aroon: {e}")

    try:
        ao = df.ta.ao()
        view_df = df.tail(150)
        cols = ['green' if v >= 0 else 'red' for v in ao.tail(150)]
        osc_traces = [go.Bar(x=view_df.index, y=ao.tail(150), name='AO', marker_color=cols)]
        create_chart(view_df, 'Awesome Oscillator', "Awesome_Oscillator.png", oscillator_traces=osc_traces)
    except Exception as e: print(f"AO: {e}")
    
    try:
        cmo = df.ta.cmo()
        view_df = df.tail(150)
        hlines = [(50, 'red', 'dash'), (-50, 'green', 'dash')]
        create_chart(view_df, 'Chande Momentum Oscillator (CMO)', "CMO.png", oscillator_traces=[go.Scatter(x=view_df.index, y=cmo.tail(150), name='CMO', line=dict(color='cyan'))], oscillator_hlines=hlines)
    except Exception as e: print(f"CMO: {e}")
    
    try:
        adosc = df.ta.adosc()
        view_df = df.tail(150)
        hlines = [(0, 'white', 'solid')]
        create_chart(view_df, 'Chaikin Oscillator', "Chaikin_Oscillator.png", oscillator_traces=[go.Scatter(x=view_df.index, y=adosc.tail(150), name='Chaikin Osc', line=dict(color='orange'))], oscillator_hlines=hlines)
    except Exception as e: print(f"Chaikin Osc: {e}")
    
    try:
        coppock = df.ta.coppock()
        if isinstance(coppock, pd.Series):
             c_view = coppock.tail(150)
        else:
             c_col = next((c for c in coppock.columns if c.startswith('COPC')), None)
             c_view = coppock[c_col].tail(150) if c_col else pd.Series()
        view_df = df.tail(150)
        if not c_view.empty:
            create_chart(view_df, 'Coppock Curve', "Coppock_Curve.png", oscillator_traces=[go.Scatter(x=view_df.index, y=c_view, name='Coppock', line=dict(color='purple'))], oscillator_hlines=[(0, 'white', 'solid')])
    except Exception as e: print(f"Coppock: {e}")
    
    try:
        dpo = df.ta.dpo()
        view_df = df.tail(150)
        hlines = [(0, 'white', 'solid')]
        create_chart(view_df, 'Detrended Price Oscillator (DPO)', "Detrended_Price_Oscillator.png", oscillator_traces=[go.Scatter(x=view_df.index, y=dpo.tail(150), name='DPO', line=dict(color='green'))], oscillator_hlines=hlines)
    except Exception as e: print(f"DPO: {e}")

    try:
        fisher = df.ta.fisher()
        f_col = next((c for c in fisher.columns if c.startswith('FISHERT_')), None)
        s_col = next((c for c in fisher.columns if c.startswith('FISHERTs_')), None)
        if f_col and s_col:
            view_df = df.tail(150)
            osc_traces = [
                go.Scatter(x=view_df.index, y=fisher[f_col].tail(150), name='Fisher', line=dict(color='cyan')),
                go.Scatter(x=view_df.index, y=fisher[s_col].tail(150), name='Signal', line=dict(color='orange'))
            ]
            hlines = [(1.5, 'red', 'dash'), (-1.5, 'green', 'dash')]
            create_chart(view_df, 'Fisher Transform', "Fisher_Transform.png", oscillator_traces=osc_traces, oscillator_hlines=hlines)
    except Exception as e: print(f"Fisher: {e}")
    
    try:
        stochrsi = df.ta.stochrsi()
        k_col = next((c for c in stochrsi.columns if c.startswith('STOCHRSIk')), None)
        d_col = next((c for c in stochrsi.columns if c.startswith('STOCHRSId')), None)
        if k_col and d_col:
            view_df = df.tail(150)
            osc_traces = [
                go.Scatter(x=view_df.index, y=stochrsi[k_col].tail(150), name='%K', line=dict(color='blue')),
                go.Scatter(x=view_df.index, y=stochrsi[d_col].tail(150), name='%D', line=dict(color='orange', dash='dot'))
            ]
            hlines = [(80, 'red', 'dash'), (20, 'green', 'dash')]
            create_chart(view_df, 'Stochastic RSI', "Stochastic_RSI.png", oscillator_traces=osc_traces, oscillator_hlines=hlines)
    except Exception as e: print(f"StochRSI: {e}")
    
    try:
        trix = df.ta.trix()
        t_col = next((c for c in trix.columns if c.startswith('TRIX_')), None)
        s_col = next((c for c in trix.columns if c.startswith('TRIXs_')), None)
        if t_col and s_col:
            view_df = df.tail(150)
            osc_traces = [
                go.Scatter(x=view_df.index, y=trix[t_col].tail(150), name='TRIX', line=dict(color='blue')),
                go.Scatter(x=view_df.index, y=trix[s_col].tail(150), name='Signal', line=dict(color='orange'))
            ]
            hlines = [(0, 'white', 'solid')]
            create_chart(view_df, 'TRIX', "TRIX.png", oscillator_traces=osc_traces, oscillator_hlines=hlines)
    except Exception as e: print(f"TRIX: {e}")

    # --- Batch 7: Volatility & Volume ---

    try:
        ad = df.ta.ad()
        view_df = df.tail(150)
        create_chart(view_df, 'Accumulation/Distribution Line (ADL)', "Accumulation_Distribution.png", oscillator_traces=[go.Scatter(x=view_df.index, y=ad.tail(150), name='ADL', line=dict(color='yellow'))])
    except Exception as e: print(f"ADL: {e}")
    
    try:
        bbw = df.ta.bbands(length=20, std=2)
        b_col = next((c for c in bbw.columns if c.startswith('BBB')), None)
        if b_col:
            view_df = df.tail(150)
            create_chart(view_df, 'Bollinger Bandwidth', "Bollinger_Bandwidth.png", oscillator_traces=[go.Scatter(x=view_df.index, y=bbw[b_col].tail(150), name='Bandwidth', line=dict(color='orange'))])
    except Exception as e: print(f"BBW: {e}")
    
    try:
        bbw = df.ta.bbands(length=20, std=2)
        p_col = next((c for c in bbw.columns if c.startswith('BBP')), None)
        if p_col:
            view_df = df.tail(150)
            hlines = [(1, 'red', 'dot'), (0, 'green', 'dot')]
            create_chart(view_df, 'Bollinger %B', "Bollinger_PctB.png", oscillator_traces=[go.Scatter(x=view_df.index, y=bbw[p_col].tail(150), name='Percent B', line=dict(color='blue'))], oscillator_hlines=hlines)
    except Exception as e: print(f"PctB: {e}")
    
    try:
        ema_hl = df.ta.ema(close=df['High']-df['Low'], length=10)
        cvi = (ema_hl - ema_hl.shift(10)) / ema_hl.shift(10) * 100
        view_df = df.tail(150)
        hlines = [(0, 'white', 'solid')]
        create_chart(view_df, 'Chaikin Volatility', "Chaikin_Volatility.png", oscillator_traces=[go.Scatter(x=view_df.index, y=cvi.tail(150), name='CVI', line=dict(color='cyan'))], oscillator_hlines=hlines)
    except Exception as e: print(f"CVI: {e}")
    
    try:
        eom = df.ta.eom()
        e_view = None
        if isinstance(eom, pd.Series):
             e_view = eom.tail(150)
        else:
            e_col = next((c for c in eom.columns if c.startswith('EOM')), None)
            if e_col: e_view = eom[e_col].tail(150)
        
        if e_view is not None:
             view_df = df.tail(150)
             hlines = [(0, 'white', 'solid')]
             create_chart(view_df, 'Ease of Movement', "Ease_of_Movement.png", oscillator_traces=[go.Scatter(x=view_df.index, y=e_view, name='EOM', line=dict(color='yellow'))], oscillator_hlines=hlines)
    except Exception as e: print(f"EOM: {e}")
    
    try:
        kvo = df.ta.kvo()
        k_col = next((c for c in kvo.columns if c.startswith('KVO_')), None)
        s_col = next((c for c in kvo.columns if c.startswith('KVOs_')), None)
        if k_col and s_col:
            view_df = df.tail(150)
            osc_traces = [
                go.Scatter(x=view_df.index, y=kvo[k_col].tail(150), name='Klinger', line=dict(color='blue')),
                go.Scatter(x=view_df.index, y=kvo[s_col].tail(150), name='Signal', line=dict(color='orange'))
            ]
            hlines = [(0, 'white', 'solid')]
            create_chart(view_df, 'Klinger Oscillator', "Klinger_Oscillator.png", oscillator_traces=osc_traces, oscillator_hlines=hlines)
    except Exception as e: print(f"Klinger: {e}")
    
    try:
        pvt = df.ta.pvt()
        view_df = df.tail(150)
        create_chart(view_df, 'Price Volume Trend (PVT)', "PVT.png", oscillator_traces=[go.Scatter(x=view_df.index, y=pvt.tail(150), name='PVT', line=dict(color='purple'))])
    except Exception as e: print(f"PVT: {e}")

    try:
        pvo = df.ta.pvo()
        p_col = next((c for c in pvo.columns if c.startswith('PVO_')), None)
        s_col = next((c for c in pvo.columns if c.startswith('PVOs_')), None)
        h_col = next((c for c in pvo.columns if c.startswith('PVOh_')), None)
        if p_col:
            view_df = df.tail(150)
            osc_traces = [
                go.Scatter(x=view_df.index, y=pvo[p_col].tail(150), name='PVO', line=dict(color='blue')),
                go.Scatter(x=view_df.index, y=pvo[s_col].tail(150), name='Signal', line=dict(color='orange')),
                 go.Bar(x=view_df.index, y=pvo[h_col].tail(150), name='Hist', marker_color=['green' if v>=0 else 'red' for v in pvo[h_col].tail(150)])
            ]
            create_chart(view_df, 'Percentage Volume Oscillator (PVO)', "Percentage_Volume_Oscillator.png", oscillator_traces=osc_traces)
    except Exception as e: print(f"PVO: {e}")
    
    try:
        rvi = df.ta.rvi()
        r_view = None
        if isinstance(rvi, pd.Series):
             r_view = rvi.tail(150)
        else:
             r_col = next((c for c in rvi.columns if c.startswith('RVI')), None)
             if r_col: r_view = rvi[r_col].tail(150)
        
        if r_view is not None:
             view_df = df.tail(150)
             hlines = [(50, 'white', 'solid')]
             create_chart(view_df, 'Relative Volatility Index (RVI)', "Relative_Volatility_Index.png", oscillator_traces=[go.Scatter(x=view_df.index, y=r_view, name='RVI', line=dict(color='green'))], oscillator_hlines=hlines)
    except Exception as e: print(f"RVI: {e}")
    
    try:
        mass = df.ta.massi()
        view_df = df.tail(150)
        hlines = [(27, 'red', 'dash'), (26.5, 'green', 'dash')]
        create_chart(view_df, 'Mass Index', "Mass_Index.png", oscillator_traces=[go.Scatter(x=view_df.index, y=mass.tail(150), name='Mass Index', line=dict(color='orange'))], oscillator_hlines=hlines)
    except Exception as e: print(f"MassI: {e}")
    
    try:
        change = df['Close'].diff()
        net_vol = df['Volume'] * (change / change.abs()).fillna(0)
        view_df = df.tail(150)
        n_view = net_vol.tail(150)
        cols = ['green' if v >= 0 else 'red' for v in n_view]
        osc_traces = [go.Bar(x=view_df.index, y=n_view, name='Net Vol', marker_color=cols)]
        create_chart(view_df, 'Net Volume', "Net_Volume.png", oscillator_traces=osc_traces)
    except Exception as e: print(f"NetVol: {e}")

    # --- Batch 8: MA & Price Transforms ---
    
    try:
        # Manual Calculation for Typical Price
        df['TYPPRICE'] = (df['High'] + df['Low'] + df['Close']) / 3
        view_df = df.tail(150)
        overlay = [go.Scatter(x=view_df.index, y=df['TYPPRICE'].tail(150), mode='lines', name='Typical Price', line=dict(color='yellow', dash='dot'))]
        create_chart(view_df, 'Typical Price', "Typical_Price.png", overlay_traces=overlay)
    except Exception as e: print(f"Typical: {e}")
    
    try:
        vwma = df.ta.vwma(length=20)
        view_df = df.tail(150)
        overlay = [go.Scatter(x=view_df.index, y=vwma.tail(150), mode='lines', name='VWMA 20', line=dict(color='orange'))]
        create_chart(view_df, 'Volume Weighted Moving Average (VWMA)', "VWMA.png", overlay_traces=overlay)
    except Exception as e: print(f"VWMA: {e}")
    
    try:
        sma = df.ta.sma(length=20)
        upper = sma * 1.025
        lower = sma * 0.975
        view_df = df.tail(150)
        overlay = [
            go.Scatter(x=view_df.index, y=upper.tail(150), line=dict(color='gray', dash='dot'), name='Upper Env'),
            go.Scatter(x=view_df.index, y=lower.tail(150), line=dict(color='gray', dash='dot'), name='Lower Env'),
            go.Scatter(x=view_df.index, y=view_df['SMA_20'], line=dict(color='blue'), name='SMA 20')
        ]
        create_chart(view_df, 'Moving Average Envelopes', "Envelopes.png", overlay_traces=overlay)
    except Exception as e: print(f"Envelopes: {e}")
    
    try:
        lsma = df.ta.linreg(length=20)
        view_df = df.tail(150)
        overlay = [go.Scatter(x=view_df.index, y=lsma.tail(150), mode='lines', name='LSMA 20', line=dict(color='magenta'))]
        create_chart(view_df, 'Least Squares Moving Average (LSMA)', "LSMA.png", overlay_traces=overlay)
    except Exception as e: print(f"LSMA: {e}")

    try:
        slope = df.ta.slope(length=20)
        view_df = df.tail(150)
        hlines = [(0, 'gray', 'dot')]
        create_chart(view_df, 'Linear Regression Slope', "Linear_Regression_Slope.png", oscillator_traces=[go.Scatter(x=view_df.index, y=slope.tail(150), name='Slope', line=dict(color='white'))], oscillator_hlines=hlines)
    except Exception as e: print(f"Slope: {e}")

    try:
        spread = df['High'] - df['Low']
        view_df = df.tail(150)
        create_chart(view_df, 'Spread (High - Low)', "Spread.png", oscillator_traces=[go.Scatter(x=view_df.index, y=spread.tail(150), name='Spread', line=dict(color='cyan'))])
    except Exception as e: print(f"Spread: {e}")

    # --- Batch 9: Others ---

    try:
        # Volume (Basic)
        view_df = df.tail(150)
        create_chart(view_df, 'Volume', "Volume.png")
    except Exception as e: print(f"Volume: {e}")

    try:
        # Average Price
        d = (df['High'] + df['Low'] + df['Close'] + df['Open']) / 4
        view_df = df.tail(150)
        overlay = [go.Scatter(x=view_df.index, y=d.tail(150), mode='lines', name='Avg Price', line=dict(color='white', dash='dot'))]
        create_chart(view_df, 'Average Price', "Average_Price.png", overlay_traces=overlay)
    except Exception as e: print(f"AvgPrice: {e}")

    try:
        # Median Price
        d = (df['High'] + df['Low']) / 2
        view_df = df.tail(150)
        overlay = [go.Scatter(x=view_df.index, y=d.tail(150), mode='lines', name='Med Price', line=dict(color='yellow', dash='dot'))]
        create_chart(view_df, 'Median Price', "Median_Price.png", overlay_traces=overlay)
    except Exception as e: print(f"MedPrice: {e}")
    
    try:
        # GMMA
        view_df = df.tail(150)
        overlay = []
        for p in [3, 5, 8, 10, 12, 15]:
            e = df.ta.ema(length=p)
            overlay.append(go.Scatter(x=view_df.index, y=e.tail(150), mode='lines', line=dict(color='cyan', width=1), showlegend=False))
        for p in [30, 35, 40, 45, 50, 60]:
            e = df.ta.ema(length=p)
            overlay.append(go.Scatter(x=view_df.index, y=e.tail(150), mode='lines', line=dict(color='red', width=1), showlegend=False))
        create_chart(view_df, 'Guppy Multiple Moving Average (GMMA)', "GMMA.png", overlay_traces=overlay)
    except Exception as e: print(f"GMMA: {e}")
    
    try:
        # Linear Regression Curve (Similar to LSMA)
        # We can just reuse LSMA plot logic but save as proper name if needed.
        # But for documentation consistency:
        lsma = df.ta.linreg(length=14)
        view_df = df.tail(150)
        overlay = [go.Scatter(x=view_df.index, y=lsma.tail(150), mode='lines', name='LinReg Curve', line=dict(color='gold'))]
        create_chart(view_df, 'Linear Regression Curve', "Linear_Regression_Curve.png", overlay_traces=overlay)
    except Exception as e: print(f"LinRegCurve: {e}")
    
    try:
        # Ratio (Close / SMA50)
        sma50 = df['Close'].rolling(50).mean()
        ratio = df['Close'] / sma50
        view_df = df.tail(150)
        osc_traces = [go.Scatter(x=view_df.index, y=ratio.tail(150), name='Close/SMA50', line=dict(color='orange'))]
        hlines = [(1, 'white', 'dash')]
        create_chart(view_df, 'Price Ratio (Close / SMA50)', "Ratio.png", oscillator_traces=osc_traces, oscillator_hlines=hlines)
    except Exception as e: print(f"Ratio: {e}")
    
    try:
        # Standard Error
        ste = df['Close'].rolling(20).std() / np.sqrt(20)
        view_df = df.tail(150)
        create_chart(view_df, 'Standard Error', "Standard_Error.png", oscillator_traces=[go.Scatter(x=view_df.index, y=ste.tail(150), name='Std Err', line=dict(color='red'))])
    except Exception as e: print(f"StdErr: {e}")
    
    try:
        # Standard Error Bands
        sma20 = df.ta.sma(length=20)
        ste = df['Close'].rolling(20).std() / np.sqrt(20)
        upper = sma20 + (2 * ste)
        lower = sma20 - (2 * ste)
        view_df = df.tail(150)
        overlay = [
            go.Scatter(x=view_df.index, y=upper.tail(150), line=dict(color='green', dash='dot'), name='Upper SEB'),
            go.Scatter(x=view_df.index, y=lower.tail(150), line=dict(color='green', dash='dot'), name='Lower SEB'),
            go.Scatter(x=view_df.index, y=sma20.tail(150), line=dict(color='blue'), name='SMA 20')
        ]
        create_chart(view_df, 'Standard Error Bands', "Standard_Error_Bands.png", overlay_traces=overlay)
    except Exception as e: print(f"SEB: {e}")
    
    try:
        # Historical Volatility (Log Returns)
        log_ret = np.log(df['Close'] / df['Close'].shift(1))
        hist_vol = log_ret.rolling(20).std() * (252 ** 0.5) * 100
        view_df = df.tail(150)
        create_chart(view_df, 'Historical Volatility (Annualized)', "Historical_Volatility.png", oscillator_traces=[go.Scatter(x=view_df.index, y=hist_vol.tail(150), name='HV', line=dict(color='cyan'))])
    except Exception as e: print(f"HV: {e}")
    
    try:
        # Volatility Close-to-Close
        vol_cc = df['Close'].pct_change().rolling(20).std()
        view_df = df.tail(150)
        create_chart(view_df, 'Volatility (Close-to-Close)', "Volatility_Close_To_Close.png", oscillator_traces=[go.Scatter(x=view_df.index, y=vol_cc.tail(150), name='Vol CC', line=dict(color='magenta'))])
    except Exception as e: print(f"VolCC: {e}")
    
    try:
        # Volatility OHLC (Garman-Klass)
        log_hl = np.log(df['High'] / df['Low'])
        log_co = np.log(df['Close'] / df['Open'])
        gk_var = 0.5 * (log_hl ** 2) - (2 * np.log(2) - 1) * (log_co ** 2)
        vol_ohlc = np.sqrt(gk_var.rolling(20).mean())
        view_df = df.tail(150)
        create_chart(view_df, 'Volatility (OHLC Garman-Klass)', "Volatility_OHLC.png", oscillator_traces=[go.Scatter(x=view_df.index, y=vol_ohlc.tail(150), name='Vol OHLC', line=dict(color='yellow'))])
    except Exception as e: print(f"VolOHLC: {e}")

    try:
        # Volatility Zero-Trend
        log_ret = np.log(df['Close'] / df['Close'].shift(1))
        vol_zt = np.sqrt((log_ret**2).rolling(20).mean())
        view_df = df.tail(150)
        create_chart(view_df, 'Volatility (Zero Trend)', "Volatility_Zero_Trend_Close_To_Close.png", oscillator_traces=[go.Scatter(x=view_df.index, y=vol_zt.tail(150), name='Vol ZT', line=dict(color='purple'))])
    except Exception as e: print(f"VolZT: {e}")

    try:
        # Williams Fractal
        # Need manual calculation for plotting markers
        # Bearish Fractal (High)
        h = df['High']
        l = df['Low']
        is_fractal_h = (h > h.shift(1)) & (h > h.shift(2)) & (h > h.shift(-1)) & (h > h.shift(-2))
        is_fractal_l = (l < l.shift(1)) & (l < l.shift(2)) & (l < l.shift(-1)) & (l < l.shift(-2))
        
        view_df = df.tail(150)
        # Filter masks for the view range
        mask_h = is_fractal_h.reindex(view_df.index).fillna(False)
        mask_l = is_fractal_l.reindex(view_df.index).fillna(False)
        
        # Apply masks to get only the points where fractals exist
        fh_points = view_df[mask_h]
        fl_points = view_df[mask_l]
        
        overlay = [
             go.Scatter(x=fh_points.index, y=fh_points['High'], mode='markers', name='Fractal High', marker=dict(symbol='triangle-down', size=10, color='red')),
             go.Scatter(x=fl_points.index, y=fl_points['Low'], mode='markers', name='Fractal Low', marker=dict(symbol='triangle-up', size=10, color='green'))
        ]
        create_chart(view_df, 'Williams Fractal', "Fractal.png", overlay_traces=overlay)
    except Exception as e: print(f"Fractal: {e}")
    
    try:
        # Hamming Moving Average
        # Manual calc
        window = np.hamming(20)
        window = window / window.sum()
        hamming = df['Close'].rolling(20).apply(lambda x: (x * window).sum(), raw=True)
        view_df = df.tail(150)
        overlay = [go.Scatter(x=view_df.index, y=hamming.tail(150), mode='lines', name='Hamming MA', line=dict(color='cyan'))]
        create_chart(view_df, 'Hamming Moving Average', "Hamming_Moving_Average.png", overlay_traces=overlay)
    except Exception as e: print(f"Hamming: {e}")
    
    try:
        # SMI Ergodic
        smi = df.ta.smi()
        # SMI_5_20_5, SMIs_5_20_5, SMIo_5_20_5
        s_col = next((c for c in smi.columns if c.startswith('SMI_')), None)
        ss_col = next((c for c in smi.columns if c.startswith('SMIs_')), None)
        if s_col and ss_col:
            view_df = df.tail(150)
            osc_traces = [
                go.Scatter(x=view_df.index, y=smi[s_col].tail(150), name='SMI', line=dict(color='orange')),
                go.Scatter(x=view_df.index, y=smi[ss_col].tail(150), name='Signal', line=dict(color='red'))
            ]
            create_chart(view_df, 'SMI Ergodic', "SMI_Ergodic.png", oscillator_traces=osc_traces)
    except Exception as e: print(f"SMI: {e}")
    
    try:
        # TSI
        tsi = df.ta.tsi()
        # TSI_13_25_13, TSIs_13_25_13
        t_col = next((c for c in tsi.columns if c.startswith('TSI_')), None)
        s_col = next((c for c in tsi.columns if c.startswith('TSIs_')), None)
        if t_col:
            view_df = df.tail(150)
            osc_traces = [go.Scatter(x=view_df.index, y=tsi[t_col].tail(150), name='TSI', line=dict(color='blue'))]
            if s_col:
                osc_traces.append(go.Scatter(x=view_df.index, y=tsi[s_col].tail(150), name='Signal', line=dict(color='red')))
            create_chart(view_df, 'True Strength Index (TSI)', "True_Strength_Index.png", oscillator_traces=osc_traces)
    except Exception as e: print(f"TSI: {e}")
    
    try:
        # Ulcer Index
        # ta.ui?
        ui = df.ta.ui()
        # UI_14
        if isinstance(ui, pd.Series): 
             u_view = ui.tail(150)
        else:
             u_view = ui[ui.columns[0]].tail(150)
             
        view_df = df.tail(150)
        create_chart(view_df, 'Ulcer Index', "Ulcer_Index.png", oscillator_traces=[go.Scatter(x=view_df.index, y=u_view, name='UI', line=dict(color='red'))])
    except Exception as e: print(f"UI: {e}")

    try:
        # Vortex
        vortex = df.ta.vortex()
        p_col = next((c for c in vortex.columns if c.startswith('VTXP')), None)
        m_col = next((c for c in vortex.columns if c.startswith('VTXM')), None)
        if p_col and m_col:
            view_df = df.tail(150)
            osc_traces = [
                go.Scatter(x=view_df.index, y=vortex[p_col].tail(150), name='VI+', line=dict(color='green')),
                go.Scatter(x=view_df.index, y=vortex[m_col].tail(150), name='VI-', line=dict(color='red'))
            ]
            create_chart(view_df, 'Vortex Indicator', "Vortex_Indicator.png", oscillator_traces=osc_traces)
    except Exception as e: print(f"Vortex: {e}")
    
    try:
        # Ultimate Oscillator
        uo = df.ta.uo()
        view_df = df.tail(150)
        hlines = [(70, 'red', 'dash'), (30, 'green', 'dash'), (50, 'gray', 'dot')]
        create_chart(view_df, 'Ultimate Oscillator', "Ultimate_Oscillator.png", oscillator_traces=[go.Scatter(x=view_df.index, y=uo.tail(150), name='UO', line=dict(color='orange'))], oscillator_hlines=hlines)
    except Exception as e: print(f"UO: {e}")

    try:
        # Williams Alligator
        # ta.alligator -> AG_13_8_5...
        # It actually returns a dataframe with 3 columns usually.
        # Check docs or try/except
        ali = df.ta.alligator()
        # Usually it returns columns like: AGj_13_8_5 (Jaw), AGt_8_5_3 (Teeth), AGl_5_3_? (Lips)
        # Let's inspect columns or assume standard mapping if names match.
        # Actually in newest pandas_ta it might return simple names.
        if ali is not None and not ali.empty:
            view_df = df.tail(150)
            # Just take the last 3 columns?
            # Or assume order is Jaw, Teeth, Lips?
            # Jaw (Blue, 13), Teeth (Red, 8), Lips (Green, 5)
            # Usually Jaw is slowest (13), Lips fastest (5)
            # Let's try to identify by name if possible, else index.
            cols = ali.columns
            overlay = [
                go.Scatter(x=view_df.index, y=ali[cols[0]].tail(150), name='Jaw', line=dict(color='blue')),
                go.Scatter(x=view_df.index, y=ali[cols[1]].tail(150), name='Teeth', line=dict(color='red')),
                go.Scatter(x=view_df.index, y=ali[cols[2]].tail(150), name='Lips', line=dict(color='green'))
            ]
            create_chart(view_df, 'Williams Alligator', "Williams_Alligator.png", overlay_traces=overlay)
    except Exception as e: print(f"Alligator: {e}")

    try:
        # Chande Kroll Stop
        cks = df.ta.cksp(p=10, x=3, q=20)
        l_col = next((c for c in cks.columns if c.startswith('CKSPl')), None)
        s_col = next((c for c in cks.columns if c.startswith('CKSPs')), None)
        
        if l_col and s_col:
            view_df = df.tail(150)
            overlay = [
                go.Scatter(x=view_df.index, y=cks[l_col].tail(150), name='Stop Long', line=dict(color='green')),
                go.Scatter(x=view_df.index, y=cks[s_col].tail(150), name='Stop Short', line=dict(color='red'))
            ]
            create_chart(view_df, 'Chande Kroll Stop (CKS)', "Chande_Kroll_Stop.png", overlay_traces=overlay)
    except Exception as e: print(f"CKS: {e}")

if __name__ == "__main__":
    # Check if data exists
    # Check if data exists
    data_path = "utils/data.csv"
    if os.path.exists(data_path):
        print(f"Loading {data_path}...")
        df = pd.read_csv(data_path, index_col=0, parse_dates=True)
    else:
        df = download_data()
        df.to_csv(data_path)
    
    print("Generating refined plots...")
    generate_plots(df)
    print("Done.")
