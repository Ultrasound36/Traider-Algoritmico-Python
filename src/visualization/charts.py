from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_price_line(df: pd.DataFrame, column: str = "close", title: str = "Precio") -> None:
    """Dibuja la serie de precio para revisar la tendencia principal."""
    # 1) Selecciona la columna de precio que se quiere visualizar.
    series = df[column]

    # 2) Genera un gráfico simple con el precio de cierre a lo largo del tiempo.
    series.plot(title=title, figsize=(12, 5), linewidth=2)
    plt.xlabel("Fecha")
    plt.ylabel("Precio")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_signal_chart(
    df: pd.DataFrame,
    close_column: str = "close",
    short_column: str = "short_ma",
    long_column: str = "long_ma",
    signal_column: str = "signal",
    save_path: str | Path | None = None,
) -> None:
    """Plotea precio, medias móviles y señales de compra/venta en una misma gráfica."""
    # 1) Se crea una copia para no alterar los datos originales del DataFrame.
    chart_df = df.copy()

    # 2) Se definen los puntos de compra/venta a partir del valor del signal.
    buy_points = chart_df[chart_df[signal_column] == 1]
    sell_points = chart_df[chart_df[signal_column] == -1]

    # 3) Se dibujan la serie de precio y las medias móviles.
    plt.figure(figsize=(14, 7))
    plt.plot(chart_df.index, chart_df[close_column], label="Precio", linewidth=2)
    plt.plot(chart_df.index, chart_df[short_column], label="Media corta", linewidth=1.5)
    plt.plot(chart_df.index, chart_df[long_column], label="Media larga", linewidth=1.5)

    # 4) Se marcan compras con flecha verde y ventas con flecha roja.
    if not buy_points.empty:
        plt.scatter(buy_points.index, buy_points[close_column], marker="^", color="green", s=100, label="Compra")
    if not sell_points.empty:
        plt.scatter(sell_points.index, sell_points[close_column], marker="v", color="red", s=100, label="Venta")

    plt.title("Señales de estrategia: precio y medias móviles")
    plt.xlabel("Fecha")
    plt.ylabel("Precio")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    # 5) Guarda el gráfico si se indicó una ruta; si no, solo muestra la figura.
    if save_path is not None:
        output = Path(save_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output, dpi=200)

    plt.show()


def plot_rsi_chart(df: pd.DataFrame, rsi_column: str = "rsi", save_path: str | Path | None = None) -> None:
    """Muestra el RSI con umbrales de sobrecompra y sobreventa para facilitar la lectura."""
    # 1) Se prepara el gráfico del indicador RSI.
    plt.figure(figsize=(14, 4))
    plt.plot(df.index, df[rsi_column], color="purple", linewidth=2, label="RSI")

    # 2) Se dibujan líneas guía para 30 y 70, que son los puntos típicos de compra/venta.
    plt.axhline(70, color="red", linestyle="--", alpha=0.7, label="Sobrecompra (70)")
    plt.axhline(30, color="green", linestyle="--", alpha=0.7, label="Sobreventa (30)")

    plt.title("Indicador RSI")
    plt.xlabel("Fecha")
    plt.ylabel("RSI")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_path is not None:
        output = Path(save_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output, dpi=200)

    plt.show()
