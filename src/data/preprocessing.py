from __future__ import annotations

import pandas as pd


def _normalize_column_name(column: object) -> str:
    """Normaliza nombres de columnas, incluyendo MultiIndex de Yahoo Finance."""
    if isinstance(column, tuple):
        parts = [
            str(part).strip().lower().replace(" ", "_")
            for part in column
            if part not in (None, "")
        ]
        return parts[0] if parts else "unnamed"

    return str(column).strip().lower().replace(" ", "_")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza nombres de columnas a formato estándar."""
    df = df.copy()
    columns = []
    for col in df.columns:
        name = _normalize_column_name(col)
        if name in {"date", "open", "high", "low", "close", "adj_close", "volume"}:
            columns.append(name)
            continue

        known_prefixes = ("adj_close", "close", "open", "high", "low", "volume")
        for prefix in sorted(known_prefixes, key=len, reverse=True):
            if name.startswith(f"{prefix}_") and len(name.split("_")) >= 2:
                columns.append(prefix)
                break
        else:
            columns.append(name)

    df.columns = columns
    return df


def ensure_datetime_index(df: pd.DataFrame, date_column: str = "date") -> pd.DataFrame:
    df = df.copy()

    if date_column in df.columns:
        df[date_column] = pd.to_datetime(df[date_column])
        df = df.sort_values(date_column).set_index(date_column)
        return df

    if isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        return df

    if hasattr(df.index, "name") and str(df.index.name).lower() == date_column:
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        return df

    raise KeyError(f"No se encontró la columna '{date_column}' ni un índice datetime.")
