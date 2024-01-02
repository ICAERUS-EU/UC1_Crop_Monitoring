
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



VINEYARD_HEIGHT = 5
VINEYARD_SEP = 12.2
PARCEL_LEN = 26



def read_orthomosaic_tif(tif_path): 

    with rasterio.open(tif_path) as src:
        ortho_data = src
        print(src)
        red_band = cv2.resize(src.read(1), None, fx=1, fy=1)
        # Obtener información general
        print("Información general:")
        print("Número de bandas:", src.count)
        print("Dimensiones (ancho, alto):", src.width, src.height)
        print("Coordenadas del conjunto de datos:", src.bounds)
        print("Transformación afín:", src.transform)
        print("Tipo de datos:", src.dtypes)

        # Obtener información específica de cada banda
        for i in range(1, src.count + 1):
            print(f"\nBanda {i}:")
            print("Nombre:", src.descriptions[i - 1])
            #print("Estadísticas de la banda:", src.get_statistics(i))
            #print("Histograma de la banda:", src.histogram(i))

    return red_band, [], []





def main():

    df =  pd.read_csv('labelled_parcels.csv')
    df_parcel_points = df['parcel']
    df_elevation = df['elevation']
    df_ndvi = df['ndvi']
    df_lai = df['lai']
    df_labels = df['diseased']

    parcel_points = [eval(parcel) for parcel in df_parcel_points]
    elevation = list(df_elevation)
    ndvi_values = list(df_ndvi)
    lai = list(df_lai)
    labels = list(df_labels)

    #print(lai)

    X = np.column_stack((elevation, ndvi_values, lai))
    X = np.column_stack((ndvi_values, lai))
    #X = np.array(elevation).reshape(-1,1)   
    y = labels

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    #print(elevation)

    # Training
    #rf = RandomForestRegressor(n_estimators = 1000, random_state = 42)
    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)
    

    # Prediction
    y_pred = rf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)
    print(y_pred)
    print(y_test)




if __name__ == "__main__":
    main()




'''# Get numerical feature importances
importances = list(rf.feature_importances_)
# List of tuples with variable and importance
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
# Sort the feature importances by most important first
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
# Print out the feature and importances 
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances];'''