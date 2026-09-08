from __future__ import annotations

import pandas as pd

from src.data.loaders import load_csv


def test_load_csv_returns_dataframe(tmp_path):
    file_path = tmp_path / "sample.csv"
    pd.DataFrame({"date": ["2024-01-01", "2024-01-02"], "close": [100, 101]}).to_csv(file_path, index=False)

    df = load_csv(file_path)

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["date", "close"]
    assert len(df) == 2
