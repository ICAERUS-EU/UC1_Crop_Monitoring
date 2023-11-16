""" Code to match channels from WA dataset and create RGB images """

__author__ = "Esther Vera"
__copyright__ = "Copyright 2023, Noumena"
__credits__ = ["Esther Vera, Oriol Arroyo, Salvador Calgua, Aldo Sollazzo"]
__version__ = "1.0.0"
__maintainer__ = "Esther Vera"
__email__ = "esther@noumena.io"
__status__ = "Production"
__license__ = "MIT"

import cv2
import yaml
import numpy as np
import copy
import json 
import random 
from tqdm import tqdm 
import pandas as pd
import rasterio
from osgeo import gdal
import os

#from searchImages import alignImages_ORB, alignImages_SIFT
select_points = False 
#select_points = True

MAX_FEATURES = 20000
GOOD_MATCH_PERCENT = 0.65

LIMIT_H = 960 - 15
LIMIT_W = 1280 - 25




def alignImages_SIFT(im1, im2, MAX_FEATURES, GOOD_MATCH_PERCENT):


    # Detect SIFT features and compute descriptors.
    sift = cv2.SIFT_create(MAX_FEATURES)
    keypoints1, descriptors1 = sift.detectAndCompute(im1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(im2, None)


    FLANN_INDEX_KDTREE = 1  
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50) 
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(descriptors1, descriptors2, k=2)     

    # Save only good matches, depending on distance ratio
    good_matches = []
    for m,n in matches: 
        if(m.distance < GOOD_MATCH_PERCENT*n.distance):
            good_matches.append(m)

 
    # Draw top matches
    imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, good_matches, None)
    cv2.imwrite("matches.jpg", imMatches)

    # Extract location of good matches
    points1 = np.zeros((len(good_matches), 2), dtype=np.float32)
    points2 = np.zeros((len(good_matches), 2), dtype=np.float32)

    for i, match in enumerate(good_matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

    # Find homography
    h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

    # Use homography
    height, width, channels = im2.shape
    im1Reg = cv2.warpPerspective(im1, h, (width, height))

    return im1Reg, h


def normalize_image(img):

    img = np.array(img, dtype=np.float32)
    img_norm = (img - np.min(img)) / (np.max(img) - np.min(img))
    img_norm *= 255.0
    img_norm = np.round(img_norm).astype(np.uint8)

    return img_norm






def main(): 

    base_path = "/home/noumena/Downloads/dataset_uav/0_V1/"
    images_folder = base_path + "SET/"
    output_folder = base_path + "RGB2/"

    # Create output folder to save RGB images
    os.makedirs(output_folder, exist_ok=True)

    # List all image names and save the RGB channels
    all_img_paths = sorted(os.listdir(images_folder))
    b_paths = [images_folder+path for path in all_img_paths if path.split('_')[-1] == '1.tif']
    g_paths = [images_folder+path for path in all_img_paths if path.split('_')[-1] == '2.tif']
    r_paths = [images_folder+path for path in all_img_paths if path.split('_')[-1] == '3.tif']


    # Process all channels and build RGB images
    for i in tqdm(range(len(b_paths))): 

        try: 
            # Read images in grayscale
            im1 = cv2.imread(b_paths[i], cv2.IMREAD_GRAYSCALE)
            im2 = cv2.imread(g_paths[i], cv2.IMREAD_GRAYSCALE)
            im3 = cv2.imread(r_paths[i], cv2.IMREAD_GRAYSCALE)

            # Reshape images
            im1 = im1.reshape(im1.shape[0], im1.shape[1], 1)
            im2 = im2.reshape(im2.shape[0], im2.shape[1], 1)
            im3 = im3.reshape(im3.shape[0], im3.shape[1], 1)

            # Normalize images
            im1 = normalize_image(im1)
            im2 = normalize_image(im2)
            im3 = normalize_image(im3)


            # Get images aligned with SIFT
            Gh_band, H1 = alignImages_SIFT(im2, im1, MAX_FEATURES, GOOD_MATCH_PERCENT)
            Gh_band = Gh_band.reshape(Gh_band.shape[0], Gh_band.shape[1], 1)

            Rh_band, H2 = alignImages_SIFT(im3, im1, MAX_FEATURES, GOOD_MATCH_PERCENT)
            Rh_band = Rh_band.reshape(Rh_band.shape[0], Rh_band.shape[1], 1)

            # Merges images to create BGR
            rgb_image = cv2.merge([im1, Gh_band, Rh_band])

            # Crops image to its limits 
            rgb_image = rgb_image[0:LIMIT_H, 0:LIMIT_W]

            # Save image
            name_img = '_'.join(b_paths[i].split('/')[-1].split('_')[0:2]) + '.tif'
            
            cv2.imwrite(output_folder + name_img, rgb_image)
            #cv2.imwrite("imagen.tif", rgb_image)
        
            #cv2.imshow('rgb_image', rgb_image)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

        except: 
            print("COULDN'T PROCESS: ", b_paths[i])
            


if __name__ == "__main__":
    main()






'''tif_path_b = "IMG_0136_1.tif"
tif_path_g = "IMG_0136_2.tif"
tif_path_r = "IMG_0136_3.tif"

tif_path_b = "IMG_0212_1.tif"
tif_path_g = "IMG_0212_2.tif"
tif_path_r = "IMG_0212_3.tif"

im1 = cv2.imread(tif_path_b, cv2.IMREAD_GRAYSCALE)
im2 = cv2.imread(tif_path_g, cv2.IMREAD_GRAYSCALE)
im3 = cv2.imread(tif_path_r, cv2.IMREAD_GRAYSCALE)'''