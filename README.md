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

![Downloads](https://img.shields.io/github/downloads/icaerus-eu/icaerus-repo-template/total) ![Contributors](https://img.shields.io/github/contributors/icaerus-eu/icaerus-repo-template?color=dark-green) ![Forks](https://img.shields.io/github/forks/icaerus-eu/icaerus-repo-template?style=social) ![Stargazers](https://img.shields.io/github/stars/icaerus-eu/icaerus-repo-template?style=social) ![Issues](https://img.shields.io/github/issues/icaerus-eu/icaerus-repo-template) ![License](https://img.shields.io/github/license/icaerus-eu/icaerus-repo-template) 

## Table Of Contents

* [Summary](#summary)
* [Structure](#structure)
* [Models](#models)
* [Authors](#authors)
* [Acknowledgements](#acknowledgements)

## Summary
In this repository you can find some models and calculation tools for crop monitoring tasks in order to predict the healthiness of vineyards with images taken with drones. 

## Structure
The repository folders are structured as follow: 

- data
- row_view
- top_view
- Models
- platform.json

## Models

The models have been divided depending on the detection level approached. Here you can find some examples of the outcome for each model and its specifications. 
 


#### _[Row-view disease detection model with YOLOv8](https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/tree/main/Vineyard_dataset_project/models/best.pt)_

<p align="center">
  <img src="https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/assets/148956768/04434b88-4913-4eb2-9af2-a2b67ff70cd9" width="400" height="400">
</p>

- **Description:** Row-view disease detection model with YOLOv8
- **Specs:**
    - **Input:** Images size (800,800,3)
    - **Output:** Labels [0 = diseased, 1 = healthy]
    - **Method:** YOLOv8
    - **Type:** Detection and classification
  - **Date:** 22/12/2023






## Authors

* **Esther Vera** - *Noumena* - [Esther Vera](https://github.com/EstherNoumena)

## Acknowledgements
This project is funded by the European Union, grant ID 101060643.

<img src="https://rea.ec.europa.eu/sites/default/files/styles/oe_theme_medium_no_crop/public/2021-04/EN-Funded%20by%20the%20EU-POS.jpg" alt="https://cordis.europa.eu/project/id/101060643" width="200"/>
