
import numpy as np
from PIL import Image
import os 
import cv2
import numpy as np



# Load image
base_path = '/home/noumena/Documents/ICAERUS/row_images_raw/'
base_output_path = './../../data/row_images/'

new_size = (633, 243)
rotation_angle = np.deg2rad(-13.5)

img_files = os.listdir(base_path)
print(img_files)

all_w = []
all_h = []
margen = 3

for img_name in img_files:


    img_path = os.path.join(base_path, img_name)
    output_path = os.path.join(base_output_path, img_name)

    # Load and rotate image
    img = Image.open(img_path)
    img = np.array(img.rotate(np.degrees(rotation_angle), fillcolor="white"))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Process image
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gris, (5, 5), 0)

    # Extract mask
    mask = cv2.inRange(blur, 0, 200)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    fila_blancos, columna_blancos = np.where(mask == 255)
    for fila, columna in zip(fila_blancos, columna_blancos):
        if (columna < margen or columna >= mask.shape[1] - margen):
            mask[fila][columna] = 0


    # Get contours and crop image
    canny = cv2.Canny(mask, 30, 100)
    contornos, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = cv2.boundingRect(contornos[0])
    #cv2.drawContours(img, contornos, -1, (0,255,0), 3)
    
    new_img = img[y:y + h, x:x + w]
    print(new_img.shape)
    all_w.append(new_img.shape[0])
    all_h.append(new_img.shape[1])

    new_img = cv2.resize(new_img, (617, 106))

    cv2.imwrite(output_path, new_img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])


    '''cv2.imshow('mask', mask)
    cv2.imshow('canny', canny)
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''


print(np.mean(all_w))
print(np.mean(all_h))

# Calculate rotation degrees
'''cov_matrix = np.cov(img_gray)
eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
max_eigen_idx = np.argmax(eigenvalues)
max_eigenvector = eigenvectors[:, max_eigen_idx]
rotation_angle =  np.arctan2(max_eigenvector[1], max_eigenvector[0]) + np.deg2rad(90)
'''
