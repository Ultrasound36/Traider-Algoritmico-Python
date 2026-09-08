from __future__ import annotations

import pandas as pd
import yfinance as yf


def _normalize_yahoo_column(column: object) -> str:
    """Normaliza columnas de Yahoo Finance, incluida la estructura MultiIndex."""
    if isinstance(column, tuple):
        parts = [
            str(part).strip().lower().replace(" ", "_")
            for part in column
            if part not in (None, "")
        ]
        if not parts:
            return "unnamed"
        if len(parts) == 1:
            return parts[0]
        return "_".join(parts)

    return str(column).strip().lower().replace(" ", "_")


def download_history(ticker: str, start: str, end: str | None = None, interval: str = "1d") -> pd.DataFrame:
    """Descarga historial de precios desde Yahoo Finance."""
    data = yf.download(ticker, start=start, end=end, interval=interval, progress=False, auto_adjust=False)
    if data.empty:
        raise ValueError(f"No se encontraron datos para el ticker {ticker}")
    data = data.reset_index()
    data.columns = [_normalize_yahoo_column(col) for col in data.columns]
    return data
