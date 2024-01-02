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

from src.vegetation_indices import VegetationIndices
from src.orthomosaic_processor import OrthomosaicProcessor
from src.parcel_calculations import ParcelProcessor


base_path = './../../data/'
base_path_images = base_path + 'images/'
base_path_features = base_path + 'features/'



def draw_labelled_parcels(ortho_image_res, all_parcels, labels):
    ortho_image_parcels = copy.deepcopy(ortho_image_res)
    
    cont = -1
    for i,parcel in enumerate(all_parcels):
       
        if(labels[i] == 2):
            # RED (DISEASE)
            color_parcel = [0,0,255]
        elif(labels[i] == 1):
            # ORANGE (RISK)
            color_parcel = [0,255,255]
        else: 
            # GREEN (HEALTHY)
            color_parcel = [0,255,0]
                            
        #color_parcel = [0,165,255]

        cv2.polylines(ortho_image_parcels, [np.array(parcel)], isClosed=True, color=color_parcel, thickness=1)

        center_x = int((parcel[0][0] + parcel[2][0]) / 2) - 2
        center_y = int((parcel[0][1] + parcel[2][1]) / 2) + 2
        center = (center_x, center_y)

        cv2.putText(ortho_image_parcels, str(i), center, cv2.FONT_HERSHEY_SIMPLEX, 0.23, (255,255,255), 1)

    return ortho_image_parcels



def main():

    # Variables
    ##########################################################################
    tam = (2346, 1805)
    op = OrthomosaicProcessor()
    pp = ParcelProcessor()
    vi = VegetationIndices()
    
    # Load images and parameters
    ##########################################################################

    # Load RGB orthomosaic
    tif_path = base_path_images + 'orthomosaic_cropped_230609.tif'
    ortho_image, r_image, g_image, b_image, mask  =  op.read_orthomosaic(tif_path)
    ortho_image_res, r_image_res, _, _, mask_res = op.resize_orthomosaic(ortho_image, r_image, g_image, b_image, mask, tam)
    print(ortho_image_res.shape)

    # Load parcel points
    parcels_per_row = op.read_json_file(base_path_features + 'parcel_points.json')
    all_parcels = [parcel for row in parcels_per_row for parcel in row]
    total_parcels = pp.count_parcels(parcels_per_row)

    # Load NIR 
    tif_path = base_path_images +'cropped_NIR_orthomosaic_230609.tif'
    nir_image =  op.read_one_channel_orthomosaic(tif_path)
    nir_image_res = op.resize_and_convert_type(nir_image, tam)
    #cv2.imwrite('nir_image_res.jpg', nir_image_res)
    print(nir_image_res.shape)

    # Load r_spectral image
    tif_path = base_path_images + 'cropped_R_orthomosaic_230609.tif'
    r_spectral = op.read_one_channel_orthomosaic(tif_path)
    r_spectral_res = op.resize_and_convert_type(r_spectral, tam)


    # Calculate NDVI and generate labels based on NDVI
    ##########################################################################
    
    # Calculate nvdi image
    ndvi_image = vi.ndvi(nir_image_res, r_spectral_res)

    # Calculate mean NDVI for each parcel 
    ndvi_parcels = pp.calculate_mean_per_parcel(ndvi_image, all_parcels, False) 
    
    # Generate labels based on NDVI 
    labels = pp.generate_ndvi_labels(ndvi_parcels)


    # Save features and show
    ##########################################################################

    # Draw parcel points in image
    ortho_image_parcels = draw_labelled_parcels(ortho_image_res, all_parcels, labels)


    cv2.imshow('ortho_image_parcels', ortho_image_parcels)
    #cv2.imwrite('ortho_image_parcels.jpg', ortho_image_parcels)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




if __name__ == "__main__":
    main()



