""" Shows the row and global images with detections """

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


class Display:
    def __init__(self, image, row_points, parcels_points_flatten, centers_points_flatten, save_images_folder):
       
        self._image = image
        self._row_points = row_points
        self._parcels_points_flatten = parcels_points_flatten
        self._centers_points_flatten = centers_points_flatten
        self._size = image.shape[0:2]
        self._save_images_folder = save_images_folder
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


    def draw_parcel_rows(self): 
        
        parcel_rows_image = self._image.copy()
        for k1, parcel in enumerate(self._parcels_points_flatten):
            cv2.polylines(parcel_rows_image, [np.array(parcel)], isClosed=True, color=[0,170,255], thickness=2)                             
            center = (int(self._centers_points_flatten[k1][0]), int(self._centers_points_flatten[k1][1]))
            cv2.circle(parcel_rows_image, center, radius=2, color=(255, 255, 255), thickness=-1)

        cv2.imshow("parcel_rows_image", parcel_rows_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def draw_drones_and_parcels(self, drone_pixels_locations, parcels_selected): 
        
        image = self._image.copy()
        # Calculate the line representing the drone's orientation in the image 
        for drone_pixel, idx_parcel in zip(drone_pixels_locations, parcels_selected): 
            if(idx_parcel != -1):
                image = cv2.circle(image, drone_pixel, 7, (255,255,0), -1)
                #image = cv2.fillPoly(image, [np.array(self._parcels_points_flatten[idx_parcel])], (255,100,100))
                image = cv2.polylines(image, [np.array(self._parcels_points_flatten[idx_parcel])], isClosed=True, color=(255,255,255), thickness=3)

        cv2.imshow("image", cv2.resize(image, None, fx=0.3, fy=0.3))
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def draw_drones_and_parcels_color(self, calc, drone_pixels_locations, parcels_selected, all_health_status): 
        
        image = self._image.copy()
        overlay = image.copy()
        overlay = np.zeros((self._size[0], self._size[1], 3), dtype=np.uint8)

        prev_idx = next((idx for idx in parcels_selected if idx != -1), None)

        # Calculate the line representing the drone's orientation in the image 
        for drone_pixel, idx_parcel, health_status in zip(drone_pixels_locations, parcels_selected, all_health_status): 
            if(idx_parcel != -1):

                while(idx_parcel - prev_idx > 1):               
                    prev_idx = prev_idx+1
                    #overlay = cv2.fillPoly(overlay, [np.array(self._parcels_points_flatten[prev_idx])], (0,0,0))
                    image = cv2.polylines(image, [np.array(self._parcels_points_flatten[prev_idx])], isClosed=True, color=(255,255,255), thickness=1)

                if(np.round(health_status) == 1):
                    overlay = cv2.fillPoly(overlay, [np.array(self._parcels_points_flatten[idx_parcel])], (0,255,0))
                else: 
                    overlay = cv2.fillPoly(overlay, [np.array(self._parcels_points_flatten[idx_parcel])], (0,0,255))

                image = cv2.polylines(image, [np.array(self._parcels_points_flatten[idx_parcel])], isClosed=True, color=(255,255,255), thickness=1)
                image = cv2.circle(image, drone_pixel, 1, (255,50,0), -1)
                pts = calc.calculate_triangle(drone_pixel)
                rot_pts = calc.rotate_triangle(drone_pixel, pts)
                overlay = cv2.fillPoly(overlay, [rot_pts], (255,180,50))

                prev_idx = idx_parcel

        cv2.addWeighted(overlay, 0.5, image, 1, 0, image)

        cv2.imwrite("image_rows.jpg", image)
        cv2.imshow("image_rows", cv2.resize(image, None, fx=0.3, fy=0.3))
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def draw_bbox(self, frame, bbox, health_status) -> np.ndarray:
        """
            Draws bounding box on a frame based on detected objects and their health status.

            Args:
                frame (numpy.ndarray): Input frame.
                bboxes (numpy.ndarray): Array of bounding boxes.

            Returns:
                frame (numpy.ndarray): Frame with bounding boxes drawn.
        """

        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[2]), int(bbox[3]))
        if np.round(health_status) == 1:
            cv2.rectangle(frame, p1, p2, (0, 255, 0), 50, 2)
        else:
            cv2.rectangle(frame, p1, p2, (0, 0, 255), 50, 2)

        return frame 
    

    def show_bbox_plants(self, frame, img_path, middle_plant, health_status): 

        # Draw bbox around plant detected 
        frame = self.draw_bbox(frame, middle_plant, health_status)

        # Save and show detected plants in images
        cv2.imwrite(self._save_images_folder + img_path, frame)
        cv2.imshow("Plant detected", cv2.resize(frame, None, fx=0.1, fy=0.1))
        cv2.waitKey(1000)            
        cv2.destroyAllWindows()


    '''def draw_intersections(self, blank_rows, size, length): 

        blank_final = np.zeros((size[0], size[1], 1), dtype=np.uint8)

        # Calculate the line representing the drone's orientation in the image 
        for drone_pixel in self._drones_pixels: 
            x2 = int(drone_pixel[0] + length * np.cos(self._drone_angle))
            y2 = int(drone_pixel[1] + length * np.sin(self._drone_angle))

            blank_final = cv2.line(blank_final, (drone_pixel[0], drone_pixel[1]), (x2, y2), (255,), 1)

        # Find positions of pixels where the intersection occurred between the drone orientation line and actual parcel
        blank_final = cv2.bitwise_or(blank_final, blank_rows)

        for inter in self._intersections: 
            blank_final = cv2.circle(blank_final, tuple(map(int, inter)), 10, (255,), -1)


        cv2.imshow("blank_final", cv2.resize(blank_final, None, fx=0.3, fy=0.3))
        cv2.waitKey(0)
        cv2.destroyAllWindows()'''