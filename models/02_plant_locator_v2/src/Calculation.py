


""" Operations needed to calculate drone positions """

__author__ = "Esther Vera"
__copyright__ = "Copyright 2023, Noumena"
__credits__ = ["Esther Vera, Aldo Sollazzo"]
__version__ = "1.0.0"
__maintainer__ = "Esther Vera"
__email__ = "esther@noumena.io"
__status__ = "Production"
__license__ = "MIT"

import cv2 
import math
import numpy as np 
from PIL import Image
from PIL.ExifTags import TAGS


class Calculation:
    def __init__(self, image, transform, parcels_points, centers_parcels):

        self._image = image
        self._transform = transform
        self._parcels_points_flatten = [parcel for row in parcels_points for parcel in row]
        self._centers_points_flatten = [center for row in centers_parcels for center in row]

        self._R = 6371000 
        self._tri_size = 25
        self._size = image.shape[0:2]
        self._length = 3000  
        self._offset = -90
        self._drone_angle = np.radians(self._offset - 8.3) # This value is extracted from the image metadata (still not integrated in the flow
        self._angle = np.rad2deg(0.22673090865593348)      # This value is extracted from the image metadata (still not integrated in the flow)

   

    def get_parcels_points_flatten(self): 
        return self._parcels_points_flatten


    def get_centers_points_flatten(self): 
        return self._centers_points_flatten


    def get_parcels_gps_location(self, centers_parcels): 
        
        for k1, row in enumerate(centers_parcels):
            for k2, center in enumerate(row):
                self._parcels_loc.append(np.flip(self._transform * center))
        self._parcels_loc = np.array(self._parcels_loc)


    def get_gps_info(self, image_path) -> None:
        """
        Extracts GPS coordinates from the EXIF metadata of an image file.

        Args:
            image_path (str): Path to the input image file.
        """

        # Extract EXIF information from the image
        img = Image.open(image_path)
        info_exif = img._getexif()

        # Iterate through EXIF tags to find GPSInfo and store GPS coordinates
        for tag, value in info_exif.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == 'GPSInfo':
                lat = self.dms2dd(value[2], value[1])
                lon = self.dms2dd(value[4], value[3])
                return [lat, lon]
        return [-1, -1]


    def calculate_gps_distance(self, ploc, loc) -> float:
        """
        Calculates the distance between two geographic points using their latitude and longitude coordinates.

        Args:
            location (tuple): Latitude and longitude coordinates of the actual point.

        Returns:
            float: Distance between two points in meters.
        """

        plat, plon, lat, lon = map(math.radians, [ploc[0], ploc[1], loc[0], loc[1]])
        dlat = plat - lat
        dlon = plon - lon
        a = math.sin(dlat/2)**2 + math.cos(lat) * math.cos(plat) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        distance = self._R * c

        return distance





    def calculate_triangle(self, drone_center):
        """
        Calculates the vertices of an equilateral triangle based on the central point.

        Args:
            drone_center (tuple): Tuple of (x, y) representing the central point of the triangle, the drone location.

        Returns:
            numpy.ndarray: Array containing the coordinates of the triangle vertices.
        """

        x, y = drone_center
        altura = np.sqrt(3) / 2 * self._tri_size
        vertices = np.array([
            [x, y - altura / 2],  
            [x - self._tri_size / 2, y + altura / 2],  
            [x + self._tri_size / 2, y + altura / 2]   
        ], np.int32)
        return vertices.reshape((-1, 1, 2))


    def rotate_triangle(self, drone_pixel, pts):             
        """
        Rotates a triangle around its center.

        Args:
            drone_center (tuple): Tuple of (x, y) representing the center of the triangle.
            pts (numpy.ndarray): Array containing the coordinates of the triangle vertices.

        Returns:
            numpy.ndarray: Array containing the coordinates of the rotated triangle.
        """
        
        drone_center = (int(drone_pixel[0]),int(drone_pixel[1]))
        rotation_matrix = cv2.getRotationMatrix2D(drone_center, self._angle, 1)
        pts = pts.reshape(3,2)
        rotated_points = cv2.transform(np.array([pts]), rotation_matrix)[0]

        pt1 = [int(rotated_points[0][0]), int(rotated_points[0][1])]
        pt2 = [int(rotated_points[1][0]), int(rotated_points[1][1])]
        pt3 = [int(rotated_points[2][0]), int(rotated_points[2][1])]

        new_pts = np.array([pt1,pt2,pt3], np.int32)
        new_pts = new_pts.reshape((-1, 1, 2))

        return new_pts

    
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
    

    
        
    def get_middle_plant(self, image_path, frame, bboxes, health_status_frame) -> None:
        
        all_centers_bbox = []
        for bbox in bboxes: 
            center_bbox = self.get_center(bbox)
            all_centers_bbox.append(center_bbox)

        h,w,_ = frame.shape
        center_image = np.array([w//2, h//2])       

        distances = np.linalg.norm(all_centers_bbox - center_image, axis=1)
        idx_plant = np.argmin(distances)
        middle_plant = bboxes[idx_plant]
        health_status = health_status_frame[idx_plant]

        return middle_plant, health_status
    

