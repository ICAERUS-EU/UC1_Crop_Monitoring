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

from src.vegetation_indices import ndvi
from src.load_save_show import GeoDataProcessor, draw_labelled_parcels, save_labelled_parcels
from src.parcel_calculations import ParcelProcessor


base_path = './../../data/'
base_path_images = base_path + 'images/'
base_path_features = base_path + 'features/'


def main():

    # Load images and parameters
    ##########################################################################
    gdp = GeoDataProcessor()
    pp = ParcelProcessor()

    tif_path = base_path_images + 'orthomosaic_cropped_230609.tif'
    ortho_image_res, r_image_res, mask_res =  gdp.read_orthomosaic(tif_path)
    
    # Load parcel points
    parcels_per_row = gdp.read_json_file(base_path_features + 'parcel_points.json')
    all_parcels = [parcel for row in parcels_per_row for parcel in row]
    total_parcels = pp.count_parcels(parcels_per_row)

    # Load DEM
    dem_path = base_path_images + 'DEM_cropped_230609.tif'
    dem, dem_res = gdp.read_dem(dem_path)    

    # Calculate mean elevation value for each parcel 
    elevation_parcels = pp.calculate_mean_per_parcel(dem_res, all_parcels, False)

    # Load NIR 
    tif_path = base_path_images +'cropped_NIR_orthomosaic_230609.tif'
    nir_image_res =  gdp.read_orthomosaic_onechannel(tif_path)
    nir_image_res = ((nir_image_res / 65535.0) * 255.0).astype(np.uint8)
    #cv2.imwrite('nir_image_res.jpg', nir_image_res)


    # Calculate NDVI, LAI and false labels
    ##########################################################################

    # Calculate nvdi image
    ndvi_image = ndvi(nir_image_res, r_image_res)
     #cv2.imwrite('ndvi_image_res.jpg', ndvi_image)

    # Calculate mean NDVI for each parcel 
    ndvi_parcels_for_lai = pp.calculate_mean_per_parcel(ndvi_image, all_parcels, True) # con limit
    ndvi_parcels = pp.calculate_mean_per_parcel(ndvi_image, all_parcels, False) # sin limit (este)

    # Calculate LAI 
    lai_parcels = pp.get_lai_per_parcel(ndvi_parcels_for_lai)

    # Generate/Load false labels 
    labels = pp.generate_false_labels_ndvi(ndvi_parcels)
    #labels = pp.generate_false_labels(total_parcels)
    #labels = gdp.read_json_file("labels.json")


    # Save features and show
    ##########################################################################

    # Save labelled parcels in csv 
    save_labelled_parcels(all_parcels, elevation_parcels, ndvi_parcels, lai_parcels, labels)
    # df =  pd.read_csv('labelled_parcels.csv')    

    # Draw parcel points in image
    ortho_image_parcels = draw_labelled_parcels(ortho_image_res, all_parcels, labels)


    cv2.imshow('ortho_image_parcels', ortho_image_parcels)
    cv2.imwrite('ortho_image_parcels.jpg', ortho_image_parcels)

    cv2.waitKey(0)
    cv2.destroyAllWindows()




if __name__ == "__main__":
    main()



