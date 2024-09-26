""" Functions to save and show data """

__author__ = "Esther Vera"
__copyright__ = "Copyright 2024, Noumena"
__credits__ = ["Esther Vera, Aldo Sollazzo"]
__version__ = "1.0.0"
__maintainer__ = "Esther Vera"
__email__ = "esther@noumena.io"
__status__ = "Production"
__license__ = "MIT"

import os 
import cv2 
import json 
import numpy as np 

def save_data(base_path, parcel_points, parallel_rows_points, centers_parcels): 
    """
    Saves parcel and row data into JSON files.

    Args:
        base_path (str): The base directory path where files will be saved.
        parcel_points (list): A list containing the points that define each parcel.
        parallel_rows_points (list): A list of points representing parallel rows.
        centers_parcels (list): A list containing the center points of each parcel.
    """
    base_path_features = base_path + 'features/'

    # Helper function to save data as a JSON file
    def save_json(data, filename):
        with open(os.path.join(base_path_features, filename), 'w') as f:
            json.dump(data, f)

    # Save all JSON files
    save_json(parcel_points, 'parcel_points_oriented.json')
    save_json(parallel_rows_points, 'parallel_rows_points_oriented.json')
    save_json(centers_parcels, 'parcel_centers_points_oriented.json')
    print("Data saved successfully")

    
def save_images(masked_rows_image, parcel_rows_image, map_rows_image): 
    """
    Saves the processed images to JPEG files.

    Args:
        masked_rows_image (numpy.ndarray): The image with masked rows.
        parcel_rows_image (numpy.ndarray): The image with drawn parcel rows.
    """
    cv2.imwrite('masked_rows_image.jpg', masked_rows_image)
    cv2.imwrite('parcel_rows_image.jpg', parcel_rows_image)
    cv2.imwrite('map_rows_image.jpg', map_rows_image)
    print("Images saved successfully")


def show_images(masked_rows_image, parcel_rows_image, map_rows_image): 
    """
    Displays the images in separate windows.

    Args:
        masked_rows_image (numpy.ndarray): The image with masked rows to be displayed.
        parcel_rows_image (numpy.ndarray): The image with drawn parcel rows to be displayed.
    """
    cv2.imshow('masked_rows_image',cv2.resize(masked_rows_image, None, fx=0.3,fy=0.3))
    cv2.imshow('parcel_rows_image', cv2.resize(parcel_rows_image, None, fx=0.3,fy=0.3))
    cv2.imshow('map_rows_image', cv2.resize(map_rows_image, None, fx=0.3,fy=0.3))
    cv2.waitKey(0)
    cv2.destroyAllWindows()