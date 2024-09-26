""" Code designed to get the vineyards rows and make the grid depending on rows direction """

__author__ = "Esther Vera"
__copyright__ = "Copyright 2023, Noumena"
__credits__ = ["Esther Vera, Aldo Sollazzo"]
__version__ = "1.0.0"
__maintainer__ = "Esther Vera"
__email__ = "esther@noumena.io"
__status__ = "Production"
__license__ = "MIT"

import os

from src.OrthomosaicProcessor import OrthomosaicProcessor
from src.VineyardRowDetector import VineyardRowDetector
from src.ParcelDetector import ParcelDetector
from src.utils import save_data, save_images, show_images


# VARIABLES 
# ===============================================================================================

# If true, the start point for the first row can be defined manually; if false, it will use the predefined coordinate
select_points = False 
#select_points = True

# Depending on the vineyard or the image size, this should be defined 
#VINEYARD_SEP = 37    # Separation between vineyards rows
#PARCEL_LEN = 70      # Size of the parcels (5.2 m in real life when taking into account image resized and resolution)
#PARCEL_LEN = 14      # Size of the parcels (1 m in real life when taking into account image resized and resolution)
#PARCEL_LEN = 27      # Size of the parcels (1 m in real life when taking into account image resized and resolution)

VINEYARD_SEP = 74     # Separation between vineyards rows
PARCEL_LEN = 141.9    # Size of the parcels (5.2 m in real life when vineyard image in real size)
VINEYARD_HEIGHT = 10  # Width of the vineyard row

# Paths to saved data
base_path = './../../data/'
base_path_images = base_path + 'images/'
base_path_features = base_path + 'features/'


# MAIN FUNCTION  
# ===============================================================================================

def main():

    # Load images to calculate the grid 
    op = OrthomosaicProcessor()
    tif_path = os.path.join(base_path_images, "orthomosaic_cropped_230609.tif")
    ortho_image, _, _, _, mask = op.read_orthomosaic(tif_path) 

    # ===============================================================================================
    # Create a VineyardRowDetector object to get the rows in the vineyard
    vrd = VineyardRowDetector(ortho_image, mask, VINEYARD_SEP)
    vrd.get_coordinates_row(select_points)
    parallel_rows_points = vrd.get_parallel_rows()
    masked_rows_image, filtered_rows_image = vrd.get_filtered_rows()

    # ===============================================================================================
    # Create a ParcelDetector object to get the parcels inside the rows
    pdet = ParcelDetector(ortho_image, mask, filtered_rows_image, parallel_rows_points, PARCEL_LEN)
    all_parcel_points, centers_parcels = pdet.get_all_parcel_points()
    parcel_rows_image = pdet.draw_rgb_parcels(all_parcel_points)
    map_rows_image = pdet.draw_map_parcels(all_parcel_points)

    # ===============================================================================================
    # Save and show data
    save_data(base_path, all_parcel_points, parallel_rows_points, centers_parcels)
    save_images(masked_rows_image, parcel_rows_image, map_rows_image)
    show_images(masked_rows_image, parcel_rows_image, map_rows_image)


if __name__ == "__main__":
    main()





