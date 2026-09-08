from __future__ import annotations

import pandas as pd


def rolling_volatility(df: pd.DataFrame, window: int = 20, column: str = "Close") -> pd.Series:
    """Calcula volatilidad móvil."""
    returns = df[column].pct_change().dropna()
    return returns.rolling(window=window).std() * (252 ** 0.5)
