import pandas as pd
import numpy as np
import os

# Global Cache (Dictionary keyed by ticker)
CACHED_DATA = {}

# Path resolution
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

def load_real_data(ticker='MES'):
    """
    Loads real market data from the local CSV file.
    Expects 'trading_sim/assets/{ticker}_data.csv' to exist.
    """
    global CACHED_DATA
    
    # Check Cache first
    if ticker in CACHED_DATA:
        return CACHED_DATA[ticker]
    
    # Map ticker to filename (MES or MES=F -> MES_data.csv)
    safe_name = ticker.split('=')[0]
    filename = f"{safe_name}_data.csv"
    data_file = os.path.join(ASSETS_DIR, filename)

    if not os.path.exists(data_file):
        print(f"Error: Data file not found at {data_file}")
        print("Please run 'python download_data.py' to fetch data.")
        return None
        
    print(f"Loading data from {data_file}...")
    try:
        df = pd.read_csv(data_file, index_col=0, parse_dates=True)
        
        # Verify columns
        required_cols = ['Open', 'High', 'Low', 'Close']
        if not all(col in df.columns for col in required_cols):
             print(f"Error: Missing columns in CSV. Found: {df.columns}")
             return None
             
        # Cache it
        CACHED_DATA[ticker] = df
        print(f"Data loaded for {ticker}. Shape: {df.shape}")
        return df
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def get_random_scenario(ticker='MES', periods=400):
    """
    Returns a slice of the real market data for the given ticker.
    """
    try:
        df = load_real_data(ticker)
        
        if df is None or df.empty:
             raise ValueError(f"Real data unavailable for {ticker}.")
        
        total_rows = len(df)
        
        if total_rows < periods + 10:
             return df
            
        # Pick a random start index
        max_start = total_rows - periods
        start_idx = np.random.randint(0, max_start)
        
        slice_df = df.iloc[start_idx : start_idx + periods].copy()
        
        return slice_df
        
    except Exception as e:
        print(f"Fallback to Synthetic due to error: {e}")
        from engine.gbm_engine import generate_scenario_data
        return generate_scenario_data(periods=periods)
