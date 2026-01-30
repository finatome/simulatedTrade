import pandas_ta as ta
import pandas as pd

def add_technical_indicators(df):
    """
    Adds a standard suite of 20 technical indicators to the DataFrame using pandas_ta.
    Modifies the DataFrame in-place (append=True).
    """
    
    # 1. Trend
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
    
    # 2. Volatility / Channels
    df.ta.bbands(length=20, std=2, append=True) # BBL, BBM, BBU
    df.ta.kc(append=True) # Keltner Channels
    df.ta.donchian(append=True) # DCL, DCM, DCU
    
    # 3. Momentum / Oscillators
    df.ta.rsi(length=14, append=True)
    df.ta.macd(append=True) # MACD, MACDh, MACDs
    df.ta.stoch(append=True) # STOCHk, STOCHd
    df.ta.adx(append=True) # ADX, DMP, DMN
    df.ta.cci(length=14, append=True)
    df.ta.roc(length=10, append=True)
    
    # 4. Volume
    df.ta.obv(append=True)
    
    # 5. Parabolic SAR
    df.ta.psar(append=True) # PSARl, PSARs
    
    return df
