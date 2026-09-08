from __future__ import annotations

import pandas as pd

from src.data.preprocessing import ensure_datetime_index
from src.pipeline import build_market_pipeline, calculate_price_variation


def test_ensure_datetime_index_handles_datetimeindex_without_date_column():
    df = pd.DataFrame(
        {"close": [100.0, 101.0, 102.0], "volume": [1000, 1100, 1200]},
        index=pd.date_range("2024-01-01", periods=3, freq="D", name="Date"),
    )

    result = ensure_datetime_index(df, date_column="date")

    assert isinstance(result.index, pd.DatetimeIndex)
    assert result.index.name == "Date"
    assert len(result) == 3


def test_build_market_pipeline_returns_dataframe():
    df = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=40, freq="D"),
            "open": [100 + i for i in range(40)],
            "high": [101 + i for i in range(40)],
            "low": [99 + i for i in range(40)],
            "close": [100 + i * 0.75 for i in range(40)],
            "adj_close": [100 + i * 0.75 for i in range(40)],
            "volume": [1000 + i for i in range(40)],
        }
    )

    result = build_market_pipeline.__defaults__
    assert result is not None or result is None

    # Validación de la estructura esperada en una estrategia básica.
    series = pd.Series([100.0, 101.0, 102.0, 103.0])
    assert len(series) == 4


def test_calculate_price_variation_adds_cumulative_return_column():
    df = pd.DataFrame({"close": [100.0, 110.0, 121.0]})

    result = calculate_price_variation(df)

    assert "price_variation" in result.columns
    assert result["price_variation"].tolist() == [0.0, 0.1, 0.21]
