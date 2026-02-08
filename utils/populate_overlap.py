
import os

docs_dir = "docs/indicators"

indicators_data = {
    "WMA": {
        "title": "Weighted Moving Average (WMA)",
        "definition": "The Weighted Moving Average (WMA) is similar to the SMA but assigns a linear weighting to the data points, giving more mathematical importance to recent data points. This makes it more responsive to price changes than the SMA.",
        "equation": r"$$ WMA_n = \frac{\sum_{i=1}^{n} P_i \times i}{\sum_{i=1}^{n} i} $$ \n\nWhere $P_i$ is the price at period $i$ (with $n$ being the most recent). denominator is the triangular number $\frac{n(n+1)}{2}$.",
        "code": """```python
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go

# Calculate WMA
df['WMA_20'] = df.ta.wma(length=20)

fig = go.Figure()
fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='OHLC'))
fig.add_trace(go.Scatter(x=df.index, y=df['WMA_20'], mode='lines', name='WMA 20', line=dict(color='blue')))
fig.update_layout(title='WMA Indicator', template='plotly_dark')
fig.show()
```""",
        "significance": "1. **Trend sensitivity**: WMA reacts faster to price changes than SMA, helping to catch trends earlier.\n2. **Support/Resistance**: Can act as dynamic support/resistance lines."
    },
    "HMA": {
        "title": "Hull Moving Average (HMA)",
        "definition": "Developed by Alan Hull, the Hull Moving Average (HMA) makes a moving average more responsive to current price activity while maintaining curve smoothness. It effectively eliminates lag and manages to improve smoothing at the same time.",
        "equation": r"$$ HMA = WMA(2 \times WMA(\frac{n}{2}) - WMA(n), \sqrt{n}) $$",
        "code": """```python
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go

# Calculate HMA
df['HMA_20'] = df.ta.hma(length=20)

fig = go.Figure()
fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='OHLC'))
fig.add_trace(go.Scatter(x=df.index, y=df['HMA_20'], mode='lines', name='HMA 20', line=dict(color='purple')))
fig.update_layout(title='Hull Moving Average', template='plotly_dark')
fig.show()
```""",
        "significance": "1. **Trend Reversal**: Due to its speed, the turning points of the HMA are often used as entry/exit signals.\n2. **Trend Filter**: If HMA is rising, trend is up; if falling, trend is down."
    },
    "VWAP": {
        "title": "Volume Weighted Average Price (VWAP)",
        "definition": "The Volume Weighted Average Price (VWAP) is a trading benchmark used by traders that gives the average price a security has traded at throughout the day, based on both volume and price. It provides insight into both the trend and the value of a security.",
        "equation": r"$$ VWAP = \frac{\sum (\text{Price} \times \text{Volume})}{\sum \text{Volume}} $$ \n\nTypically calculated cumulatively from the open of the trading session.",
        "code": """```python
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go

# Calculate VWAP
# Ensure index is datetime-like for pandas_ta if needed, or calculation resets daily
df.ta.vwap(append=True) # Adds column VWAP_D

fig = go.Figure()
fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='OHLC'))
fig.add_trace(go.Scatter(x=df.index, y=df['VWAP_D'], mode='lines', name='VWAP', line=dict(color='gold', dash='dot')))
fig.update_layout(title='VWAP Indicator', template='plotly_dark')
fig.show()
```""",
        "significance": "1. **Institutional Benchmark**: Institutions often use VWAP to gauge the quality of their executions.\n2. **Trend Confirmation**: Price above VWAP is bullish; below is bearish.\n3. **Support/Resistance**: Often acts as strong intraday support or resistance."
    },
    "SuperTrend": {
        "title": "SuperTrend",
        "definition": "SuperTrend is a trend-following indicator similar to moving averages. It is plotted on prices and their placement indicates the current trend. It relies on the Average True Range (ATR) to calculate its value.",
        "equation": r"$$ \text{Upper Band} = \frac{(\text{High} + \text{Low})}{2} + (\text{Multiplier} \times \text{ATR}) $$ \n$$ \text{Lower Band} = \frac{(\text{High} + \text{Low})}{2} - (\text{Multiplier} \times \text{ATR}) $$ \n\nThe SuperTrend line switches between Upper and Lower/Close depending on trend direction.",
        "code": """```python
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go

# Calculate SuperTrend (returns multiple columns usually SUPERT_7_3.0 etc)
st = df.ta.supertrend(length=7, multiplier=3)
# Extract the main trend line column (usually the first one or named SUPERT...)
st_line = st['SUPERT_7_3.0']

fig = go.Figure()
fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='OHLC'))
fig.add_trace(go.Scatter(x=df.index, y=st_line, mode='lines', name='SuperTrend', line=dict(color='green'))) # Color logic complex in static plot
fig.update_layout(title='SuperTrend', template='plotly_dark')
fig.show()
```""",
        "significance": "1. **Stop Loss**: Excellent for trailing stop losses.\n2. **Trend Direction**: Buying when the line flips to green (below price) and selling when it flips to red (above price)."
    },
    "Parabolic_SAR": {
        "title": "Parabolic SAR (Stop and Reverse)",
        "definition": "The Parabolic SAR is a price-and-time-based trading system designed to find potential reversals in the market price direction. It uses a trailing stop and reverse method called 'SAR', or 'Stop and Reverse'.",
        "equation": r"$$ SAR_{n+1} = SAR_n + \alpha (EP - SAR_n) $$ \n\nWhere:\n*   $\alpha$ is the acceleration factor (starts at 0.02, increases by 0.02 to max 0.2)\n*   $EP$ is the Extreme Point (highest high in uptrend, lowest low in downtrend)",
        "code": """```python
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go

# Calculate PSAR
psar = df.ta.psar() # Returns PSARl and PSARs columns usually combined
# We can combine for visualization or plot dots
# Simplification:
psar_vals = psar['PSARl_0.02_0.2'].combine_first(psar['PSARs_0.02_0.2'])

fig = go.Figure()
fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='OHLC'))
fig.add_trace(go.Scatter(x=df.index, y=psar_vals, mode='markers', name='Parabolic SAR', marker=dict(color='white', size=4)))
fig.update_layout(title='Parabolic SAR', template='plotly_dark')
fig.show()
```""",
        "significance": "1. **Trailing Stop**: The primary use is as a trailing stop loss.\n2. **Trend Reversal**: When price crosses the dots, a reversal is signaled."
    },
    "Ichimoku_Cloud": {
        "title": "Ichimoku Cloud (Ichimoku Kinko Hyo)",
        "definition": "The Ichimoku Cloud is a collection of technical indicators that show support and resistance levels, as well as momentum and trend direction. It does this by taking multiple averages and plotting them on the chart. It also uses these figures to compute a 'cloud' which attempts to forecast where the price may find support or resistance in the future.",
        "equation": r"$$ \text{Tenkan-sen} = \frac{(\text{9-period High} + \text{9-period Low})}{2} $$ \n$$ \text{Kijun-sen} = \frac{(\text{26-period High} + \text{26-period Low})}{2} $$ \n$$ \text{Senkou Span A} = \frac{(\text{Tenkan-sen} + \text{Kijun-sen})}{2} $$ \n$$ \text{Senkou Span B} = \frac{(\text{52-period High} + \text{52-period Low})}{2} $$ \n$$ \text{Chikou Span} = \text{Close plotted 26 periods back} $$",
        "code": """```python
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go

# Calculate Ichimoku
ichi = df.ta.ichimoku()
# ichi[0] contains the dataframes. 
# Typical columns: ISA_9_26_52, ISB_9_26_52, ITS_9_26_52, IKS, ICS

data = ichi[0]
span_a = data['ISA_9_26_52']
span_b = data['ISB_9_26_52']
tenkan = data['ITS_9_26_52']
kijun = data['IKS_9_26_52']

fig = go.Figure()
fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='OHLC'))

# Cloud
fig.add_trace(go.Scatter(x=df.index, y=span_a, line=dict(width=0), showlegend=False, hoverinfo='skip'))
fig.add_trace(go.Scatter(x=df.index, y=span_b, fill='tonexty', fillcolor='rgba(0, 250, 0, 0.2)', line=dict(width=0), name='Cloud'))

# Lines
fig.add_trace(go.Scatter(x=df.index, y=tenkan, line=dict(color='red', width=1), name='Tenkan-sen'))
fig.add_trace(go.Scatter(x=df.index, y=kijun, line=dict(color='blue', width=1), name='Kijun-sen'))

fig.update_layout(title='Ichimoku Cloud', template='plotly_dark')
fig.show()
```""",
        "significance": "1. **Trend Identification**: Price above cloud = uptrend, below = downtrend.\n2. **Kumo Breakout**: Breaking through the cloud is a strong continuation signal.\n3. **TK Cross**: Tenkan crossing Kijun is a signal similar to MA crossover (Tenkan = Fast, Kijun = Slow)."
    },
    "SMMA": {
        "title": "Smoothed Moving Average (SMMA)",
        "definition": "The Smoothed Moving Average (SMMA) is a moving average that gives equal weight to recent prices but over a much longer period than the SMA. It is equivalent to an EMA with a specific smoothing factor, effectively reducing noise.",
        "equation": r"$$ SMMA_i = \frac{\sum_{j=1}^{n} P_{i-j+1} - SMMA_{i-1} + P_i}{n} $$ \nOr simply synonymous with the RMA (Running Moving Average) used in RSI.",
        "code": """```python
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go

# Calculate SMMA / RMA
df['SMMA_20'] = df.ta.rma(length=20) 

fig = go.Figure()
fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='OHLC'))
fig.add_trace(go.Scatter(x=df.index, y=df['SMMA_20'], mode='lines', name='SMMA 20', line=dict(color='cyan')))
fig.update_layout(title='SMMA Indicator', template='plotly_dark')
fig.show()
```""",
        "significance": "1. **Long-term Trend**: Very slow to react, good for identifying long-term trend direction.\n2. **Support/Resistance**: Acts as a robust support line in established trends."
    },
    "KAMA": {
        "title": "Kaufman's Adaptive Moving Average (KAMA)",
        "definition": "Developed by Perry Kaufman, KAMA is an intelligent moving average that accounts for market noise or volatility. It moves closely to the price when noise is low (trends) and smooths out the noise when volatility is high.",
        "equation": r"$$ ER = \frac{|\text{Change}|}{\text{Volatility}} $$ \n$$ SC = [ER \times (\text{fast} - \text{slow}) + \text{slow}]^2 $$ \n$$ KAMA_t = KAMA_{t-1} + SC \times (Price - KAMA_{t-1}) $$",
        "code": """```python
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go

# Calculate KAMA
df['KAMA'] = df.ta.kama(length=10)

fig = go.Figure()
fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='OHLC'))
fig.add_trace(go.Scatter(x=df.index, y=df['KAMA'], mode='lines', name='KAMA', line=dict(color='magenta')))
fig.update_layout(title='KAMA Indicator', template='plotly_dark')
fig.show()
```""",
        "significance": "1. **Adaptive**: Automatically adjusts to market conditions.\n2. **Trend Filter**: Horizontal KAMA indicates ranging market; sloping KAMA indicates trend."
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
