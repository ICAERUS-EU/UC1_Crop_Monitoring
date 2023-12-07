""" Code to extract and compare vegetation indexes """

__author__ = "Esther Vera"
__copyright__ = "Copyright 2023, Noumena"
__credits__ = ["Esther Vera, Oriol Arroyo, Salvador Calgua, Aldo Sollazzo"]
__version__ = "1.0.0"
__maintainer__ = "Esther Vera"
__email__ = "esther@noumena.io"
__status__ = "Production"
__license__ = "MIT"

import cv2
import numpy as np
import copy
from tqdm import tqdm 
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

from src.vegetation_indices import ndvi, gndvi, ndre, ndwi, vari
from src.geodataprocessor import GeoDataProcessor


# Setup paths
base_path = './../../data/'
base_path_images = base_path + 'images/'
base_path_features = base_path + 'features/'



# FUNCTIONS
##################################################################################################################

def normalize_image(img): 
    min_val = np.min(img)
    range_val = np.max(img) - min_val
    norm_image = (((img - min_val) / range_val)*255).astype(np.uint8)

    return norm_image

def apply_colormap(img, mask_res_rgb, vmin, vmax):
        
    # Prepare colormap and normalization
    colormap = plt.get_cmap('RdYlGn')  
    norm = Normalize(vmin=vmin, vmax=vmax)  
    colormap_norm = (np.array(colormap(norm(img))) * 255).astype(np.uint8)
    colormap_norm = colormap_norm[:, :, :-1]

    # Transform from gray to rgb and copy
    img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    # Apply coloramp to mask region in img_rgb 
    img_colormap_black = np.where(mask_res_rgb != 0, colormap_norm, img_rgb)

    # Changes black background to white background
    white_image = np.ones_like(img_colormap_black) * 255
    img_colormap_white = np.where(mask_res_rgb != 0, img_colormap_black, white_image)

    return img_colormap_white

def save_colormap(img, output_name, show=False): 

    fig, ax = plt.subplots(figsize=(27.91, 18.35), tight_layout=True)
    ax.imshow(img)
    ax.axis('off')
    fig.savefig(output_name, bbox_inches='tight', pad_inches=0)
    if show: 
        plt.show()


# MAIN
##################################################################################################################

def main():

    # Load images
    ##########################################################################
    gdp = GeoDataProcessor()

    tif_path = base_path_images + 'orthomosaic_cropped_230609.tif'
    ortho_image_res, r_image_res, g_image_res, b_image_res, mask_res =  gdp.read_orthomosaic(tif_path)
    print(ortho_image_res.shape)

    # Load NIR 
    tif_path = base_path_images +'cropped_NIR_orthomosaic_230609.tif'
    nir_image_res =  gdp.read_orthomosaic_onechannel(tif_path)
    nir_image_res = ((nir_image_res / 65535.0) * 255.0).astype(np.uint8)


    # Load spectral R
    tif_path = base_path_images + 'cropped_R_orthomosaic_230609.tif'
    r_spectral_res =  gdp.read_orthomosaic_onechannel(tif_path)
    print(r_spectral_res.shape)


    # Load RE
    '''tif_path = base_path_images + 'cropped_RE_orthomosaic_230609.tif'
    re_image_res =  gdp.read_orthomosaic_onechannel(tif_path)
    print(re_image_res.shape)'''


    # Resize images
    '''ortho_image_res = cv2.resize(ortho_image_res, None, fx = 0.2, fy = 0.2)
    r_image_res = cv2.resize(r_image_res, None,  fx = 0.2, fy = 0.2)
    g_image_res = cv2.resize(g_image_res, None,  fx = 0.2, fy = 0.2)
    b_image_res = cv2.resize(b_image_res, None,  fx = 0.2, fy = 0.2)
    nir_image_res = cv2.resize(nir_image_res, None, fx = 0.2, fy = 0.2)
    r_spectral_res = cv2.resize(r_spectral_res, None,  fx = 0.2, fy = 0.2)

    mask_res = cv2.resize(mask_res, None, fx = 0.2, fy = 0.2)'''
    mask_res_rgb = cv2.cvtColor(mask_res, cv2.COLOR_GRAY2RGB)
        
    print(nir_image_res.shape)


    # Calculate vegetation indexes
    ##########################################################################
    

    # Calculate nvdi
    ndvi_image = ndvi(nir_image_res, r_spectral_res)
    ndvi_image = normalize_image(ndvi_image)
  
    # Get colormap and save
    ndvi_final = apply_colormap(ndvi_image, mask_res_rgb, 0, 255)
    save_colormap(ndvi_final, 'ndvi_map.png', False)

    ndvi_final = apply_colormap(ndvi_image, mask_res_rgb, -5, 20)
    save_colormap(ndvi_final, 'ndvi_map_-5_20.png', True)


  

    # Calculate gndvi
    '''gndvi_image = gndvi(nir_image_res, g_image_res)
    gndvi_image = normalize_image(gndvi_image)
  
    # Get colormap and save
    gndvi_final = apply_colormap(gndvi_image, mask_res_rgb, 0, 255)
    save_colormap(gndvi_final, 'gndvi_map.png', True)

  

    # Calculate ndwi
    ndwi_image = ndwi(nir_image_res, g_image_res)
    ndwi_image = normalize_image(ndwi_image)
  
    # Get colormap and save
    ndwi_final = apply_colormap(np.max(ndwi_image) - ndwi_image, mask_res_rgb, 0, 255)
    save_colormap(ndwi_final, 'ndwi_map.png', True)'''



    '''# Calculate ndre
    ndre_image = ndre(nir_image_res, re_image_res)
    ndre_image = normalize_image(ndre_image)
  
    # Get colormap and save
    ndre_final = apply_colormap(ndre_image, mask_res_rgb, 0, 50)
    save_colormap(ndre_final, 'ndre_map.png', True)
    '''

  
    # Calculate vari
    vari_image = vari(r_image_res, g_image_res, b_image_res)
    vari_image = normalize_image(vari_image)
  
    # Get colormap and save
    vari_final = apply_colormap(vari_image, mask_res_rgb, 0, 255)
    save_colormap(vari_final, 'vari_map.png', False)
 


    # Save images
    ##########################################################################3

    # RGB
    cv2.imwrite('ortho_image_rgb.png', ortho_image_res)
    cv2.imwrite('r_ortho_image.png', r_image_res)
    cv2.imwrite('g_ortho_image.png', g_image_res)
    cv2.imwrite('b_ortho_image.png', b_image_res)

    # SPECTRAL 
    cv2.imwrite('nir_ortho_image.png', nir_image_res)
    cv2.imwrite('r_spectral_ortho_image.png', r_spectral_res)
    #cv2.imwrite('g_spectral_ortho_image.png', g_spectral_res)
    #cv2.imwrite('re_ortho_image.png', re_res)

    

    




if __name__ == "__main__":
    main()



