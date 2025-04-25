import os
import sys

# Agregar el directorio src al path para importar módulos desde allí
root_path = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(root_path, '..', 'src')
sys.path.append(src_path)

# Importar la función de cargar datos
from data.load import load_results_csv
from model.train import train_model

def main():
    # Cargar los datos
    data = load_results_csv()
    if data is None:
        print("No se pudieron cargar los datos.")
        return
    
    # En este punto se deben preprocesar los datos 

    # Entrenar el modelo
    target_column = 'result'  # Columna objetivo a predecir
    model_output_path = os.path.join(root_path, 'model', 'trained_model.pkl')
    train_model(data, target_column, model_output_path)
    print("Modelo entrenado y guardado en:", model_output_path)

if __name__ == "__main__":
    main()