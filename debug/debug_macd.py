import pandas as pd
import sys
import os

# Add key paths
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'trading_sim'))

from trading_sim.engine.gbm_engine import generate_scenario_data

print("Generating scenario data...")
df = generate_scenario_data(periods=400)

print("Checking MACD Columns:")
cols = [c for c in df.columns if 'MACD' in c]
print("Found MACD cols:", cols)

if not cols:
    print("ERROR: No MACD columns found!")
    sys.exit(1)

print("\nSample Data (Tail 10):")
print(df[cols].tail(10))

# Check if they are identical
macd = df['MACD_12_26_9']
signal = df['MACDs_12_26_9']

if macd.equals(signal):
    print("\nCRITICAL: MACD and Signal columns are IDENTICAL!")
else:
    print("\nOK: MACD and Signal are distinct.")

# Check for NaNs
print("\nNaN Counts:")
print(df[cols].isna().sum())
