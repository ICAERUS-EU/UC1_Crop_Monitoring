""" Functions to read jsons and images with rasterio """

__author__ = "Esther Vera"
__copyright__ = "Copyright 2023, Noumena"
__credits__ = ["Esther Vera, Aldo Sollazzo"]
__version__ = "1.0.0"
__maintainer__ = "Esther Vera"
__email__ = "esther@noumena.io"
__status__ = "Production"
__license__ = "MIT"

import json 
import rasterio 
import numpy as np 


def read_json(json_path): 
    """
    Reads JSON data from a file.
    
    Args:
        json_path (str): The path to the JSON file.
    
    Returns:
        data (numpy.ndarray): The JSON data converted into a NumPy array.
    """
    with open(json_path, 'r') as f:
        data = np.array(json.load(f))

    return data


def read_list_json(json_path): 
    """
    Reads JSON data from a file.
    
    Args:
        json_path (str): The path to the JSON file.
    
    Returns:
        data (numpy.ndarray): The JSON data converted into a NumPy array.
    """
    with open(json_path, 'r') as f:
        data = list(json.load(f))

    return data


def read_transform_and_mask(image_path): 
    """
    Reads an image file using rasterio and extracts its transformation matrix and mask.
    
    Args:
        image_path (str): The path to the image file.
    
    Returns:
        transform (affine.Affine): The affine transformation matrix of the image.
        mask (numpy.ndarray): The mask extracted from the image.
    """
    with rasterio.open(image_path) as src:
        transform = src.transform
        mask = src.read(4)

    return transform, mask




