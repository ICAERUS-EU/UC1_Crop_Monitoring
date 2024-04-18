import cv2
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



def smooth_mask(mask): 
    """
    Applies a series of image processing operations to smooth a binary mask.

    Args:
    - mask: The binary mask to be smoothed.

    Returns:
    - smoothed_mask: The smoothed mask.
    """
    # Definition of kernels
    kernel7 = np.ones((7, 7), np.uint8)
    kernel3 = np.ones((5, 5), np.uint8)

    # Smooth the mask
    smoothed_mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel7)
    smoothed_mask = cv2.erode(smoothed_mask, kernel3, iterations=5)
    smoothed_mask = cv2.GaussianBlur(smoothed_mask, (5, 5), 0)

    return smoothed_mask


