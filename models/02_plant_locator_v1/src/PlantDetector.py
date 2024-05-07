""" Code to detect the middle plants of a row-view image """

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
import math
import time 
import numpy as np 
from PIL import Image
from PIL.ExifTags import TAGS
from ultralytics import YOLO
import matplotlib.pyplot as plt



class PlantDetector:
    def __init__(self, model_path, row_images_path, save_images_folder):
        self._R = 6371000 
        self._add_dist = 0
        self._health_middle_plant = -1
        self._first  = True
        self._location = [0, 0]
        self._plocation = [0, 0]
        self._middle_plant = []
        self._all_locations = []
        self._all_health_status = []
        self._model = YOLO(model_path)
        self._row_images_path = row_images_path
        self._save_images_folder = save_images_folder
        self._all_images = os.listdir(row_images_path)
    
    
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
    


    

    def distance_between_points(self) -> float:
        """
        Calculates the distance between two geographic points using their latitude and longitude coordinates.

        Args:
            location (tuple): Latitude and longitude coordinates of the actual point.

        Returns:
            float: Distance between two points in meters.
        """

        plat, plon, lat, lon = map(math.radians, [self._plocation[0], self._plocation[1], self._location[0], self._location[1]])
        dlat = plat - lat
        dlon = plon - lon
        a = math.sin(dlat/2)**2 + math.cos(lat) * math.cos(plat) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        distance = self._R * c

        return distance
    

    def dms2dd(self, dms, geodir) -> np.float64:
        """
        Converts degrees, minutes, and seconds (DMS) coordinates to decimal degrees (DD).

        Args:
            dms (tuple): Degrees, minutes, and seconds values.
            geodir (str): Geographic direction ('N', 'S', 'E', 'O').

        Returns:
            numpy.float64: Decimal degrees coordinate.
        """

        if geodir in ['S', 'O']:
            dd = -1
        else:
            dd = 1
        return np.float64((dms[0] + dms[1] / 60 + dms[2] / 3600) * dd)
    

    def get_gps_info(self, image_path) -> None:
        img = Image.open(image_path)
        info_exif = img._getexif()
        
        for tag, value in info_exif.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == 'GPSInfo':
                lat = self.dms2dd(value[2], value[1])
                lon = self.dms2dd(value[4], value[3])
                self._location = [lat, lon]
                break
    

    def draw_bbox(self, frame) -> np.ndarray:
        """
            Draws bounding boxes on a frame based on detected objects and their health status.

            Args:
                frame (numpy.ndarray): Input frame.
                bboxes (numpy.ndarray): Array of bounding boxes.

            Returns:
                frame (numpy.ndarray): Frame with bounding boxes drawn.
        """

        for bbox, health in zip([self._middle_plant], [self._health_middle_plant]):
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[2]), int(bbox[3]))
            if health == 1:
                cv2.rectangle(frame, p1, p2, (0, 255, 0), 50, 2)
            else:
                cv2.rectangle(frame, p1, p2, (0, 0, 255), 50, 2)
        return frame 
    

    def get_center(self, bbox) -> list:
        """
            Calculates the center of a bounding box.

            Args:
                bbox (list): Coordinates of the bounding box [x1, y1, x2, y2].

            Returns:
                center (list): Coordinates of the center [x_center, y_center].
        """

        x = bbox[2] - ((bbox[2]-bbox[0]) / 2)
        y = bbox[3] - ((bbox[3]-bbox[1]) / 2)
        return [x, y]
    

    def get_middle_plant(self, frame, bboxes, health_status) -> None:
        """
        Finds the middle plant in the frame based on bounding box centers and their distances from the frame's center.

        Args:
            frame (numpy.ndarray): Input frame.
            bboxes (numpy.ndarray): Array of bounding boxes.
            health_status (list): List of health statuses corresponding to each bounding box.
        """

        # Limit distance to consider a plant in the middle 
        limit = frame.shape[1] // 6

        # Calculate the distances between the center of each bounding box and the center of the frame
        center_frame = np.array([frame.shape[1]//2, frame.shape[0]//2])
        all_centers = np.array([self.get_center(bbox) for bbox in bboxes])
        distances = np.linalg.norm(all_centers - center_frame, axis=1)

        # Select the bbox related to the middle plant and its health 
        self._middle_plant = bboxes[np.argmin(distances)]
        self._health_middle_plant = np.round(health_status[np.argmin(distances)])
        
        # Update the middle plant and its health if another plant is closer to the center within a certain distance and with high confidence
        '''for dist, conf, bbox in zip(distances, health_status, bboxes): 
            if abs(dist) < limit and conf > 0.6:
                self._middle_plant = bbox
                self._health_middle_plant = np.round(conf)'''
        

    def get_middle_plant_location(self, image_path, frame, bboxes, health_status) -> None:
        """
        Gets the location of the middle plant in the image based on its GPS coordinates and calculates its distance from the previous location.

        Args:
            image_path (str): Path to the image file containing GPS metadata.
            frame (numpy.ndarray): Input frame.
            bboxes (numpy.ndarray): Array of bounding boxes.
            health_status (list): List of health statuses corresponding to each bounding box.

        Returns:
            tuple: Tuple containing the location of the middle plant, its bounding box, and health status.
        """

        # Reset variables
        self._health_middle_plant = -1
        self._middle_plant = []
        
        # Get plant location and distance from previous location
        self.get_gps_info(image_path)

        # Get distance between the previous and actual drone position 
        if self._first:  
            dist = 100
            self._first = False
        else:
            dist = self.distance_between_points()
            dist += self.add_dist 

        # If the drone has moved enough distance from previous detection, it is a different plant 
        if dist >= 0.6:
            # Gets plant position and status 
            self.get_middle_plant(frame, bboxes, health_status) 
            self._add_dist = 0 # Reset distance from plant 
        else: 
            # Add new distance to plant 
            self._add_dist += self._pdist
        
        # Save previous location and distance
        self._plocation = self._location
        self._pdist = dist
        
    

    def track_plants(self) -> None:
        """
        Tracks plants in a series of images, saves their health status and locations, and displays images with detected plants.
        """

        self._first = True

        cont = 0
        for img_path in self._all_images:
            cont = cont+1

            if(cont ==2):
                break
            
            # Read row image 
            complete_img_path = os.path.join(self._row_images_path, img_path)
            frame = cv2.imread(complete_img_path)

            # Detect plant and health status in image 
            results = self._model.predict(frame)
            health_status = np.array(results[0].boxes.conf.cpu().numpy().astype(float))
            bboxes = self.filter_predictions(results)

            # Get middle plant detected 
            self.get_middle_plant_location(complete_img_path, frame, bboxes, health_status)
            
            # If plant detected, save location and health 
            if self._health_middle_plant > -1:
                self.all_health_status.append(self._health_middle_plant)
                self.all_locations.append(self._location)

                # Draw bbox around plant detected 
                frame = self.draw_bbox(frame)

            # Save and show detected plants in images
            #cv2.imwrite(self._save_images_folder + img_path, frame)
            cv2.imshow("Plant detected", cv2.resize(frame, None, fx=0.1, fy=0.1))
            if cv2.waitKey(3) & 0xFF == ord('s'):
                break
        cv2.destroyAllWindows()


