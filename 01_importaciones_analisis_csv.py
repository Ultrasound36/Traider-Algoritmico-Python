import pandas as pd
import os

file_path = os.path.join(os.path.dirname(__file__), "EUR-USD_Day_2025-09-01_to_2025-09-30_America_Santiago.csv")


def load_data(file_path):
    """Carga los datos desde un archivo CSV y devuelve un DataFrame de pandas."""
    try:
        data = pd.read_csv(file_path)
        print("Datos cargados exitosamente.")
        #print(data.info())  # Muestra información sobre el DataFrame
        #print(data.head())  # Muestra las primeras filas del DataFrame
        #print(data.describe())  # Muestra estadísticas descriptivas del DataFrame
        print(data.iloc[1, 1])
        return data
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        return None

data = load_data(file_path)
