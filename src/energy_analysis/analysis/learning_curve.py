"""
Compute cost adjustment based on cumulative capacity using a simple learning curve.
"""

from typing import Iterable
import pandas as pd
import numpy as np

def learning_curve(
    costs: Iterable[float],
    cumulative_capacities: Iterable[float],
    learning_rate: float = 0.1
) -> pd.Series:
    """
    Apply a basic learning curve:
      adjusted_cost = original_cost * (base_capacity / current_capacity) ** learning_rate

    - costs: sequence of cost values.
    - cumulative_capacities: matching sequence of cumulative capacity values.
    - learning_rate: exponent factor (e.g., 0.1 for 10% learning).
    """
    costs = pd.Series(costs)
    cum = pd.Series(cumulative_capacities).replace(0, np.nan).fillna(method="bfill").fillna(1.0)
    base_cap = cum.iloc[0] if cum.iloc[0] > 0 else 1.0
    adjusted = costs * (base_cap / cum) ** learning_rate
    return adjusted