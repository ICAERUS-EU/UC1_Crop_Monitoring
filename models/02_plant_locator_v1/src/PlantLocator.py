""" Code to locate the detected plants into a global orthomosaic image """

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
from tqdm import tqdm


class PlantLocator:
    def __init__(self, image, mask, transform, all_coords, row_points, all_locations, all_health_status):

        self.R = 6371000 
        self._length = 3000  
        self._rect_size = 25
        self._tri_size = 25
        self._offset = -90
        self._alpha = 0.4
        self._INT_MAX = np.iinfo(np.int64).max
        self._angle = np.rad2deg(0.22673090865593348)      # This value is extracted from the image metadata (still not integrated in the flow)
        self._drone_angle = np.radians(self._offset - 8.3) # This value is extracted from the image metadata (still not integrated in the flow

        self._image = image
        self._mask = mask
        self._transform = transform
        self._size = image.shape[0:2]
        self.__all_pixels = np.indices((self._size[0], self._size[1])).reshape(2, -1).T

        self._all_coords = all_coords
        self._row_points = row_points
        self._all_locations = all_locations
        self._all_health_status = all_health_status
        self._rows_pixels_location = None 
        self._rows_location = None
        self._blank_rows = self.draw_rows()


    def draw_rows(self):
        """
        Draws rows on a blank canvas based on provided row points.

        Returns:
            numpy.ndarray: Image with rows drawn.
        """

        blank_rows = np.zeros((self._size[0], self._size[1], 1), dtype=np.uint8)

        for line in self._row_points:
            cv2.line(blank_rows, line[0], line[1], (255), 1)

        return blank_rows
    

    def get_row_pixels(self): 
        """
        Retrieves the pixel locations of rows.

        Returns:
            list: List of row pixel locations.
        """

        all_pixels = []
        rows_mask = cv2.bitwise_and(self._blank_rows, self._blank_rows, mask=self._mask)
        all_pixels_yx = np.transpose(np.where(rows_mask == 255))
        self._rows_pixels_location = [np.flip(pixel) for pixel in all_pixels_yx]
        
        return self._rows_pixels_location
    

    def get_row_location(self) -> np.ndarray: 
        """
        Transforms row pixel locations to their corresponding locations in GPS.

        Returns:
            numpy.ndarray: Array of row locations.
        """

        self._rows_location = np.array([np.flip(self._transform * pixel) for pixel in tqdm(self._rows_pixels_location)])
        
        return self._rows_location


    def calculate_gps_distance(self, plocation, location) -> float:
        """
        Calculates the great-circle distance between two GPS coordinates.

        Args:
            plocation (tuple): Tuple of (latitude, longitude) for the first location.
            location (tuple): Tuple of (latitude, longitude) for the second location.

        Returns:
            float: The calculated distance between the two locations.
        """

        plat, plon, lat, lon = map(math.radians, [plocation[0], plocation[1], location[0], location[1]])
        dlat = plat - lat
        dlon = plon - lon
        a = math.sin(dlat/2)**2 + math.cos(lat) * math.cos(plat) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        distance = self.R * c
        return distance


    def get_possible_plant_locations(self, drone_pixel_loc) -> list: 
        """
        Retrieves possible pixel locations based on the drone's orientation.

        Args:
            drone_pixel_loc (tuple): Tuple of (x, y) representing the drone's pixel location.

        Returns:
            list: List of possible pixel locations.
        """

        blank_orientation = np.zeros((self._size[0], self._size[1], 1), dtype=np.uint8)

        # Calculate the line representing the drone's orientation in the image 
        x2 = int(drone_pixel_loc[0] + self._length * np.cos(self._drone_angle))
        y2 = int(drone_pixel_loc[1] + self._length * np.sin(self._drone_angle))
        blank_orientation = cv2.line(blank_orientation, (drone_pixel_loc[0], drone_pixel_loc[1]), (x2, y2), (255), 1)
        
        # Find positions of pixels where the intersection occurred between the drone orientation line and the vineyards row
        blank_final = cv2.bitwise_and(blank_orientation, self._blank_rows)
        pos_pixels_found = np.where(blank_final == 255)
        possible_pixels_loc = list(zip(pos_pixels_found[1], pos_pixels_found[0])) # List of possible plant positions 

        return possible_pixels_loc


    def get_plant_location(self, drone_pixel_loc, drone_loc):
        """
        Determines the final location of the drone and the nearest row based on its pixel location and GPS coordinates.

        Args:
            drone_pixel_loc (tuple): Tuple of (x, y) representing the drone's pixel location.
            drone_loc (tuple): Tuple of (latitude, longitude) representing the drone's GPS coordinates.

        Returns:
            tuple: Tuple containing the final pixel location and the corresponding GPS location.
        """

        # Init variables
        min_dist = self._INT_MAX
        final_plant_loc = drone_loc
        final_pixel_plant_loc = drone_pixel_loc

        # Generate a list of possible plant locations 
        possible_pixels_loc = self.get_possible_plant_locations(drone_pixel_loc)

        # For each possible pixel location
        for pos in possible_pixels_loc:
            # For each row's pixel location and corresponding row location
            for pixel_loc, row_loc in zip(self._rows_pixels_location, self._rows_location):
                # Check if the current pixel location matches the possible position
                if((pixel_loc == pos).all()):
                    break

            # Calculate distance between drone's location and the row's location
            dist = self.calculate_gps_distance(drone_loc, row_loc)

            # Update location if distance is smaller
            if(dist < min_dist): 
                min_dist = dist        
                final_pixel_plant_loc = pixel_loc
                final_plant_loc = row_loc

        return final_pixel_plant_loc, final_plant_loc


    def get_drone_location(self, location):
        """
        Determines the drone's pixel and GPS locations based on the provided GPS location.

        Args:
            location (tuple): Tuple of (latitude, longitude) representing the target GPS location.

        Returns:
            tuple: Tuple containing the drone's pixel location and its GPS location.
        """

        min_dist = self._INT_MAX

        for idx_coord, coord in tqdm(enumerate(self._all_coords), total = len(self._all_coords)):
            dist = self.calculate_gps_distance(coord, location)

            if(dist < min_dist):
                min_dist = dist
                drone_loc = coord
                drone_pixel_loc = self.__all_pixels[idx_coord]

        return drone_pixel_loc, drone_loc


    def get_all_final_plant_locations(self):
        """
        Obtains the final pixel and GPS locations for all plants based on the drone's path.

        Returns:
            tuple: Tuple containing lists of all pixel locations of the drone, final pixel locations of the plants, and GPS locations of the plants.
        """

        all_pixel_drone_loc = []
        all_pixel_plant_loc = []
        all_plant_loc = []

        for location in tqdm(self._all_locations):

            drone_pixel_loc, drone_loc = self.get_drone_location(location)
            final_pixel_loc, final_loc = self.get_plant_location(drone_pixel_loc, drone_loc)
            
            all_pixel_drone_loc.append(drone_pixel_loc)
            all_pixel_plant_loc.append(final_pixel_loc)
            all_plant_loc.append(final_loc)

        return all_pixel_drone_loc, all_pixel_plant_loc, all_plant_loc


    def rotate_rectangle(self, cx, cy): 
        """
        Rotates a rectangle around its center.

        Args:
            cx (int): x-coordinate of the center of the rectangle.
            cy (int): y-coordinate of the center of the rectangle.

        Returns:
            numpy.ndarray: Array containing the coordinates of the rotated rectangle.
        """
        
        rotation_matrix = cv2.getRotationMatrix2D((cx, cy), self._angle, 1)
        rect_points = np.array([[cx - self._rect_size / 2, cy - self._rect_size / 2],
                                [cx + self._rect_size / 2, cy - self._rect_size / 2],
                                [cx + self._rect_size / 2, cy + self._rect_size / 2],
                                [cx - self._rect_size / 2, cy + self._rect_size / 2]], dtype=np.float32) 

        rotated_rect_points = cv2.transform(np.array([rect_points]), rotation_matrix)[0]
        pt1 = [int(rotated_rect_points[0][0]), int(rotated_rect_points[0][1])]
        pt2 = [int(rotated_rect_points[1][0]), int(rotated_rect_points[1][1])]
        pt3 = [int(rotated_rect_points[2][0]), int(rotated_rect_points[2][1])]
        pt4 = [int(rotated_rect_points[3][0]), int(rotated_rect_points[3][1])]

        pts = np.array([pt1,pt2,pt3,pt4], np.int32)
        pts = pts.reshape((-1, 1, 2))

        return pts


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


    def rotate_triangle(self, drone_center, pts):             
        """
        Rotates a triangle around its center.

        Args:
            drone_center (tuple): Tuple of (x, y) representing the center of the triangle.
            pts (numpy.ndarray): Array containing the coordinates of the triangle vertices.

        Returns:
            numpy.ndarray: Array containing the coordinates of the rotated triangle.
        """
        
        rotation_matrix = cv2.getRotationMatrix2D(drone_center, self._angle, 1)
        pts = pts.reshape(3,2)
        rotated_points = cv2.transform(np.array([pts]), rotation_matrix)[0]

        pt1 = [int(rotated_points[0][0]), int(rotated_points[0][1])]
        pt2 = [int(rotated_points[1][0]), int(rotated_points[1][1])]
        pt3 = [int(rotated_points[2][0]), int(rotated_points[2][1])]

        new_pts = np.array([pt1,pt2,pt3], np.int32)
        new_pts = new_pts.reshape((-1, 1, 2))

        return new_pts


    def draw_drone_location(self, image_show, all_pixel_drone_loc):
        """
        Draws the real-time location of the drone on the image.

        Args:
            image_show (numpy.ndarray): Image to display.
            all_pixel_drone_loc (list): List of tuples containing the pixel locations of the drone.

        Returns:
            numpy.ndarray: Image with the drone's location drawn.
        """

        overlay = self._image.copy()

        # Draw drone as a blue triangle
        for drone_pixel_location in all_pixel_drone_loc: 
            
            # Calculate triangle to show drone position
            pts = self.calculate_triangle(drone_pixel_location)
            drone_center = (int(drone_pixel_location[0]),int(drone_pixel_location[1]))
            rot_pts = self.rotate_triangle(drone_center, pts)
            overlay = cv2.fillPoly(overlay, [rot_pts], (255, 200, 100))
            
            # Draw precise location of drone as a white point
            image_show = cv2.circle(image_show, drone_center, 1, (255,255,255), -1)

        # Draw the drone position with transparency  
        image_show = cv2.addWeighted(overlay, self._alpha, image_show, 1 - self._alpha, 0)

        return image_show


    def draw_plants_and_drone(self, all_pixel_plant_loc, all_pixel_drone_loc, drawDrone = True): 
        """
        Draws plants and the drone on the image.

        Args:
            all_pixel_plant_loc (list): List of tuples containing the pixel locations of the plants.
            all_pixel_drone_loc (list): List of tuples containing the pixel locations of the drone.
            drawDrone (bool): Whether to draw the drone or not. Default is True.

        Returns:
            numpy.ndarray: Image with plants and the drone drawn.
        """

        image_show = self._image.copy()
        overlay = self._image.copy()

        # For each plant, gets rectangle of its position, rotates it and draw it 
        for final_pixel_loc, health_status in zip(all_pixel_plant_loc, self._all_health_status):
            plant_center = (int(final_pixel_loc[0]), int(final_pixel_loc[1]))
            pts = self.rotate_rectangle(plant_center[0], plant_center[1])
            image_show = cv2.circle(image_show, plant_center, 1, (255,255,255), -1)

            if(health_status==1):
                cv2.fillPoly(overlay, [pts], color=(0,255,0))
            else:
                cv2.fillPoly(overlay, [pts], color=(0,0,255))

        # Show rectangle with transparency 
        image_show = cv2.addWeighted(overlay, self._alpha, image_show, 1 - self._alpha, 0)

        # Draw the drone position as a blue triangle 
        if(drawDrone):
            image_show = self.draw_drone_location(image_show, all_pixel_drone_loc)

        return image_show
