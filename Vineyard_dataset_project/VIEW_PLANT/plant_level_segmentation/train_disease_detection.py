""" Code to train disease segmentation in plant level """

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
import os
import matplotlib.pyplot as plt

import torch
import torchvision
import torch.nn.functional as F
#from keras.optimizers import Adam

from src.model_resnet import UNetResnet
from src.load_and_save_data import Dataset
from src.train_resnet_functions import fit2, iou



# FUNCTIONS
########################################################################################################################################################
def get_updated_labels(y): 
        
    y = np.array(y)
    new_y = np.zeros_like(y)

    # BLUE (disease)
    blue_condition = (y[:, :, :, 0] > 100) & (y[:, :, :, 0] > y[:, :, :, 1])
    new_y[blue_condition] = 2

    # GREEN (plant)
    green_condition = (y[:, :, :, 1] > 100) & (y[:, :, :, 1] > y[:, :, :, 0])
    new_y[green_condition] = 1

    new_y = np.zeros((y.shape[0], y.shape[1], y.shape[2]), dtype=np.uint8)

    return new_y



def get_class_weights(new_y): 

    # Count each label appearance
    green = np.sum(new_y == 1)
    blue = np.sum(new_y == 2)
    total = new_y.size
    black = total - green - blue

    class_frequencies = [black/total, green/total, blue/total]
    print(class_frequencies)

    class_weights = [total / (len(class_frequencies) * freq) for freq in class_frequencies]
    print(class_weights)

    return class_weights




# MAIN
########################################################################################################################################################
def main(): 

    n_classes = 3
    folder_plants = "/run/media/noumena/ICAERUS/ICAERUS/01-MEDIA/LABELLED_IMAGES_ALESSANDRO/"

    # Get path of all images
    all_image_names = sorted(os.listdir(folder_plants))
    X_names = [image_name for image_name in all_image_names if image_name.split('_')[-1].split('.')[0] == 'D']
    y_names = [image_name for image_name in all_image_names if image_name.split('_')[-1].split('.')[0] == 'Dpintado']


    # Load all images 
    inter = cv2.INTER_LINEAR
    X_color = np.array([ cv2.cvtColor(cv2.resize(cv2.imread(folder_plants + image_name), (224,224), interpolation=inter), cv2.COLOR_BGR2RGB ) for image_name in X_names])
    X = np.array([cv2.resize(cv2.imread(folder_plants + image_name, cv2.IMREAD_GRAYSCALE), (224,224), interpolation=inter) for image_name in X_names])
    X = (X / 255).astype(np.float32)

    y = np.array([cv2.resize(cv2.imread(folder_plants + image_name), (224,224), interpolation=inter) for image_name in y_names])

    # Convert pixels values for labelling to 0,1,2 
    new_y = get_updated_labels(y)

    # Calcular el peso de cada clase para el entrenamiento
    class_weights = get_class_weights(new_y)


    ########################################################################################################################################################

    # Create datasets for training and test with images loaded
    dataset = {
        'train': Dataset(X[:-9], new_y[:-9],n_classes),
        'test': Dataset(X[-9:], new_y[-9:],n_classes)
    }
    print(len(dataset['train']))

    dataloader = {
        'train': torch.utils.data.DataLoader(dataset['train'], batch_size=4, shuffle=True, pin_memory=True),
        'test': torch.utils.data.DataLoader(dataset['test'], batch_size=4, pin_memory=True)
    }

    imgs, masks = next(iter(dataloader['train']))
    print(len(dataset['train']), len(dataset['test']))
    print(imgs.shape, masks.shape)

    ########################################################################################################################################################

    # Train model
    model = UNetResnet(n_classes=n_classes)
    model, hist = fit2(model, dataloader, class_weights, epochs=30, lr=3e-4)

    # Save model
    torch.save(model, 'my_model.pth')

    # Show training loss and accuracy during training
    df = pd.DataFrame(hist)
    df.plot(grid=True)
    plt.show()


    ########################################################################################################################################################
    # Load model
    model = torch.load('my_model.pth')

    # Process prediction for test image and show results
    model.eval()
    with torch.no_grad():
        ix = 0#random.randint(0, len(dataset['test'])-1)
        img, mask = dataset['test'][ix]
        output = model(img.unsqueeze(0).to(device))[0]
        pred_mask = torch.argmax(output, axis=0)
        
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(30,10))
    ax1.imshow(img.squeeze(0))
    ax2.imshow(torch.argmax(mask, axis=0))
    ax3.imshow(pred_mask.squeeze().cpu().numpy())
    plt.show()





if __name__ == "__main__":
    main()



