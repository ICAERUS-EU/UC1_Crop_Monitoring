# 02 - PLANT LOCATOR FROM ROW-VIEW TO GLOBAL-VIEW -> GRID

## 🌿 Overview

 This respository contains the complete workflow from detecting a plant in an image and locate this plant in the global-view orthomosaic following a predefined grid to visualize its health status. Besides, it also locates the drone positions from where the images where captured and the plant was analyzed. 

 ## 🗂️ Structure

- **src:** 
  - **Calculation.py**: class to calculate drone positions. 
  - **Display.py**: class to show row and global images with analysis. 
  - **GridPlantLocator.py**: class to detect the middle plants of a rowview image and locate them in a global visualization. 
  - **LinesIntersection.py**: class that calculates the intersection between the drone position and the parcels in a row. 
  - **Output.py**: class to organize the data generated and export it. 
  - **read.py**: functions to read the data before the processing. 
- **README.md**: explanation of the model and usage. 
- **locate_plants_grid.py**: main code to execute. 
- **requirements.txt**: file to easily install the libraries. 


## 📄 Dataset 
The dataset needed to execute this model should be download from [UC1 GITHUB DATA FOLDER](https://zenodo.org/records/11195994) and copy the content to the data folder present in this repository. This UC1 GITHUB DATA FOLDER contains images and data that has been generated with the codes available in the section _top_view_. 

No specific data preparation is needed. 


## 💻 Requirements

- **Environment configuration**: please install the _requirements.txt_ file into a conda environment to install the necessary libraries to execute the code. 
- **Model**: download the [Yolov8 model](https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/blob/main/models/01_plant_disease_detection_yolov8_v1/best.pt) to perform the plant detection and be able to execute the code and adjust the model path. 
- **Data**: download and add the dataset [UC1 GITHUB DATA FOLDER](https://zenodo.org/records/11195994) to the data folder. 


## ⚙️ Parameters

The parameters are defined directly in the code. 

- **Data paths**: usually the data paths point directly to the data folder. You can check and adjusts these paths in the _locate_plants_grid.py_ file.
- **Variables**: the constant variables are defined inside the init function of the classes in the _src_.


## 🚀 Usage

For using the model, just type the following command in the _02_plant_locator_v2_ directory with the environment active: 

```
python locate_plants_grid.py
```

The row images, such as the one shown on the left, are analyzed using the YOLOv8 model to detect the plant health. The results from this analysis are then mapped onto the orthomosaic view of the vineyards, as illustrated in the image on the right. This process allows for a comprehensive visualization of the detection outcomes across the entire vineyard.

<p align="center"> <img src="https://github.com/user-attachments/assets/8e5708b6-ee3b-4aff-a0b0-a78a25ccc337" alt="Row Image Example" width="45%"> <img src="https://github.com/user-attachments/assets/9792253b-f08f-40bb-99c9-055095e4af18" alt="Orthomosaic Image Example" width="45%"> </p>


## 📊 Results
As a result, the orthomosaic image of the vineyards will show the plant locations, their health status and the drone's positions. The plant locations follow a grid layout, meaning that the positions of the plants are predetermined to this grid structure. The grid was generated using the [create_grid](https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/tree/main/top_view/create_grid) code. The drone’s position is determined through GPS data embedded in the images captured during flight. These coordinates can be mapped onto the orthomosaic view, as each pixel in the orthomosaic contains location-specific information.ains this information. 

After processing all the row images, it is obtained the global visualization of the vineyards where the drones' positions are marked as blue triangles and the health status of the plants are shown as green rectangles (healthy) or red rectangles (unhealthy): 

<p align="center">
  <img src="https://github.com/user-attachments/assets/651b875e-fac6-4b35-9c35-cf24758487a3" width=769 height=590>
</p>

Upon zooming in on the output, the positions of the drones and the grid which marks the locations become clearly visible. The grid cells without color indicate areas where no drone captures were recorded close enough to those positions.

<p align="center">
  <img src="https://github.com/user-attachments/assets/5d6a953b-b82b-4b3d-8b7b-e5b7ec3c204d" width=700 height=396>
</p>


## Authors

* **Esther Vera** - *Noumena* - [Esther Vera](https://github.com/EstherNoumena)

## Acknowledgements
This project is funded by the European Union, grant ID 101060643.

<img src="https://rea.ec.europa.eu/sites/default/files/styles/oe_theme_medium_no_crop/public/2021-04/EN-Funded%20by%20the%20EU-POS.jpg" alt="https://cordis.europa.eu/project/id/101060643" width="200"/>
