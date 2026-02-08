
import os

docs_dir = "docs/indicators"

indicators_data = {
    "MFI": {
        "title": "Money Flow Index (MFI)",
        "definition": "The Money Flow Index (MFI) is a technical oscillator that uses price and volume data for identifying overbought or oversold signals in an asset. It can also be used to spot divergences which warn of a trend change in price.",
        "equation": r"$$ \text{Typical Price} = \frac{\text{High} + \text{Low} + \text{Close}}{3} $$ \n$$ \text{Raw Money Flow} = \text{Typical Price} \times \text{Volume} $$ \n$$ \text{Money Flow Ratio} = \frac{\text{14-period Positive Money Flow}}{\text{14-period Negative Money Flow}} $$ \n$$ MFI = 100 - \frac{100}{1 + \text{Money Flow Ratio}} $$",
        "code": """```python
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Calculate MFI
mfi = df.ta.mfi(length=14)

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3])

fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='OHLC'), row=1, col=1)

fig.add_trace(go.Scatter(x=df.index, y=mfi, mode='lines', name='MFI', line=dict(color='orange')), row=2, col=1)

fig.add_hline(y=80, line_dash="dash", line_color="red", row=2, col=1)
fig.add_hline(y=20, line_dash="dash", line_color="green", row=2, col=1)

fig.update_layout(title='Money Flow Index (MFI)', template='plotly_dark')
fig.show()
```""",
        "significance": "1. **Overbought/Oversold**: MFI > 80 is overbought, < 20 is oversold.\n2. **Divergence**: Price making new highs but MFI failing to surpass 80 signals a reversal."
    },
    "CMF": {
        "title": "Chaikin Money Flow (CMF)",
        "definition": "Chaikin Money Flow (CMF) measures the amount of Money Flow Volume over a specific period. CMF sums Money Flow Volume over a specific look-back period, typically 20 or 21 days.",
        "equation": r"$$ \text{MF Multiplier} = \frac{(\text{Close} - \text{Low}) - (\text{High} - \text{Close})}{\text{High} - \text{Low}} $$ \n$$ \text{MF Volume} = \text{MF Multiplier} \times \text{Volume} $$ \n$$ \text{CMF} = \frac{\sum \text{MF Volume}}{\sum \text{Volume}} $$",
        "code": """```python
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Calculate CMF
cmf = df.ta.cmf(length=20)

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3])

fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='OHLC'), row=1, col=1)

fig.add_trace(go.Scatter(x=df.index, y=cmf, mode='lines', name='CMF', line=dict(color='green')), row=2, col=1)

fig.add_hline(y=0, line_color="white", row=2, col=1)

fig.update_layout(title='Chaikin Money Flow (CMF)', template='plotly_dark')
fig.show()
```""",
        "significance": "1. **Buying/Selling Pressure**: CMF > 0 indicates buying pressure. CMF < 0 indicates selling pressure.\n2. **Confirmation**: Rising prices with rising CMF confirms uptrend."
    },
    "EFI": {
        "title": "Elder's Force Index (EFI)",
        "definition": "The Force Index is an indicator that uses price and volume to assess the power behind a move or identify possible turning points.",
        "equation": r"$$ \text{Force Index} = (\text{Close}_{\text{current}} - \text{Close}_{\text{prev}}) \times \text{Volume}_{\text{current}} $$ \n\nThe result is typically smoothed with an EMA (e.g., 2-period or 13-period).",
        "code": """```python
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Calculate EFI
efi = df.ta.efi(length=13)

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3])

fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='OHLC'), row=1, col=1)

fig.add_trace(go.Scatter(x=df.index, y=efi, mode='lines', name='EFI', line=dict(color='cyan')), row=2, col=1)

fig.add_hline(y=0, line_color="white", row=2, col=1)

fig.update_layout(title="Elder's Force Index", template='plotly_dark')
fig.show()
```""",
        "significance": "1. **Trend Confirmation**: Force Index confirms the trend. Positive values confirm uptrends; negative values confirm downtrends.\n2. **Divergence**: Divergences between 13-day EMA of Force Index and price often signal reversals."
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
