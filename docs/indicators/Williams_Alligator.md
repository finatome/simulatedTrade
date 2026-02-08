# Williams Alligator

| Name | Type | Prerequisite | Use Cases |
| :--- | :--- | :--- | :--- |
| Williams Alligator (ALLI) | Trend/Regime | SMA | Identifying "sleep" (range) and "hunger" (trend) phases. |

## Definition

The Williams Alligator indicator uses three smoothed moving averages, set at specific periods and offsets, to identify trends. The lines are metaphorical:

*   **Jaw (Blue)**: 13-period SMMA, shifted 8 bars into future.

*   **Teeth (Red)**: 8-period SMMA, shifted 5 bars.

*   **Lips (Green)**: 5-period SMMA, shifted 3 bars.

## Visualization

![Williams Alligator](plots/Williams_Alligator.png)

## Trading Significance

1.  **Sleeping**: When lines are intertwined, the market is range-bound (Alligator is sleeping).

2.  **Awakening**: When lines separate, a trend is beginning (Alligator is feeding).

3.  **Trend Direction**:

    *   **Uptrend**: Green > Red > Blue.

    *   **Downtrend**: Blue > Red > Green.

