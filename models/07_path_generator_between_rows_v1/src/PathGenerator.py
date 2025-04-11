""" Class to generate the GPS path between rows for the drone """

__author__ = "Esther Vera"
__copyright__ = "Copyright 2025, Noumena"
__credits__ = ["Esther Vera, Oriol Arroyo, Salvador Calgua, Aldo Sollazzo"]
__version__ = "1.0.0"
__maintainer__ = "Esther Vera"
__email__ = "esther@noumena.io"
__status__ = "Production"
__license__ = "MIT"


import cv2
import math
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Optional


class PathGenerator:
    """
    A class to generate and visualize optimal paths between row segments.
    
    Methods:
        - distance(point1, point2): Euclidean distance between two points.
        - line_equation(point1, point2): Coefficients of row equation (Ax + By + C = 0).
        - projected_intersection_point(A, B, P): Finds perpendicular projection of P onto AB.
        - distance_to_line_segment(A, B, P): Minimum distance from P to segment AB.
        - generate_path(rows): Computes optimal path connecting all row segments.
        - draw_path(rows, path): Visualizes original rows and generated path.
    """

    def __init__(self, rows: List[List[Tuple[float, float]]]):
        self.original_rows = rows
        self.path_rows = self.displace_rows(rows)


    @staticmethod
    def distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """Calculate Euclidean distance between two points."""
        return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)


    @staticmethod
    def line_equation(point1: Tuple[float, float], point2: Tuple[float, float]) -> Tuple[float, float, float]:
        """
        Returns coefficients (A, B, C) of the row equation Ax + By + C = 0.
        
        Args:
            point1: First point (x1, y1).
            point2: Second point (x2, y2).
        
        Returns:
            Tuple (A, B, C) representing the row equation.
        """
        x1, y1 = point1
        x2, y2 = point2
        
        if x1 == x2:  # Vertical row
            return (1.0, 0.0, -x1)
        else:
            slope = (y2 - y1) / (x2 - x1)
            return (slope, -1.0, y1 - slope * x1)


    @staticmethod
    def projected_intersection_point(A: Tuple[float, float], B: Tuple[float, float], P: Tuple[float, float]) -> Tuple[Tuple[float, float], bool]:
        """
        Calculates the perpendicular projection of point P onto line segment AB.
        
        Args:
            A: Start point of the segment.
            B: End point of the segment.
            P: Point to project.
        
        Returns:
            Tuple of (projected_point, is_within_segment) where:
                - projected_point: (x, y) coordinates of the projection.
                - is_within_segment: True if projection lies within AB.
        """
        x1, y1 = A
        x2, y2 = B
        x0, y0 = P
        
        # Handle vertical line
        if x1 == x2:
            return (x1, y0), (min(y1, y2) <= y0 <= max(y1, y2))
        
        # Handle horizontal line
        if y1 == y2:
            return (x0, y1), (min(x1, x2) <= x0 <= max(x1, x2))
        
        # General case
        slope = (y2 - y1) / (x2 - x1)
        perpendicular_slope = -1 / slope
        
        # Calculate intersection point
        x_intersect = (slope * x1 - y1 - perpendicular_slope * x0 + y0) / (slope - perpendicular_slope)
        y_intersect = slope * (x_intersect - x1) + y1
        
        # Check if within segment
        within_segment = False
        if (min(x1, x2) <= x_intersect <= max(x1, x2) and 
            min(y1, y2) <= y_intersect <= max(y1, y2)):
            within_segment = True

        return (x_intersect, y_intersect), within_segment
        

    def distance_to_line_segment(
        self,
        A: Tuple[float, float],
        B: Tuple[float, float],
        P: Tuple[float, float]
    ) -> Tuple[float, Tuple[float, float], bool]:
        """
        Computes minimum distance from point P to row segment AB.
        
        Args:
            A: Start point of segment.
            B: End point of segment.
            P: Target point.
        
        Returns:
            Tuple of (distance, closest_point, is_projection) where:
                - distance: Shortest distance to segment.
                - closest_point: Nearest point on AB to P.
                - is_projection: True if closest point is a projection.
        """
        projected_point, is_within = self.projected_intersection_point(A, B, P)
        
        if is_within:
            return self.distance(projected_point, P), projected_point, True
        else:
            dist_A = self.distance(A, P)
            dist_B = self.distance(B, P)
            
            if dist_A < dist_B:
                return dist_A, A, False
            else:
                return dist_B, B, False


    def desplazar_linea(self, linea, distancia):
        """Desplaza una línea en dirección perpendicular en una distancia dada."""
        (x1, y1), (x2, y2) = linea

        # Calcular el vector director
        dx = x2 - x1
        dy = y2 - y1

        # Calcular el vector perpendicular normalizado
        length = np.sqrt(dx**2 + dy**2)
        perp_dx = -dy / length * distancia
        perp_dy = dx / length * distancia

        # Generar la nueva línea desplazada
        nueva_linea = [(x1 + perp_dx, y1 + perp_dy), (x2 + perp_dx, y2 + perp_dy)]
        return nueva_linea

    def displace_rows(self, rows):
        rows2 = [self.desplazar_linea(row, 150) for row in rows]
        return rows2
    

    def generate_path(self) -> List[Tuple[float, float]]:
        """
        Generates optimal path connecting all row segments.
        
        Args:
            rows: List of row segments, each as [(x1,y1), (x2,y2)].
        
        Returns:
            Ordered list of points representing the path.
        """
        if not self.path_rows:
            return []
        
        remaining_rows = [row.copy() for row in self.path_rows]
        path = []
        
        # Start with last row
        current_line = remaining_rows.pop()
        path.extend([current_line[0], current_line[1]])
        last_point = current_line[1]
        
        while remaining_rows:
            min_distance = float('inf')
            best_line = None
            best_connection_point = None
            is_projection = False
            
            for row in remaining_rows:
                dist, point, is_proj = self.distance_to_line_segment(
                    row[0], row[1], last_point)
                
                if dist < min_distance:
                    min_distance = dist
                    best_line = row
                    best_connection_point = point
                    is_projection = is_proj
            
            # Connect to best row
            if is_projection:
                # Choose direction along the row
                dist_to_start = self.distance(best_connection_point, best_line[0])
                dist_to_end = self.distance(best_connection_point, best_line[1])
                
                if dist_to_start < dist_to_end:
                    path.extend([best_line[0], best_line[1]])
                    last_point = best_line[1]
                else:
                    path.extend([best_line[1], best_line[0]])
                    last_point = best_line[0]
            else:
                if best_connection_point == best_line[0]:
                    path.extend([best_line[0], best_line[1]])
                    last_point = best_line[1]
                else:
                    path.extend([best_line[1], best_line[0]])
                    last_point = best_line[0]
            
            remaining_rows.remove(best_line)
        
        return path


    def draw_path(self, path: List[Tuple[float, float]]) -> None:
        """
        Visualizes original rows and generated path.
        
        Args:
            path: Generated path points.
        """
        plt.figure(figsize=(15, 10))
        
        # Draw original rows (red)
        for row in self.original_rows:
            x_coords = [p[0] for p in row]
            y_coords = [-p[1] for p in row]
            plt.plot(x_coords, y_coords, 'r-', linewidth=5, alpha=0.6)
            plt.scatter(x_coords, y_coords, c='red', s=50, alpha=1.0)
        
        # Draw path (blue)
        if path:
            path_x = [p[0] for p in path]
            path_y = [-p[1] for p in path]
            plt.plot(path_x, path_y, 'b-', linewidth=2, alpha=0.9)
            
            # Path points
            plt.scatter(path_x[1:-1], path_y[1:-1], c='blue', s=40, 
                     edgecolors='darkblue', linewidths=0.5)
            
            # Start/end markers
            plt.scatter([path_x[-1]], [path_y[-1]], c='orange', s=200,
                     edgecolors='darkorange', linewidths=2, label='End', zorder=6)
            plt.scatter([path_x[0]], [path_y[0]], c='lime', s=200,
                     edgecolors='darkgreen', linewidths=2, label='Start', zorder=6)
            
            # Direction arrows
            for i in range(0, len(path)-1, 2):
                dx = path[i+1][0] - path[i][0]
                dy = path[i+1][1] - path[i][1]
                plt.arrow(
                    path[i][0], -path[i][1], 
                    dx*0.9, -dy*0.9,
                    head_width=50, head_length=70,
                    fc='dodgerblue', ec='navy', alpha=0.7, zorder=3
                )
        
        # Show image
        #plt.grid(True, alpha=0.3)
        plt.title('Drone path', fontsize=14, pad=20)
        plt.xlabel('X Coordinate', fontsize=12)
        plt.ylabel('Y Coordinate', fontsize=12)
        plt.legend(fontsize=10, loc='upper right')
        plt.tight_layout()
        # plt.axis('off') 
        # plt.savefig('drone_row_path1.png', bbox_inches='tight', pad_inches=0, dpi=300)
        plt.show()


    def draw_path_image(self, path: List[Tuple[float, float]], image: np.ndarray) -> None:
        """
        Draws the generated path and original rows on an image.
        
        Args:
            path: Generated path points.
            image: Image on which to draw the path.
        """

        # Draw original rows (red)
        for row in self.original_rows:
            for i in range(len(row)-1):
                pt1 = (int(row[i][0]), int(row[i][1]))
                pt2 = (int(row[i+1][0]), int(row[i+1][1]))
                cv2.line(image, pt1, pt2, (0, 0, 255), 80)  # Red lines
                cv2.circle(image, pt1, 50, (0, 0, 255), -1)  # Red points
                cv2.circle(image, pt2, 50, (0, 0, 255), -1)  # Red points

        # Draw path (blue)
        if path:
            for i in range(len(path) - 1):
                pt1 = (int(path[i][0]), int(path[i][1]))
                pt2 = (int(path[i+1][0]), int(path[i+1][1]))
                cv2.line(image, pt1, pt2, (255, 0, 0), 20)  # Blue line
            
            # Path points (blue)
            for i in range(1, len(path)-1):
                pt = (int(path[i][0]), int(path[i][1]))
                cv2.circle(image, pt, 50, (255, 0, 0), -1)  # Blue points

            # Start/end markers
            start_point = (int(path[0][0]), int(path[0][1]))
            end_point = (int(path[-1][0]), int(path[-1][1]))

            # Start point (green circle)
            cv2.circle(image, start_point, 50, (0, 255, 0), -1)  # Lime green

            # End point (orange circle)
            cv2.circle(image, end_point, 50, (0, 165, 255), -1)  # Orange

            # Draw arrows (direction)
            for i in range(0, len(path)-1, 2):
                pt1 = (int(path[i][0]), int(path[i][1]))
                pt2 = (int(path[i+1][0]), int(path[i+1][1]))
                dx = pt2[0] - pt1[0]
                dy = pt2[1] - pt1[1]
                cv2.arrowedLine(image, pt1, pt2, (255, 0, 0), 20)  # DodgerBlue arrow

        # Display the image
        cv2.imshow("Drone path in image", cv2.resize(image, None, fx=0.06, fy=0.06))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # cv2.imwrite("drone_row_paths2.jpg", cv2.resize(image, None, fx=0.06, fy=0.06))
   

    def pixel_to_gps(self, tif_path, x, y):
        self.dataset = rasterio.open(tif_path)

        #with rasterio.open(tif_path) as dataset:
        lon, lat = self.dataset.xy(y, x)  # rasterio usa (fila, columna) en lugar de (x, y)
        return lon, lat
    
    def get_drone_path_in_gps(self, tif_path, path): 
       gps_drone_path = []
       for position in path:
        longitude, latitude = self.pixel_to_gps(tif_path, position[0], position[1])
        gps_drone_path.append([longitude,latitude])

        return gps_drone_path
