
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
import matplotlib.pyplot as plt 
from tqdm import tqdm 

from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay

from sklearn import datasets
from sklearn.cluster import KMeans

from src.load_save_show import GeoDataProcessor, draw_labelled_parcels, save_labelled_parcels

base_path = './../../data/'
base_path_images = base_path + 'images/'
base_path_features = base_path + 'features/'

def main():
    
    gdp = GeoDataProcessor()
    
    tif_path = base_path_images + 'orthomosaic_cropped_230609.tif'
    ortho_image_res, r_image_res, mask_res =  gdp.read_orthomosaic(tif_path)
    print(ortho_image_res.shape)
 

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

    for ele in elevation: 
        if(ele < 100):
            idx = elevation.index(ele)
            print(idx)

            elevation.pop(idx)
            ndvi_values.pop(idx)
            lai.pop(idx)
            labels.pop(idx)
            parcel_points.pop(idx)





    #X = np.column_stack((elevation, ndvi_values, lai))
    X = np.column_stack((ndvi_values, lai))
    #X = np.array(elevation).reshape(-1,1)   
    y = labels

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    
    # Declaring Model
    model = KMeans(n_clusters=3)


    # Fitting Model
    model.fit(X)


    # Prediction on the entire data
    all_predictions = model.predict(X)


    # Show relation
    labels = model.labels_
    centroids = model.cluster_centers_
    plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis')
    plt.scatter(centroids[:, 0], centroids[:, 1], marker='X', s=200, linewidths=3, color='r')
    plt.savefig('ndvi_lai_relation.png', bbox_inches='tight', pad_inches=0)

    plt.show()


    '''plt.scatter(X[:, 0], X[:, 2], c=labels, cmap='viridis')
    plt.scatter(centroids[:, 0], centroids[:, 2], marker='X', s=200, linewidths=3, color='r')
    plt.show()
        
    plt.scatter(X[:, 1], X[:, 2], c=labels, cmap='viridis')
    plt.scatter(centroids[:, 1], centroids[:, 2], marker='X', s=200, linewidths=3, color='r')
    plt.show()'''

    ortho_image_parcels = draw_labelled_parcels(ortho_image_res, parcel_points, labels)


    cv2.imshow('ortho_image_parcels', ortho_image_parcels)
    cv2.imwrite('ortho_image_parcels.jpg', ortho_image_parcels)

    cv2.waitKey(0)
    cv2.destroyAllWindows()



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