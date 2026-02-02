import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

asset = 'EURUSD=X'
arrAssets = ['EURUSD=X', 'EURGBP=X', 'AUDUSD=X', 'NZDUSD=X']    
start_date = '2021-01-01'
end_date = '2026-02-01'
interval = '1d'
resample_rule = 'MS'
period = '2y'


def resample_data(asset, interval, start_date, end_date, resample_rule):
    try:
        # Descargar los datos desde yfinance
        df = yf.download(asset, start=start_date, end=end_date, interval=interval, auto_adjust=True)
        
        # Aplanar las columnas si es MultiIndex (común en yfinance para un solo ticker)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)  # Dropear el nivel 'Ticker', dejando 'Price' como columnas
        
        # Verificar si el DataFrame no está vacío
        if df.empty:
            print(f"No se encontraron datos para {asset} en el rango especificado.")
            return None
        
        # Resamplear los datos según la regla proporcionada
        resampled_df = df.resample(resample_rule).agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum'
        }).dropna()

        print(df.resample(resample_rule).mean())

        
        
        print(df.resample(resample_rule, offset='14D').sum())
        
        # Graficar los datos resampleados
        """ plt.figure(figsize=(15, 6))
        plt.plot(resampled_df.index, resampled_df['Close'], label='Precio de Cierre')
        plt.title(f"Precio de Cierre Resampleado ({resample_rule}) para {asset}")
        plt.xlabel("Fecha")
        plt.ylabel("Precio de Cierre")
        plt.legend()
        plt.grid()
        plt.show() """
        
        return resampled_df
    except Exception as e:
        print(f"Error al procesar los datos: {e}")
        return None

data = resample_data(asset, interval, start_date, end_date, resample_rule)