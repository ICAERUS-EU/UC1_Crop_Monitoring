
# 05 - PLANT DISEASE DETECTION YOLOV12 WITH 3 CLASSES

## 🌿 Overview

This repository contains the code used for training the model to detect diseased plants. The model is designed to classify vine leaves into three categories:

- Healthy
- Mildew
- Low Iron

 ## 🗂️ Structure

- **README.md**: explanation of the repository and usage. 
- **best.pt:** 
- **plant_disease_detection_yolov12_3clases_v1.py**: main notebook code to execute. 


## 📄 Dataset 

The necessary data for this code is provided in the [ICAERUS VINEYARDS DATASET](https://zenodo.org/records/15090766). If you are using Google Colab, ensure that this dataset is downloaded and saved to your drive. The dataset consists of 508 labeled images across three classes, captured using a DJI Mavic 3M drone.


## 💻 Requirements

- **Environment configuration**: the code is meant to be executed with google colab.
- **Data**: download the [ICAERUS VINEYARDS DATASET](https://zenodo.org/records/15090766) which contains the vine images labelled and add it to your google drive account. 

## ⚙️ Parameters

The parameters are defined directly in the code. 

- **Data paths**: the paths for reading the dataset or the yolov12 model and the dataset should be adjusted in the code. This are specify for using Google Colab. 
- **Variables**: variables are defined inside the code and are adjusted for this purpose. 
- **Model**: download [yolov12n.pt](https://docs.ultralytics.com/models/yolo12/#detection-performance-coco-val2017) and add it to your google drive.

## 🚀 Usage
To run the code faster, upload it to Google Colab and enable TPU acceleration by following these steps:

1. Go to **Runtime** > **Change runtime type**.
2. Select **TPU** from the **Hardware accelerator** dropdown menu.

After starting running the code, the libraries will be installed and imported. Next, you will have to initialize the session with Google Drive after:


```ruby
from google.colab import drive, files
drive.mount('/content/drive')
```


 
 Specify correctly the paths to the datasets and the model in cell 7. Then the training will start in batches of 32, with an image size of 640 for 300 epochs. The final model saved will be the one with more accuracy after the 300 epochs training. You can adjust the number of epochs or add early stopping. After the training, the model is saved to **/content/runs/detect/train/weights/best.pt** and you can test the predictions using the test data. 
 


## 📊 Results
The trained model is applied to vineyard imagery to detect signs of disease. Below is a compilation of the resulting predictions:

<p align="center">
  <img src="https://github.com/user-attachments/assets/faf93d78-31d0-4b4a-af48-09524b140480" width="600" height="600">
</p>




## Authors

* **Esther Vera** - *Noumena* - [Esther Vera](https://github.com/EstherNoumena)

## Acknowledgements
This project is funded by the European Union, grant ID 101060643.

<img src="https://rea.ec.europa.eu/sites/default/files/styles/oe_theme_medium_no_crop/public/2021-04/EN-Funded%20by%20the%20EU-POS.jpg" alt="https://cordis.europa.eu/project/id/101060643" width="200"/>
