import pandas as pd
import sys
import os

# Add key paths
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'trading_sim'))

from trading_sim.engine.gbm_engine import generate_scenario_data

print("Generating scenario data...")
try:
    df = generate_scenario_data(periods=400)
    print(f"DataFrame Shape: {df.shape}")
    print("Columns:", df.columns.tolist())
    print("\nHead(5):")
    print(df.head())
    print("\nTail(5):")
    print(df.tail())
    
    if df.empty:
        print("\nERROR: DataFrame is empty!")
    elif len(df) < 50:
        print(f"\nWARNING: DataFrame has only {len(df)} rows, less than 50.")
    else:
        print("\nSUCCESS: Data seems valid for plotting.")

except Exception as e:
    print(f"\nCRITICAL ERROR: {e}")
    import traceback
    traceback.print_exc()
