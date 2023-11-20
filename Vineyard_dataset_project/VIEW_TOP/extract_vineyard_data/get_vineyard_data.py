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
import rasterio
from osgeo import gdal

from src.utils import load_config, create_grid_with_color_mapping, extract_vineyard_health_data
from src.grid import get_coordinates_row, get_parallel_rows, mask_ortho_image_rows, get_filtered_rows, get_parcel_rows_image
from src.vegetation_indices import ndvi

select_points = False 
#select_points = True

VINEYARD_HEIGHT = 5
VINEYARD_SEP = 12.2
PARCEL_LEN = 26
NDVI_LIM = 0



def read_images(config): 
    nir_path =  config["nir_image_filepath"]
    ortho_path = 'masked_terrain.jpg' 

    nir_image = cv2.imread(nir_path, cv2.IMREAD_GRAYSCALE)
    nir_image_res = cv2.resize(nir_image, None, fx=0.25,fy=0.25)
    
    ortho_image_res = cv2.imread(ortho_path)
    #ortho_image_res = cv2.resize(ortho_image_res, None, fx=0.25,fy=0.25)

    r_image_res = ortho_image_res[:,:,2] 

    return nir_image_res, r_image_res, ortho_image_res


def count_parcels(parcel_points): 

    total_parcels = 0
    for row in parcel_points:
        total_parcels += len(row)
    return total_parcels


def generate_false_labels(total_parcels): 

    labels = []
    for i in range(total_parcels):
      labels.append(random.randint(0, 1))

    with open('labels.json', 'w') as f:
        json.dump(labels, f)
    
    return labels



def generate_false_labels_ndvi(ndvi_parcels): 
    
    labels = []

    for i, value in enumerate(ndvi_parcels):
        if(value<0.1):
            labels.append(1)
        else: 
            labels.append(0)


    with open('labels.json', 'w') as f:
        json.dump(labels, f)
       
    return labels

def read_json_file(path_json): 

    file_content = []
    with open(path_json, 'r') as f:
        file_content = json.load(f)

    return file_content


def read_orthomosaic_tif(tif_path): 

    with rasterio.open(tif_path) as src:

        red_band = cv2.resize(src.read(1), None, fx=1, fy=1)
        green_band = cv2.resize(src.read(2), None, fx=1, fy=1)
        blue_band = cv2.resize(src.read(3), None, fx=1, fy=1)
        rgb_image = cv2.merge([blue_band, green_band, red_band])
        
        mask = src.read(4)

    return rgb_image, red_band, mask




def read_dem(dem_path):

    dataset = gdal.Open(dem_path, gdal.GA_ReadOnly)
    band = dataset.GetRasterBand(1)
    dem_array = band.ReadAsArray()

    # Close the dataset
    dataset = None

    return dem_array



