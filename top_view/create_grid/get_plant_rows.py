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

from src.orthomosaic_processor import OrthomosaicProcessor
from src.grid import get_coordinates_row, get_parallel_rows, mask_ortho_image_rows, get_filtered_rows, get_all_parcel_points, draw_parcels, get_all_centers_parcels

select_points = False 
#select_points = True

VINEYARD_HEIGHT = 10
VINEYARD_SEP = 37
PARCEL_LEN = 70 # 5.2 metros 
PARCEL_LEN = 14 # 1 metro en la vida real teniendo en cuenta el tamaño de la imagen resized y la resolución

VINEYARD_SEP = 74
PARCEL_LEN = 27 # 1 metro en la vida real teniendo en cuenta el tamaño de la imagen resized y la resolución


base_path = './../../data/'
base_path_images = base_path + 'images/'
base_path_features = base_path + 'features/'



def main():

    # Load images to calculate the grid 
    op = OrthomosaicProcessor()
    tif_path = base_path_images + "orthomosaic_cropped_230609.tif"
    ortho_image, red_band, green_band, blue_band, mask = op.read_orthomosaic(tif_path)
    ortho_image_res = cv2.resize(ortho_image, None, fx=1, fy=1)#, fx=0.5, fy=0.5)
    mask = cv2.resize(mask, None, fx=1, fy=1)#, fx=0.5, fy=0.5)

    
    ######################################
    
    # Select vineyard row and extract coordinates and angle
    coordinates, angle = get_coordinates_row(ortho_image_res, select_points)

    # Get vineyards rows  
    ortho_rows_image, parallel_rows_points = get_parallel_rows(ortho_image_res, mask, coordinates, VINEYARD_SEP)

    # Mask vineyard rows with shape_mask
    masked_rows_image = mask_ortho_image_rows(ortho_rows_image, mask)
    print(masked_rows_image.shape)


    ###################################### 

    # Calculate vineyards rows 
    filtered_rows_image = get_filtered_rows(masked_rows_image)
    parcel_points = get_all_parcel_points(filtered_rows_image, PARCEL_LEN)
    parcel_rows_image = draw_parcels(ortho_image_res, parcel_points)
    centers_parcels = get_all_centers_parcels(parcel_points)


    # Save parcel_points in JSON file inside base_path_features
    with open(base_path_features + 'parcel_points1.json', 'w') as f:
        json.dump(parcel_points, f)

    # Save parallel_rows_points 
    with open(base_path_features + 'parallel_rows_points1.json', 'w') as f:
        json.dump(parallel_rows_points, f)

    # Save parcel_ points centers in JSON file inside base_path_features
    with open(base_path_features + 'parcel_centers_points1.json', 'w') as f:
        json.dump(centers_parcels, f)

    # Save and show image
    cv2.imwrite('masked_rows_image2.jpg', masked_rows_image)
    cv2.imwrite('parcel_rows_image2.jpg', parcel_rows_image)
    
    #cv2.imshow('masked_rows_image1', masked_rows_image)
    #cv2.imshow('parcel_rows_image1', cv2.resize(parcel_rows_image, None, fx=0.1,fy=0.1))
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()




if __name__ == "__main__":
    main()



