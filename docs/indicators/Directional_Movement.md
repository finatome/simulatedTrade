# Directional Movement (DM)

| Name | Type | Prerequisite | Use Cases |
| :--- | :--- | :--- | :--- |
| Directional Movement (DM) | Momentum | OHLC Data | Building block for trend-strength indicators. |

## Definition

Directional Movement (DM) consists of two components: +DM (Positive Directional Movement) and -DM (Negative Directional Movement). It is the foundational calculation for the ADX indicator.

## Mathematical Equation

*   **+DM**: Current High - Previous High (if > 0 and > |Low - Prev Low|)

*   **-DM**: Previous Low - Current Low (if > 0 and > |High - Prev High|)

## Special cases

*   **Maximum possible value:** 100
*   **Minimum possible value:** 0
*   **Behavior:** Oscillates between 0 and 100 for both +DI and -DI lines to determine trend direction.

## Trading Significance

1.  **Direction**: If +DM is above -DM, the trend is up.

