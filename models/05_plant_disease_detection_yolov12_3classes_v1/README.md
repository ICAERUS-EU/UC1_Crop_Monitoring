
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
- **Data**: download the [ICAERUS VINEYARDS DATASET](https://zenodo.org/records/15090766) which contains the vine images labelled. 

## ⚙️ Parameters

The parameters are defined directly in the code. 

- **Data paths**: the paths for reading the dataset or the yolov12 model are adjusted for using Google Colab. 
- **Variables**: variables are defined inside the code and are adjusted for this purpose. 


## 🚀 Usage
To run the code faster, upload it to Google Colab and enable TPU acceleration by following these steps:

1. Go to Runtime > Change runtime type.
2. Select TPU from the "Hardware accelerator" dropdown menu.

Next, you will have to initialize the session with Google Drive after:

´´´
# Import data from colab
from google.colab import drive, files
drive.mount('/content/drive')
´´´
     

<!--

First of all, the orthomosaic image and its mask are read. Then it uses the class *VineyardRowDetector* to detect the rows of the vineyards in the orthomosaic image. This is done in the following manner: 

- There is already a row definition with its coordinates (2250, 3453) and (4876, 2855). This coordinates were obtained setting the *select_points* variable to *True* and manually selecting the first row. The points are scalated automatically in the mouse callback.
- Then, from this row, the rest of the rows are generating by knowing the distance between rows and with an arbitrary wide and length (*get_parallel_rows*).
- When all the rows are drawn we filter them using the orthomosaic mask to adjust them to the image (*filter_rows*).


<p align="center"> <img src="https://github.com/user-attachments/assets/1a0d1eec-85a0-48a9-a6af-69d46f94b503" alt="Row Image Example" width="60%"></p>

- We detect the rows coordinates using contour detection and save also the lower line of this contour (*get_rows_coordinates*).

Now that we have the lines (saved in *rows* variable) that define each vineyard row, we can generate the path. The path will happen a little bit lower in the image, between each row and an optimized path should be generated. 

- The code uses the class PathGenerator, with *generate_path* function, that will build the path between rows in zigzag as the drone movement will be. Starting from the *current_line* it finds the closest row and moves in that direction taking into account the start and ending of each row. 


Once we have the path in pixel coordinates, it is changed to GPS coordinates using the transform matrix saved in the orthomosaic image. With the GPS coordinates, we transform them to the drone simulation format in YAML using **(code not uploaded yet)**, that includes the height and the type of movement and this can be used for moving the anafi drone in simulation or real life directly using the [04_drone_simulation_v1](https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/tree/main/models/04_drone_simulation_v1) code. 



## 📊 Results
As a final result, we get the path generated in pixel coordinates and GPS coordinates and ready for flying the drone. 



Before, we have compute the rectangle contours that define each vineyard row in the image, which is saved in **rows_contour_coordinates.json** and the lower line of each row in **rows_coordinates.json**. 

**rows_contour_coordinates.json**
```text
[
  [[8844, 14352], [11063, 13848], [8864, 14437], [11082, 13933]],
  [[8500, 14127], [11678, 13403], [8520, 14212], [11698, 13488]],
  [[8180, 13896], [12065, 13012], [8200, 13981], [12085, 13097]],
  [[7944, 13646], [12384, 12636], [7964, 13731], [12403, 12720]],
  ...
]
```

**rows_coordinates.json**
```text
[
  [[[8864, 14437], [11082, 13933]],
  [[8520, 14212], [11698, 13488]],
  [[8200, 13981], [12085, 13097]],
  [[7964, 13731], [12403, 12720]],
  ...
]
```



The final path is shown in the following matplotlib image 
<p align="center"> <img src="https://github.com/user-attachments/assets/1954e59b-d55b-4aa2-aa82-b663d8583f1e" alt="Row Image Example" width="60%"></p>

If we draw it over the orthomosaic image we can see how the drone will move between the vineyard rows: 
<p align="center"> <img src="https://github.com/user-attachments/assets/616aae72-1c3f-4ccc-9100-931cccaf92f6" alt="Row Image Example" width="60%"></p>

The **drone_path_pixel.json** is saved too. The final **drone_path_gps.json** is saved in the format shown in the image. The movement between points would be linear. 



> [!TIP]
> The **DETECT VINEYARD ROWS** section of the code can be comented as the *rows_coordinates.json* is already generated and can be just read and avoid executing the row detection functions.  

-->
## Authors

* **Esther Vera** - *Noumena* - [Esther Vera](https://github.com/EstherNoumena)

## Acknowledgements
This project is funded by the European Union, grant ID 101060643.

<img src="https://rea.ec.europa.eu/sites/default/files/styles/oe_theme_medium_no_crop/public/2021-04/EN-Funded%20by%20the%20EU-POS.jpg" alt="https://cordis.europa.eu/project/id/101060643" width="200"/>
