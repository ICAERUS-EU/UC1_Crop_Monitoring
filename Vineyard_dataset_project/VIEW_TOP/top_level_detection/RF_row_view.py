
""" Code to  """

__author__ = "Esther Vera"
__copyright__ = "Copyright 2023, Noumena"
__credits__ = ["Esther Vera, Oriol Arroyo, Salvador Calgua, Aldo Sollazzo"]
__version__ = "1.0.0"
__maintainer__ = "Esther Vera"
__email__ = "esther@noumena.io"
__status__ = "Production"
__license__ = "MIT"


from osgeo import gdal
import cv2
import yaml
import numpy as np
import copy
import json 
import random 
import pandas as pd
import rasterio
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from PIL import Image
import os 


VINEYARD_HEIGHT = 5
VINEYARD_SEP = 12.2
PARCEL_LEN = 26




def main():

    # Load images
    path_row_images = './../../data/row_images/'
    path_row_labels = './../../data/features/row_labels.json'
    
    img_files = os.listdir(path_row_images)
    
    X = []
    for img_name in img_files: 
        print(img_name)
        img_path = os.path.join(path_row_images, img_name)

        X.append(np.array(Image.open(img_path)).flatten())

    X = np.array(X)

    with open(path_row_labels, 'r') as f:
        y = np.array(json.load(f)).astype(np.float32)


    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=4)

    # Training
    #rf = RandomForestRegressor(n_estimators = 100, random_state = 42)
    #rf = RandomForestClassifier()


    '''rf_classifier = RandomForestClassifier()

    # Definir el espacio de búsqueda de hiperparámetros
    param_dist = {
        'n_estimators': [int(x) for x in np.linspace(start=200, stop=2000, num=10)],
        'max_features': ['auto', 'sqrt', 'log2'],
        'max_depth': [int(x) for x in np.linspace(10, 110, num=11)] + [None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'bootstrap': [True, False]
    }

    # Configurar la búsqueda aleatoria
    random_search = RandomizedSearchCV(
        rf_classifier,
        param_distributions=param_dist,
        n_iter=100,  # Número de combinaciones aleatorias a probar
        scoring='accuracy',  # Puedes cambiar la métrica según tu problema
        cv=5,  # Número de divisiones en la validación cruzada
        verbose=2,
        n_jobs=-1  # Utilizar todos los núcleos de la CPU para la búsqueda
    )


    # Realizar la búsqueda aleatoria
    random_search.fit(X_train, y_train)

    # Imprimir los mejores hiperparámetros encontrados
    print("Mejores hiperparámetros:")
    print(random_search.best_params_)'''
    


    print("Training...")
    rf = RandomForestClassifier(n_estimators=1400, min_samples_split=5, min_samples_leaf=4, 
                                max_features='sqrt', max_depth=80, class_weight={0:1, 1:10000000000}, bootstrap=True)
    rf.fit(X_train, y_train)


    # Prediction
    y_pred = rf.predict(X_test)

    proba_predictions = rf.predict_proba(X_test)
    print("Probabilidades predichas:", proba_predictions)


    print(y_pred)
    print(y_test)

    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)




if __name__ == "__main__":
    main()


