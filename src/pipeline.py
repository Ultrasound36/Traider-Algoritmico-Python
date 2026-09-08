from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.analysis.metrics import cumulative_return
from src.data.providers.yahoo_finance import download_history
from src.data.preprocessing import ensure_datetime_index, normalize_columns
from src.indicators.moving_average import moving_average
from src.strategies.simple_moving_average import moving_average_strategy, rsi_strategy


def export_market_data(df: pd.DataFrame, output_path: str | Path) -> Path:
    """Guarda el DataFrame final en CSV para inspección y uso posterior."""
    # 1) Creo la carpeta de salida si no existe.
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    # 2) Exporto con el índice de fecha como parte de la tabla para preservar el tiempo.
    df.to_csv(path)
    return path


def calculate_price_variation(df: pd.DataFrame, price_column: str = "close") -> pd.DataFrame:
    """Añade la variación acumulada del precio respecto al primer valor observado."""
    if price_column not in df.columns:
        raise KeyError(f"La columna '{price_column}' no existe en el DataFrame.")

    result = df.copy()
    result["price_variation"] = cumulative_return(result[price_column]).round(10)
    return result


def summarize_ticker_metrics(df: pd.DataFrame, ticker: str) -> dict[str, float | int | str]:
    """Resume el estado financiero del ticker con métricas rápidas y legibles."""
    # 1) Se toma el primer y último precio para calcular rendimiento desde inicio del período.
    first_close = float(df["close"].iloc[0]) if not df.empty else 0.0
    last_close = float(df["close"].iloc[-1]) if not df.empty else 0.0

    if "price_variation" in df.columns and not df.empty:
        performance = float(df["price_variation"].iloc[-1]) * 100
    else:
        performance = ((last_close / first_close) - 1) * 100 if first_close else 0.0

    # 2) Se resumen volumen medio y último valor de RSI para evaluar fuerza del movimiento.
    avg_volume = float(df["volume"].mean()) if "volume" in df.columns and not df.empty else 0.0
    last_rsi = float(df["rsi"].iloc[-1]) if "rsi" in df.columns and not df.empty else 50.0
    last_signal = int(df["signal"].iloc[-1]) if "signal" in df.columns and not df.empty else 0

    # 3) Se devuelven valores útiles para análisis rápido y reportes.
    return {
        "ticker": ticker.upper(),
        "first_close": round(first_close, 2),
        "last_close": round(last_close, 2),
        "performance_pct": round(performance, 2),
        "avg_volume": round(avg_volume, 2),
        "last_rsi": round(last_rsi, 2),
        "last_signal": last_signal,
    }


def build_market_pipeline(
    ticker: str,
    start: str,
    end: str | None = None,
    export_path: str | Path | None = None,
) -> pd.DataFrame:
    """Flujo completo del análisis: descarga, limpia, calcula indicadores y genera señales.

    El proceso hace lo siguiente:
    1) descarga datos reales desde Yahoo Finance,
    2) normaliza columnas a nombres estándar,
    3) convierte la fecha a índice datetime,
    4) calcula medias móviles y RSI,
    5) genera señales de compra/venta,
    6) opcionalmente exporta a CSV.
    """
    # 1) Descarga el historial OHLCV del ticker solicitado.
    df = download_history(ticker=ticker, start=start, end=end)

    # 2) Ajusta nombres de columnas para que el resto del pipeline no dependa del origen.
    df = normalize_columns(df)
    df = ensure_datetime_index(df, date_column="date")

    # 3) La columna close es la base del análisis. Si no existe, falla explícitamente.
    if "close" not in df.columns:
        raise KeyError("La columna 'close' no existe en los datos descargados.")

    # 4) Calcula la variación acumulada del precio respecto al primer valor para revisar la evolución.
    df = calculate_price_variation(df, price_column="close")

    # 5) Cálculo de medias móviles para detectar tendencia y cruces.
    df["short_ma"] = moving_average(df, window=10, column="close")
    df["long_ma"] = moving_average(df, window=30, column="close")

    # 5) Genera señales de compra/venta con una lógica de cruce de medias.
    df = moving_average_strategy(df, short_window=10, long_window=30, price_column="close")

    # 6) Añade indicador RSI para validar fuerza del movimiento antes de operar.
    df = rsi_strategy(df, period=14, price_column="close")

    # 7) Exporta a CSV si se especificó una ruta de salida.
    if export_path is not None:
        export_market_data(df, export_path)

    return df
