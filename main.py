import os
import sys

# Agregar el directorio src al path para importar módulos desde allí
root_path = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(root_path, '..', 'src')
sys.path.append(src_path)

# Importar la funciones necesarias
from data.load import load_results_csv
from data.transform import process_data
from model.train import scale_data
from model.train import train_regression_models
from model.train import train_classification_models

def main():
    # Cargar los datos
    results_df = load_results_csv()
    if results_df is None:
        print("No se pudieron cargar los datos.")
        return

    # Procesar los datos
    results_df = process_data(results_df)
    if results_df is None:
        print("No se pudieron procesar los datos.")
        return

    # Preparar los datos para los modelos
    data = results_df.copy()
    # Filtrar los datos para que solo contengan fechas posteriores a 1996 para tener datos previos del ranking
    data = data[data['date'] > '1996-01-01']
    # Convertir las columnas 'neutral' y 'world_cup' a tipo entero
    data['neutral'] = data['neutral'].astype(int)
    data['world_cup'] = data['world_cup'].astype(int)

    # Dividir los datos en conjuntos de entrenamiento y prueba
    train_data = data[data['date'] < '2016-01-01']
    test_data = data[data['date'] >= '2016-01-01']

    # Predicción de la diferencia de puntos
    X_train = train_data[['neutral', 'world_cup', 'ranking_home_points', 'ranking_away_points', 'home_performance', 'away_performance']]
    y_train = train_data['margin']

    X_test = test_data[['neutral', 'world_cup', 'ranking_home_points', 'ranking_away_points', 'home_performance', 'away_performance']]
    y_test = test_data['margin']

    X_train_scaled, X_test_scaled = scale_data(X_train, X_test)

    # Entrenar y evaluar los modelos de regresión
    train_regression_models(X_train_scaled, y_train, X_test_scaled, y_test)

    # Predicción del resultado del partido 
    y_train = train_data['result']
    y_test = test_data['result']

    # Entrenar y evaluar los modelos de clasificación
    train_classification_models(X_train_scaled, y_train, X_test_scaled, y_test)
    

if __name__ == "__main__":
    main()