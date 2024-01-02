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

from src.vegetation_indices import ndvi
from src.load_save_show import GeoDataProcessor, draw_labelled_parcels, save_labelled_parcels
from src.parcel_calculations import ParcelProcessor


base_path = './../../data/'
base_path_images = base_path + 'images/'
base_path_features = base_path + 'features/'


def normalize_image(img): 
    min_val = np.min(img)
    range_val = np.max(img) - min_val
    norm_image = (((img - min_val) / range_val)*255).astype(np.uint8)

    return norm_image

def apply_colormap(img, mask_res_rgb, vmin, vmax):
        
    # Prepare colormap and normalization
    colormap = plt.get_cmap('RdYlGn')  
    norm = Normalize(vmin=vmin, vmax=vmax)  
    colormap_norm = (np.array(colormap(norm(img))) * 255).astype(np.uint8)
    colormap_norm = colormap_norm[:, :, :-1]

    # Transform from gray to rgb and copy
    img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    # Apply coloramp to mask region in img_rgb 
    img_colormap_black = np.where(mask_res_rgb != 0, colormap_norm, img_rgb)

    # Changes black background to white background
    white_image = np.ones_like(img_colormap_black) * 255
    img_colormap_white = np.where(mask_res_rgb != 0, img_colormap_black, white_image)

    return img_colormap_white

def show_colormap(img): 

    fig, ax = plt.subplots(figsize=(27.91, 18.35), tight_layout=True)
    ax.imshow(img)
    ax.axis('off')
    plt.show()


def main():

    # Load images and parameters
    ##########################################################################
    gdp = GeoDataProcessor()
    pp = ParcelProcessor()

    tif_path = base_path_images + 'orthomosaic_cropped_230609.tif'
    ortho_image_res, r_image_res, mask_res =  gdp.read_orthomosaic(tif_path)
    print(ortho_image_res.shape)

    ''''# Load parcel points
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
    print(nir_image_res.shape)

    # Calculate NDVI, LAI and false labels
    ##########################################################################

    tif_path = base_path_images + 'cropped_R_orthomosaic_230609.tif'
    r_spectral_res =  gdp.read_orthomosaic_onechannel(tif_path)
    r_spectral_res = ((r_spectral_res / 65535.0) * 255.0).astype(np.uint8)

    print(r_image_res.shape)
    # Calculate nvdi image
    ndvi_image = ndvi(nir_image_res, r_spectral_res)
    #cv2.imwrite('ndvi_image_res.jpg', ndvi_image)

      

    # Calculate mean NDVI for each parcel 
    ndvi_parcels = pp.calculate_mean_per_parcel(ndvi_image, all_parcels, False) # sin limit (este)
    #ndvi_parcels_for_lai = pp.calculate_mean_per_parcel(ndvi_image, all_parcels, True) # con limit


    # Calculate LAI 
    lai_parcels = pp.get_lai_per_parcel(ndvi_parcels)

 
    # Generate/Load false labels 
    labels = pp.generate_false_labels_ndvi(ndvi_parcels)
    #labels = pp.generate_false_labels(total_parcels)
    #labels = gdp.read_json_file("labels.json")'''


    # Save features and show
    ##########################################################################

    # Save labelled parcels in csv 
    #save_labelled_parcels(all_parcels, elevation_parcels, ndvi_parcels, lai_parcels, labels)
    df =  pd.read_csv('labelled_parcels.csv')    
    df_parcel_points = df['parcel']
    df_labels = df['diseased']

    all_parcels = [eval(parcel) for parcel in df_parcel_points]
    labels = list(df_labels)

    # Draw parcel points in image
    ortho_image_parcels = draw_labelled_parcels(ortho_image_res, all_parcels, labels)


    cv2.imshow('ortho_image_parcels', ortho_image_parcels)
    cv2.imwrite('ortho_image_parcels_thickerlines.jpg', ortho_image_parcels)

    cv2.waitKey(0)
    cv2.destroyAllWindows()




if __name__ == "__main__":
    main()



