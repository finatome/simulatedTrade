
import os

docs_dir = "docs/indicators"

indicators_data = {
    "ATR": {
        "title": "Average True Range (ATR)",
        "definition": "The Average True Range (ATR) is a technical analysis indicator that measures market volatility. It is typically derived from the 14-day simple moving average of a series of true range indicators.",
        "equation": r"$$ TR = \max[(High - Low), |High - Close_{prev}|, |Low - Close_{prev}|] $$ \n$$ ATR = SMA(TR, n) $$",
        "code": """```python
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Calculate ATR
atr = df.ta.atr(length=14)

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3])

fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='OHLC'), row=1, col=1)

fig.add_trace(go.Scatter(x=df.index, y=atr, mode='lines', name='ATR', line=dict(color='brown')), row=2, col=1)

fig.update_layout(title='Average True Range (ATR)', template='plotly_dark')
fig.show()
```""",
        "significance": "1. **Volatility Measurement**: High ATR = High Volatility. Low ATR = Ranges.\n2. **Stop Loss**: A multiple of ATR is often used to set stop-loss levels (e.g., 2x ATR)."
    },
    "Keltner_Channels": {
        "title": "Keltner Channels",
        "definition": "Keltner Channels are volatility-based bands that are placed on either side of an asset's price and can aid in determining the direction of a trend.",
        "equation": r"$$ \text{Middle Line} = \text{EMA}_{20} $$ \n$$ \text{Upper Band} = \text{EMA}_{20} + (2 \times \text{ATR}_{10}) $$ \n$$ \text{Lower Band} = \text{EMA}_{20} - (2 \times \text{ATR}_{10}) $$",
        "code": """```python
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go

# Calculate KC
kc = df.ta.kc() # Returns columns like KCLe_20_2, KCBe_20_2, KCUe_20_2

# Extract typical columns (check your specific implementation output names)
lower = kc[kc.columns[0]]
middle = kc[kc.columns[1]]
upper = kc[kc.columns[2]]

fig = go.Figure()
fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='OHLC'))

fig.add_trace(go.Scatter(x=df.index, y=upper, line=dict(color='cyan', width=1), name='Upper Check'))
fig.add_trace(go.Scatter(x=df.index, y=lower, line=dict(color='cyan', width=1), fill='tonexty', fillcolor='rgba(0, 255, 255, 0.1)', name='Lower Channel'))
fig.add_trace(go.Scatter(x=df.index, y=middle, line=dict(color='blue', width=1.5), name='EMA 20'))

fig.update_layout(title='Keltner Channels', template='plotly_dark')
fig.show()
```""",
        "significance": "1. **Trend Identification**: Breakout above upper channel signals uptrend.\n2. **Reversion**: Price often reverts to the middle EMA in trends."
    },
    "Donchian_Channels": {
        "title": "Donchian Channels",
        "definition": "Donchian Channels are formed by taking the highest high and the lowest low of the last n periods. The area between the high and the low is the Donchian Channel.",
        "equation": r"$$ \text{Upper Channel} = \max(\text{High}, n) $$ \n$$ \text{Lower Channel} = \min(\text{Low}, n) $$ \n$$ \text{Middle Channel} = \frac{\text{Upper} + \text{Lower}}{2} $$",
        "code": """```python
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go

# Calculate Donchian
dc = df.ta.donchian(lower_length=20, upper_length=20)
# Returns DCL_20_20, DCM_20_20, DCU_20_20

lower = dc['DCL_20_20']
middle = dc['DCM_20_20']
upper = dc['DCU_20_20']

fig = go.Figure()
fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='OHLC'))

fig.add_trace(go.Scatter(x=df.index, y=upper, line=dict(color='green', width=1), name='Upper Donchian'))
fig.add_trace(go.Scatter(x=df.index, y=lower, line=dict(color='red', width=1), fill='tonexty', fillcolor='rgba(0, 255, 0, 0.1)', name='Lower Donchian'))
fig.add_trace(go.Scatter(x=df.index, y=middle, line=dict(color='gray', width=1, dash='dot'), name='Middle'))

fig.update_layout(title='Donchian Channels', template='plotly_dark')
fig.show()
```""",
        "significance": "1. **Breakouts**: New Highs (touching upper band) signal buy. New Lows (touching lower band) signal sell.\n2. **Turtle Trading**: Famous Turtle Trading system used Donchian Channel breakouts."
    },
    "Standard_Deviation": {
        "title": "Standard Deviation",
        "definition": "Standard Deviation is a statistical measure of volatility. In finance, it represents the dispersion of returns from the average return.",
        "equation": r"$$ \sigma = \sqrt{\frac{\sum(x - \bar{x})^2}{n}} $$",
        "code": """```python
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Calculate Std Dev
std = df['Close'].rolling(window=20).std()

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3])

fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='OHLC'), row=1, col=1)

fig.add_trace(go.Scatter(x=df.index, y=std, mode='lines', name='Std Dev', line=dict(color='magenta')), row=2, col=1)

fig.update_layout(title='Standard Deviation', template='plotly_dark')
fig.show()
```""",
        "significance": "1. **Volatility**: High Std Dev implies high volatility and potential risk.\n2. **Market Tops/Bottoms**: Extremely high volatility often marks tops/bottoms."
    },
    "Choppiness_Index": {
        "title": "Choppiness Index",
        "definition": "The Choppiness Index (CHOP) is designed to determine if the market is choppy (trading sideways) or not choppy (trading within a trend in either direction).",
        "equation": r"$$ CHOP = 100 \times \frac{\log_{10}(\frac{\sum \text{ATR}(1)}{\text{MaxHi}(n) - \text{MinLo}(n)})}{\log_{10}(n)} $$",
        "code": """```python
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Calculate CHOP
chop = df.ta.chop(length=14)

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3])

fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='OHLC'), row=1, col=1)

fig.add_trace(go.Scatter(x=df.index, y=chop, mode='lines', name='Choppiness Index', line=dict(color='yellow')), row=2, col=1)

fig.add_hline(y=61.8, line_dash="dot", line_color="red", row=2, col=1)
fig.add_hline(y=38.2, line_dash="dot", line_color="green", row=2, col=1)

fig.update_layout(title='Choppiness Index', template='plotly_dark')
fig.show()
```""",
        "significance": "1. **Market State**: Values > 61.8 indicate consolidation (choppy). Values < 38.2 indicate a trend.\n2. **Breakout Anticipation**: High values often precede a breakout."
    }
}

for name, data in indicators_data.items():
    file_path = os.path.join(docs_dir, f"{name}.md")
    content = f"""# {data['title']}

## Definition
{data['definition']}

## Mathematical Equation
{data['equation']}

## Visualization Code
{data['code']}

## Trading Significance
{data['significance']}
"""
    with open(file_path, "w") as f:
        f.write(content)
    print(f"Filled {file_path}")
