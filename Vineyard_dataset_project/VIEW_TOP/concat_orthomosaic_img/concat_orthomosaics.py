""" Code to generate orthomosaic mixed image """

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


from src.load_save_show import GeoDataProcessor
from src.load_save_show import draw_labelled_parcels


def get_features_data(path_df): 

    df =  pd.read_csv(path_df)    

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

    return parcel_points, elevation, ndvi_values, lai, labels



base_path = './../../data/'
base_path_images = base_path + 'images/'
base_path_images_saved = base_path + 'images_saved/'
base_path_features = base_path + 'features/'

gdp = GeoDataProcessor()


# Load orthomosaic image 
img_path = base_path_images + 'orthomosaic_cropped_230609.tif'
img_ortho = cv2.resize(cv2.imread(img_path), (2346, 1805))

# Load mask
_, _, mask_res =  gdp.read_orthomosaic(img_path)
mask_res = cv2.resize(mask_res, (2346, 1805))
kernel3 =  cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
mask_res = cv2.erode(mask_res, kernel3, iterations=1)

# Load NDVI image
img_path = base_path_images + 'NDVI_orthomosaic_cropped_230609.tif'
img_ndvi = (cv2.resize(cv2.imread(img_path), (2346, 1805)))

# Load parcels image
img_path = base_path_images_saved + 'ortho_grid_text_image_parcels.jpg'
img_parcels = cv2.imread(img_path)
img_parcels = cv2.resize(img_parcels, (2346, 1805))


# Load labelled image
'''img_path = base_path_images_saved + 'ortho_image_parcels.jpg'
img_labelled = cv2.imread(img_path)
img_labelled = cv2.resize(img_labelled, (2346, 1805))'''

path_df = 'labelled_parcels.csv'
parcel_points, elevation, ndvi_values, lai, labels = get_features_data(path_df)
img_labelled = draw_labelled_parcels(img_ortho, parcel_points, labels)


# Apply mask to images
img_ortho = cv2.bitwise_and(img_ortho, img_ortho, mask=mask_res)
img_ndvi = cv2.bitwise_and(img_ndvi, img_ndvi, mask=mask_res)
img_parcels = cv2.bitwise_and(img_parcels, img_parcels, mask=mask_res)
img_labelled = cv2.bitwise_and(img_labelled, img_labelled, mask=mask_res)


# Concatenate images
h, w, _ = img_ortho.shape
cut_img_ortho = img_ortho[0:h, 0:int(w/4)]
cut_img_ndvi = img_ndvi[0:h, int(w/4):int(w/2)]
cut_img_parcels = img_parcels[0:h, int(w/2):int(3*w/4)]
cut_img_labelled = img_labelled[0:h, int(3*w/4):w]

concat_image = cv2.hconcat([cut_img_ortho, cut_img_ndvi, cut_img_parcels, cut_img_labelled])

# Save and show image
cv2.imwrite('uc1_image1.jpg', concat_image)


cv2.imshow('concat_image', concat_image)
cv2.waitKey(0)
cv2.destroyAllWindows()


