""" Code designed to get the vineyards data organised and labelled """

__author__ = "Esther Vera"
__copyright__ = "Copyright 2023, Noumena"
__credits__ = ["Esther Vera, Oriol Arroyo, Salvador Calgua, Aldo Sollazzo"]
__version__ = "1.0.0"
__maintainer__ = "Esther Vera"
__email__ = "esther@noumena.io"
__status__ = "Production"
__license__ = "MIT"

import cv2
import yaml
import numpy as np
import copy
import json 
import random 
from tqdm import tqdm 
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import os 

from src.vegetation_indices import ndvi
from src.load_save_show import GeoDataProcessor, draw_labelled_parcels, save_labelled_parcels
from src.parcel_calculations import ParcelProcessor


base_path = './../../data/'
base_path_images = base_path + 'images/'
base_path_features = base_path + 'features/'
base_path_saved_images = base_path + 'images_gif/'
os.makedirs(base_path_saved_images, exist_ok=True)





def draw_each_parcel(ortho_image_res, all_parcels, labels):
    ortho_image_parcels = copy.deepcopy(ortho_image_res)
    alpha = 0.4
    blank_mask = copy.deepcopy(ortho_image_res) # np.zeros_like(ortho_image_res)

    cont = -1
    for i,parcel in tqdm(enumerate(all_parcels)):
    
        if(labels[i] == 2):
            # RED (DISEASE)
            color_parcel = [0,0,255]
        elif(labels[i] == 1):
            # ORANGE (RISK)
            color_parcel = [0,255,255]
        else: 
            # GREEN (HEALTHY)
            color_parcel = [0,255,0]

        color_parcel = [0,165,255]

        cv2.polylines(ortho_image_parcels, [np.array(parcel)], isClosed=True, color=color_parcel, thickness=2)
        #cv2.fillPoly(blank_mask, [np.array(parcel)], color=color_parcel)
        #cv2.putText(ortho_image_parcels, str(i), (parcel[0][0], parcel[0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (255,255,255), 1)

        center_x = int((parcel[0][0] + parcel[2][0]) / 2) - 2
        center_y = int((parcel[0][1] + parcel[2][1]) / 2) + 2
        center = (center_x, center_y)


        #ortho_image_parcels = cv2.addWeighted(ortho_image_res, 1 - alpha, blank_mask, alpha, 0)
        cv2.imwrite(base_path_saved_images + 'ortho_image_parcels_' + str(i+1)  + '.jpg', ortho_image_parcels)
    return ortho_image_parcels



def draw_each_row_parcel(ortho_image_res, parcels):
    ortho_image_parcels = copy.deepcopy(ortho_image_res)
    alpha = 0.4
    blank_mask = copy.deepcopy(ortho_image_res) # np.zeros_like(ortho_image_res)

    cont = -1
    for i in tqdm(range(len(parcels))):
        print(parcels[i][0])

        parcel = [parcels[i][0][0], parcels[i][0][1], parcels[i][-1][2], parcels[i][-1][3] ]

        color_parcel = [0,165,255]

        cv2.polylines(ortho_image_parcels, [np.array(parcel)], isClosed=True, color=color_parcel, thickness=2)
        #cv2.fillPoly(blank_mask, [np.array(parcel)], color=color_parcel)
        #cv2.putText(ortho_image_parcels, str(i), (parcel[0][0], parcel[0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (255,255,255), 1)

        center_x = int((parcel[0][0] + parcel[2][0]) / 2) - 2
        center_y = int((parcel[0][1] + parcel[2][1]) / 2) + 2
        center = (center_x, center_y)


        #ortho_image_parcels = cv2.addWeighted(ortho_image_res, 1 - alpha, blank_mask, alpha, 0)
        cv2.imwrite(base_path_saved_images + 'ortho_image_parcels_' + str(i+1)  + '.jpg', ortho_image_parcels)
    return ortho_image_parcels


def main():

  

    gdp = GeoDataProcessor()

    tif_path = base_path_images + 'orthomosaic_cropped_230609.tif'
    ortho_image_res, r_image_res, mask_res =  gdp.read_orthomosaic(tif_path)
    print(ortho_image_res.shape)
    cv2.imwrite(base_path_saved_images + 'ortho_image_parcels_0.jpg', ortho_image_res)


    df =  pd.read_csv('labelled_parcels.csv')
    df_parcel_points = df['parcel']
    df_elevation = df['elevation']
    df_ndvi = df['ndvi']
    df_lai = df['lai']
    df_labels = df['diseased']

    all_parcels = [eval(parcel) for parcel in df_parcel_points]
    elevation = list(df_elevation)
    ndvi_values = list(df_ndvi)
    lai = list(df_lai)
    labels = list(df_labels)

    print(base_path_features + 'parcel_points.json')
    with open(base_path_features + 'parcel_points.json', 'r') as f:
        parcels = json.load(f)


    # Draw parcel points in image
    ortho_image_parcels = draw_each_parcel(ortho_image_res, all_parcels, labels)
    #ortho_image_parcels = draw_each_row_parcel(ortho_image_res, parcels)






if __name__ == "__main__":
    main()



