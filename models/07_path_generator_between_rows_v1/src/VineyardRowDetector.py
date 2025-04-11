""" Class designed to extract the vineyards rows """

__author__ = "Esther Vera"
__copyright__ = "Copyright 2024, Noumena"
__credits__ = ["Esther Vera, Aldo Sollazzo"]
__version__ = "1.0.0"
__maintainer__ = "Esther Vera"
__email__ = "esther@noumena.io"
__status__ = "Production"
__license__ = "MIT"

import cv2
import copy 
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt


class VineyardRowDetector:
    def __init__(self, ortho_image, mask, VINEYARD_HEIGHT, VINEYARD_SEP) -> None:
        """
        Initializes the VineyardRowDetector class with vineyard row separation, ortho image, and mask.

        Args:
            ortho_image (np.ndarray): The orthomosaic image of the vineyard.
            mask (np.ndarray): The mask defining the vineyard area.
            VINEYARD_HEIGHT (int): Height parameter for vineyard row visualization.
            VINEYARD_SEP (float): Separation between vineyard rows in pixels.
        """
        self._lower_red = np.array([0, 120, 70])
        self._upper_red = np.array([10, 255, 255])
        self._coordinates = []
        self._vineyard_height = VINEYARD_HEIGHT    
        self._vineyard_sep = VINEYARD_SEP    
        self._ortho_image = ortho_image
        self._mask = mask
        self._ortho_image_rows = copy.deepcopy(ortho_image)
        self._smoothed_mask = self.smooth_mask()
        self._h, self._w, _ = self._ortho_image_rows.shape


    def smooth_mask(self) -> np.ndarray: 
        """
        Smoothes the mask to avoid cropping the lines close to the borders.

        Returns:
            smoothed_mask (np.ndarray): The smoothed mask image.
        """
        kernel7 = np.ones((7, 7), np.uint8)
        kernel3 = np.ones((5, 5), np.uint8)
        smoothed_mask = cv2.morphologyEx(self._mask, cv2.MORPH_OPEN, kernel7)
        smoothed_mask = cv2.erode(smoothed_mask, kernel3, iterations=5)
        smoothed_mask = cv2.GaussianBlur(smoothed_mask, (5, 5), 0)

        return smoothed_mask


    def get_coordinates(self, event, x, y, flags, param) -> None:
        """
        Callback function to capture mouse click coordinates on the image.
        Used for manual selection of vineyard row endpoints.

        Args:
            event: Mouse event type.
            x (int): x-coordinate of the mouse click.
            y (int): y-coordinate of the mouse click.
            flags: Additional flags related to the mouse event.
            param: self._coordinates - Parameter containing the list of coordinates to update.
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            self._coordinates = param 
            # Rescale selected points to match with original size 
            x1 = int(x * (14441/ 1155)) 
            y1 = int(y * (18767 / 1501))
            print(x1,y1)
            self._coordinates.append([x1, y1])


    def get_init_row_coordinates(self, select_points=False) -> None: 
        """
        Obtains the coordinates of the selected point on the image, either manually or automatically.

        Args:
            select_points (bool): If True, allows manual point selection via mouse clicks;
                                  if False, uses predefined coordinates in self._coordinates.
        """
        # Manual selection 
        if select_points:
            # Image is resized, points selected are rescaled
            res_image = cv2.resize(self._ortho_image, None, fx=0.08, fy=0.08)
            cv2.imshow('Image', res_image)

            cv2.setMouseCallback('Image', self.get_coordinates, (self._coordinates))
            while(len(self._coordinates) < 1):
                cv2.waitKey(1)

            cv2.setMouseCallback('Image', self.get_coordinates, (self._coordinates))
            while(len(self._coordinates) < 2):
                cv2.waitKey(1)
            cv2.destroyAllWindows()

        # Automatic selection
        else:
            # self._coordinates = [[69, 750], [2298, 237]]    # Image size 50%
            # self._coordinates = [[568, 867], [1215, 718]]   # Image size (4692, 3610)
            self._coordinates = [[2250, 3453], [4876, 2855]]  # Original size image (14441, 18767)
            self._angle = np.arctan2(self._coordinates[1][1] - self._coordinates[0][1], self._coordinates[1][0] - self._coordinates[0][0])


    def get_parallel_rows(self) -> list:
        """
        Generates parallel lines that define the vineyard rows based on initial coordinates.

        Returns:
            parallel_rows_points (list): A list of points defining the parallel rows.
            The coordinates of these rows are not adjusted for the actual length of the rows in the image, they are larger. 
        """
        added_length = 20000 # Added length to initial row to cover the whole image 
        reached = False      # Varible to stop drawing parallel lines
        self._parallel_rows_points = []

        #  Init and final coordinates of the selected row
        x1 = self._coordinates[0][0]
        y1 = self._coordinates[0][1]
        x2 = self._coordinates[1][0]
        y2 = self._coordinates[1][1]

        # Direction and length of the row
        v_dir = (x2 - x1, y2 - y1)
        length = (v_dir[0] ** 2 + v_dir[1] ** 2) ** 0.5
        v_dir_normalized = (v_dir[0] / length, v_dir[1] / length)
        v_perp = (-v_dir_normalized[1], v_dir_normalized[0]) 

        # Draws parallel lines until it reaches the limits of the image
        it = -1
        while True:
            # Draws the parallel lines in each direction (up - down)
            if(reached):
                it -= 1
            else:
                it += 1

            # Calculates the points of the new parallel line (not adjusted for the image size)
            x1_parallel = x1 + it * self._vineyard_sep * v_perp[0] - added_length * v_dir_normalized[0]
            y1_parallel = y1 + it * self._vineyard_sep * v_perp[1] - added_length * v_dir_normalized[1]
            x2_parallel = x2 + it * self._vineyard_sep * v_perp[0] + added_length * v_dir_normalized[0]
            y2_parallel = y2 + it * self._vineyard_sep * v_perp[1] + added_length * v_dir_normalized[1]

            point1 = (int(x1_parallel), int(y1_parallel))
            point2 = (int(x2_parallel), int(y2_parallel))

            # Check if the line is visible 
            blank_rows = np.zeros((self._h, self._w, 1), dtype=np.uint8)
            cv2.line(blank_rows, point1, point2, (255), 2)
            rows_mask = cv2.bitwise_and(blank_rows, blank_rows, mask=self._smoothed_mask)
            visible_pixels_yx = np.transpose(np.where(rows_mask == 255))

            # If line is not visible, change the direction of drawing new parallel lines
            if(len(visible_pixels_yx) == 0 and not reached):
                reached = True
                it = 0

            # If line is not visible, and we already changed the direction, stop drawing parallel rows
            elif(len(visible_pixels_yx) == 0 and reached):
                break

            else:   # Saves the rows points and draw a red line marking the row
                self._parallel_rows_points.append([point1, point2])
                cv2.line(self._ortho_image_rows, point1, point2, (0,0,255), self._vineyard_height)

        # The coordinates of these rows are not adjusted for the actual length of the rows in the image, they are larger. 
        return self._parallel_rows_points
    

    def filter_rows(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Filters the red vineyard rows from the image in the vineyard area.

        Returns:
            masked_rows_image (np.ndarray): The original orthomosaic image masked by the vineyard area
            self._filtered_rows_image (np.ndarray): A blank image only containing the red rows
        """        
        # Apply the mask to get only the rows drawn inside the vineyard (with the vineyard below)
        masked_rows_image = cv2.bitwise_and(self._ortho_image_rows, self._ortho_image_rows, mask=self._smoothed_mask)
        
        return masked_rows_image
     

    def get_rows_coordinates(self, masked_rows_image) -> tuple[list, list]: 
        """
        Extracts coordinates of vineyard rows from the masked image.

        Args:
            masked_rows_image (np.ndarray): Image containing the masked vineyard rows.

        Returns:
            rows_contours (list): List of contour points for each row (top-left, top-right, bottom-left, bottom-right)
            rows (lsit): List of bottom coordinates for each row (bottom-left, bottom-right)
        """
        # Create variables
        rows_contours, rows = [], []
        image_contours = self._ortho_image.copy()

        # Detect red lines in masked_rows_image
        hsv = cv2.cvtColor(masked_rows_image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self._lower_red, self._upper_red)

        # Detect contours of the mask (rows)
        _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # For each contour
        for cnt in tqdm(contours, desc="Defining rows lines  "):     
            if cv2.contourArea(cnt) > 50000:

                # Get minimum rectangle that encompasses the contour
                x, y, w, h = cv2.boundingRect(cnt)
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box = np.int0(box)

                # Select the two rightmost points (with highest 'x')
                rightmost_points = sorted(box, key=lambda p: p[0], reverse=True)[:2]
                # Select the two leftmost points (with lowest 'x')
                leftmost_points = sorted(box, key=lambda p: p[0])[:2]

                # Select the corners of the rows contours 
                bottom_right = max(rightmost_points, key=lambda p: p[1])
                top_right = min(rightmost_points, key=lambda p: p[1])
                bottom_left = max(leftmost_points, key=lambda p: p[1])
                top_left = min(leftmost_points, key=lambda p: p[1])

                # Save rows coordinates and bottom coordinates
                rows_contours.append([top_left, top_right, bottom_left, bottom_right])
                rows.append([bottom_left, bottom_right])

                # Draw the rectangle and points
                cv2.drawContours(image_contours, [box], 0, (0, 0, 255), 25)
                cv2.circle(image_contours, tuple(bottom_left), 50, (0, 200, 255), -1)
                cv2.circle(image_contours, tuple(bottom_right), 50, (0, 255, 0), -1)

        rows = [[p1.tolist(), p2.tolist()] for p1, p2 in rows]  
        rows_contours = [[p1.tolist(), p2.tolist(), p3.tolist(), p4.tolist()] for p1, p2, p3, p4 in rows_contours]  

        return rows_contours, rows




   


