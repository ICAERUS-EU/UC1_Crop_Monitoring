""" Code to locate plants from row-view images to global orthomosaic view following a grid layout"""

__author__ = "Esther Vera"
__copyright__ = "Copyright 2023, Noumena"
__credits__ = ["Esther Vera, Aldo Sollazzo"]
__version__ = "1.0.0"
__maintainer__ = "Esther Vera"
__email__ = "esther@noumena.io"
__status__ = "Production"
__license__ = "MIT"


import cv2 
from src.read import read_json, read_list_json, read_transform_and_mask
from src.GridPlantLocator import GridPlantLocator
from src.Output import Output


# LOAD VARIABLES 
# ==========================================================================================

# Path to files 
image_path = "../../data/images/orthomosaic_cropped_230609.tif" # Created with Agisoft software
row_points_path = "../../data/features/parallel_rows_points1.json"  # Extracted with the file: UC1_Crop_Monitoring/top_view/create_grid/get_plant_rows.py
parcels_points_path = "../../data/features/parcel_points1.json" 
centers_parcels_path = "../../data/features/parcel_centers_points1.json" 
date = image_path.split('/')[-1].split('.')[0].split('_')[-1]

gps_path = "../../data/features/all_coords.json"  # This was extracted from the orthomosaic information (code still not provided)
model_path = "../01_plant_disease_detection_yolov8_v1/best.pt"
save_images_path = "../../data/"
row_images_path = "../../data/images_row/"
#"/run/media/noumena/nmn_dufry/ICAERUS/01-MEDIA/RAW_IMAGES/ROWS/230609_D/"

# Load image   
image = cv2.imread(image_path)
transform, mask = read_transform_and_mask(image_path)

# Read the points that define each row 
row_points = read_json(row_points_path)
parcels_points = read_list_json(parcels_points_path)
centers_parcels = read_list_json(centers_parcels_path)

# Read GPS coordinates for every pixel in orthomosaic image
print("Loading gps coordinates...")
all_coords = read_json(gps_path)


# PROCESSING
# ==========================================================================================

# Create GridPlantLocator class variable
gridPlant = GridPlantLocator(image, transform, model_path, all_coords, row_points, row_images_path, parcels_points, centers_parcels, save_images_path)

# Get GPS position of the drones from the row images
all_row_images, all_drone_gps_locations = gridPlant.get_drones_gps_location(row_images_path)


# Get pixel location of the drones transforming its GPS location to pixel using the transform matrix of the orthomosaic 
all_drone_pixels_locations = gridPlant.get_drones_pixels_locations()

# Match the pixel position of the drone in the orthomosaic to the closest parcel depending on the orientation of the drone
print("Matching parcels to drone images")
parcels_selected, parcels_points_flatten = gridPlant.match_parcel_to_row_image()

# For each drone position, perform yolo detection of the image and classify plants into the global image  
all_health_status = gridPlant.track_plants(False)



# EXPORT DATA
# ==========================================================================================

# Delete data not used in global visualization 
out = Output(all_row_images, all_drone_gps_locations, all_drone_pixels_locations, parcels_selected, parcels_points_flatten, all_health_status)
out.filter()

# Export drone pixels, drone GPS, parcels position and plant status 
out.export_data(date)


# SHOW AND SAVE IMAGES
# ==========================================================================================

# Draws and saves the row detections and drone positions
gridPlant.draw_grid()
