# Chaikin Volatility (CVI)

| Name | Type | Prerequisite | Use Cases |
| :--- | :--- | :--- | :--- |
| Chaikin Volatility (CV) | Volatility | EMA | Identifying volatility peaks that lead to reversals. |

## Definition

Chaikin Volatility (CVI) is an indicator that calculates the volatility of a security by measuring the percent change in the high-low range over a specified period. It was developed by Marc Chaikin. It is different from Average True Range (ATR) because it does not account for gaps.

## Mathematical Equation

1.  Calculate the High-Low range for each period: $HL = High - Low$

2.  Calculate an $N$-period EMA of the HL range: $EMA_{HL}$

3.  Calculate the percent change of the EMA over $M$ periods (usually 10):

    

$$
CVI = \frac{EMA_{HL}(t) - EMA_{HL}(t-M)}{EMA_{HL}(t-M)} \times 100
$$

## Visualization

![Chaikin Volatility](plots/Chaikin_Volatility.png)

## Trading Significance

1.  **Volatility Expansion/Contraction**: High values indicate high volatility (expansion), while low values indicate low volatility (contraction).

2.  **Tops and Bottoms**: Sharp increases in volatility often coincide with market tops or bottoms. A rapid decline in volatility may signal a consolidation period.

