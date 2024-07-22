
import cv2 
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
import numpy as np 


def apply_colormap(img, mask_res_rgb, vmin=0, vmax=255):
    colormap = plt.get_cmap('RdYlGn')
    norm = Normalize(vmin=vmin, vmax=vmax)
    colormap_norm = (np.array(colormap(norm(img))) * 255).astype(np.uint8)
    colormap_norm = colormap_norm[:, :, :-1]

    img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    img_colormap_black = np.where(mask_res_rgb != 0, colormap_norm, img_rgb)

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
