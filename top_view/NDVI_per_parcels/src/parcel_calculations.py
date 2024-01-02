import numpy as np 
import random
import json
from tqdm import tqdm 
import cv2




class ParcelProcessor:

    def __init__(self, ndvi_limit=-1.2):   
        self.NDVI_LIM = ndvi_limit


    def count_parcels(self, parcel_points): 
        total_parcels = 0
        for row in parcel_points:
            total_parcels += len(row)
        return total_parcels


    def generate_random_labels(self, total_parcels, path_labels='labels.json'): 
        labels = []
        for i in range(total_parcels):
            labels.append(random.randint(0, 1))

            with open(path_labels, 'w') as f:
                json.dump(labels, f)

        return labels


    def generate_ndvi_labels(self, ndvi_parcels, path_labels='labels.json'): 
        labels = []
        for i, value in enumerate(ndvi_parcels):
            if(value>0.35):
                labels.append(0)
            elif(value>0.25): 
                labels.append(1)    
            else: 
                labels.append(2)

        with open(path_labels, 'w') as f:
            json.dump(labels, f)
        
        return labels


    def calculate_mean_per_parcel(self, array_aux, all_parcels, lai_process): 
        h, w = array_aux.shape[0:2]
        mean_values = []
        for parcel in tqdm(all_parcels, desc='Processing parcels...', unit='parcel'): 

            # Get actual parcel mask  
            parcel_mask = np.zeros((h, w, 1), dtype=np.uint8)
            cv2.fillPoly(parcel_mask, [np.array(parcel)], color = (255,255,255))
            masked_parcel = cv2.bitwise_and(array_aux, array_aux, mask=parcel_mask)
            area_parcel = np.count_nonzero(masked_parcel)
            

            if(not lai_process):
                value = np.sum(masked_parcel) / area_parcel

            else: 
                all_values = masked_parcel[masked_parcel > self.NDVI_LIM].tolist()
                if(len(all_values)>0):
                    value = np.sum(all_values) / area_parcel
                else: 
                    value = 0.0

            mean_values.append(value)

        return mean_values



    def get_lai_per_parcel(self, ndvi_parcels):
        lai_parcels = []
        for ndvi_val in ndvi_parcels: 
            lai_parcels.append((1 - np.exp(-0.69 * ndvi_val)) / 0.69)
        
        return lai_parcels
