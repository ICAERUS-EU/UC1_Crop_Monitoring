

import cv2
import rasterio
import json
from osgeo import gdal
import copy 
import pandas as pd
import numpy as np



class GeoDataProcessor:
    def __init__(self):
        pass

    @staticmethod
    def read_json_file(path_json):
        with open(path_json, 'r') as f:
            file_content = json.load(f)
        return file_content

    @staticmethod
    def read_orthomosaic(tif_path):
        with rasterio.open(tif_path) as src:
            red_band = cv2.resize(src.read(1), None, fx=1, fy=1)
            green_band = cv2.resize(src.read(2), None, fx=1, fy=1)
            blue_band = cv2.resize(src.read(3), None, fx=1, fy=1)
            rgb_image = cv2.merge([blue_band, green_band, red_band])
            mask = src.read(4)


        res = 0.2
        res = 0.5
        rgb_image_res = cv2.resize(rgb_image, (2346, 1805))
        r_image_res = cv2.resize(red_band, None, fx=res, fy=res)
        mask_res = cv2.resize(mask, None, fx=res, fy=res)

        return rgb_image_res, r_image_res, mask_res

    @staticmethod
    def read_orthomosaic_onechannel(tif_path):
        with rasterio.open(tif_path) as src:
            #img_res = cv2.resize(src.read(1), (938, 722))
            img_res = cv2.resize(src.read(1), (2346, 1805))


        return img_res

    @staticmethod
    def read_dem(dem_path):
        dataset = gdal.Open(dem_path, gdal.GA_ReadOnly)
        band = dataset.GetRasterBand(1)
        dem = band.ReadAsArray()
        res = 0.2
        res = 0.5
        dem_res = cv2.resize(dem, None, fx=res, fy=res)

        dataset = None
        return dem, dem_res



def draw_labelled_parcels(ortho_image_res, all_parcels, labels):
    ortho_image_parcels = copy.deepcopy(ortho_image_res)
    
    cont = -1
    for i,parcel in enumerate(all_parcels):
       
        if(labels[i] == 2):
            # YELLOW (RISK)
            color_parcel = [0,255,255]
        elif(labels[i] == 1):
            # RED (DISEASE)
            color_parcel = [0,0,255]
        else: 
            # GREEN (HEALTHY)
            color_parcel = [0,255,0]
                            
        cv2.polylines(ortho_image_parcels, [np.array(parcel)], isClosed=True, color=color_parcel, thickness=2)
        #cv2.putText(ortho_image_parcels, str(i), (parcel[0][0], parcel[0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (255,255,255), 1)

        center_x = int((parcel[0][0] + parcel[2][0]) / 2) - 2
        center_y = int((parcel[0][1] + parcel[2][1]) / 2) + 2
        center = (center_x, center_y)

        cv2.putText(ortho_image_parcels, str(i), center, cv2.FONT_HERSHEY_SIMPLEX, 0.23, (255,255,255), 1)

    return ortho_image_parcels






def save_labelled_parcels(all_parcels, elevation_parcels, ndvi_parcels, lai_parcels, labels):

    data = {} 
    data['parcel'] = all_parcels
    data['elevation'] = elevation_parcels
    data['ndvi'] = ndvi_parcels
    data['lai'] = lai_parcels
    data['diseased'] = labels

    df = pd.DataFrame(data)
    df.to_csv('labelled_parcels.csv', index=False)