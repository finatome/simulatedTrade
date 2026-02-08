# SMI Ergodic

| Name | Type | Prerequisite | Use Cases |
| :--- | :--- | :--- | :--- |
| SMI Ergodic Indicator (SMI) | Momentum | EMA | Providing smoother, more reliable signals than standard Stochastics. |

## Definition

The SMI Ergodic Indicator (Stochastic Momentum Index) is a double-smoothed variation of the True Strength Index (TSI). It is used to spot trend direction and reversals. It includes a signal line for crossovers.

## Mathematical Equation

Derived from the Stochastic Momentum Index (SMI):

$$
SMI = \frac{\text{DoubleSmooth}(Close - \frac{High+Low}{2})}{\text{DoubleSmooth}(\frac{High-Low}{2})}
$$

The Ergodic version typically uses specific smoothing periods suitable for trend following.

## Visualization

![SMI Ergodic](plots/SMI_Ergodic.png)

## Trading Significance

1.  **Crossovers**:

    *   **Buy**: SMI (Main) crosses above Signal line.

    *   **Sell**: SMI (Main) crosses below Signal line.

2.  **Zero Line**: Crossing zero confirms trend direction.

