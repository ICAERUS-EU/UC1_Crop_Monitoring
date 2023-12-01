
import numpy as np
import os 
import json
import cv2 
import matplotlib.pyplot as plt 

# Save row labels
base_path = './../../data/'
base_path_features = base_path + 'features/'


# PAULA ANNOTATIONS
'''
row_labels = [1,0,1,0,0,0,0,0,1,1,0,0,
              1,0,0,1,1,0,0,0,1,0,0,0,
              1,0,1,0,1,0,0,1,0,0,
              1,0,1,0,1,0,0,0,0,1,
              0,0,0,0,0,0,0,0,1,0]'''



# CREATE ANNOTATIONS BASED ON GREENESS

# Load image
#base_path = '/home/noumena/Documents/ICAERUS/row_images_raw/'
base_row_images_path = './../../data/row_images/'


img_files = os.listdir(base_row_images_path)
img_files = sorted(img_files, key=lambda x: (int(x.split('_')[1]), int(x.split('_')[2].split('.')[0])))

print(img_files)


all_vari_imgs = []
for img_name in img_files:

    img_path = os.path.join(base_row_images_path, img_name)
    print(img_path)
    img = cv2.imread(img_path)

    b_img, g_img, r_img = cv2.split(img/255)
    vari_img = np.zeros_like((b_img))
    for i in range(len(b_img)):
        for j in range(len(b_img[i])):
            den = (g_img[i][j] + r_img[i][j] - b_img[i][j])  
            #print(den)
            if(den != 0):
                vari_img[i][j] = (g_img[i][j] - r_img[i][j])/den
    
    all_vari_imgs.append(vari_img)


row_labels = []
tam = (vari_img.shape[0]*vari_img.shape[1]) 
for vari_img in all_vari_imgs:
    total_vari = np.sum(vari_img)/tam

    if(total_vari > -0.02):
        row_labels.append(1)
    else: 
        row_labels.append(0)

print(row_labels)

# Savel row_labels
output_path = base_path_features + 'row_labels.json'
with open(output_path, 'w') as f:
    json.dump(row_labels, f)
