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
    from trading_sim.engine.indicators import add_technical_indicators

ASSETS_DIR = os.path.join('trading_sim', 'assets')
DATA_FILE = os.path.join(ASSETS_DIR, 'futures_data.csv')

def download_and_process(ticker='MES=F', period='59d', interval='5m'):
    print(f"Downloading {ticker} data ({period}, {interval})...")
    
    # Download data
    df = yf.download(ticker, period=period, interval=interval, progress=True)
    
    if df.empty:
        print("Error: Downloaded data is empty.")
        return

    # Flatten MultiIndex columns if present (yfinance update)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    # Ensure standard columns
    required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    if not all(col in df.columns for col in required_cols):
        print(f"Error: Missing columns. Got {df.columns}")
        return

    # Normalize Index
    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)

    print(f"Data downloaded. Shape: {df.shape}")
    print("Calculating technical indicators...")
    
    # Add indicators
    df = add_technical_indicators(df)
    
    # Clean up NaN (warmup period)
    # We keep NaNs in the CSV? Or drop them? 
    # Better to keep them or drop the initial warmup. 
    # Let's drop the first 200 rows to save space and avoid NaN handling in app.
    if len(df) > 200:
        df = df.iloc[200:]
    
    print(f"Indicators added. Final Shape: {df.shape}")
    
    # Save to CSV
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR)
        
    df.to_csv(DATA_FILE)
    print(f"Data saved to {DATA_FILE}")

if __name__ == "__main__":
    download_and_process()
