import pandas as pd
import numpy as np
import os
# from engine.indicators import add_technical_indicators # Already in CSV

# Global Cache
CACHED_DATA = None

# Path resolution
# __file__ = .../trading_sim/engine/real_data_engine.py
# target = .../trading_sim/assets/spy_data.csv
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, 'assets', 'futures_data.csv')

def load_real_data():
    """
    Loads real market data from the local CSV file.
    Expects 'trading_sim/assets/spy_data.csv' to exist.
    """
    global CACHED_DATA
    
    if CACHED_DATA is not None:
        return CACHED_DATA
    
    if not os.path.exists(DATA_FILE):
        print(f"Error: Data file not found at {DATA_FILE}")
        print("Please run 'python download_data.py' to fetch data.")
        return None
        
    print(f"Loading data from {DATA_FILE}...")
    try:
        df = pd.read_csv(DATA_FILE, index_col=0, parse_dates=True)
        
        # Verify columns
        required_cols = ['Open', 'High', 'Low', 'Close']
        if not all(col in df.columns for col in required_cols):
             print(f"Error: Missing columns in CSV. Found: {df.columns}")
             return None
             
        # Check if indicators are present (if we pre-calculated them)
        # If download_data.py added them, they should be there.
        # If not, we might need to add them here. 
        # Ideally, download_data.py handled it.
        
        CACHED_DATA = df
        print(f"Data loaded. Shape: {df.shape}")
        return df
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def get_random_scenario(periods=400):
    """
    Returns a slice of the real market data of length `periods`.
    """
    try:
        df = load_real_data()
        
        if df is None or df.empty:
             raise ValueError("Real data unavailable.")
        
        total_rows = len(df)
        
        if total_rows < periods + 10:
             return df
            
        # Pick a random start index
        # We don't need warmup slice logic if CSV already handled it (download_data chopped 200).
        # We can just pick any slice of length 'periods'.
        
        max_start = total_rows - periods
        start_idx = np.random.randint(0, max_start)
        
        slice_df = df.iloc[start_idx : start_idx + periods].copy()
        
        return slice_df
        
    except Exception as e:
        print(f"Fallback to Synthetic due to error: {e}")
        from engine.gbm_engine import generate_scenario_data
        return generate_scenario_data(periods=periods)
