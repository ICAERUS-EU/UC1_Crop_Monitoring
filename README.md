<div align="center">
  <p>
    <a href="https://icaerus.eu" target="_blank">
      <img width="50%" src="https://raw.githubusercontent.com/ICAERUS-EU/.github/refs/heads/main/profile/ICAERUS_transparent.png"></a>
    <h3 align="center">UC1: Crop Monitoring📷</h3>
    
   <p align="center">
    This repository contains Crop Monitoring models developed with drone images and computer vision 
    <br/>
    <br/>
    <br/>
    <br/>
    <a href="https://github.com/icaerus-eu/icaerus-repo-template/issues">Report Bug</a>
    -
    <a href="https://github.com/icaerus-eu/icaerus-repo-template/issues">Request Feature</a>
  </p>
</p>
</div>

![Downloads](https://img.shields.io/github/downloads/icaerus-eu/UC1_Crop_Monitoring/total) ![Contributors](https://img.shields.io/github/contributors/icaerus-eu/UC1_Crop_Monitoring?color=dark-green) ![Forks](https://img.shields.io/github/forks/icaerus-eu/UC1_Crop_Monitoring?style=social) ![Stargazers](https://img.shields.io/github/stars/icaerus-eu/UC1_Crop_Monitoring?style=social) ![Issues](https://img.shields.io/github/issues/icaerus-eu/UC1_Crop_Monitoring) ![License](https://img.shields.io/github/license/icaerus-eu/UC1_Crop_Monitoring) 

## Table Of Contents

* [Summary](#summary)
* [Structure](#structure)
* [Models](#models)
* [Authors](#authors)
* [Acknowledgements](#acknowledgements)

## Summary
Within this repository, you'll discover various models and computational tools designed for crop monitoring purposes. These resources can be used for predicting the health status of vineyards using images captured by drones.

## Structure
The repository folders are structured as follow: 

- **data:** here you should add the [UC1 GITHUB DATA FOLDER](https://zenodo.org/records/11195994) that you could download from Zenodo.
- **top_view:** it has some top-view level calculations for vegetation analysis.
  - **create_grid**: detects rows and parcels and define a grid
  - **create_grid_aligned**: detects rows and parcels and define a grid after aligned the orthomosaic vineyard image
  - **calculate_vegetation_indexes**: calculates different vegetation indexes of the orthomosaic vineyard image
  - **NDVI_per_parcels**: calculates the NDVI in each parcel
- **models:** models developed for crop monitoring
- **platform.json:** organized information about the models

## Models

The [models](https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/blob/main/models/) developed are the following:
 

#### _[Row-view disease detection model with YOLOv8](https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/blob/main/models/01_plant_disease_detection_yolov8_v1/)_
This model has been trained with YOLOv8 and is able to detect the plants and provide information about its health status from a plant-view level. 

#### _[Plant locator from row-view to global-view](https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/blob/main/models/02_plant_locator_v1/)_
This algorithm contains the complete workflow from detecting a plant in a row-view image to locate this plant in the global-view orthomosaic to visualize its health status at a global scope. It also locates the drone positions.

#### _[Plant locator from row-view to global-view -> grid](https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/blob/main/models/02_plant_locator_v2/)_
This algorithm contains the complete workflow from detecting a plant in a row-view image to locate this plant in the global-view orthomosaic in a grid based visualization to observe its health status at a global scope. It also locates the drone positions.

#### _[Plant leaves analysis](https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/blob/main/models/03_plant_leaves_analysis_v1)_
This code approaches some methods for performing analysis and detect early disease development in vineyard leaves using color detection, VARI index and clustering algorithms.

#### _[Drone simulation with ROS2 and Sphinx in a vineyard model](https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/tree/main/models/04_drone_simulation_v1)_
This code is designed to simulate the Anafi Parrot drone using ROS2 and Sphinx, enabling the drone's movement within a vineyard model and automating the capture of images.

#### _[Plant disease detection model with YOLO12 - 3 classes](https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/tree/main/models/05_plant_disease_detection_yolov12_3classes_v1)_
This repository includes the code used to train a YOLOv12 model and the resulting trained model for detecting diseased vine leaves. It classifies leaves into three categories: healthy, mildew, and low iron.

#### _[Plant disease detection model with YOLO12 - 4 classes](https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/tree/main/models/06_plant_disease_detection_yolov12_4classes_v1)_
This repository includes the code used to train a YOLOv12 model and the resulting trained model for detecting diseased vine leaves. It classifies leaves into three categories: healthy, risk, mildew, and low iron.

#### _[Path generator for drone between rows](https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/tree/main/models/07_path_generator_between_rows_v1)_
This algorithm generates a GPS-based path between vineyard rows for low-altitude drone flights. The output is a file that contains the with coordinates optimized for the flying drone to cover the whole vineyard.


## Authors

* **Esther Vera** - *Noumena* - [Esther Vera](https://github.com/EstherNoumena)

## Acknowledgements
This project is funded by the European Union, grant ID 101060643.

<img src="https://rea.ec.europa.eu/sites/default/files/styles/oe_theme_medium_no_crop/public/2021-04/EN-Funded%20by%20the%20EU-POS.jpg" alt="https://cordis.europa.eu/project/id/101060643" width="200"/>
