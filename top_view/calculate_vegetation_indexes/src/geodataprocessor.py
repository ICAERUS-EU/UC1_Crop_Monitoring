

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

        rgb_image_res = cv2.resize(rgb_image, (2346, 1805))
        r_image_res = cv2.resize(red_band, (2346, 1805))
        g_image_res = cv2.resize(green_band, (2346, 1805))
        b_image_res = cv2.resize(blue_band, (2346, 1805))

        mask_res = cv2.resize(mask, (2346, 1805))

        return rgb_image_res, r_image_res, g_image_res, b_image_res, mask_res

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


