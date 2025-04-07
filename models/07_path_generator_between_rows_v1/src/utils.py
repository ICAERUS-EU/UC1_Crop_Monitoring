""" Functions to save and read data """

__author__ = "Esther Vera"
__copyright__ = "Copyright 2025, Noumena"
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


# Helper function to save data as a JSON file
def save_json(base_path_features, filename, data):
    with open(os.path.join(base_path_features, filename), 'w') as f:
        json.dump(data, f)


# Helper function to read json data
def read_json(base_path_features, filename):
    with open(os.path.join(base_path_features, filename), 'r') as f:
        data = json.load(f)
    return data

