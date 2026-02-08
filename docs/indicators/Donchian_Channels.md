# Donchian Channels

| Name | Type | Prerequisite | Use Cases |
| :--- | :--- | :--- | :--- |
| Price Channel / Donchian (DC) | Structure/Trend | OHLC Data | Classic breakout trading (e.g., Turtle Trading). |

## Definition

Donchian Channels are formed by taking the highest high and the lowest low of the last n periods. The area between the high and the low is the Donchian Channel.

## Mathematical Equation

$$
\text{Upper Channel} = \max(\text{High}, n)
$$

 

$$
\text{Lower Channel} = \min(\text{Low}, n)
$$

 

$$
\text{Middle Channel} = \frac{\text{Upper} + \text{Lower}}{2}
$$

## Visualization

![Donchian_Channels](plots/Donchian_Channels.png)

## Trading Significance

1. **Breakouts**: New Highs (touching upper band) signal buy. New Lows (touching lower band) signal sell.

2. **Turtle Trading**: Famous Turtle Trading system used Donchian Channel breakouts.

