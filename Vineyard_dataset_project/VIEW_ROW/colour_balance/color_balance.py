

import cv2 
import os 
from tqdm import tqdm
from skimage import data
from skimage import exposure
from skimage.exposure import match_histograms


input_folder =  '/home/noumena/Documents/WU_DATA/dataset_uav/0_V1/RGB/'
output_folder = '/home/noumena/Documents/WU_DATA/dataset_uav/0_V1/RGB_balanced/'

reference =  cv2.imread('balanced_img_V1.png')

img_files = os.listdir(input_folder)

for img_name in tqdm(img_files):

    image = cv2.imread(input_folder + img_name)
    matched = match_histograms(image, reference, channel_axis=-1)
    cv2.imwrite(output_folder + img_name, matched)