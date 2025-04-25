from pathlib import Path
import pandas as pd

def load_results_csv():
    # Construir la ruta relativa al archivo
    project_root = Path(__file__).resolve().parents[3]
    file_path = project_root / "data" / "results.csv"
    
    # Cargar el archivo CSV
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"Error: El archivo no se encontró en la ruta {file_path}")
        return None