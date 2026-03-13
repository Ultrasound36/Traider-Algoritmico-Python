import pandas as pd
import os
import datetime
import yfinance as yf
import plotly.graph_objects as go
from dotenv import load_dotenv
from alpha_vantage.foreignexchange import ForeignExchange
from polygon import RESTClient

load_dotenv()

api_alpha_vantage = os.getenv("TOKEN_ALPHA_VANTAGE")
api_polygon = os.getenv("POLYGON_API_KEY")

asset = 'EURUSD=X'
start_date = '2025-01-01'
end_date = '2026-02-01'


def load_data(asset, start_date, end_date):
    try:
        # Descargar los datos desde yfinance
        df = yf.download(asset, start=start_date, end=end_date)

        # Aplanar las columnas si es MultiIndex (común en yfinance para un solo ticker)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)

        # Verificar si el DataFrame no está vacío
        if df.empty:
            print(f"No se encontraron datos para {asset} en el rango especificado.")
            return None
        #download_and_save_alpha_vantage_data(asset, start_date, end_date)
        download_and_save_polygon_data(asset, start_date, end_date)
        print(df.head())  # Mostrar las primeras filas del DataFrame

        # Crear gráfico de candlestick para datos financieros
        grafico = go.Figure()
        grafico.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Precio'
        ))

        grafico.update_layout(
            title=f"Gráfico de Candlestick para {asset} desde {start_date} hasta {end_date}",
            xaxis_title="Fecha",
            yaxis_title="Precio",
            xaxis_rangeslider_visible=False
        )

        grafico.show()  # Mostrar el gráfico interactivo

        return df
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        return None

def download_and_save_yahoo_data(asset, start_date, end_date):
    """
    Descarga datos de Yahoo Finance para un activo y los guarda en un archivo CSV
    en la carpeta 'CSV' del directorio del proyecto
    """
    csv_dir = os.path.join(os.path.dirname(__file__), "CSV")
    os.makedirs(csv_dir, exist_ok = True)
    try:
        ticker = asset
        print(f"Descargando datos de {ticker}...")
        df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)
        if not df.empty:
            tipo_divisa = f"{ticker[:3]}-{ticker[3:6]}"
            file_name = f"{tipo_divisa}_{start_date}_to_{end_date}_{datetime.datetime.now().strftime('%H:%M:%S')}.csv"
            file_path = os.path.join(csv_dir, file_name)
            df.to_csv(file_path)
            print(f"Datos de {ticker} guardados en {file_path}")
        else:
            print(f"No se encontraron datos para {ticker}")
    except Exception as e:
        print(f"Error al descargar o guardar los datos: {e}")

def download_and_save_alpha_vantage_data(asset, start_date, end_date):
    """
    Descarga datos de Alpha Vantage para un activo (divisa) y los guarda en un archivo CSV
    en la carpeta 'CSV' del directorio del proyecto, filtrando por fechas
    """
    csv_dir = os.path.join(os.path.dirname(__file__), "CSV")
    os.makedirs(csv_dir, exist_ok=True)
    fx = ForeignExchange(key=api_alpha_vantage, output_format='pandas')

    # Parsear el asset para obtener from_symbol y to_symbol (e.g., 'EURUSD=X' -> 'EUR', 'USD')
    from_symbol = asset[:3].upper()
    to_symbol = asset[3:6].upper()

    try:
        print(f"Descargando datos de {from_symbol}/{to_symbol} desde Alpha Vantage...")
        data, _ = fx.get_currency_exchange_daily(from_symbol=from_symbol, to_symbol=to_symbol, outputsize='full')

        # Filtrar por fechas
        data = data[(data.index >= start_date) & (data.index <= end_date)]

        if not data.empty:
            tipo_divisa = f"{from_symbol}-{to_symbol}"
            file_name = f"{tipo_divisa}_{start_date}_to_{end_date}_{datetime.datetime.now().strftime('%H:%M:%S')}.csv"
            file_path = os.path.join(csv_dir, file_name)
            data.to_csv(file_path)
            print(f"Datos de {from_symbol}/{to_symbol} guardados en {file_path}")
        else:
            print(f"No se encontraron datos para {from_symbol}/{to_symbol} en el rango especificado")
    except Exception as e:
        print(f"Error al descargar o guardar los datos: {e}")

def download_and_save_polygon_data(asset, start_date, end_date):
    """
    Descarga datos de Polygon.io para un activo (divisa) y los guarda en un archivo CSV
    en la carpeta 'CSV' del directorio del proyecto, incluyendo volumen
    """
    csv_dir = os.path.join(os.path.dirname(__file__), "CSV")
    os.makedirs(csv_dir, exist_ok=True)
    client = RESTClient(api_polygon)

    # Parsear el asset para obtener from_symbol y to_symbol (e.g., 'EURUSD=X' -> 'EUR', 'USD')
    from_symbol = asset[:3].upper()
    to_symbol = asset[3:6].upper()
    ticker = f"C:{from_symbol}{to_symbol}"

    try:
        print(f"Descargando datos de {ticker} desde Polygon.io...")
        aggs = client.get_aggs(ticker, 1, "day", start_date, end_date)

        # Convertir a DataFrame
        data = pd.DataFrame([{
            'timestamp': agg.timestamp,
            'open': agg.open,
            'high': agg.high,
            'low': agg.low,
            'close': agg.close,
            'volume': agg.volume
        } for agg in aggs])

        if not data.empty:
            data['date'] = pd.to_datetime(data['timestamp'], unit='ms')
            data.set_index('date', inplace=True)
            data.drop('timestamp', axis=1, inplace=True)

            tipo_divisa = f"{from_symbol}-{to_symbol}"
            file_name = f"{tipo_divisa}_{start_date}_to_{end_date}_{datetime.datetime.now().strftime('%H:%M:%S')}.csv"
            file_path = os.path.join(csv_dir, file_name)
            data.to_csv(file_path)
            print(f"Datos de {ticker} guardados en {file_path}")
        else:
            print(f"No se encontraron datos para {ticker} en el rango especificado")
    except Exception as e:
        print(f"Error al descargar o guardar los datos: {e}")

#data = load_data(asset, start_date, end_date)

client = RESTClient(api_polygon)

# Parsear el asset para obtener from_symbol y to_symbol (e.g., 'EURUSD=X' -> 'EUR', 'USD')
from_symbol = asset[:3].upper()
to_symbol = asset[3:6].upper()
ticker = f"C:{from_symbol}{to_symbol}"

print(f"Descargando datos de {ticker} desde Polygon.io...")

# List Aggregates (Bars)
aggs = []
for a in client.list_aggs(ticker=ticker, multiplier=1, timespan="minute", from_="2025-01-01", to="2025-06-01", limit=10):
    aggs.append(a)
print(f"List Aggregates (Bars): ", aggs)

# Get Last Trade
trade = client.get_last_trade(ticker=ticker)
print(f"Get Last Trade: ", trade)

# List Trades
trades = client.list_trades(ticker=ticker, timestamp="2025-01-04")
for trade in trades:
    print(f"List Trades: ", trade)

# Get Last Quote
quote = client.get_last_quote(ticker=ticker)
print(f"Get Last Quote: ", quote)

# List Quotes
quotes = client.list_quotes(ticker=ticker, timestamp="2025-01-04")
for quote in quotes:
    print(f"List Quotes", quote)