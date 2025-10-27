from datetime import datetime
import os
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.style

plt.style.use('ggplot')

file_path = os.path.join(os.path.dirname(__file__), "EUR-USD_Day_2025-09-01_to_2025-09-30_America_Santiago.csv")

asset = 'EURUSD=X'
arrAssets = ['EURUSD=X', 'EURGBP=X', 'AUDUSD=X', 'NZDUSD=X']    
start_date = '2024-10-01'
end_date = '2025-10-01'
interval = '1d'
period = '2y'
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

#data = load_data(asset, interval, start_date, end_date)

def print_graph_array_yahoo(arrAssets, interval, start_date, end_date):
    try:
        for ticker in arrAssets:
            df = yf.download(ticker, start=start_date, end=end_date, interval=interval, auto_adjust=True)
            # Verifica si existe 'Adj Close', si no usa 'Close'
            if 'Adj Close' in df.columns:
                close_price[ticker] = df['Adj Close']
            elif 'Close' in df.columns:
                close_price[ticker] = df['Close']
            else:
                print(f"No se encontraron datos de cierre para {ticker}")
        #print(close_price.info())
        close_price["EURUSD=X"].plot(figsize=(15, 6))
        plt.show()

        return close_price
    except Exception as e:
        print(f"Error al mostrar la información de los datos: {e}")
    return None

#data = print_data_info(arrAssets, interval, start_date, end_date)

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
#data = print_data_diccionary_yahoo(arrAssets, interval, period)

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