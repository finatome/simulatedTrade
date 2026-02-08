# Ease of Movement (EOM)

| Name | Type | Prerequisite | Use Cases |
| :--- | :--- | :--- | :--- |
| Ease of Movement (EOM) | Volume | OHLC Data | Identifying trends that require very little volume to persist. |

## Definition

Ease of Movement (EOM) is a volume-based oscillator developed by Richard Arms. It evaluates the relationship between price change and volume. It is designed to show how much volume is required to move the price. High EOM values essentially mean that the price moved with little volume resistance.

## Mathematical Equation

$$
\text{Distance Moved} = \frac{High + Low}{2} - \frac{High_{prev} + Low_{prev}}{2}
$$

$$
\text{Box Ratio} = \frac{Volume}{High - Low}
$$

$$
EOM = \frac{\text{Distance Moved}}{\text{Box Ratio}}
$$

Usually, a smoothed moving average of the EOM is plotted.

## Visualization

![Ease of Movement](plots/Ease_of_Movement.png)

## Trading Significance

1.  **Trend Strength**: High positive values indicate prices are advancing with ease (low volume resistance), suggesting a strong bullish trend.

2.  **Trend Weakness**: Low negative values indicate prices are declining with ease.

3.  **Zero Line**: Moves above zero are buy signals; moves below zero are sell signals.

