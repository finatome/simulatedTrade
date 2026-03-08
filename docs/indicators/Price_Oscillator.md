# Price Oscillator (PO)

| Name | Type | Prerequisite | Use Cases |
| :--- | :--- | :--- | :--- |
| Price Oscillator (PO) | Momentum | OHLC Data | Comparing momentum across different assets regardless of price level. |

## Definition

The percentage difference between two moving averages.

## Mathematical Equation

$$
(\frac{MA_{fast} - MA_{slow}}{MA_{slow}}) \times 100
$$

## Special cases

*   **Maximum possible value:** Unbounded
*   **Minimum possible value:** Unbounded
*   **Behavior:** Oscillates around zero based on the difference between two moving averages of price.

## Visualization

![Price Oscillator (PO)](plots/Price_Oscillator.png)

## Trading Significance

*   **Category**: Momentum

*   **Use Case**: Comparing momentum across different assets regardless of price level.

