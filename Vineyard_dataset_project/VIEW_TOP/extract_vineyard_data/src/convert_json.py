import cv2
import numpy as np
import json 
import pandas as pd

from src.load_save_show import GeoDataProcessor



base_path = './../../data/'
base_path_images = base_path + 'images/'
base_path_features = base_path + 'features/'


# Change parcel_points format 
###########################################################################
'''gdp = GeoDataProcessor()
parcel_points = gdp.read_json_file(base_path_features + 'parcel_points.json') 
parcel_points_str = str(parcel_points)

listas_numeros = parcel_points_str.split("], [")
listas_modificadas = [lista.replace(",", ";") for lista in listas_numeros]
new_parcel_points = "], [".join(listas_modificadas)

with open('new_parcel_points.json', 'w') as f:
    json.dump(new_parcel_points, f)'''


# Change labelled_parcels format 
###########################################################################
df =  pd.read_csv(base_path_features + 'labelled_parcels.csv')    

new_parcel_points = []
for i in range(len(df['parcel'])):
    listas_numeros = df['parcel'][i].split("], [")
    listas_modificadas = [lista.replace(",", ";") for lista in listas_numeros]
    new_parcel = "], [".join(listas_modificadas)
    
    df.at[i, 'parcel'] = new_parcel


df.to_csv('new_labelled_parcels.csv', index=False)




