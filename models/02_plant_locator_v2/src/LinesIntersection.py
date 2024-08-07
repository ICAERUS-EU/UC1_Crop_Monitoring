""" Calculates the intersection between drone position and the parcels in a row """

__author__ = "Esther Vera"
__copyright__ = "Copyright 2023, Noumena"
__credits__ = ["Esther Vera, Aldo Sollazzo"]
__version__ = "1.0.0"
__maintainer__ = "Esther Vera"
__email__ = "esther@noumena.io"
__status__ = "Production"
__license__ = "MIT"


import cv2
import numpy as np
from tqdm import tqdm 


class LinesIntersection:
    def __init__(self, drones_pixels, drone_angle, row_points, parcel_points_flatten, center_parcels_flatten, row_images):
        self._drones_pixels = drones_pixels
        self._drone_angle = drone_angle
        self._drone_vector = self.drone2vector()
        self._row_lines = [self.points2line(p1, p2) for p1, p2 in row_points]
        self._row_images = row_images
        self._parcels_points_flatten = np.array(parcel_points_flatten)
        self._center_parcels_flatten = np.array(center_parcels_flatten)
        self._INT_MAX = np.iinfo(np.int64).max

        self._intersections = []
        self._parcels_intersected = []
        self._distances_intersected = []


    def drone2vector(self):
        d = np.array([np.cos(self._drone_angle), np.sin(self._drone_angle)])
        return d


    def points2line(self, p1, p2):
        """
        Transforms row lines defined by two points to line equation: Ax + By = C
        """
        x1, y1 = p1
        x2, y2 = p2
        A = y2 - y1
        B = x1 - x2
        C = A * x1 + B * y1
        return A, B, C


    # Calculates intersection between drone vector and row lines
    def intersection_drone_row(self, A, B, C, drone_pixel):
        numerador = C - A * drone_pixel[0] - B * drone_pixel[1]
        denominador = A * self._drone_vector[0] + B * self._drone_vector[1]
        if denominador != 0:
            return numerador / denominador
        else:
            return float('inf')  # No hay intersección si el denominador es 0



    def get_drone_intersections(self): 
        
        for drone_pixel in tqdm(self._drones_pixels): 
            # Look for the first intersection between the drone line and a row
            t_min = float('inf')
            linea_interseccion = None

            for row in self._row_lines:
                A, B, C = row
                t = self.intersection_drone_row(A, B, C, drone_pixel)
                if 0 <= t < t_min:
                    t_min = t
                    line_intersected = row

            if line_intersected:
                self._intersections.append(drone_pixel + t_min * self._drone_vector)
            else:
                self._intersections.append([-1,-1])
        
        return self._intersections


    def get_parcels_intersected(self): 

        self._parcels_intersected = len(self._intersections) * [-1]
        self._distances_intersected = len(self._intersections) * [self._INT_MAX]

        for id_, (drone_intersection, drone_pixel) in tqdm(enumerate(zip(self._intersections, self._drones_pixels)), total=len(self._intersections), desc="Getting parcels intersected"): 
            if not np.array_equal(drone_intersection, np.array([-1, -1])):
                distances = np.linalg.norm(self._center_parcels_flatten - drone_intersection, axis=1)
                idx_center = np.argmin(distances)
                
                # Filter drones that are too close to any parcel 
                dist_drone_position = np.linalg.norm(self._center_parcels_flatten[idx_center] - drone_pixel)

                if(dist_drone_position > 20):
                    self._parcels_intersected[id_] = idx_center
                    self._distances_intersected[id_] = distances[idx_center]


    def filter_drones(self):

        parcels_filtered = []
        self._parcels_selected = len(self._parcels_intersected) * [-1]
        for idx1 in tqdm(range(len(self._parcels_intersected)), desc="Filter drones with parcels"):
            selected_idx = 0
            min_dist = self._INT_MAX
            
            for idx2 in range(idx1, len(self._parcels_intersected)):
                if(self._parcels_intersected[idx1] not in parcels_filtered and self._parcels_intersected[idx1] != -1 and self._parcels_intersected[idx1] == self._parcels_intersected[idx2]):
                    if(self._distances_intersected[idx1] < self._distances_intersected[idx2]):
                        min_dist = self._distances_intersected[idx1]
                        sel_idx = idx1

                    elif(self._distances_intersected[idx1] >= self._distances_intersected[idx2]):
                        min_dist = self._distances_intersected[idx2]
                        sel_idx = idx2

            parcels_filtered.append(self._parcels_intersected[idx1])
            self._parcels_selected[sel_idx] = self._parcels_intersected[idx1]

        return self._parcels_selected
    

    def draw_drones_and_parcels(self, image, blank_rows, size, length): 

        # Calculate the line representing the drone's orientation in the image 
        for drone_pixel, idx_parcel in zip(self._drones_pixels, self._parcels_selected): 
            if(idx_parcel != -1):
                image = cv2.circle(image, drone_pixel, 10, (255,255, 0), -1)
                image = cv2.fillPoly(image, [np.array(self._parcels_points_flatten[idx_parcel])], (0,200,0))
                image = cv2.polylines(image, [np.array(self._parcels_points_flatten[idx_parcel])], isClosed=True, color=(255, 255, 255), thickness=3)

        cv2.imshow("image", cv2.resize(image, None, fx=0.3, fy=0.3))
        cv2.waitKey(0)
        cv2.destroyAllWindows()