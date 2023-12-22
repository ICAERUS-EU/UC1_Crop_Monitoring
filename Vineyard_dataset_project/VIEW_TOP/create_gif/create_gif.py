""" Code"""

__author__ = "Esther Vera"
__copyright__ = "Copyright 2023, Noumena"
__credits__ = ["Esther Vera, Oriol Arroyo, Salvador Calgua, Aldo Sollazzo"]
__version__ = "1.0.0"
__maintainer__ = "Esther Vera"
__email__ = "esther@noumena.io"
__status__ = "Production"
__license__ = "MIT"

from PIL import Image
import imageio
import os
from tqdm import tqdm
import cv2 

base_path = './../../data/'
base_path_images = base_path + 'images/'
base_path_features = base_path + 'features/'
base_path_gif_images = base_path + 'images_gif/'







def main():

        
    # Obtener la lista de archivos de imagen en el directorio
    image_files = [f for f in os.listdir(base_path_gif_images) if f.endswith('.jpg')]


    image_files = sorted(image_files, key=lambda x: int(x.split('_')[-1].split('.')[0]))

    # Lista para almacenar imágenes
    images = []


    # Read the first frame to get dimensions
    first_frame = cv2.imread(os.path.join(base_path_gif_images, image_files[0]))
    height, width, layers = first_frame.shape
    print("jere")

    # Create a VideoWriter object
    video = cv2.VideoWriter('row_vineyards.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 7, (width, height))

    print("Saving video...")

 
    cont = 0
    # Leer cada imagen y agregarla a la lista
    for image_file in tqdm(image_files):
        frame_path = os.path.join(base_path_gif_images, image_file)
        frame = cv2.imread(frame_path)

        video.write(frame)
        cont = cont+1
        #if(cont==15):
        #    break

    video.release()

    print(f"Video saved")




if __name__ == "__main__":
    main()