def draw_labelled_parcels(ortho_image_res, all_parcels, labels):
    ortho_image_parcels = copy.deepcopy(ortho_image_res)
    
    cont = -1
    for i,parcel in enumerate(all_parcels):
       
        if(labels[i] == 1):
            color_parcel = [0,0,255]
        else: 
            color_parcel = [0,255,0]

        cv2.polylines(ortho_image_parcels, [np.array(parcel)], isClosed=True, color=color_parcel, thickness=1)
        cv2.putText(ortho_image_parcels, str(i), (parcel[0][0], parcel[0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (255,255,255), 1)

    return ortho_image_parcels



def calculate_mean_per_parcel(array_aux, all_parcels, ndvi_process): 
    
    h, w = array_aux.shape[0:2]

    mean_values = []
    for parcel in tqdm(all_parcels, desc='Processing parcels...', unit='parcel'): 

        # Get actual parcel mask and apply to dem 
        parcel_mask = np.zeros((h, w, 1), dtype=np.uint8)
        cv2.fillPoly(parcel_mask, [np.array(parcel)], color = (255,255,255))
        masked_parcel = cv2.bitwise_and(array_aux, array_aux, mask=parcel_mask)
        
        # If DEM is processing, calculate the mean elevation value of the parcel
        if(not ndvi_process):
            value_count = np.count_nonzero(masked_parcel)
            value = np.sum(masked_parcel) / value_count

        # If NDVI is processing, calculate the mean ndvi value of the parcel
        else: 
            all_values = masked_parcel[masked_parcel > NDVI_LIM].tolist()
            '''for row in masked_parcel:
                for val in row: 
                    if(val!=0):
                        print(val)'''
            value = np.sum(all_values)/len(all_values)


        mean_values.append(value)

        
    return mean_values



def get_lai_per_parcel(ndvi_parcels):

    #pixel_size = 0.002118 #pixel_size_in_meters
    #vegetation_mask = ndvi_image > NDVI_LIM
    #lai_parcels.append(ndvi_val * pixel_size**2)

    lai_parcels = []
    for ndvi_val in ndvi_parcels: 
        lai_parcels.append(1 - np.exp(-0.69 * ndvi_val)) / 0.69
    
    return lai_parcels






def save_labelled_parcels(all_parcels, elevation_parcels, ndvi_parcels, lai_parcels, labels):

    data = {} 
    data['parcel'] = all_parcels
    data['elevation'] = elevation_parcels
    data['ndvi'] = ndvi_parcels
    data['lai'] = lai_parcels
    data['diseased'] = labels

    df = pd.DataFrame(data)
    df.to_csv('labelled_parcels.csv', index=False)




def main():

    # Load orthomosaic images, parcels and labels
    ##########################################################################

    tif_path = "orthomosaic_cropped_230609.tif"
    ortho_image, r_image, mask =  read_orthomosaic_tif(tif_path)
    ortho_image_res = cv2.resize(ortho_image, None, fx=0.2, fy=0.2)
    cv2.imwrite("ortho_image_resized.jpg", ortho_image_res)
    r_image_res = cv2.resize(r_image, None, fx=0.2, fy=0.2)

    # Load parcel points
    parcel_points = read_json_file("parcel_points.json")
    all_parcels = [parcel for row in parcel_points for parcel in row]

    # Create/load false labels
    total_parcels = count_parcels(parcel_points)
    #labels = generate_false_labels(total_parcels)
    #labels = read_json_file("labels.json")


    # Load DEM
    ##########################################################################
 
    dem_path = 'DEM_cropped_230609.tif'
    dem = read_dem(dem_path)    
    dem_res = cv2.resize(dem, None, fx=0.2, fy=0.2)
    cv2.imwrite("DEM_image_resized.jpg", dem_res)

    # Calculate mean elevation value for each parcel 
    elevation_parcels = calculate_mean_per_parcel(dem_res, all_parcels, False)


    # Load NIR 
    ##########################################################################
    tif_path = "NDVI_orthomosaic_cropped_230609.tif"
    nir_image, _, mask =  read_orthomosaic_tif(tif_path)
    nir_image_res = cv2.resize(nir_image, None, fx=0.2, fy=0.2)
    nir_image_gray = cv2.cvtColor(nir_image_res, cv2.COLOR_BGR2GRAY)
    ndvi_image = cv2.cvtColor(nir_image_res, cv2.COLOR_BGR2GRAY)

    print(ndvi_image)
    for i in range(len(ndvi_image)):
        for j in range(len(ndvi_image[i])):
            if(ndvi_image[i][j] != 255):
                print(ndvi_image[i][j])


    # Calculate nvdi image
    #ndvi_image = ndvi(nir_image_gray, r_image_res)
    
    #cv2.imwrite('cropped_NDVI_orthomosaic_resized.jpg', nir_image_res)

    # Calculate mean NDVI for each parcel 
    #ndvi_parcels = calculate_mean_per_parcel(ndvi_image, all_parcels, True) # con limit
    ndvi_parcels = calculate_mean_per_parcel(ndvi_image, all_parcels, False) # sin limit (este)
    labels = generate_false_labels_ndvi(ndvi_parcels)


    # Calculate LAI values 
    lai_parcels = get_lai_per_parcel(ndvi_parcels)




    #####################################

    # Save labelled parcels in csv 
    save_labelled_parcels(all_parcels, elevation_parcels, ndvi_parcels, lai_parcels, labels)
    # df =  pd.read_csv('labelled_parcels.csv')    

    # Draw parcel points in image
    ortho_image_parcels = draw_labelled_parcels(ortho_image_res, all_parcels, labels)

    cv2.imwrite('ortho_image_parcels.jpg', ortho_image_parcels)

    cv2.imshow('ortho_image_parcels', ortho_image_parcels)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




if __name__ == "__main__":
    main()



