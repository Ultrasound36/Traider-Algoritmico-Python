from __future__ import annotations

import pandas as pd


def cumulative_return(prices: pd.Series) -> pd.Series:
    """Retorno acumulado sobre una serie de precios."""
    return (prices / prices.iloc[0]) - 1
