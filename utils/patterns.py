import json
import os
import plotly.graph_objects as go
import pandas as pd

# Define paths
DATA_FILE = os.path.join(os.path.dirname(__file__), 'pattern_data.json')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'docs', 'patterns', 'plots')

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_plots():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    for pattern_name, candle_data in data.items():
        df = pd.DataFrame(candle_data)
        
        fig = go.Figure(data=[go.Candlestick(
            x=df['Date'],
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            increasing_line_color='green', 
            decreasing_line_color='red'
        )])

        fig.update_layout(
            title=pattern_name.replace('_', ' '),
            xaxis_title='Date',
            yaxis_title='Price',
            xaxis_rangeslider_visible=False,
            template='plotly_white',
            width=800,
            height=600
        )
        
        output_path = os.path.join(OUTPUT_DIR, f"{pattern_name}.png")
        try:
            fig.write_image(output_path)
            print(f"Generated {output_path}")
        except Exception as e:
            print(f"Failed to generate {output_path}: {e}")
            print("Ensure kaleido is installed: pip install kaleido")

if __name__ == "__main__":
    generate_plots()
