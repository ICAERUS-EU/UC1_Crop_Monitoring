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

from src.orthomosaic_processor import OrthomosaicProcessor
from src.colormaps import apply_colormap, save_colormap
from src.vegetation_indices import VegetationIndices


# Setup paths
base_path = './../../data/'
base_path_images = base_path + 'images/'
base_path_features = base_path + 'features/'



# MAIN
##################################################################################################################

def main():

    # Variables
    tam = (2346, 1805)
    op = OrthomosaicProcessor()
    vi = VegetationIndices()

    # Load images
    ##########################################################################
    tif_path = base_path_images + 'orthomosaic_cropped_230609.tif'
    ortho_image, r_image, g_image, b_image, mask = op.read_orthomosaic(tif_path)
    ortho_image_res, r_image_res, g_image_res, b_image_res, mask_res = op.resize_orthomosaic(ortho_image, r_image, g_image, b_image, mask, tam)
    mask_res_rgb = cv2.cvtColor(mask_res, cv2.COLOR_GRAY2RGB)
    print(ortho_image_res.shape)

    # Load NIR 
    tif_path = base_path_images +'cropped_NIR_orthomosaic_230609.tif'
    nir_image = op.read_one_channel_orthomosaic(tif_path)
    nir_image_res = op.resize_and_convert_type(nir_image, tam)

    # Load spectral R
    tif_path = base_path_images + 'cropped_R_orthomosaic_230609.tif'
    r_spectral = op.read_one_channel_orthomosaic(tif_path)
    r_spectral_res = op.resize_and_convert_type(r_spectral, tam)

    # Load spectral G
    tif_path = base_path_images + 'cropped_G_orthomosaic_230609.tif'
    g_spectral = op.read_one_channel_orthomosaic(tif_path)
    g_spectral_res = op.resize_and_convert_type(g_spectral, tam)

    # Load RE
    tif_path = base_path_images + 'cropped_RE_orthomosaic_230609.tif'
    re_image = op.read_one_channel_orthomosaic(tif_path)
    re_image_res = op.resize_and_convert_type(re_image, tam)
  

    # Calculate vegetation indexes
    ##########################################################################
    
    # Calculate nvdi
    ndvi_image = vi.ndvi(nir_image_res, r_spectral_res)
    ndvi_image = op.normalize_image(ndvi_image)
  
    # Get colormap and save
    ndvi_final = apply_colormap(ndvi_image, mask_res_rgb, 0, 255)
    save_colormap(ndvi_final, 'ndvi_map.png', False)


    # Calculate gndvi
    gndvi_image = vi.gndvi(nir_image_res, g_spectral_res)
    gndvi_image = op.normalize_image(gndvi_image)
  
    # Get colormap and save
    gndvi_final = apply_colormap(gndvi_image, mask_res_rgb, 0, 255)
    save_colormap(gndvi_final, 'gndvi_map.png', False)

  
    # Calculate ndwi
    ndwi_image = vi.ndwi(nir_image_res, g_spectral_res)
    ndwi_image = op.normalize_image(ndwi_image)
  
    # Get colormap and save
    ndwi_final = apply_colormap(np.max(ndwi_image) - ndwi_image, mask_res_rgb, 0, 255)
    save_colormap(ndwi_final, 'ndwi_map.png', False)


    # Calculate ndre
    ndre_image = vi.ndre(nir_image_res, re_image_res)
    ndre_image = op.normalize_image(ndre_image)
  
    # Get colormap and save
    ndre_final = apply_colormap(ndre_image, mask_res_rgb, 0, 255)
    save_colormap(ndre_final, 'ndre_map.png', True)
    

    # Calculate vari
    vari_image = vi.vari(r_image_res, g_image_res, b_image_res)
    vari_image = op.normalize_image(vari_image)
  
    # Get colormap and save
    vari_final = apply_colormap(vari_image, mask_res_rgb, 0, 255)
    save_colormap(vari_final, 'vari_map.png', False)
 


    # Save images
    ##########################################################################3

    # RGB
    #cv2.imwrite('ortho_image_rgb.png', ortho_image_res)
    #cv2.imwrite('r_ortho_image.png', r_image_res)
    #cv2.imwrite('g_ortho_image.png', g_image_res)
    #cv2.imwrite('b_ortho_image.png', b_image_res)

    # SPECTRAL 
    #cv2.imwrite('nir_ortho_image.png', nir_image_res)
    #cv2.imwrite('r_spectral_ortho_image.png', r_spectral_res)
    #cv2.imwrite('g_spectral_ortho_image.png', g_spectral_res)
    #cv2.imwrite('re_ortho_image.png', re_image_res)

    

    

if __name__ == "__main__":
    main()



