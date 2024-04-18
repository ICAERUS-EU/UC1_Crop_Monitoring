
import rasterio 
import cv2 
import numpy as np
import json 
import math
from tqdm import tqdm 

from src.read import read_transform_and_mask, read_json, smooth_mask
from src.PlantLocator import PlantLocator
from src.PlantDetector import PlantDetector





# PLANT DETECTION IN ROW IMAGES 
# ==========================================================================================

# Get plant detections and health status 

detector = PlantDetector()
detector.track_plants("images_tracking/")
print(detector.all_locations)  
print(detector.all_health_status)





# LOAD VARIABLES 
# ==========================================================================================

all_coords = []
all_pixels = []
all_locations = detector.all_locations
all_health_status = detector.all_health_status
location = all_locations[0]


# Path to files 
image_path = "orthomosaic_cropped_230609.tif"
row_points_path = 'parallel_rows_points.json'
gps_path = 'all_coords.json'


# Load image   
image = cv2.imread(image_path)
transform, mask = read_transform_and_mask(image_path)
smoothed_mask = smooth_mask(mask)
size = image.shape


# Read the points that define each row 
row_points = read_json(row_points_path)

# Read GPS coordinates for every pixel in orthomosaic image
print("Loading gps coordinates...")
all_coords = read_json(gps_path)

# Load PlantLocator
print("Creating plant locator object...")
plantloc = PlantLocator(image, mask, transform, all_coords, row_points, all_locations, all_health_status)

# Get location in pixels of the plants in the rows
print("Getting pixels of the plants in the rows...")
rows_pixels_location = plantloc.get_row_pixels()

# Get location in GPS of the plants in the rows
print("Getting GPS location of the rows...")
rows_location = plantloc.get_row_location()



# PROCESS PLANT LOCATION 
# ==========================================================================================

print("Getting plant location in the rows...")
all_pixel_drone_loc, all_pixel_plant_loc, all_plant_loc = plantloc.get_all_final_plant_locations()


print("Drawing plant and drone positions in image...")
plant_positions_image = plantloc.draw_plant_positions(all_pixel_plant_loc, all_pixel_drone_loc) 

print("all_pixel_drone_loc", all_pixel_drone_loc)
print("all_pixel_plant_loc", all_pixel_plant_loc)
print("all_plant_loc", all_plant_loc)



cv2.imwrite("plant_positions_image.jpg", plant_positions_image)
cv2.imshow("plant_positions_image", plant_positions_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
