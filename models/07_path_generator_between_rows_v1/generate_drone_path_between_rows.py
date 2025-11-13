""" Code designed to generate a path for the drone to flight between rows """

__author__ = "Esther Vera"
__copyright__ = "Copyright 2025, Noumena"
__credits__ = ["Esther Vera, Aldo Sollazzo"]
__version__ = "1.0.0"
__maintainer__ = "Esther Vera"
__email__ = "esther@noumena.io"
__status__ = "Production"
__license__ = "MIT"


from src.OrthomosaicProcessor import OrthomosaicProcessor
from src.VineyardRowDetector import VineyardRowDetector
from src.PathGenerator import PathGenerator
from src.utils import save_json, read_json

import cv2
# VARIABLES 
# ===============================================================================================

# If true, the start point for the first row can be defined manually; if false, it will use the predefined coordinate
select_points = False 

# Depending on the vineyard or the image size, this should be defined 
VINEYARD_HEIGHT = 85  # Height of the vineyard row (original ortho size)
VINEYARD_SEP = 296    # Separation between vineyards rows (original ortho size)

# Paths to saved data
base_path = './../../data/'
base_path_images = base_path + 'images/'
base_path_features = base_path + 'features/'

# Select orthomosaic
base_path = "/run/media/noumena/8TB/ZENODO/2023"
date = '230609'


# MAIN FUNCTION  
# ===============================================================================================

def main():

    # LOAD ORTHOMOSAIC AND MASK
    # ===============================================================================================
    ortho_processor = OrthomosaicProcessor()
    tif_path = "{0}/{1}/ORTHOMOSAICS/CROPPED_ORTHOMOSAIC_{1}.tif".format(base_path, date)        
    ortho_image, _, _, _, mask =  ortho_processor.read_orthomosaic(tif_path)    


    # DETECT VINEYARD ROWS
    # ===============================================================================================
    '''# Create a VineyardRowDetector object to get the rows in the vineyard
    row_detector = VineyardRowDetector(ortho_image, mask, VINEYARD_HEIGHT, VINEYARD_SEP)
    row_detector.get_init_row_coordinates(select_points)
    parallel_rows_points = row_detector.get_parallel_rows()
    masked_rows_image = row_detector.filter_rows()

    # Get vineyard row points and convert them to list 
    rows_contours, rows = row_detector.get_rows_coordinates(masked_rows_image) 

    # Save rows points to json
    save_json(base_path_features, 'rows_contour_coordinates.json', rows_contours) 
    save_json(base_path_features, 'rows_coordinates.json', rows)
    '''

    # GENERATE DRON PATH AND GET GPS COORDINATES 
    # ===============================================================================================
    # You can comment the section "DETECT VINEYARD ROWS" and go directly to this reading function
    rows = read_json(base_path_features, 'rows_coordinates.json') 

    # Get drone path in pixel coordinates 
    path_generator = PathGenerator(rows)
    path = path_generator.generate_path()

    # Get drone path between rows in gps coordinates
    drone_path_gps = path_generator.get_drone_path_in_gps(tif_path, path)

    # Save drone gps path between rows    
    save_json(base_path_features, 'drone_path_gps.json', drone_path_gps)

    # Draw path in matplotlib and over orthomosaic image in pixel coordinatess
    path_generator.draw_path_image(path, ortho_image)
    path_generator.draw_path(path)


if __name__ == "__main__":
    main()





