""" Class designed to extract the vineyards rows """

__author__ = "Esther Vera"
__copyright__ = "Copyright 2024, Noumena"
__credits__ = ["Esther Vera, Oriol Arroyo, Salvador Calgua, Aldo Sollazzo"]
__version__ = "1.0.0"
__maintainer__ = "Esther Vera"
__email__ = "esther@noumena.io"
__status__ = "Production"
__license__ = "MIT"

import cv2
import copy 
import numpy as np
from tqdm import tqdm


class VineyardRowDetector:
    def __init__(self, ortho_image, mask, VINEYARD_HEIGHT, VINEYARD_SEP):
        """
        Initializes the class with vineyard row separation, ortho image, and mask.

        Args:
            ortho_image (numpy.ndarray): The orthomosaic image of the vineyard.
            mask (numpy.ndarray): The mask defining the vineyard area.
            VINEYARD_SEP (float): Separation between vineyard rows.
        """
        self._coordinates = []
        self._vineyard_height = VINEYARD_HEIGHT    
        self._vineyard_sep = VINEYARD_SEP    
        self._ortho_image = ortho_image
        self._mask = mask
        self._ortho_image_rows = copy.deepcopy(ortho_image)
        self._smoothed_mask = self.smooth_mask()


    def smooth_mask(self) -> np.ndarray: 
        """
        Smoothes the mask to avoid cropping the lines close to the borders.

        Returns:
            smoothed_mask: Mask image smoothed.
        """
        kernel7 = np.ones((7, 7), np.uint8)
        kernel3 = np.ones((5, 5), np.uint8)
        smoothed_mask = cv2.morphologyEx(self._mask, cv2.MORPH_OPEN, kernel7)
        smoothed_mask = cv2.erode(smoothed_mask, kernel3, iterations=5)
        smoothed_mask = cv2.GaussianBlur(smoothed_mask, (5, 5), 0)

        return smoothed_mask


    def get_coordinates(self, event, x, y, flags, param):
        """
        Callback function to capture mouse click coordinates on the image.

        Args:
            event: Mouse event type.
            x (int): X-coordinate of the mouse click.
            y (int): Y-coordinate of the mouse click.
            flags: Additional flags related to the mouse event.
            param: Parameter containing the list of coordinates to update.

        """
        if event == cv2.EVENT_LBUTTONDOWN:
            self._coordinates = param  
            self._coordinates.append([x, y])


    def get_coordinates_row(self, select_point=False): 
        """
        Obtains the coordinates of the selected point on the image, either manually or automatically.

        Args:
            select_point (bool): If True, allows manual point selection; otherwise, uses predefined coordinates.

        Returns:
            coordinates (list): List containing the selected coordinates.
        """

        if select_point:  # Manual selection 
            cv2.imshow('Image', self._ortho_image)
            cv2.setMouseCallback('Image', self.get_coordinates, (self._coordinates))

            while(len(self._coordinates) < 1):
                cv2.waitKey(1)
            cv2.destroyAllWindows()
        else: # Automatic selection 
            self._coordinates = [1033, 971]  # Predefined coordinates 


    def get_parallel_rows(self) -> list:
        """
        Generates parallel lines that define the vineyard rows.

        Args:
            ortho_image_res (numpy.ndarray): The orthomosaic image.
            mask (numpy.ndarray): The mask defining the vineyard area.
            coordinates (list): Starting and ending coordinates of a selected row.

        Returns:
            parallel_rows_points (list): A list of points defining the parallel rows.
        """
        reached = False
        parallel_rows_points = [] # To store the parallel rows points
        h, w, _ = self._ortho_image_rows.shape

        # Define the initial points for the first row line
        x1, y1, x2, y2 = 0, self._coordinates[1], w, self._coordinates[1]
            
        # Generate parallel rows until no more valid rows can be found
        while not reached:
            point1 = (int(x1), int(y1))
            point2 = (int(x2), int(y2))

            # Mask the row with vineyard area 
            blank_rows = np.zeros((h, w, 1), dtype=np.uint8)
            cv2.line(blank_rows, point1, point2, (255), 2)
            rows_mask = cv2.bitwise_and(blank_rows, blank_rows, mask=self._smoothed_mask)  

            # If the row intersects the vineyard mask
            if np.any(rows_mask): 
                parallel_rows_points.append([point1, point2])
                cv2.line(self._ortho_image_rows, point1, point2, (0, 0, 255), self._vineyard_height)
            else:
                reached = True  #

            # Position of new row depending on vineyard row separation
            y1 += self._vineyard_sep
            y2 += self._vineyard_sep

        return parallel_rows_points


    def get_filtered_rows(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Filters the red vineyard rows from the image in the vineyard area.

        Returns:
            filtered_rows_image (numpy.ndarray): The filtered image with only red rows.
        """
        # Create a mask for the red rows
        lower_red = np.array([0, 0, 250])
        upper_red = np.array([0, 0, 255])

        # Apply the mask to get only the rows drawn inside the vineyard (with the vineyard below)
        masked_rows_image = cv2.bitwise_and(self._ortho_image_rows, self._ortho_image_rows, mask=self._smoothed_mask)
        
        # Filter red color to get the rows in the image (without the vineyard, only in black and red)
        red_mask = cv2.inRange(masked_rows_image, lower_red, upper_red)
        filtered_rows_image = cv2.bitwise_and(masked_rows_image, masked_rows_image, mask=red_mask)
        filtered_rows_image = cv2.medianBlur(filtered_rows_image, 5)  # Smooth the filtered rows

        return masked_rows_image, filtered_rows_image