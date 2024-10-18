""" Class to get the parcels (groups of plants) in the vineyards rows """

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


class ParcelDetector:
    def __init__(self, ortho_image, mask, filtered_rows_image, parallel_rows_points, PARCEL_LEN):
        """
        Initializes the ParcelDetector class with necessary attributes.

        Args:
            ortho_image (numpy.ndarray): Orthomosaic image.
            mask (numpy.ndarray): Mask image for the vineyard.
            filtered_rows_image (numpy.ndarray): Image with vineyard rows filtered.
            parallel_rows_points (list): List of points representing the parallel rows.
            PARCEL_LEN (int): Length of each parcel.
        """
        self._ortho_image = ortho_image
        self._mask = mask
        self._filtered_rows_image = filtered_rows_image
        self._parallel_rows_points = parallel_rows_points
        self._parcel_len = PARCEL_LEN


    def get_center_of_parcel(self, parcel, center_parcels) -> list: 
        """
        Calculates the centroid (center of mass) of a given parcel (polygon).

        Args:
            parcel (list or ndarray): List of coordinates representing the vertices of the parcel.
                                    Assumes that the parcel has 4 vertices.
            center_parcels (list): A list where the computed centroid will be appended.

        Returns:
            list: The updated list `center_parcels` containing the centroid coordinates of the parcel.
        """
        n = 4     # The number of vertices
        A = 0     # Initialize the area of the polygon
        C_x = 0   # Initialize the x-coordinate of the centroid
        C_y = 0   # Initialize the y-coordinate of the centroid

        # Convert the parcel to a list and ensure the polygon is closed by appending the first point at the end
        closed_parcel = parcel.tolist()
        closed_parcel.append(parcel[0])

        # Calculate the center of the parcel 
        for i in range(n):
            factor = closed_parcel[i][0] * closed_parcel[i + 1][1] - closed_parcel[i + 1][0] * closed_parcel[i][1]
            A += factor
            C_x += (closed_parcel[i][0] + closed_parcel[i + 1][0]) * factor
            C_y += (closed_parcel[i][1] + closed_parcel[i + 1][1]) * factor

        A = A / 2
        C_x = C_x / (6 * A)
        C_y = C_y / (6 * A)
        center_parcels.append([])
        center_parcels[-1].append([C_x, C_y])

        return center_parcels


    def get_total_parcels_and_deltas(self, all_corners) -> tuple[int, list]: 
        """
        Gets the total number of parcels that can fit in a vineyard row defined by its corner points,
        along with the displacement (deltas) in the x and y directions for each parcel.

        Args:
            all_corners (list): A list containing the coordinates of the four corners of the vineyard row.

        Returns:
            tuple: A tuple containing the following values:
                - total_parcels (int): The total number of parcels that can fit within the defined vineyard row.
                - deltas (list): A list containing two elements:
                    - delta_x (float): The displacement in the x-direction for each parcel.
                    - delta_y (float): The displacement in the y-direction for each parcel.
        """
        # Calculates total length of the actual vineyard row
        dist_total = int(np.sqrt((all_corners[2][0] - all_corners[0][0])**2 + (all_corners[2][1] - all_corners[0][1])**2))
        
        # Calculates the total of parcel dividing the total distance between the length ot the parcel
        total_parcels = (dist_total/self._parcel_len)

        # Calculates displacement of x,y for each parcel 
        delta_x = (all_corners[2][0] - all_corners[0][0]) / total_parcels
        delta_y = (all_corners[2][1] - all_corners[0][1]) / total_parcels
        deltas = [delta_x, delta_y]

        # If the total parcels is not a round number, one parcel is added (ex. 5.3 parcels >> 6 parcels)
        if(total_parcels - int(total_parcels) >=0.4):
            total_parcels = int(total_parcels) + 1
        else: 
            total_parcels = int(total_parcels)

        return total_parcels, deltas


    def get_parcel_points(self, k, all_parcel_points, center_parcels, total_parcels, all_corners, deltas) -> tuple[list, list]:
        """
        Gets the points that define each parcel in the vineyard row.

        Args:
            all_parcel_points (list): List containing the points of each parcel.
            center_parcels (list): List containing the central points of each parcel.
            total_parcels (int): Total number of parcels.
            all_corners (list): List of corner points of the vineyard row.

        Returns:
            tuple: Updated all_parcel_points (list), center_parcels (list).
        """
        # Calculates the angle between the left-up corner and the right-up corner
        angle = np.arctan2(all_corners[2][1] - all_corners[0][1], all_corners[2][0] - all_corners[0][0])

        # Get parcel points depending on k, displacement and size of parcel
        p1_init_x = all_corners[0][0] + k * deltas[0]
        p1_init_y = all_corners[0][1] + k * deltas[1]
        p2_init_x = all_corners[1][0] + k * deltas[0]
        p2_init_y = all_corners[1][1] + k * deltas[1]

        p1_end_x = p1_init_x + self._parcel_len * np.cos(angle)
        p1_end_y = p1_init_y + self._parcel_len * np.sin(angle)
        p2_end_x = p2_init_x + self._parcel_len * np.cos(angle)
        p2_end_y = p2_init_y + self._parcel_len * np.sin(angle)

        p1_init = (p1_init_x, p1_init_y)
        p2_init = (p2_init_x, p2_init_y)

        # If it's the last parcel, the end points will be the ones in all_corners
        if(k == total_parcels - 1):
            p1_end = all_corners[2]
            p2_end = all_corners[3]
        else: 
            p1_end = (p1_end_x, p1_end_y)
            p2_end = (p2_end_x, p2_end_y)

        parcel = np.array([p1_init, p2_init, p2_end, p1_end], np.int32)
        center_parcels = self.get_center_of_parcel(parcel, center_parcels)

        return parcel, center_parcels


    def get_corners(self, contour) -> list:
        """
        Gets the corner points of a contour that represents a vineyard row.

        Args:
            contour (np.ndarray): Contour of a vineyard row.

        Returns:
            list: A list containing the four corner points
        """
        # Get the minimum rectangle that encloses the contour
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        # Sort the four points
        rect_sorted = sorted(box, key=lambda x: x[0], reverse=False)
        rect_sorted_left = sorted(rect_sorted[:2], key=lambda x: x[1], reverse=False)
        rect_sorted_right = sorted(rect_sorted[2:4], key=lambda x: x[1], reverse=False)

        # Get each corner of the parcel
        corner_LU = [int(rect_sorted_left[0][0]), int(rect_sorted_left[0][1])]
        corner_LD = [int(rect_sorted_left[1][0]), int(rect_sorted_left[1][1])]
        corner_RU = [int(rect_sorted_right[0][0]), int(rect_sorted_right[0][1])]
        corner_RD = [int(rect_sorted_right[1][0]), int(rect_sorted_right[1][1])]

        return [corner_LU, corner_LD, corner_RU, corner_RD]


    def get_all_parcel_points(self)-> tuple[list, list]: 
        """
        Calculates the position of each parcel in the vineyard rows.

        Returns:
            tuple: all_parcel_points (list), center_parcels (list).
        """
        all_parcel_points = []
        center_parcels = []

        # Detects edges and contours
        edges = cv2.Canny(self._filtered_rows_image,10,50) 
        contours = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[0]
        sorted_contours = self.sort_contours(contours)

        # For each contour
        for cnt in tqdm(sorted_contours, desc="Defining parcel points"): 
            # Draw contour 
            self._filtered_rows_image = cv2.drawContours(self._filtered_rows_image, [cnt], -1, (255, 155, 0), 2)

            # Get 4 corners of the rectangle that defines the contour
            all_corners = self.get_corners(cnt)

            # Get the total of parcels in the rows and the displacement in x,y (deltas)
            total_parcels, deltas = self.get_total_parcels_and_deltas(all_corners)

            if(total_parcels>0):
                all_parcel_points.append([])

            # For each parcel in the row
            for k in range(total_parcels):
                # Get all parcels points
                parcel, center_parcels = self.get_parcel_points(k, all_parcel_points, center_parcels, total_parcels, all_corners, deltas)   
                all_parcel_points[-1].append(parcel.tolist())    

        return all_parcel_points, center_parcels


    def sort_contours(self, contours) -> list:
        """
        Sorts the contours based on the vineyard rows and returns them in order. 
        Red lines stored in parallel_rows_points are in order but not the contours.

        Args:
            contours (list): List of contours.

        Returns:
            sorted_contours (list): Sorted contours.
        """
        self._rows = []
        sorted_contours = []
        contours = list(contours)

        # For each row defined in parallel_rows_points (red lines)
        for points in tqdm(self._parallel_rows_points, desc="Sorting contours defining rows"):
            appended_contours = []
            indexes = []

            # Draw the line on the blank image to represent the current row
            blank1 = np.zeros_like(self._filtered_rows_image)
            blank1 = cv2.line(blank1, points[0], points[1], (255,255,255), 9)

            # For each one of the contours detected 
            for i,cnt in enumerate(contours): 
                # Draw the contour
                blank2 = np.zeros_like(self._filtered_rows_image)
                blank2 = cv2.drawContours(blank2, [cnt], -1, (255, 255, 255), -1)

                # Check if the line and the contour detected are overlapping
                mask = cv2.bitwise_and(blank1, blank2)
                if np.any(mask): 
                    # Save contour and index overlapped in a list. It can be more than one contour overlapped with a row line 
                    indexes.append(i)
                    appended_contours.append(cnt) 
            
            # For every contour overlapped
            if appended_contours:
                # Sort contours overlapped
                appended_contours = sorted(appended_contours, key=lambda c: cv2.boundingRect(c)[0])
                rect = cv2.minAreaRect(appended_contours[0])
                box = np.int0(cv2.boxPoints(rect))
                self._rows.append(box[0])

                # Delete contours overlapped from contours to reduce executing time 
                indexes = sorted(indexes, reverse=True)
                for index, appended_cnt in zip(indexes, appended_contours): 
                    sorted_contours.append(appended_cnt)
                    contours.pop(index)

        return sorted_contours


    def get_total_parcels(self, all_corners) -> int: 
        """
        Calculates the total number of parcels in the vineyard row.

        Args:
            all_corners (list): List of corner points of the vineyard row.

        Returns:
            total_parcels (int): Total number of parcels.
        """
        # Calculates total length of the actual vineyard row and total of parcels
        dist_total = int(all_corners[2][0] - all_corners[0][0])
        total_parcels = (dist_total/self._parcel_len)

        # If the total parcels is not a round number, one parcel is added (ex. 5.3 parcels -> 6 parcels)
        if(total_parcels - int(total_parcels) >=0.4):
            total_parcels = int(total_parcels) + 1
        else: 
            total_parcels = int(total_parcels)

        return total_parcels


    def draw_rgb_parcels(self, all_parcel_points) -> np.ndarray: 
        """
        Draws rectangles representing parcels in the vineyard rows in a rgb image.

        Args:
            all_parcel_points (list): List of parcel corner points.

        Returns:
            parcel_rows_image (np.ndarray): Image with parcels drawn on it in rgb.
        """
        parcel_rows_image = copy.deepcopy(self._ortho_image)
   
        # Draw each parcel 
        total = 0
        for k1, row in enumerate(all_parcel_points):
            for k2, parcel in enumerate(row):
                total = total + 1
                center_x = int((parcel[0][0] + parcel[2][0]) / 2) - 2
                center_y = int((parcel[0][1] + parcel[2][1]) / 2) + 2
                center = (center_x, center_y)
                cv2.polylines(parcel_rows_image, [np.array(parcel).astype(np.int32)], isClosed=True, color=[255,255,255], thickness=2)
                cv2.putText(parcel_rows_image, str(total), center, cv2.FONT_HERSHEY_SIMPLEX, 0.23, (255,255,255), 1)

        # Add padding to the left and write row numbers
        parcel_rows_image = cv2.copyMakeBorder(parcel_rows_image, 0, 0, 150, 0, cv2.BORDER_CONSTANT, value = (255,255,255)) 
        for k1, center in enumerate(self._rows):
            cv2.putText(parcel_rows_image, str(k1+1), (50, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,0), 2)

        return parcel_rows_image
    
    
    def draw_map_parcels(self, all_parcel_points) -> np.ndarray: 
        """
        Draws rectangles representing parcels in the vineyard rows in a schematic format.

        Args:
            all_parcel_points (list): List of parcel corner points.

        Returns:
            parcel_rows_image (np.ndarray): Image with parcels drawn on it in black and white.
        """
        # Get external contours of image and draw 
        gray_image = cv2.cvtColor(self._ortho_image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)
        thresh = cv2.bitwise_not(thresh)
        contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        map_rows_image = np.ones_like(self._ortho_image) * 255
        for contorno in contornos:
            map_rows_image = cv2.drawContours(map_rows_image, [contorno], -1, (0, 0, 0), 2)

        # Draw each parcel
        total = 0
        for k1, row in enumerate(all_parcel_points):
            for k2, parcel in enumerate(row):
                total = total + 1
                center_x = int((parcel[0][0] + parcel[2][0]) / 2) - 2
                center_y = int((parcel[0][1] + parcel[2][1]) / 2) + 2
                center = (center_x, center_y)
                cv2.polylines(map_rows_image, [np.array(parcel).astype(np.int32)], isClosed=True, color=[0,0,0], thickness=2)
                cv2.putText(map_rows_image, str(total), center, cv2.FONT_HERSHEY_SIMPLEX, 0.23, (0,0,0), 1)

        # Add padding to the left and write row numbers
        map_rows_image = cv2.copyMakeBorder(map_rows_image, 0, 0, 150, 0, cv2.BORDER_CONSTANT, value = (255,255,255)) 
        for k1, center in enumerate(self._rows):
            cv2.putText(map_rows_image, str(k1+1), (50, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,0), 2)

        return map_rows_image
        