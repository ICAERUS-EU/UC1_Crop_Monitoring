""" Code to locate plants from row-view images to global orthomosaic view """

__author__ = "Esther Vera"
__copyright__ = "Copyright 2023, Noumena"
__credits__ = ["Esther Vera, Aldo Sollazzo"]
__version__ = "1.0.0"
__maintainer__ = "Esther Vera"
__email__ = "esther@noumena.io"
__status__ = "Production"
__license__ = "MIT"


import cv2 
import json 
import math
import rasterio 
import numpy as np
from tqdm import tqdm 

from src.read import read_json, read_transform_and_mask
from src.PlantLocator import PlantLocator
from src.PlantDetector import PlantDetector


# LOAD VARIABLES 
# ==========================================================================================

# Path to files 
image_path = "../../data/images/orthomosaic_cropped_230609.tif" # Created with Agisoft software
row_points_path = "../../data/features/parallel_rows_points.json"  # Extracted with the file: UC1_Crop_Monitoring/top_view/create_grid/get_plant_rows.py
gps_path = "../../data/features/all_coords.json"  # This was extracted from the orthomosaic information (code still not provided)
model_path = "../01_plant_disease_detection_yolov8_v1/best.pt"
save_images_path = "../../data/"
row_images_path = "../../data/images_row/"

# Load image   
image = cv2.imread(image_path)
transform, mask = read_transform_and_mask(image_path)

# Read the points that define each row 
row_points = read_json(row_points_path)

# Read GPS coordinates for every pixel in orthomosaic image
print("Loading gps coordinates...")
all_coords = read_json(gps_path)


# PLANT DETECTION IN ROW IMAGES 
# ==========================================================================================

# Detect the middle plant of each row image and its health status 
det = PlantDetector(model_path, row_images_path, save_images_path)
det.track_plants()
print("\nPlant locations in row images: ", det._all_locations)  
print("Plant status in row images: ", det._all_health_status)


# PLANT LOCATION FROM ROW IMAGE DETECTION TO GLOBAL ORTHOMOSAIC IMAGE 
# ==========================================================================================

# Init plantlocator object to perform the location operations
print("\nStarting plant locator from row-view to global-view")
loc = PlantLocator(image, mask, transform, all_coords, row_points, det._all_locations, det._all_health_status)

# Get location in pixels of the plants in the rows
print("Getting pixels of the plants in the rows...")
rows_pixels_location = loc.get_row_pixels()

# Get location in GPS of the plants in the rows
print("Getting GPS location of the rows...")
rows_location = loc.get_row_location()

# Get location of the detected plant in the global orthomosaic view
print("Getting plant location in the rows...")
all_pixel_drone_loc, all_pixel_plant_loc, all_plant_loc = loc.get_all_final_plant_locations()

# Draw these plant and drone locations in the global view
print("Drawing plant and drone positions in image...")
drawDrone = True # If true, draws the drone position
plant_positions_image = loc.draw_plants_and_drone(all_pixel_plant_loc, all_pixel_drone_loc, drawDrone) 

print("\nPlant GPS positions", all_plant_loc)
print("Plant pixel positions: ", all_pixel_plant_loc)
print("Drone pixel positions: ", all_pixel_drone_loc)


# SHOW AND SAVE IMAGES
# ==========================================================================================

cv2.imwrite("plants_and_drone_located.jpg", plant_positions_image)
cv2.imshow("plant_positions_image", plant_positions_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
