from dash import html, dcc

INDICATOR_INFO = {
    # --- DEFAULT ---
    'SMA': {'name': 'Simple MA', 'category': 'Trend', 'math': r'$$SMA = \frac{\Sigma P_i}{N}$$', 'significance': 'The Simple Moving Average (SMA) smoothes out price data by calculating the average price over a specific number of periods. It helps identify the direction of the trend and often acts as a dynamic support or resistance level in trending markets.', 'color': '#2979FF'},
    'EMA': {'name': 'Exponential MA', 'category': 'Trend', 'math': r'$$EMA_t = P_t \cdot k + EMA_{t-1} (1-k)$$', 'significance': 'The Exponential Moving Average (EMA) places a greater weight and significance on the most recent data points. It reacts more significantly to recent price changes than the SMA, making it preferred by traders for capturing short-term trend reversals.', 'color': '#2979FF'},
    'BBM': {'name': 'Bollinger Bands', 'category': 'Volatility', 'math': r'$$Mid=SMA$$ $$Up/Lo=SMA\pm 2\sigma$$', 'significance': 'Bollinger Bands consist of a middle SMA and two outer bands representing standard deviation levels. Expanding bands indicate high volatility, while contracting bands (squeeze) suggest low volatility and a potential upcoming breakout.', 'color': '#00B8D9'},
    'SUPERT': {'name': 'Supertrend', 'category': 'Trend', 'math': r'$$HL/2 \pm m \cdot ATR$$', 'significance': 'Supertrend is a trend-following indicator based on Average True Range (ATR). It plots a line on the chart that changes color based on trend direction (Green for Up, Red for Down) and is widely used as a trailing stop-loss level.', 'color': '#00E676'},
    'MACD': {'name': 'MACD', 'category': 'Momentum', 'math': r'$$EMA_{12} - EMA_{26}$$', 'significance': 'The Moving Average Convergence Divergence (MACD) is a trend-following momentum indicator. It shows the relationship between two moving averages of a security’s price. Crossovers of the MACD and Signal line indicate buy/sell signals.', 'color': '#FF9100'},
    'RSI': {'name': 'RSI', 'category': 'Momentum', 'math': r'$$100 - \frac{100}{1+RS}$$', 'significance': 'The Relative Strength Index (RSI) is a momentum oscillator that measures the speed and change of price movements. Values above 70 indicate an overbought condition (potential sell), while values below 30 indicate oversold (potential buy).', 'color': '#AA00FF'},

    # --- FIRST ORDER ---
    'AVGPRICE': {'name': 'Average Price', 'category': 'Primitive', 'math': r'$$(H+L+C)/3$$', 'significance': 'Calculates the mean of the High, Low, and Close prices for a given period. It provides a simple smoothed view of the price action, filtering out some of the noise from extreme highs or lows.', 'color': '#FFF'},
    'MEDPRICE': {'name': 'Median Price', 'category': 'Primitive', 'math': r'$$(H+L)/2$$', 'significance': 'Represents the midpoint of the trading range for the period, calculated as the average of the High and Low. It focuses on the center of the trading activity, ignoring the closing price.', 'color': '#FFF'},
    'TYPPRICE': {'name': 'Typical Price', 'category': 'Primitive', 'math': r'$$(H+L+C)/3$$', 'significance': 'Also known as the Pivot Point, the Typical Price is the average of High, Low, and Close. It gives a more balanced view of the daily trading value than the Close alone and is used in many other indicators like CCI.', 'color': '#FFF'},
    'STDDEV': {'name': 'Standard Dev', 'category': 'Volatility', 'math': r'$$\sqrt{\frac{\Sigma(x-\bar{x})^2}{N}}$$', 'significance': 'Standard Deviation measures the dispersion of prices from their mean. High values indicate high volatility and significant price movement, while low values indicate calm, consolidating markets.', 'color': '#FF5252'},
    'HISTVOL': {'name': 'Historical Vol', 'category': 'Volatility', 'math': r'$$StdDev(LnRet) \cdot \sqrt{252}$$', 'significance': 'Historical Volatility quantifies the annualized standard deviation of log returns. It is a key metric for assessing the risk associated with the asset price moves over a specific timeframe.', 'color': '#FF5252'},
    'VOL': {'name': 'Volatility', 'category': 'Volatility', 'math': r'$$f(H,L,C,O)$$', 'significance': 'General volatility metrics derived from open, high, low, and close prices. These estimators (like Garman-Klass or Rogers-Satchell) provide more efficient volatility estimates than close-to-close calculations.', 'color': '#FF5252'},
    'ROC': {'name': 'Rate of Change', 'category': 'Momentum', 'math': r'$$\frac{P_t - P_{t-n}}{P_{t-n}} \cdot 100$$', 'significance': 'The Price Rate of Change (ROC) is a momentum oscillator that measures the percentage change in price between the current price and the price n periods ago. It highlights the velocity of the trend.', 'color': '#FFA726'},
    'MOM': {'name': 'Momentum', 'category': 'Momentum', 'math': r'$$P_t - P_{t-n}$$', 'significance': 'Momentum measures the absolute change in price over a set period. Positive values indicate an upward trend, while negative values indicate a downward trend. It is a leading indicator of weakness or strength.', 'color': '#FFA726'},
    'SPREAD': {'name': 'H-L Spread', 'category': 'Primitive', 'math': r'$$High - Low$$', 'significance': 'Calculate the absolute difference between the High and Low prices of the bar. It is a direct measure of intraday volatility and trading range.', 'color': '#FFF'},
    'RATIO': {'name': 'Price/SMA Ratio', 'category': 'Primitive', 'math': r'$$Price / SMA_{50}$$', 'significance': 'Measures how far the current price is extended from its 50-period moving average. High ratios may indicate an overextended trend susceptible to mean reversion.', 'color': '#FFF'},
    'NETVOL': {'name': 'Net Volume', 'category': 'Volume', 'math': r'$$Vol \cdot sign(C-O)$$', 'significance': 'Net Volume distinguishes between buying and selling volume. It assigns positive volume to up-days and negative volume to down-days, helping to identify the dominant market side.', 'color': '#69F0AE'},
    'FRACTAL': {'name': 'Fractals', 'category': 'Pattern', 'math': r'$$H_{i-2} < H_i > H_{i+2}$$', 'significance': 'Williams Fractals identify reversal points on the chart. An up-fractal occurs when a high is preceded and followed by two lower highs, signaling a potential bearish turn, and vice-versa.', 'color': '#E040FB'},

    # --- SECOND ORDER ---
    'WMA': {'name': 'Weighted MA', 'category': 'Smoothing', 'math': r'$$\frac{\Sigma (P_i \cdot i)}{\Sigma i}$$', 'significance': 'The Weighted Moving Average (WMA) assigns more weight to recent data points linearly. It reacts quicker to price changes than the SMA but is not as aggressive as the EMA.', 'color': '#448AFF'},
    'RMA': {'name': 'Smoothed MA', 'category': 'Smoothing', 'math': r'$$P_t/N + RMA_{t-1}(1-1/N)$$', 'significance': 'The Running Moving Average (RMA), also known as the Smoothed Moving Average (SMMA), is used in the calculation of RSI. It provides a very smooth curve that reacts slowly to price changes.', 'color': '#448AFF'},
    'ALMA': {'name': 'Arnaud Legoux MA', 'category': 'Smoothing', 'math': r'$$Gaussian Filter$$', 'significance': 'ALMA uses a Gaussian filter to act as a moving average. It offers the smoothness of an SMA with significantly reduced lag, making it superior for trend identification.', 'color': '#448AFF'},
    'HMA': {'name': 'Hull MA', 'category': 'Smoothing', 'math': r'$$WMA(2\cdot WMA(N/2) - WMA(N))$$', 'significance': 'The Hull Moving Average (HMA) is designed to eliminate lag while improving smoothness. It achieves this by using weighted moving averages of different lengths, providing a very responsive signal.', 'color': '#448AFF'},
    'LREG': {'name': 'Least Sq MA', 'category': 'Smoothing', 'math': r'$$LinReg_t(Endpoint)$$', 'significance': 'The Least Squares Moving Average (LSMA) calculates the endpoint of the linear regression line for each window. It attempts to predict what the value would be if the regression trend continued.', 'color': '#448AFF'},
    'VWMA': {'name': 'Volume Wtd MA', 'category': 'Smoothing', 'math': r'$$\frac{\Sigma (P \cdot V)}{\Sigma V}$$', 'significance': 'The Volume Weighted Moving Average (VWMA) weights prices by trading volume. It gives more importance to price moves that happen on high volume, effectively highlighting valid trends.', 'color': '#448AFF'},
    'HAMMING': {'name': 'Hamming MA', 'category': 'Smoothing', 'math': r'$$Signal \cdot Window_{Hamming}$$', 'significance': 'A moving average based on the Hamming window function from signal processing. It provides excellent smoothing properties by reducing spectral leakage compared to a simple boxcar average.', 'color': '#448AFF'},
    'KAMA': {'name': 'Kaufman Adaptive', 'category': 'Adaptive', 'math': r'$$EMA(ER \cdot (f-s) + s)^2$$', 'significance': 'Kaufman’s Adaptive Moving Average (KAMA) adjusts its smoothing factor based on market volatility. It follows prices closely when noise is low and smooths out the line when volatility increases.', 'color': '#FF4081'},

    # --- THIRD ORDER ---
    'MA': {'name': 'MA Cross', 'category': 'Oscillator', 'math': r'$$SMA_F - SMA_S$$', 'significance': 'Tracks the difference between a Fast and Slow SMA. Positive values suggest the fast MA is above the slow MA (Bullish), while negative values suggest the opposite (Bearish).', 'color': '#FFAB40'},
    'EMA': {'name': 'EMA Cross', 'category': 'Oscillator', 'math': r'$$EMA_F - EMA_S$$', 'significance': 'Tracks the difference between a Fast and Slow EMA. Due to EMAs reacting faster, this provides earlier crossover signals than simple MA crossovers.', 'color': '#FFAB40'},
    'PO': {'name': 'Price Osc', 'category': 'Oscillator', 'math': r'$$\frac{Fast - Slow}{Slow}$$', 'significance': 'The Percentage Price Oscillator (PPO) shows the relationship between two moving averages as a percentage. This allows for comparison and ranking of volatility across different assets.', 'color': '#FFAB40'},
    'BB': {'name': 'Bollinger Metrics', 'category': 'Volatility', 'math': r'$$\%B = \frac{C-L}{U-L}$$', 'significance': 'Bollinger %B tells you where the price is relative to the bands. 1.0 means price is at the upper band, 0.0 at the lower band. It is key for identifying overbought/oversold levels relative to volatility.', 'color': '#00B8D9'},
    'SEB': {'name': 'Std Err Bands', 'category': 'Channel', 'math': r'$$SMA \pm 2 \cdot StdErr$$', 'significance': 'Standard Error Bands plot lines above and below a Linear Regression line or SMA. They show the mathematical reliability of the trend; tight bands indicate a strong, consistent trend.', 'color': '#00B8D9'},
    'DCL': {'name': 'Donchian', 'category': 'Channel', 'math': r'$$Max(H, N) / Min(L, N)$$', 'significance': 'Donchian Channels plot the highest high and lowest low over the last N periods. They identify breakout levels and the current trading range clearly.', 'color': '#00B8D9'},
    'KC': {'name': 'Keltner', 'category': 'Channel', 'math': r'$$EMA \pm 2 \cdot ATR$$', 'significance': 'Keltner Channels are volatility-based envelopes set above and below an EMA using ATR. Unlike Bollinger Bands, they use ATR, so they don’t contract as violently, offering smoother trend guidance.', 'color': '#00B8D9'},
    'MACH': {'name': 'MA Channel', 'category': 'Channel', 'math': r'$$MA \pm \sigma$$', 'significance': 'A simple channel created by shifting a Moving Average up and down by a standard deviation factor. It creates a dynamic zone of expected price action around the mean.', 'color': '#00B8D9'},
    'ENV': {'name': 'Envelopes', 'category': 'Channel', 'math': r'$$MA \pm \%Band$$', 'significance': 'Moving Average Envelopes are lines plotted at a fixed percentage above and below a moving average. They help identify overextended price deviations from the mean trend.', 'color': '#00B8D9'},
    'DPO': {'name': 'Detrended Price', 'category': 'Oscillator', 'math': r'$$P - SMA(N/2+1)$$', 'significance': 'The Detrended Price Oscillator (DPO) removes the trend from price to estimate the length of price cycles. It peaks when prices reach the top of the cycle and troughs at the bottom.', 'color': '#7C4DFF'},
    'ATR': {'name': 'ATR', 'category': 'Volatility', 'math': r'$$Avg(Max(H-L, |H-C_p|...))$$', 'significance': 'The Average True Range (ATR) measures market volatility by decomposing the entire range of an asset price for that period. Higher ATR means higher volatility.', 'color': '#FF5252'},
    'CCI': {'name': 'CCI', 'category': 'Oscillator', 'math': r'$$\frac{TP - SMA}{0.015 \cdot MD}$$', 'significance': 'The Commodity Channel Index (CCI) measures the current price level relative to an average price level over a given period of time. High values indicate the price is unusually high compared to its average.', 'color': '#7C4DFF'},
    'STD': {'name': 'Std Error', 'category': 'Statistics', 'math': r'$$StdDev / \sqrt{N}$$', 'significance': 'Standard Error measures the accuracy with which a sample distribution represents a population. In trading, it quantifies how well the price fits the linear regression line.', 'color': '#9E9E9E'},
    'LINREG': {'name': 'LinReg Curve', 'category': 'Statistics', 'math': r'$$y = mx + b$$', 'significance': 'The Linear Regression Curve plots the end points of linear regression lines drawn over consecutive windows. It reduces noise and lag, following the "true" direction of the market.', 'color': '#9E9E9E'},
    'SLOPE': {'name': 'LinReg Slope', 'category': 'Statistics', 'math': r'$$Rise / Run$$', 'significance': 'Measures the rate of change of the Linear Regression line. A steep positive slope indicates a strong uptrend, while a steep negative slope indicates a strong downtrend.', 'color': '#9E9E9E'},

    # --- FOURTH ORDER ---
    'STOCHk': {'name': 'Stochastic', 'category': 'Momentum', 'math': r'$$\frac{C-L}{H-L} \cdot 100$$', 'significance': 'The Stochastic Oscillator compares a closing price to the price range over a specific period. It is used to generate overbought and oversold trading signals.', 'color': '#AA00FF'},
    'STOCHRSIk': {'name': 'Stoch RSI', 'category': 'Momentum', 'math': r'$$Stoch(RSI)$$', 'significance': 'Stochastic RSI applies the Stochastic formula to RSI values instead of price. It is more sensitive than standard RSI and moves faster between overbought and oversold levels.', 'color': '#AA00FF'},
    'SMI': {'name': 'SMI Ergodic', 'category': 'Momentum', 'math': r'$$TSI(Price)$$', 'significance': 'The SMI Ergodic Indicator is a double-smoothed True Strength Index. It acts as a reliable trend oscillator that is less prone to whipsaws than other momentum oscillators.', 'color': '#AA00FF'},
    'TSI': {'name': 'True Strength', 'category': 'Momentum', 'math': r'$$\frac{Sm(Sm(\Delta P))}{Sm(Sm(|\Delta P|))}$$', 'significance': 'The True Strength Index (TSI) uses double smoothing of price changes to identify trends and reversals. It highlights the underlying strength of the market move.', 'color': '#AA00FF'},
    'ADX': {'name': 'ADX', 'category': 'Trend', 'math': r'$$Avg(|DI+ - DI-| / Sum)$$', 'significance': 'The Average Directional Index (ADX) measures the strength of a trend, regardless of direction. Values above 25 indicate a strong trend, while values below 20 suggest a weak or ranging market.', 'color': '#00C853'},
    'AROONOSC': {'name': 'Aroon Osc', 'category': 'Trend', 'math': r'$$Up - Down$$', 'significance': 'The Aroon Oscillator measures the difference between Aroon Up and Aroon Down. It identifies whether the market is trending or range-bound and the strength of that trend.', 'color': '#00C853'},
    'AO': {'name': 'Awesome Osc', 'category': 'Momentum', 'math': r'$$SMA_5 - SMA_{34}$$', 'significance': 'The Awesome Oscillator (AO) calculates the difference between a 34-period and 5-period Simple Moving Average. It is used to measure market momentum and affirm trends.', 'color': '#FF6D00'},
    'AC': {'name': 'Accelerator', 'category': 'Momentum', 'math': r'$$AO - SMA(AO)$$', 'significance': 'The Accelerator Oscillator (AC) measures the acceleration or deceleration of the current driving force (AO). It changes direction before the price, serving as an early warning signal.', 'color': '#FF6D00'},
    'TRIX': {'name': 'TRIX', 'category': 'Momentum', 'math': r'$$ROC(EMA(EMA(EMA)))$$', 'significance': 'TRIX is a triple-smoothed exponential moving average oscillator. It filters out insignificant price movements and focuses on the underlying trend, acting as both a trend and momentum indicator.', 'color': '#FF6D00'},
    'COPC': {'name': 'Coppock', 'category': 'Momentum', 'math': r'$$WMA(ROC_L + ROC_S)$$', 'significance': 'The Coppock Curve is a long-term price momentum indicator used primarily to recognize major market bottoms and the start of a new bull market.', 'color': '#FF6D00'},
    'FISHERT': {'name': 'Fisher Xform', 'category': 'Cycles', 'math': r'$$0.5 \cdot \ln(\frac{1+X}{1-X})$$', 'significance': 'The Fisher Transform converts prices into a Gaussian normal distribution. It emphasizes extreme price movements, helping to identify turning points with sharp, distinct signals.', 'color': '#D500F9'},
    'RVI': {'name': 'Rel Vigor/Vol', 'category': 'Momentum', 'math': r'$$Close \approx Open$$', 'significance': 'The Relative Vigor Index (RVI) measures the conviction of a recent price action and likelihood of it continuing. It assumes prices close higher than they open in uptrends.', 'color': '#D500F9'},
    'CMO': {'name': 'Chande Mom', 'category': 'Momentum', 'math': r'$$\frac{\Sigma U - \Sigma D}{\Sigma U + \Sigma D}$$', 'significance': 'The Chande Momentum Oscillator (CMO) measures pure momentum by summing all recent gains and losses. It oscillates between -100 and +100 to identify overbought/oversold conditions.', 'color': '#AA00FF'},
    'UO': {'name': 'Ultimate Osc', 'category': 'Momentum', 'math': r'$$WtAvg(BP/TR)$$', 'significance': 'The Ultimate Oscillator combines short, medium, and long-term timeframes into a single oscillator. It aims to avoid the false divergence signals common in single-timeframe indicators.', 'color': '#AA00FF'},
    'VTXP': {'name': 'Vortex', 'category': 'Trend', 'math': r'$$VI+ / VI-$$', 'significance': 'The Vortex Indicator consists of two lines capturing positive and negative trend movements. Crossovers identify the start of a new trend and its direction.', 'color': '#00C853'},

    # --- FIFTH ORDER ---
    'VWAP': {'name': 'VWAP', 'category': 'Volume', 'math': r'$$\frac{\Sigma (P \cdot V)}{\Sigma V}$$', 'significance': 'The Volume Weighted Average Price (VWAP) is the average price a security has traded at throughout the day, based on both volume and price. It is a benchmark for institutional traders.', 'color': '#00E676'},
    'OBV': {'name': 'OBV', 'category': 'Volume', 'math': r'$$OBV_{prev} \pm Vol$$', 'significance': 'On-Balance Volume (OBV) uses volume flow to predict changes in stock price. It assumes that volume precedes price, so rising OBV confirms an uptrend.', 'color': '#00E676'},
    'MFI': {'name': 'Money Flow', 'category': 'Volume', 'math': r'$$100 - \frac{100}{1+MR}$$', 'significance': 'The Money Flow Index (MFI) is a volume-weighted RSI. It measures buying and selling pressure to identify overbought or oversold conditions influenced by volume.', 'color': '#00E676'},
    'CMF': {'name': 'Chaikin Flow', 'category': 'Volume', 'math': r'$$\frac{\Sigma AD}{\Sigma Vol}$$', 'significance': 'Chaikin Money Flow (CMF) measures the amount of Money Flow Volume over a specific period. It confirms the strength of a trend; positive values indicate buying pressure.', 'color': '#00E676'},
    'AD': {'name': 'Accum/Dist', 'category': 'Volume', 'math': r'$$Vol \cdot \frac{C-L - (H-C)}{H-L}$$', 'significance': 'The Accumulation/Distribution Line uses volume and price to determine whether a stock is being accumulated (bought) or distributed (sold). It helps spot divergences.', 'color': '#00E676'},
    'ADOSC': {'name': 'Chaikin Osc', 'category': 'Volume', 'math': r'$$EMA_3(AD) - EMA_{10}(AD)$$', 'significance': 'The Chaikin Oscillator is a momentum indicator for the Accumulation/Distribution Line. It anticipates changes in the A/D line, often leading price changes.', 'color': '#00E676'},
    'PVT': {'name': 'Price Vol Trend', 'category': 'Volume', 'math': r'$$PVT + Vol \cdot \%Chg$$', 'significance': 'Price Volume Trend (PVT) is similar to OBV but adjusts the cumulative volume by the percentage change in price, giving a more accurate picture of flow.', 'color': '#00E676'},
    'EFI': {'name': 'Force Index', 'category': 'Volume', 'math': r'$$\Delta P \cdot Vol$$', 'significance': 'Elder’s Force Index uses price change and volume to measure the power behind a move. It identifies potential turning points and trend confirmations.', 'color': '#00E676'},
    'EOM': {'name': 'Ease of Move', 'category': 'Volume', 'math': r'$$\frac{\Delta P}{Vol/Range}$$', 'significance': 'Ease of Movement (EOM) relates price change to volume and trading range. High values indicate prices are moving upward with little resistance (volume).', 'color': '#00E676'},
    'KVO': {'name': 'Klinger', 'category': 'Volume', 'math': r'$$VForce(Short) - VForce(Long)$$', 'significance': 'The Klinger Oscillator determines long-term trends of money flow while remaining sensitive enough to detect short-term fluctuations, predicting price reversals.', 'color': '#00E676'},
    'PVO': {'name': 'Pct Vol Osc', 'category': 'Volume', 'math': r'$$\frac{EMA_S(V) - EMA_L(V)}{EMA_L(V)}$$', 'significance': 'The Percentage Volume Oscillator (PVO) is a momentum oscillator for volume. It measures the difference between two volume moving averages as a percentage.', 'color': '#00E676'},

    # --- SIXTH ORDER ---
    'MCGD': {'name': 'McGinley', 'category': 'Adaptive', 'math': r'$$Mg_{prev} + \frac{P - Mg}{k \cdot (P/Mg)^4}$$', 'significance': 'The McGinley Dynamic is a smoothing indicator that looks like a moving average but tracks the market better. It minimizes lag and avoids the whipsaws common in standard MAs.', 'color': '#FF4081'},
    'PSARl': {'name': 'Parabolic SAR', 'category': 'Trend', 'math': r'$$SAR_{prev} + \alpha(EP - SAR)$$', 'significance': 'Parabolic SAR (Stop and Reverse) is a trend-following indicator that highlights potential reversals. The dots below price indicate an uptrend and are used as trailing stops.', 'color': '#FF4081'},
    'CHOP': {'name': 'Choppiness', 'category': 'Regime', 'math': r'$$Log_{10}(\Sigma TR / Range)$$', 'significance': 'The Choppiness Index determines if the market is trending or chopping (trading sideways). High values indicate consolidation, while low values indicate a strong directional trend.', 'color': '#607D8B'},
    'CHAIKIN': {'name': 'Chaikin Vol', 'category': 'Volatility', 'math': r'$$ROC(EMA(H-L))$$', 'significance': 'Chaikin Volatility measures the rate of change of the trading range. It helps identify tops and bottoms, as volatility often peaks at market reversals.', 'color': '#FF5252'},
    'CKSPl': {'name': 'Chande Kroll', 'category': 'Stop', 'math': r'$$High - x \cdot ATR$$', 'significance': 'The Chande Kroll Stop is a trend-following indicator that calculates stop-loss levels based on the Average True Range. It attempts to keep the stop loss from being triggered by volatility.', 'color': '#FF4081'},
    'ISA': {'name': 'Ichimoku', 'category': 'System', 'math': r'$$Tenkan/Kijun/Senkou$$', 'significance': 'Ichimoku Kinko Hyo is a versatile indicator that defines support and resistance, identifies trend direction, gauges momentum, and provides trading signals all in one view.', 'color': '#607D8B'},
    'GMMA': {'name': 'Guppy MMA', 'category': 'System', 'math': r'$$EMAs(3..15) vs EMAs(30..60)$$', 'significance': 'The Guppy Multiple Moving Average (GMMA) uses two groups of MAs (short-term and long-term) to identify the changing nature of the trend and the agreement between traders and investors.', 'color': '#2962FF'},
    'AG': {'name': 'Alligator', 'category': 'System', 'math': r'$$Jaw, Teeth, Lips$$', 'significance': 'Williams Alligator uses three smoothed moving averages to isolate trends. It follows the premise that markets only trend 15-30% of the time, helping traders stay out of choppy markets.', 'color': '#2E7D32'},
    'MASSI': {'name': 'Mass Index', 'category': 'Reversal', 'math': r'$$\Sigma \frac{EMA}{EMA(EMA)}$$', 'significance': 'The Mass Index detects trend reversals by identifying range bulges. It does not predict direction, but rather signals that the current trend is likely to reverse soon.', 'color': '#D500F9'},
}

