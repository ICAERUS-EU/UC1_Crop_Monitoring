<div align="center">
  <p>
    <a href="https://icaerus.eu" target="_blank">
      <img width="50%" src="https://icaerus.eu/wp-content/uploads/2022/09/ICAERUS-logo-white.svg"></a>
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

- **data:** here you should add the data folder that you could download from Zenodo in [UC1 GITHUB DATA FOLDER](https://zenodo.org/uploads/11127440).
- **top_view:** it has some top-view level calculations for vegetation analysis.
  - **calculate_vegetation_indexes**
  - **create_grid**
  - **extract_vineyard_data**
  - **top_level_detection**
- **models:** models developed for crop monitoring
- **platform.json:** organized information about the models

## Models

The [models](https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/blob/main/models/) developed are the following:
 

#### _[Row-view disease detection model with YOLOv8](https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/blob/main/models/01_plant_disease_detection_yolov8_v1/)_
This model has been trained with YOLOv8 and is able to detect the plants and provide information about its health status from a plant-view level. 

#### _[Plant locator from row-view to global-view](https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/blob/main/models/02_plant_locator_v1/)_
This algorithm contains the complete workflow from detecting a plant in a row-view image to locate this plant in the global-view orthomosaic to visualize its health status at a global scope. It also locates the drone positions.


## Authors

* **Esther Vera** - *Noumena* - [Esther Vera](https://github.com/EstherNoumena)

## Acknowledgements
This project is funded by the European Union, grant ID 101060643.

<img src="https://rea.ec.europa.eu/sites/default/files/styles/oe_theme_medium_no_crop/public/2021-04/EN-Funded%20by%20the%20EU-POS.jpg" alt="https://cordis.europa.eu/project/id/101060643" width="200"/>
