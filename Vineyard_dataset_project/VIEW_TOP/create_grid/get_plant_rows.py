""" Code designed to get the vineyards rows and make the grid """

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
import rasterio

from src.utils import load_config
from src.vegetation_indices import ndvi
from src.grid import get_coordinates_row, get_parallel_rows, mask_ortho_image_rows, get_filtered_rows, get_parcel_rows_image

select_points = False 
#select_points = True

#VINEYARD_HEIGHT = 5
#VINEYARD_SEP = 14.8
#PARCEL_LEN = 26

VINEYARD_HEIGHT = 10
VINEYARD_SEP = 37
PARCEL_LEN = 70



base_path = './../../data/'
base_path_images = base_path + 'images/'
base_path_features = base_path + 'features/'


def read_images(config): 
    nir_path =  config["nir_image_filepath"]
    ortho_path = 'masked_terrain.jpg' 

    nir_image = cv2.imread(nir_path, cv2.IMREAD_GRAYSCALE)
    nir_image_res = cv2.resize(nir_image, None, fx=0.25,fy=0.25)
    
    ortho_image_res = cv2.imread(ortho_path)
    #ortho_image_res = cv2.resize(ortho_image_res, None, fx=0.25,fy=0.25)

    r_image_res = ortho_image_res[:,:,2] 

    return nir_image_res, r_image_res, ortho_image_res


def read_orthomosaic_tif(tif_path): 

    with rasterio.open(tif_path) as src:
        ortho_data = src
        red_band = cv2.resize(src.read(1), None, fx=1, fy=1)
        green_band = cv2.resize(src.read(2), None, fx=1, fy=1)
        blue_band = cv2.resize(src.read(3), None, fx=1, fy=1)
        rgb_image = cv2.merge([blue_band, green_band, red_band])

        mask = src.read(4)

    return rgb_image, mask

def mask_images(nir, r): 

    mask = cv2.imread('blank_mask.jpg', cv2.IMREAD_GRAYSCALE)
    masked_nir = cv2.bitwise_and(nir, nir, mask=mask)
    masked_r = cv2.bitwise_and(r, r, mask=mask)

    return mask, masked_nir, masked_r


'''def get_ndvi_filtered(masked_nir, masked_r): 

    # Calculate ndvi
    ndvi_image = ndvi(masked_nir, masked_r)
    #ndvi_image_gray =  cv2.cvtColor(ndvi_image, cv2.COLOR_BGR2GRAY)

    _, segmented_image = cv2.threshold(ndvi_image, 0, 100, cv2.THRESH_BINARY)

    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    ndvi_filtered = cv2.dilate(segmented_image, kernel2, iterations = 2)

    return ndvi_filtered'''


def main():

    # Load the configuration file
    #config = load_config("config.yaml")    
    #nir_image_res, r_image_res, _ = read_images(config)
    #mask, masked_nir, masked_r = mask_images(nir_image_res, r_image_res)

    # Get ndvi from image
    #ndvi_filtered = get_ndvi_filtered(masked_nir, masked_r)
    #ndvi_filtered = cv2.normalize(ndvi_filtered, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    
    tif_path = base_path_images + "orthomosaic_cropped_230609.tif"
    ortho_image, mask =  read_orthomosaic_tif(tif_path)
    ortho_image_res = cv2.resize(ortho_image, None, fx=0.5, fy=0.5)
    mask = cv2.resize(mask, None, fx=0.5, fy=0.5)

    
    ######################################
    
    # Select vineyard row and extract coordinates and angle
    coordinates, angle = get_coordinates_row(ortho_image_res, select_points)

    # Get vineyards rows  
    ortho_rows_image = get_parallel_rows(ortho_image_res, coordinates, VINEYARD_SEP)

    # Mask vineyard rows with shape_mask
    masked_rows_image = mask_ortho_image_rows(ortho_rows_image, mask)

    ################################## 

    # Get vineyards rows calculated 
    filtered_rows_image = get_filtered_rows(masked_rows_image)
    parcel_rows_image, parcel_points = get_parcel_rows_image(ortho_image_res, filtered_rows_image, PARCEL_LEN)

    # Guardar la lista en un archivo JSON
    with open(base_path_features + 'parcel_points.json', 'w') as f:
        json.dump(parcel_points, f)

    cv2.imshow('masked_rows_image', masked_rows_image)
    cv2.imshow('parcel_rows_image', parcel_rows_image)
    cv2.imwrite('masked_rows_image.jpg', masked_rows_image)
    cv2.imwrite('parcel_rows_image.jpg', parcel_rows_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()




if __name__ == "__main__":
    main()