def get_indicator_meta(ind_code):
    """
    Returns metadata for a given indicator code (e.g., SMA_20 -> SMA metadata).
    """
    # 1. Exact Match Check (if needed)
    
    # 2. Prefix Match
    prefix = ind_code.split('_')[0]
    
    # 3. Special Prefix Heuristics
    if 'BBM' in ind_code or 'BBL' in ind_code or 'BBU' in ind_code: prefix = 'BBM'
    if 'SUPERT' in ind_code: prefix = 'SUPERT'
    if 'FRACTAL' in ind_code: prefix = 'FRACTAL'
    if 'STOCHk' in ind_code: prefix = 'STOCHk'
    if 'STOCHRSI' in ind_code: prefix = 'STOCHRSIk'
    if 'RMA' in ind_code: prefix = 'RMA'
    if 'VWMA' in ind_code: prefix = 'VWMA'
    if 'TRIX' in ind_code: prefix = 'TRIX'
    if 'FISHERT' in ind_code: prefix = 'FISHERT'
    if 'PSAR' in ind_code: prefix = 'PSARl'
    if 'CKSP' in ind_code: prefix = 'CKSPl'
    if 'ISA' in ind_code: prefix = 'ISA'
    if 'AG_' in ind_code: prefix = 'AG'
    if 'MASSI' in ind_code: prefix = 'MASSI'
    
    # Return matched info or generic fallback
    info = INDICATOR_INFO.get(prefix)
    
    if not info:
        # Try generic substring matching for some tricky ones
        for key in INDICATOR_INFO:
            if key in ind_code:
                return INDICATOR_INFO[key]

        return {
            'name': ind_code,
            'category': 'Technical',
            'math': 'N/A',
            'significance': 'Custom Indicator',
            'color': '#555'
        }
    return info

