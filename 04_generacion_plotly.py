import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

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
        print(f"Datos cargados exitosamente para {asset} desde {start_date} hasta {end_date}.")
        print("Primeras filas del DataFrame:")
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
data = load_data(asset, start_date, end_date)