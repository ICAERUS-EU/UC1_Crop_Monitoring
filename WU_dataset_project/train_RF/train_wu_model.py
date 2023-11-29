""" Code to match channels from WA dataset and create RGB images """

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
import os



def organise_data(df):

    data = []

    for col in df.columns:
        print(col)

            

    return data



def main(): 


    # Read images and labels names

    excel_data = pd.read_excel('/home/noumena/Documents/WU_DATA/GT.xlsx')

    df = pd.DataFrame(excel_data, columns=['Row_Right_1', 'ID_1_1', 'Image_ID_1_1', 
                                           'Row_Left_1', 'ID_1_2', 'Image_ID_1_2', 
                                           'Row_Right_2', 'ID_2_1', 'Image_ID_2_1', 
                                           'Row_Left_2', 'ID_2_2', 'Image_ID_2_2',
                                           'Row_Right_3', 'ID_3_1', 'Image_ID_3_1',
                                           'Row_Left_3', 'ID_3_2', 'Image_ID_3_2'])

    #print(df['ID_1_1'])

    data = {}
    
    for col in df.columns:
        data[col] = df[col].dropna().tolist()

    print(data)

    X_files = []  
    y_files = []


if __name__ == "__main__":
    main()


