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
    # Technical Indicators for the trader
    from engine.indicators import add_technical_indicators
    add_technical_indicators(df)
    
    # Drop NaNs created by indicators (e.g. SMA200 removes first 200 rows)
    # Instead of strict dropna() which might kll everything if one indicator is bad,
    # let's just slice off the warmup period.
    # SMA 200 is the longest lookback.
    if len(df) > 210:
        df = df.iloc[210:]
    
    return df
