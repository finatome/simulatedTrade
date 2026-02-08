
import os

docs_dir = "docs/indicators"

indicators_data = {
    "Stochastic": {
        "title": "Stochastic Oscillator",
        "definition": "The Stochastic Oscillator is a momentum indicator comparing a particular closing price of a security to a range of its prices over a certain period of time. The sensitivity of the oscillator to market movements is reducible by adjusting that time period or by taking a moving average of the result.",
        "equation": r"$$ \%K = 100 \times \frac{C - L_{14}}{H_{14} - L_{14}} $$ \n$$ \%D = \text{SMA}_3(\%K) $$ \n\nWhere:\n*   $C$ = The most recent closing price\n*   $L_{14}$ = The lowest price traded of the 14 previous trading sessions\n*   $H_{14}$ = The highest price traded during the same 14-day period\n*   $\%K$ = The current value of the stochastic indicator",
        "code": """```python
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Calculate Stochastic
stoch = df.ta.stoch(k=14, d=3, smooth_k=3)
# Returns STOCHk_14_3_3, STOCHd_14_3_3
k_line = stoch['STOCHk_14_3_3']
d_line = stoch['STOCHd_14_3_3']

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3])

fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='OHLC'), row=1, col=1)

fig.add_trace(go.Scatter(x=df.index, y=k_line, mode='lines', name='%K', line=dict(color='blue')), row=2, col=1)
fig.add_trace(go.Scatter(x=df.index, y=d_line, mode='lines', name='%D', line=dict(color='orange', dash='dot')), row=2, col=1)

# Overbought/Oversold
fig.add_hline(y=80, line_dash="dash", line_color="red", row=2, col=1)
fig.add_hline(y=20, line_dash="dash", line_color="green", row=2, col=1)

fig.update_layout(title='Stochastic Oscillator', template='plotly_dark')
fig.show()
```""",
        "significance": "1. **Overbought/Oversold**: Values > 80 indicate overbought; < 20 indicate oversold.\n2. **Crossovers**: %K crossing above %D is a buy signal; below is a sell signal.\n3. **Divergence**: Bullish/Bearish divergence signals potential reversals."
    },
    "ADX": {
        "title": "Average Directional Index (ADX)",
        "definition": "The Average Directional Index (ADX) is used to quantify the strength of a trend. ADX stands for Average Directional Movement Index and is used to measure the overall strength of a trend. The ADX indicator is an average of expanding price range values.",
        "equation": r"$$ +DI = 100 \times \frac{\text{EMA}(+DM)}{\text{ATR}} $$ \n$$ -DI = 100 \times \frac{\text{EMA}(-DM)}{\text{ATR}} $$ \n$$ DX = 100 \times \frac{|(+DI) - (-DI)|}{(+DI) + (-DI)} $$ \n$$ ADX = \text{EMA}(DX) $$",
        "code": """```python
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Calculate ADX
adx_df = df.ta.adx(length=14)
# Returns ADX_14, DMP_14, DMN_14

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3])

fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='OHLC'), row=1, col=1)

fig.add_trace(go.Scatter(x=df.index, y=adx_df['ADX_14'], mode='lines', name='ADX', line=dict(color='white')), row=2, col=1)
fig.add_trace(go.Scatter(x=df.index, y=adx_df['DMP_14'], mode='lines', name='+DI', line=dict(color='green')), row=2, col=1)
fig.add_trace(go.Scatter(x=df.index, y=adx_df['DMN_14'], mode='lines', name='-DI', line=dict(color='red')), row=2, col=1)

fig.add_hline(y=25, line_dash="dot", line_color="gray", row=2, col=1)

fig.update_layout(title='ADX Indicator', template='plotly_dark')
fig.show()
```""",
        "significance": "1. **Trend Strength**: ADX > 25 indicates a strong trend (either up or down). ADX < 20 indicates a weak or non-existent trend.\n2. **Direction**: If +DI > -DI, trend is bullish. If -DI > +DI, trend is bearish."
    },
    "CCI": {
        "title": "Commodity Channel Index (CCI)",
        "definition": "The Commodity Channel Index (CCI) is a momentum-based oscillator used to help determine when an investment vehicle is reaching a condition of being overbought or oversold. It is also used to assess direction and strength of price returns.",
        "equation": r"$$ CCI = \frac{TP - SMA(TP)}{0.015 \times \text{MD}} $$ \n\nWhere:\n*   $TP = \frac{\text{High} + \text{Low} + \text{Close}}{3}$\n*   $MD$ = Mean Deviation",
        "code": """```python
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Calculate CCI
cci = df.ta.cci(length=14)

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3])

fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='OHLC'), row=1, col=1)

fig.add_trace(go.Scatter(x=df.index, y=cci, mode='lines', name='CCI', line=dict(color='orange')), row=2, col=1)

fig.add_hline(y=100, line_dash="dash", line_color="red", row=2, col=1)
fig.add_hline(y=-100, line_dash="dash", line_color="green", row=2, col=1)

fig.update_layout(title='CCI Indicator', template='plotly_dark')
fig.show()
```""",
        "significance": "1. **Overbought/Oversold**: CCI > +100 implies overbought conditions. CCI < -100 implies oversold conditions.\n2. **Trend Emerging**: Movement from inside the +/-100 range to outside can signal a new trend."
    },
    "ROC": {
        "title": "Rate of Change (ROC)",
        "definition": "The Price Rate of Change (ROC) is a momentum-based technical indicator that measures the percentage change in price between the current price and the price a certain number of periods ago.",
        "equation": r"$$ ROC = \frac{\text{Close}_t - \text{Close}_{t-n}}{\text{Close}_{t-n}} \times 100 $$",
        "code": """```python
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Calculate ROC
roc = df.ta.roc(length=10)

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3])

fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='OHLC'), row=1, col=1)

fig.add_trace(go.Scatter(x=df.index, y=roc, mode='lines', name='ROC', line=dict(color='cyan')), row=2, col=1)

fig.add_hline(y=0, line_color="white", row=2, col=1)

fig.update_layout(title='Rate of Change (ROC)', template='plotly_dark')
fig.show()
```""",
        "significance": "1. **Momentum**: Rising ROC indicates increasing bullish momentum. Falling ROC (even if positive) indicates waning momentum.\n2. **Zero Line Cross**: Crossing above zero is a buy signal; below zero is a sell signal."
    },
    "OBV": {
        "title": "On-Balance Volume (OBV)",
        "definition": "On-Balance Volume (OBV) is a technical trading momentum indicator that uses volume flow to predict changes in stock price. It accumulates buying and selling volume.",
        "equation": r"$$ OBV_t = OBV_{t-1} + \begin{cases} \text{Volume}_t & \text{if } P_t > P_{t-1} \\ 0 & \text{if } P_t = P_{t-1} \\ -\text{Volume}_t & \text{if } P_t < P_{t-1} \end{cases} $$",
        "code": """```python
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Calculate OBV
obv = df.ta.obv()

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3])

fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='OHLC'), row=1, col=1)

fig.add_trace(go.Scatter(x=df.index, y=obv, mode='lines', name='OBV', line=dict(color='yellow')), row=2, col=1)

fig.update_layout(title='On-Balance Volume (OBV)', template='plotly_dark')
fig.show()
```""",
        "significance": "1. **Volume Precedes Price**: Use OBV to confirm trends. If price is rising but OBV is flat or falling, the trend may be weak.\n2. **Divergence**: Bullish/Bearish divergence between price and OBV often signals reversals."
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
