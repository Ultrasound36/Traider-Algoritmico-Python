from __future__ import annotations

import pandas as pd


def moving_average(df: pd.DataFrame, window: int = 20, column: str = "Close") -> pd.Series:
    """Calcula la media móvil simple."""
    return df[column].rolling(window=window).mean()