def render_indicator_cards(selected_indicators):
    """
    Renders a list of cards for the selected indicators.
    """
    if not selected_indicators:
        return html.Div("No Indicators Selected", className='no-indicators-message')

    cards = []
    
    for ind in selected_indicators:
        meta = get_indicator_meta(ind)
        
        # Determine border color based on meta color if available, else default
        accent_color = meta.get('color', 'var(--accent-cyan)')
        
        card = html.Div([
            # Header
            html.Div([
                html.H4(meta['name'], className='card-title', style={'color': accent_color}),
                html.Span(meta['category'], className='card-category')
            ], className='card-header'),
            
            # Math Section
            html.Div([
                dcc.Markdown(meta['math'], mathjax=True, className='markdown-math', style={'fontSize': '0.85rem'})
            ], className='card-math'),
            
            # Significance
            html.Div([
                html.P(meta['significance'], className='card-significance')
            ])
        ], className='indicator-card', style={'borderLeftColor': accent_color})
        
        cards.append(card)
        
    # The wrapper is already defined in CSS grid, so we just return the list of cards directly?
    # No, app.py expects a children list or a container. app.py puts this INTO #indicator-cards-wrapper.
    # So we should return the LIST of formatting cards, OR a Div that contains them?
    # app.py matches `Output('indicator-cards-wrapper', 'children')`.
    # So we should return a LIST of components if possible. 
    # Dash callbacks can return a list of components for 'children'.
    # HOWEVER, render_indicator_cards previously returned a Div.
    # Let's verify `controls.py`.
    # `html.Div(id="indicator-cards-wrapper")`
    # If we return a list, Dash puts them as children. Perfect.
    
    return cards
