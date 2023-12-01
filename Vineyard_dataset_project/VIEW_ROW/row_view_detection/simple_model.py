
""" Code to  """

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
import pandas as pd
import rasterio
from PIL import Image

import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization


VINEYARD_HEIGHT = 5
VINEYARD_SEP = 12.2
PARCEL_LEN = 26




def main():

    # Load images
    path_row_images = './../../data/row_images/'
    path_row_labels = './../../data/features/row_labels.json'
    
    img_files = os.listdir(path_row_images)
    img_files = sorted(img_files, key=lambda x: (int(x.split('_')[1]), int(x.split('_')[2].split('.')[0])))

    X = []
    for img_name in img_files: 
        print(img_name)
        img_path = os.path.join(path_row_images, img_name)

        X.append(np.array(Image.open(img_path)))  #.flatten())
                 
    X = np.array(X)
    print(X.shape)

    with open(path_row_labels, 'r') as f:
        y = np.array(json.load(f)).astype(np.float32)


    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=4)


    input_shape = (106, 617,3)
    import keras
    from keras.applications import VGG16
    from keras.applications.vgg16 import preprocess_input
    from keras import layers, models

    ## Loading VGG16 model
    base_model = VGG16(weights="imagenet", include_top=False, input_shape=input_shape)
    base_model.trainable = False ## Not trainable weights

    ## Preprocessing input
    train_ds = preprocess_input(X_train) 
    test_ds = preprocess_input(X_test)


    flatten_layer = layers.Flatten()
    dense_layer_1 = layers.Dense(50, activation='relu')
    dense_layer_2 = layers.Dense(20, activation='relu')
    prediction_layer = layers.Dense(1, activation='softmax')


    model = models.Sequential([
        base_model,
        flatten_layer,
        dense_layer_1,
        dense_layer_2,
        prediction_layer
    ])

    from keras import backend as K
    class_weights = K.variable([200.0, 1.0])  # Puedes ajustar estos valores según tus necesidades

    def weighted_binary_crossentropy(y_true, y_pred):
        # Utilizar la variable de peso de clase previamente definida
        weighted_loss = K.binary_crossentropy(y_true, y_pred) * class_weights

        return K.mean(weighted_loss)



    model.compile(loss=weighted_binary_crossentropy,
                optimizer=keras.optimizers.Adam(),
                metrics=['accuracy'])
    

    #model.fit(X_train, y_train, epochs=3, batch_size=16, validation_data=(X_test, y_test))
    model.fit(train_ds, y_train, epochs=4 , validation_split=0.2, batch_size=16)


    model.save("row_view_model.h5py")

    test_eval = model.evaluate(test_ds, y_test, verbose=1)
    
    print('Test loss:', test_eval[0])
    print('Test accuracy:', test_eval[1])


    # Prediction
    y_pred = model.predict(test_ds)
    
    print(y_pred.flatten())
    print(y_test)





if __name__ == "__main__":
    main()


