import numpy as np
import pandas as pd
import pandas_ta as ta

def generate_scenario_data(periods=400, start_price=1000):
    """
    Generates a realistic 5-minute market slice using GBM 
    with a volatility multiplier to simulate 'news' or 'spikes'.
    """
    dt = 1  # Time step
    mu = 0.0001  # Drift
    sigma_base = 0.002  # Base volatility
    
    prices = [start_price]
    sigs = [sigma_base]
    
    for i in range(1, periods):
        # Volatility clustering: Sigma evolves based on previous sigma
        shock = np.random.normal(0, 1)
        # Random walk for volatility, clamped
        new_sig = sigs[-1] + np.random.normal(0, 0.0001)
        new_sig = max(min(new_sig, 0.005), 0.001) # Clamp volatility
        sigs.append(new_sig)
        
        # GBM formula: S_t = S_t-1 * exp((mu - 0.5 * sigma^2) * dt + sigma * sqrt(dt) * shock)
        price = prices[-1] * np.exp((mu - 0.5 * new_sig**2) * dt + new_sig * np.sqrt(dt) * shock)
        prices.append(price)
    
    df = pd.DataFrame({'Close': prices})
    
    # Add DatetimeIndex for pandas_ta (VWAP requires it)
    # Generate synthetic timestamps ending "now"
    end_time = pd.Timestamp.now().round('5min')
    timestamps = [end_time - pd.Timedelta(minutes=5 * (periods - 1 - i)) for i in range(periods)]
    df.index = pd.DatetimeIndex(timestamps)
    
    df['Open'] = df['Close'].shift(1).fillna(start_price)
    
    # Generate High/Low relative to the volatility at that moment
    noise = np.array(sigs) * 0.5
    df['High'] = df[['Open', 'Close']].max(axis=1) * (1 + np.random.uniform(0, noise))
    df['Low'] = df[['Open', 'Close']].min(axis=1) * (1 - np.random.uniform(0, noise))
    df['Volume'] = (np.random.randint(100, 1000, size=periods) * (np.array(sigs) / sigma_base)).astype(int)
    
    # Ensure High is highest and Low is lowest (sanity check)
    df['High'] = df[['High', 'Open', 'Close']].max(axis=1)
    df['Low'] = df[['Low', 'Open', 'Close']].min(axis=1)

    # Technical Indicators for the trader
    # Suppress pandas_ta warnings if any, or just ensure it works
    # Technical Indicators (Top 20)
    # Trend
    df.ta.sma(length=20, append=True)
    df.ta.sma(length=50, append=True)
    df.ta.sma(length=200, append=True)
    df.ta.ema(length=9, append=True)
    df.ta.ema(length=21, append=True)
    df.ta.ema(length=50, append=True)
    df.ta.wma(length=21, append=True)
    df.ta.hma(length=21, append=True)
    df.ta.vwap(append=True)
    df.ta.supertrend(append=True) # Generates SUPERT_7_3.0 etc
    
    # Volatility / Channels
    df.ta.bbands(length=20, std=2, append=True) # BBL, BBM, BBU
    df.ta.kc(append=True) # Keltner Channels
    df.ta.donchian(append=True) # DCL, DCM, DCU
    
    # Momentum / Oscillators
    df.ta.rsi(length=14, append=True)
    df.ta.macd(append=True) # MACD, MACDh, MACDs
    df.ta.stoch(append=True) # STOCHk, STOCHd
    df.ta.adx(append=True) # ADX, DMP, DMN
    df.ta.cci(length=14, append=True)
    df.ta.roc(length=10, append=True)
    
    # Volume
    df.ta.obv(append=True)
    
    # Parabolic SAR
    df.ta.psar(append=True) # PSARl, PSARs
    
    # Drop NaNs created by indicators (e.g. SMA200 removes first 200 rows)
    # Instead of strict dropna() which might kll everything if one indicator is bad,
    # let's just slice off the warmup period.
    # SMA 200 is the longest lookback.
    if len(df) > 210:
        df = df.iloc[210:]
    
    return df
