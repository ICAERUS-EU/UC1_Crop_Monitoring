""" Organize and export data"""

__author__ = "Esther Vera"
__copyright__ = "Copyright 2023, Noumena"
__credits__ = ["Esther Vera, Aldo Sollazzo"]
__version__ = "1.0.0"
__maintainer__ = "Esther Vera"
__email__ = "esther@noumena.io"
__status__ = "Production"
__license__ = "MIT"


import numpy as np
import pandas as pd 


class Output:
    def __init__(self, all_row_images, all_drone_gps_locations, all_drone_pixels_locations, parcels_selected, parcels_points_flatten, sel_health_status):
       
        self._sel_row_images = np.array(all_row_images)
        self._sel_drone_gps_locations = np.array(all_drone_gps_locations)
        self._sel_drone_pixels_locations = np.array(all_drone_pixels_locations)
        self._sel_parcels = np.array(parcels_selected)
        self._sel_parcels_points_flatten = np.array(parcels_points_flatten)
        self._sel_health_status = np.array(sel_health_status)


    def filter(self):
        # Masked array and valid indexes
        mask = (self._sel_parcels != -1)
        self._valid_indexes = list(self._sel_parcels[mask])

        # Select drone positions and images depending on the values that are not -1 in parcels_selected  
        self._sel_row_images = self._sel_row_images[mask]
        self._sel_drone_gps_locations = list(self._sel_drone_gps_locations[mask])
        self._sel_drone_pixels_locations = list(self._sel_drone_pixels_locations[mask])

        # Select parcels depending on its index 
        self._sel_parcels_points_flatten = list(self._sel_parcels_points_flatten[self._valid_indexes])


    def export_data(self, date): 
        
        # Create dataframe with the selected data
        data = {
            'row_images': self._sel_row_images,
            'drone_gps': self._sel_drone_gps_locations,
            'drone_pixels': self._sel_drone_pixels_locations,
            'parcels_indexes': self._valid_indexes,
            'parcels': self._sel_parcels_points_flatten
        }

        df = pd.DataFrame(data)

        # Export dataframe to CSV
        df.to_csv('parcels_drones_{0}.csv'.format(date), index=False)

        print("\nExported data to 'selected_data.csv'")
                

