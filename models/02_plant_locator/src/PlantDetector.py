from ultralytics import YOLO
import cv2 
import time 
import os 
import numpy as np 
import matplotlib.pyplot as plt
import math
from PIL import Image
from PIL.ExifTags import TAGS



class PlantDetector:
    def __init__(self):
        self.plocation = [0, 0]
        self.add_dist = 0
        self.all_locations = []
        self.all_health_status = []
    
    
    def filter_predictions(self, results):
        for result in results:
            bboxes = result.boxes.xyxy
            scores = np.array(result.boxes.conf.cpu())
            bboxes_arr = np.array([np.array(bbox.cpu()) for bbox in bboxes])
            selected_indices = cv2.dnn.NMSBoxes(bboxes_arr, scores, 0.15, 0.6)
            bboxes_selected = np.array([bboxes_arr[i] for i in selected_indices])
        return bboxes_selected
    
    def draw_bbox(self, frame, bboxes, health_status):
        for bbox, health in zip(bboxes, health_status):
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[2]), int(bbox[3]))
            if health == 1:
                cv2.rectangle(frame, p1, p2, (0, 255, 0), 50, 2)
            else:
                cv2.rectangle(frame, p1, p2, (0, 0, 255), 50, 2)
        return frame 
    
    def get_center(self, bbox):
        x = bbox[2] - ((bbox[2]-bbox[0]) / 2)
        y = bbox[3] - ((bbox[3]-bbox[1]) / 2)
        return [x, y]
    
    def get_middle_plant(self, frame, bboxes, health_status):
        all_centers = []
        center_frame = np.array([frame.shape[1]//2, frame.shape[0]//2])
        limit = frame.shape[1] // 6
        
        for bbox in bboxes:
            all_centers.append(self.get_center(bbox))
        all_centers = np.array(all_centers)
        
        distances = np.linalg.norm(all_centers - center_frame, axis=1)
        middle_plant = bboxes[np.argmin(distances)]
        health_middle_plant = np.round(health_status[np.argmin(distances)])
        
        for dist, conf, bbox in zip(distances, health_status, bboxes): 
            if abs(dist) < limit and conf > 0.6:
                middle_plant = bbox
                health_middle_plant = np.round(conf)
        
        return middle_plant, health_middle_plant
    
    def distancia_entre_puntos(self, plocation, location):
        plat, plon, lat, lon = map(math.radians, [plocation[0], plocation[1], location[0], location[1]])
        dlat = plat - lat
        dlon = plon - lon
        a = math.sin(dlat/2)**2 + math.cos(lat) * math.cos(plat) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        R = 6371000 
        distance = R * c
        return distance
    
    def dms2dd(self, dms, geodir):
        if geodir in ['S', 'O']:
            dd = -1
        else:
            dd = 1
        return np.float64((dms[0] + dms[1] / 60 + dms[2] / 3600) * dd)
    
    def get_middle_plant_location(self, image_path, frame, bboxes, health_status):
        location = -1
        middle_plant = []
        health_middle_plant = -1
        img = Image.open(image_path)
        info_exif = img._getexif()
        
        for tag, value in info_exif.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name == 'GPSInfo':
                lat = self.dms2dd(value[2], value[1])
                lon = self.dms2dd(value[4], value[3])
                location = [lat, lon]
                break
        
        if self.first:
            dist = 100
            self.first = False
        else:
            dist = self.distancia_entre_puntos(self.plocation, location)
            dist += self.add_dist 
        
        if dist >= 0.6:
            middle_plant, health_middle_plant = self.get_middle_plant(frame, bboxes, health_status)
            self.add_dist = 0
        else: 
            self.add_dist += self.pdist
        
        self.plocation = location
        self.pdist = dist
        
        return location, middle_plant, health_middle_plant
    
    def track_plants(self, folder_name):
        self.first = True
        all_images = os.listdir(folder_name)
        model = YOLO('best.pt')
        for img_path in all_images:
            complete_img_path = os.path.join(folder_name, img_path)
            frame = cv2.imread(complete_img_path)
            results = model.predict(frame)
            health_status = np.array(results[0].boxes.conf.cpu().numpy().astype(float))
            bboxes = self.filter_predictions(results)
            location, bbox_middle_plant, health_middle_plant = self.get_middle_plant_location(complete_img_path, frame, bboxes, health_status)
            if health_middle_plant > -1:
                self.all_health_status.append(health_middle_plant)
                self.all_locations.append(location)
                frame = self.draw_bbox(frame, [bbox_middle_plant], [health_middle_plant])
            frame = cv2.resize(frame, None, fx=0.1, fy=0.1)
            cv2.imwrite("images_tracking_detections/"+img_path, frame)
            cv2.imshow("tracking", frame)
            if cv2.waitKey(1) & 0xFF == ord('s'):
                break
        cv2.destroyAllWindows()


# Ejemplo de uso
'''tracker = PlantDetector()
tracker.track_plants("images_tracking/")
print(tracker.all_locations)
print(tracker.all_health_status)
'''

