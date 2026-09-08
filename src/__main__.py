import datetime as dt
from pathlib import Path

from src.pipeline import build_market_pipeline, summarize_ticker_metrics
from src.utils.paths import CSV_DIR, GRAFICOS_DIR
from src.visualization.charts import plot_rsi_chart, plot_signal_chart


start_date = '2026-01-01'
end_date = '2026-08-28'
asset = 'EURUSD=X'

if __name__ == "__main__":
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    GRAFICOS_DIR.mkdir(parents=True, exist_ok=True)

    tipo_divisa = f"{asset[:3]}-{asset[3:6]}"
    file_name = f"{tipo_divisa}_{start_date}_to_{end_date}_{dt.datetime.now().strftime('%H:%M:%S')}.csv"

    try:
        df = build_market_pipeline(
            ticker=asset,
            start=start_date,
            end=end_date,
            export_path=CSV_DIR / file_name,
        )
        print(f"Datos de {asset} guardados en {CSV_DIR}")
    except Exception as e:
        print(f"Error al descargar o guardar los datos: {e}")
        raise

    summary = summarize_ticker_metrics(df, ticker=asset)
    print("Resumen financiero:", summary)
    print("Archivo guardado en:", CSV_DIR)
    print(df[["close", "short_ma", "long_ma", "signal", "buy_signal", "sell_signal", "position", "rsi"]].tail())

    plot_signal_chart(df, save_path=GRAFICOS_DIR / f"{tipo_divisa}_signals_{start_date}_to_{end_date}.png")
    plot_rsi_chart(df, save_path=GRAFICOS_DIR / f"{tipo_divisa}_rsi_{start_date}_to_{end_date}.png")