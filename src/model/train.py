# Este archivo contendrá el código para entrenar el modelo de machine learning de forecasting de partidos de rugby.
# Importar las librerías necesarias
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import os
import joblib
from pathlib import Path
import logging
import sys

# Configurar el logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configurar el logger para que escriba en un archivo
log_file = Path(__file__).resolve().parents[3] / "logs" / "train.log"
if not os.path.exists(log_file.parent):
    os.makedirs(log_file.parent)
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Configurar el logger para que escriba en la consola
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def train_model(data: pd.DataFrame, target_column: str, model_output_path: str):
    """
    Entrena un modelo de clasificación basado en RandomForest.

    Args:
        data (pd.DataFrame): DataFrame con los datos de entrada.
        target_column (str): Nombre de la columna objetivo.
        model_output_path (str): Ruta donde se guardará el modelo entrenado.

    Returns:
        None
    """
    try:
        logger.info("Iniciando el proceso de entrenamiento del modelo.")

        # Separar características y variable objetivo
        X = data.drop(columns=[target_column])
        y = data[target_column]

        # Dividir los datos en conjuntos de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        logger.info("Datos divididos en entrenamiento y prueba.")

        # Crear y entrenar el modelo
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        logger.info("Modelo entrenado exitosamente.")

        # Evaluar el modelo
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        logger.info(f"Precisión del modelo: {accuracy:.2f}")

        # Mostrar métricas adicionales
        logger.info("Reporte de clasificación:")
        logger.info("\n" + classification_report(y_test, y_pred))

        # Mostrar matriz de confusión
        cm = confusion_matrix(y_test, y_pred)
        ConfusionMatrixDisplay(cm).plot()
        plt.title("Matriz de Confusión")
        plt.show()

        # Guardar el modelo entrenado
        joblib.dump(model, model_output_path)
        logger.info(f"Modelo guardado en: {model_output_path}")

    except Exception as e:
        logger.error(f"Error durante el entrenamiento del modelo: {e}")
        raise