from datetime import datetime
import os
import pandas as pd
import yfinance as yf
from clases.YahooFinanceDataManager import YahooDataManager
import matplotlib.pyplot as plt

plt.style.use('ggplot')

yf_manager = YahooDataManager()

file_path = os.path.join(os.path.dirname(__file__), "EUR-USD_Day_2025-09-01_to_2025-09-30_America_Santiago.csv")

asset = 'EURUSD=X'
arrAssets = ['EURUSD=X', 'EURGBP=X', 'AUDUSD=X', 'NZDUSD=X']    
start_date = '2026-01-01'
end_date = '2026-08-31'
interval = '1d'
period = '1mo'  # 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
close_price = pd.DataFrame()
ohlcv_data = {}


def print_data_simple_yahoo(asset, interval, start_date, end_date):
    print(f"Descargando datos de {asset} con intervalo {interval} y periodo {period}")
    try:
        dataYfinance = yf.download(asset, start_date, end_date, interval, auto_adjust=True)
        print("Datos cargados exitosamente.")
        print(dataYfinance)
        return dataYfinance
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        return None

#data = print_data_simple_yahoo(asset, interval, start_date, end_date)

def print_graph_asset_yahoo(asset, interval, start_date, end_date):
    try:
        df = yf.download(asset, start=start_date, end=end_date, interval=interval, auto_adjust=True)
        # Verifica si existe 'Adj Close', si no usa 'Close'
        if 'Adj Close' in df.columns:
            close_price[asset] = df['Adj Close']
        elif 'Close' in df.columns:
            close_price[asset] = df['Close']
        else:
            print(f"No se encontraron datos de cierre para {asset}")
        #print(close_price.info())
        tipo_divisa = f"{asset[:3]}-{asset[3:6]}"
        os.makedirs("Gráficos", exist_ok=True)
        close_price[asset].plot(figsize=(15, 6))
        plt.title(f"Precio de Cierre [divisa: {tipo_divisa}] :: [start-date: {start_date}] to [end-date: {end_date}]")
        plt.ylabel("Precio de Cierre")
        plt.xlabel("Fecha")
        plt.savefig(os.path.join("Gráficos", f"{tipo_divisa}-{start_date}_to_{end_date}.png"))
        """ plt.show() """

        return close_price
    except Exception as e:
        print(f"Error al mostrar la información de los datos: {e}")
    return None

data = print_graph_asset_yahoo(asset, interval, start_date, end_date)

def print_data_diccionary_yahoo(arrAssets, interval, period):
    try:
        for ticker in arrAssets:
            df = yf.download(ticker, period=period, interval=interval, auto_adjust=True)
            ohlcv_data[ticker] = df
        #print(ohlcv_data)
        print(ohlcv_data["EURUSD=X"]["Open"])
        return ohlcv_data
    except Exception as e:
        print(f"Error al mostrar la información de los datos: {e}")
    return None
data = print_data_diccionary_yahoo(arrAssets, interval, period)

def print_and_pick_dataframe():
    df = pd.DataFrame(data=
                      {
                        'Columna 1': [1, 2, 3, 4],
                        'Columna 2': ['A', 'B', 'C', 'D'],
                        'Columna 3': [10.5, 20.3, 30.2, 40.1],
                        'Columna 4': [True, False, True, False]
                    },
                      index=
                         ['2018', '2019', '2020', '2021'])
    try:
        #print(df['Columna 4']) # Muestra una columna específica
        #print(df.loc['2020'])  # Muestra una fila específica
        print(df.iloc[2, 1])  # Muestra el valor en la <row> 2, <column> 1 (C)
        return df
    except Exception as e:
        print(f"Error al mostrar la información de los datos: {e}")
    return None
# data = print_and_pick_dataframe()

def parse_date(date_str):
    """Intenta convertir la fecha usando varios formatos posibles."""
    for fmt in ("%d/%m/%Y %H:%M:%S", "%d.%m.%Y %H:%M:%S %Z%z", "%d.%m.%Y %H:%M:%S UTC%z"):
        try:
            return datetime.strptime(date_str, fmt)
        except Exception:
            continue
    return pd.NaT  # Si no se puede convertir, retorna NaT

def cast_and_print_types():
    try:        
        data = pd.read_csv(file_path)
        # Aplica strptime para manejar formatos mixtos
        data['America/Santiago'] = data['America/Santiago'].apply(lambda x: parse_date(str(x)))
        data = data.set_index('America/Santiago')
        print(data.head())

        return data
    except Exception as e:
        print(f"Error al mostrar la información de los datos: {e}")
    return None

data = cast_and_print_types()

def download_and_save_yahoo_data(arrAssets, start_date, end_date, interval):
    """
    Descarga datos de Yahoo Finance para una lista de activos y los guarda en archivos CSV
    en la carpeta 'CSV' del directorio del proyecto
    """
    csv_dir = os.path.join(os.path.dirname(__file__), "CSV")
    os.makedirs(csv_dir, exist_ok=True)
    try:
        for ticker in arrAssets:
            print(f"Descargando datos de {ticker}...")
            df = yf.download(ticker, start=start_date, end=end_date, interval=interval, auto_adjust=True)
            if not df.empty:
                tipo_divisa = f"{ticker[:3]}-{ticker[3:6]}"
                file_name = f"{tipo_divisa}_{start_date}_to_{end_date}.csv"
                file_path = os.path.join(csv_dir, file_name)
                df.to_csv(file_path)
                print(f"Datos de {ticker} guardados en {file_path}")
            else:
                print(f"No se encontraron datos para {ticker}")
    except Exception as e:
        print(f"Error al descargar o guardar los datos: {e}")

# Llamada a la función con las variables definidas
#download_and_save_yahoo_data(arrAssets, start_date, end_date, interval)