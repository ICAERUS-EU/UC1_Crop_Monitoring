import cv2
import numpy as np
import rasterio


class OrthomosaicProcessor:
    def __init__(self):
        pass

    def read_orthomosaic(self, tif_path):
        with rasterio.open(tif_path) as src:
            red_band = src.read(1)
            green_band = src.read(2)
            blue_band = src.read(3)
            rgb_image = cv2.merge([blue_band, green_band, red_band])
            mask = src.read(4)

        return rgb_image, red_band, green_band, blue_band, mask

    def resize_orthomosaic(self, ortho_image, r_image, g_image, b_image, mask, tam=(2346, 1805)):
        ortho_image_res = cv2.resize(ortho_image, tam)
        r_image_res = cv2.resize(r_image, tam)
        g_image_res = cv2.resize(g_image, tam)
        b_image_res = cv2.resize(b_image, tam)
        mask_res = cv2.resize(mask, tam)

        return ortho_image_res, r_image_res, g_image_res, b_image_res, mask_res

    def read_one_channel_orthomosaic(self, tif_path):
        with rasterio.open(tif_path) as src:
            img = src.read(1)
        return img

    def resize_and_convert_type(self, img, tam=(2346, 1805)):
        img_res = cv2.resize(img, tam)
        img_res = ((img_res / 65535.0) * 255.0).astype(np.uint8)
        return img_res

    def normalize_image(self, img):
        min_val = np.min(img)
        range_val = np.max(img) - min_val
        norm_image = (((img - min_val) / range_val) * 255).astype(np.uint8)

        return norm_image


