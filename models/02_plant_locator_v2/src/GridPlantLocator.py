""" Detects the middle plants of a row-view image and locate them in a global visualization """

__author__ = "Esther Vera"
__copyright__ = "Copyright 2023, Noumena"
__credits__ = ["Esther Vera, Aldo Sollazzo"]
__version__ = "1.0.0"
__maintainer__ = "Esther Vera"
__email__ = "esther@noumena.io"
__status__ = "Production"
__license__ = "MIT"

import os 
import cv2 
import numpy as np 
from ultralytics import YOLO
from scipy.spatial import KDTree

from src.LinesIntersection import LinesIntersection
from src.Display import Display
from src.Calculation import Calculation


class GridPlantLocator:
    def __init__(self, image, transform, model_path, all_coords, row_points, row_images_path, parcels_points, centers_points, save_images_folder):
        
        self._image = image
        self._size = image.shape[0:2]
        self._all_pixels = np.indices((self._size[0], self._size[1])).reshape(2, -1).T
        self._transform = transform
        self._model = YOLO(model_path)
        self._all_coords = all_coords
        self._row_points = row_points
        self._row_images_path = row_images_path
        self._all_images = sorted(os.listdir(row_images_path))
        
        self._length = 3000  
        self._offset = -90
        self._drone_angle = np.radians(self._offset - 8.3) # This value is extracted from the image metadata (still not integrated in the flow
        self._INT_MAX = np.iinfo(np.int64).max
        self._first = True

        self.calc = Calculation(image, row_points, parcels_points, centers_points)
        self._parcels_points_flatten = self.calc.get_parcels_points_flatten()
        self._centers_points_flatten = self.calc.get_centers_points_flatten()
        self.display = Display(image, row_points, self._parcels_points_flatten, self._centers_points_flatten, save_images_folder)

        self._drone_gps_locations = []
        self._all_row_images = []
        self._drone_pixels_locations = []
        self._parcels_selected = []
        self._parcels_drones = []
        self._all_health_status = []


    def get_drones_gps_location(self, row_images_path): 
        for image_name in sorted(os.listdir(row_images_path)):
            image_path = row_images_path + image_name
            self._all_row_images.append(image_path)
            self._drone_gps_locations.append(self.calc.get_gps_info(image_path))
        
        return self._all_row_images, self._drone_gps_locations


    def get_drones_pixels_locations(self):
        """
        Determines the drone's pixel location based on its GPS position and the orthomosaic GPS relation between pixels.
        """

        # Build a KDTree for the orthomosaic coordinates
        tree = KDTree(self._all_coords)

        # Find the closest coordinates from orthomosaic coordinates to the drones locations
        distances, indexes = tree.query(self._drone_gps_locations)

        # Get the drone coordinates related to the orthomosaic and its pixels
        drone_orthomosaic = self._all_coords[indexes]
        self._drone_pixels_locations = self._all_pixels[indexes]

        return self._drone_pixels_locations


    def drone_in_parcel(self, parcel_image, drone_pixel) -> list: 

        drone_inside = False
        all_selected_parcels = []
        all_distances = []
        blank_orientation = np.zeros((self._size[0], self._size[1], 1), dtype=np.uint8)

        # Calculate the line representing the drone's orientation in the image 
        x2 = int(drone_pixel[0] + self._length * np.cos(self._drone_angle))
        y2 = int(drone_pixel[1] + self._length * np.sin(self._drone_angle))
        blank_orientation = cv2.line(blank_orientation, (drone_pixel[0], drone_pixel[1]), (x2, y2), (255), 1)
        
        # Find positions of pixels where the intersection occurred between the drone orientation line and actual parcel
        blank_final = cv2.bitwise_and(blank_orientation, self._blank_rows)

        #blank_final = cv2.bitwise_and(blank_orientation, parcel_image)
        pos_pixels_found = np.where(blank_final == 255)
        possible_pixels_loc = list(zip(pos_pixels_found[1], pos_pixels_found[0])) # List of possible plant positions 
        if(possible_pixels_loc):
            drone_inside = True
            
            if(self._first):
                self._first = False
                self._blank_or = cv2.bitwise_or(blank_orientation, self._blank_rows)
            else: 
                self._blank_or = cv2.bitwise_or(self._blank_or, blank_orientation)
                
            min_dist = self._INT_MAX
            selected_parcel = -1
            for possible_drone_pixel in possible_pixels_loc: 

                distances = np.linalg.norm(np.array(self._centers_points_flatten) - np.array(possible_drone_pixel), axis=1)
                idx_center = np.argmin(distances)
                center_parcel = self._centers_points_flatten[idx_center]

                dist_original = np.linalg.norm(possible_drone_pixel - drone_pixel)

                if(dist_original < min_dist):
                    min_dist = dist_original
                    selected_parcel = center_parcel
                    idx_parcel = idx_center

            all_selected_parcels.append(selected_parcel) 
            all_distances.append(min_dist)

        return all_selected_parcels, all_distances
        
        
    def match_parcel_to_row_image(self):
      
        inter = LinesIntersection(self._drone_pixels_locations, self._drone_angle, self._row_points, self._parcels_points_flatten, self._centers_points_flatten, self._all_row_images) 
        inter.get_drone_intersections()
        self._parcels_drones = inter.get_parcels_intersected()
        self._parcels_selected = inter.filter_drones()
        self.display.draw_drones_and_parcels(self._drone_pixels_locations, self._parcels_selected)

        return self._parcels_selected, self._parcels_points_flatten
    

    def filter_predictions(self, results) -> np.ndarray:
        """
            Filters predictions based on confidence scores using Non-Maximum Suppression (NMS).

            Args:
                results (list): List of prediction results.

            Returns:
                bboxes_selected (numpy.ndarray): Selected bounding boxes after filtering.
        """

        for result in results:
            bboxes = result.boxes.xyxy
            scores = np.array(result.boxes.conf.cpu())
            bboxes_arr = np.array([np.array(bbox.cpu()) for bbox in bboxes])
            selected_indices = cv2.dnn.NMSBoxes(bboxes_arr, scores, 0.15, 0.6)
            bboxes_selected = np.array([bboxes_arr[i] for i in selected_indices])
        return bboxes_selected
    
        
    def get_middle_plant(self, image_path, frame, bboxes, health_status_frame) -> None:
        
        all_centers_bbox = []
        for bbox in bboxes: 
            center_bbox = self.calc.get_center(bbox)
            all_centers_bbox.append(center_bbox)

        h,w,_ = frame.shape
        center_image = np.array([w//2, h//2])       

        distances = np.linalg.norm(all_centers_bbox - center_image, axis=1)
        idx_plant = np.argmin(distances)
        middle_plant = bboxes[idx_plant]
        health_status = health_status_frame[idx_plant]

        return middle_plant, health_status
    

    def track_plants(self, show=False) -> None:
        """
        Tracks plants in a series of images, saves their health status and locations, and displays images with detected plants.
        """

        self._all_health_status = len(self._all_images) * [-1]

        for idx, img_path in enumerate(self._all_images):
            
            if(self._parcels_selected != -1):

                # Read row image 
                complete_img_path = os.path.join(self._row_images_path, img_path)
                frame = cv2.imread(complete_img_path)

                # Detect plant and health status in image 
                results = self._model.predict(frame)
                health_status_frame = np.array(results[0].boxes.conf.cpu().numpy().astype(float))
                bboxes = self.filter_predictions(results)

                # Get middle plant detected 
                if(len(bboxes)):
                    middle_plant, health_status = self.get_middle_plant(complete_img_path, frame, bboxes, health_status_frame)
                    self._all_health_status[idx] = health_status
                    
                    if(show):
                        self.display.show_bbox_plants(frame, img_path, middle_plant, health_status)     
                else: 
                    self._parcels_selected[idx] = -1


    def draw_grid(self) -> None:
        self.display.draw_drones_and_parcels_color(self.calc, self._drone_pixels_locations, self._parcels_selected, self._all_health_status)

