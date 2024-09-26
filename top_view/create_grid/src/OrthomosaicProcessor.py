""" Class to load and process orthomosaic images """

__author__ = "Esther Vera"
__copyright__ = "Copyright 2024, Noumena"
__credits__ = ["Esther Vera, Oriol Arroyo, Salvador Calgua, Aldo Sollazzo"]
__version__ = "1.0.0"
__maintainer__ = "Esther Vera"
__email__ = "esther@noumena.io"
__status__ = "Production"
__license__ = "MIT"

import cv2
import rasterio
import numpy as np


class OrthomosaicProcessor:
    def __init__(self):
        """
        Initializes an instance of the OrthomosaicProcessor class.
        """
        pass

    def read_orthomosaic(self, tif_path):
        """
        Reads an orthomosaic image from a TIF file and extracts its color bands.

        Args:
            tif_path (str): The file path to the TIF orthomosaic image.

        Returns:
            tuple: A tuple containing the RGB image (as a numpy array), 
                   the red band, green band, blue band, and a mask (numpy arrays).
        """
        with rasterio.open(tif_path) as src:
            red_band = src.read(1)
            green_band = src.read(2)
            blue_band = src.read(3)
            rgb_image = cv2.merge([blue_band, green_band, red_band])
            mask = src.read(4)

        return rgb_image, red_band, green_band, blue_band, mask

    def resize_orthomosaic(self, ortho_image, r_image, g_image, b_image, mask, tam=(2346, 1805)):
        """
        Resizes the orthomosaic image and its associated color bands and mask to a specified size.

        Args:
            ortho_image (numpy.ndarray): The original orthomosaic image.
            r_image (numpy.ndarray): The red color band.
            g_image (numpy.ndarray): The green color band.
            b_image (numpy.ndarray): The blue color band.
            mask (np.ndarray): The mask image.
            tam (tuple): The target size for resizing (default is (2346, 1805)).

        Returns:
            tuple: A tuple containing the resized images in the order of 
                   orthomosaic image, red band, green band, blue band, and mask.
        """
        ortho_image_res = cv2.resize(ortho_image, tam)
        r_image_res = cv2.resize(r_image, tam)
        g_image_res = cv2.resize(g_image, tam)
        b_image_res = cv2.resize(b_image, tam)
        mask_res = cv2.resize(mask, tam)

        return ortho_image_res, r_image_res, g_image_res, b_image_res, mask_res

    def read_one_channel_orthomosaic(self, tif_path):
        """
        Reads a single channel (band) from a TIF orthomosaic image.

        Args:
            tif_path (str): The file path to the TIF orthomosaic image.

        Returns:
            img (np.ndarray): The single channel image.
        """
        with rasterio.open(tif_path) as src:
            img = src.read(1)
        return img
    

    def resize_and_convert_type(self, img, tam=(2346, 1805)):
        """
        Resizes an image to a specified size and converts its data type.

        Args:
            img (np.ndarray): The image to be resized and converted.
            tam (tuple): The target size for resizing (default is (2346, 1805)).

        Returns:
            norm_image (np.ndarray): The resized image with pixel values scaled to 0-255 as uint8.
        """
        img_res = cv2.resize(img, tam)
        img_res = ((img_res / 65535.0) * 255.0).astype(np.uint8)
        return img_res

    def normalize_image(self, img):
        """
        Normalizes the pixel values of an image to a range of 0-255.

        Args:
            img (numpy.ndarray): The image to be normalized.

        Returns:
            numpy.ndarray: The normalized image with pixel values in the range 0-255.
        """
        min_val = np.min(img)
        range_val = np.max(img) - min_val
        norm_image = (((img - min_val) / range_val) * 255).astype(np.uint8)

        return norm_image


    def preprocess_images(self, ortho_image, mask, angle): 
        """
        Rotates the orthomosaic image and mask by a specified angle.

        Args:
            ortho_image (numpy.ndarray): The orthomosaic image to be rotated.
            mask (numpy.ndarray): The mask associated with the orthomosaic image.
            angle (float): The angle by which to rotate the images.

        Returns:
            tuple: A tuple containing the rotated orthomosaic image and mask.
        """
        # Calculate the rotation matrix based on the center, angle, and scale.       
        (h, w) = mask.shape[:2]
        center = (w // 2, h // 2)

        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        cos = np.abs(rotation_matrix[0, 0])
        sin = np.abs(rotation_matrix[0, 1])
        new_w = int((h * sin) + (w * cos))
        new_h = int((h * cos) + (w * sin))
        rotation_matrix[0, 2] += (new_w / 2) - center[0]
        rotation_matrix[1, 2] += (new_h / 2) - center[1]
        
        ortho_image = cv2.warpAffine(ortho_image, rotation_matrix, (new_w, new_h), borderValue=(255,255,255))
        mask = cv2.warpAffine(mask, rotation_matrix, (new_w, new_h), borderValue=(0,0,0))

        return ortho_image, mask