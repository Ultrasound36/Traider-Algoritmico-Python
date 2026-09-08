from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_csv(file_path: str | Path) -> pd.DataFrame:
    """Carga un CSV y devuelve un DataFrame."""
    return pd.read_csv(file_path)
