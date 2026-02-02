import yfinance as yf
import pandas as pd
import os
import sys

# Ensure we can import from trading_sim
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from trading_sim.engine.indicators import add_technical_indicators
except ImportError:
    # If running from root, maybe trading_sim is a package
    from engine.indicators import add_technical_indicators

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')

# Ticker Mapping
# MES=F: Micro E-mini S&P 500
# MGC=F: Micro Gold
# SIL=F: Micro Silver
# MNQ=F: Micro E-mini Nasdaq 100
# MBT=F: Micro Bitcoin
TICKERS = ['MES=F', 'MGC=F', 'SIL=F', 'MNQ=F', 'MBT=F']

def download_and_process_all(period='59d', interval='5m'):
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR)
        
    for ticker in TICKERS:
        print(f"--- Processing {ticker} ---")
        try:
            download_one(ticker, period, interval)
        except Exception as e:
            print(f"Failed to process {ticker}: {e}")

def download_one(ticker, period, interval):
    print(f"Downloading {ticker}...")
    
    # Download data
    df = yf.download(ticker, period=period, interval=interval, progress=True)
    
    if df.empty:
        print(f"Error: Downloaded data for {ticker} is empty.")
        return

    # Flatten MultiIndex columns if present (yfinance update)
    if isinstance(df.columns, pd.MultiIndex):
        try:
             # If just Ticker level exists, drop it
            df.columns = df.columns.get_level_values(0)
        except:
             pass
    
    # Ensure standard columns & Fix naming if needed (sometimes yfinance weirdness)
    # yfinance often returns: Open, High, Low, Close, Adj Close, Volume
    # We need strictly Open, High, Low, Close, Volume
    
    # Check if we have Ticker as column level (happens if we download multiple, 
    # but here we download one by one, should be fine).
    
    required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    current_cols = df.columns.tolist()
    
    # Normalize MultiIndex columns usually result in 'Price', 'Ticker'
    # Actually, yf.download(..., multi_level_index=False) helps in newer versions
    # But let's stick to cleaning manually just in case.
    
    if not all(col in df.columns for col in required_cols):
        print(f"Error: Missing columns. Got {df.columns}")
        # Try to be smarter? No, fail safe.
        return

    # Normalize Index
    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)

    print(f"Data downloaded. Shape: {df.shape}")
    print("Calculating technical indicators...")
    
    # Add indicators
    df = add_technical_indicators(df)
    
    # Drop warmup
    if len(df) > 200:
        df = df.iloc[200:]
    
    print(f"Indicators added. Final Shape: {df.shape}")
    
    # Save to CSV
    # Clean ticker for filename (e.g. MES=F -> MES)
    safe_name = ticker.split('=')[0]
    filename = f"{safe_name}_data.csv"
    filepath = os.path.join(ASSETS_DIR, filename)
        
    df.to_csv(filepath)
    print(f"Data saved to {filepath}\n")

if __name__ == "__main__":
    download_and_process_all()
