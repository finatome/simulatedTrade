# Standard Error

| Name | Type | Prerequisite | Use Cases |
| :--- | :--- | :--- | :--- |
| Standard Error (SE) | Volatility/Statistics | StdDev | Gauging the consistency of a trend. |

## Definition

Standard Error measures the statistical accuracy of the linear regression estimate. It measures the dispersion of the price data around the linear regression line.

## Mathematical Equation

$$
SE = \sqrt{ \frac{\sum (y_i - \hat{y}_i)^2}{N} }
$$

Where $y_i$ is the actual price and $\hat{y}_i$ is the predicted price from the regression line.

## Visualization

![Standard Error](plots/Standard_Error.png)

## Trading Significance

1.  **Trend Reliability**: Low Standard Error indicates that prices are clustering closely to the regression line, suggesting a strong, reliable trend.

2.  **Volatility**: High Standard Error indicates high volatility and a less reliable trend structure.

