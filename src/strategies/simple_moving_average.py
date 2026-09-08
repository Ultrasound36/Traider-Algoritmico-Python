from __future__ import annotations

import pandas as pd


def moving_average_strategy(
    df: pd.DataFrame,
    short_window: int = 10,
    long_window: int = 30,
    price_column: str = "close",
) -> pd.DataFrame:
    """Genera señales útiles de compra/venta usando un cruce de medias móviles.

    Regla práctica:
    - Compra cuando la media corta cruza por encima de la media larga.
    - Venta cuando la media corta cruza por debajo de la media larga.
    - position indica si el sistema está posicionado (1) o en cash (0).
    """
    strategy_df = df.copy()

    # 1) Calculamos dos medias móviles para detectar tendencias y cambios de dirección.
    strategy_df["short_ma"] = strategy_df[price_column].rolling(window=short_window).mean()
    strategy_df["long_ma"] = strategy_df[price_column].rolling(window=long_window).mean()

    # 2) El estado inicial es neutral. No operamos hasta detectar un cruce real.
    strategy_df["signal"] = 0

    # 3) Compra: la media corta pasa por encima de la larga y antes no estaba alcista.
    buy_condition = (
        (strategy_df["short_ma"] > strategy_df["long_ma"]) &
        (strategy_df["short_ma"].shift(1) <= strategy_df["long_ma"].shift(1))
    )
    strategy_df.loc[buy_condition, "signal"] = 1

    # 4) Venta: la media corta pasa por debajo de la larga y antes no estaba bajista.
    sell_condition = (
        (strategy_df["short_ma"] < strategy_df["long_ma"]) &
        (strategy_df["short_ma"].shift(1) >= strategy_df["long_ma"].shift(1))
    )
    strategy_df.loc[sell_condition, "signal"] = -1

    # 5) position mantiene la exposición actual: 1 = largo, 0 = fuera del mercado.
    strategy_df["position"] = strategy_df["signal"].shift(1).fillna(0).clip(lower=0, upper=1)

    # 6) Se exponen señales binarias para facilitar análisis posterior.
    strategy_df["buy_signal"] = (strategy_df["signal"] == 1).astype(int)
    strategy_df["sell_signal"] = (strategy_df["signal"] == -1).astype(int)
    return strategy_df


def relative_strength_index(
    df: pd.DataFrame,
    period: int = 14,
    price_column: str = "close",
) -> pd.Series:
    """Calcula el RSI para detectar niveles de sobrecompra y sobreventa."""
    # 1) Se toma el cambio del precio para medir velocidad y dirección del movimiento.
    delta = df[price_column].diff()

    # 2) Se separan ganancias y pérdidas para evaluar impulso al alza y a la baja.
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    # 3) Se suavizan los valores con media exponencial para evitar ruido excesivo.
    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()

    # 4) El ratio de fuerza relativo compara el impulso de ganancias vs pérdidas.
    rs = avg_gain / avg_loss.replace(0, pd.NA)

    # 5) El RSI normaliza a 0-100, siendo 70 sobrecompra y 30 sobreventa.
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)


def rsi_strategy(df: pd.DataFrame, period: int = 14, price_column: str = "close") -> pd.DataFrame:
    """Crea una estrategia basada en RSI con señales de compra y venta claras."""
    strategy_df = df.copy()

    # 1) Se calcula el RSI para cada dato del histórico.
    strategy_df["rsi"] = relative_strength_index(strategy_df, period=period, price_column=price_column)

    # 2) Señal de compra: RSI cae por debajo de 30 y luego asciende.
    buy_condition = (strategy_df["rsi"] < 30) & (strategy_df["rsi"].shift(1) >= 30)
    strategy_df["rsi_signal"] = 0
    strategy_df.loc[buy_condition, "rsi_signal"] = 1

    # 3) Señal de venta: RSI sube por encima de 70 y luego desciende.
    sell_condition = (strategy_df["rsi"] > 70) & (strategy_df["rsi"].shift(1) <= 70)
    strategy_df.loc[sell_condition, "rsi_signal"] = -1

    # 4) Se mantienen valores binarios para ser fáciles de interpretar en análisis.
    strategy_df["rsi_buy_signal"] = (strategy_df["rsi_signal"] == 1).astype(int)
    strategy_df["rsi_sell_signal"] = (strategy_df["rsi_signal"] == -1).astype(int)
    return strategy_df


def signal_summary(df: pd.DataFrame) -> dict[str, int | float]:
    """Resuma cuántas señales de compra y venta tuvo la estrategia."""
    buy_signals = int((df["signal"] == 1).sum())
    sell_signals = int((df["signal"] == -1).sum())
    last_position = int(df["position"].iloc[-1]) if not df.empty else 0
    return {
        "buy_signals": buy_signals,
        "sell_signals": sell_signals,
        "last_position": last_position,
    }
