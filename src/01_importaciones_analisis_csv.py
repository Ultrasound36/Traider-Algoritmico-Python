import pandas as pd
import os

csv_dir = os.path.join(os.path.dirname(__file__), "CSV")
print("Archivos CSV disponibles para revisión:")
for file in os.listdir(csv_dir):
    if file.endswith('.csv'):
        print(f" - {file}")

file_path = os.path.join(csv_dir, "EUR-USD_2024-10-01_to_2026-01-31.csv")


def load_data(file_path):
    """Carga los datos desde un archivo CSV y devuelve un DataFrame de pandas."""
    try:
        data: object = pd.read_csv(file_path)
        print("\n Datos cargados exitosamente..")
        print(data.info(), "\n Muestra información sobre el DataFrame")  # Muestra información sobre el DataFrame
        #print(data.head(), "\n Muestra las primeras filas del DataFrame")  # Muestra las primeras filas del DataFrame
        #print(data.describe(), "\n Muestra estadísticas descriptivas del DataFrame")  # Muestra estadísticas descriptivas del DataFrame
        #print(data.iloc[1, 1])
        return data
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        return None

data = load_data(file_path)
