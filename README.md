<div align="center">
  <p>
    <a href="https://icaerus.eu" target="_blank">
      <img width="50%" src="https://icaerus.eu/wp-content/uploads/2022/09/ICAERUS-logo-white.svg"></a>
    <h3 align="center">UC1: Crop Monitoring📷</h3>
    
   <p align="center">
    Some text....
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
* [Models](#models)
* [Authors](#authors)
* [Acknowledgements](#acknowledgements)

## Summary


## Models

The models developed for crop monitoring are splitted in three groups depending on the detection level approached.

### Top-View Level


 


### Row-View Level
#### _[Row-view disease detection model with RF](https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/tree/main/Vineyard_dataset_project/VIEW_ROW/row_view_detection)_

<p align="center">
  <img src="https://github.com/EstherNoumena/UC1_Crop_Monitoring/assets/148956768/4d0014d9-d34b-4fdb-86dd-6d3a86e71a07">
</p>

-**Description:** Row-view disease detection model with RF
- **Accuracy:** 0.81
- **Dataset used:** []()
- **Specs:**
  - **Input:** Images size (617,106,3)
  - **Output:** Labels [0 = normal,1 = diseased]
  - **Method:** RF
  - **Type:** Classification
- **Date:** 25/10/2023


#### _[Row-view disease detection model with YOLOv8](https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/tree/main/Vineyard_dataset_project/models/best.pt)_

<p align="center">
  <img src="https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/assets/148956768/04434b88-4913-4eb2-9af2-a2b67ff70cd9" width="500" height="500">
</p>

- **Description:** Row-view disease detection model with YOLOv8
- **Accuracy:**
- **Dataset used:** []()
- **Specs:**
    - **Input:** Images size (800,800,3)
    - **Output:** Labels [0 = diseased, 1 = healthy]
    - **Method:** YOLOv8
    - **Type:** Detection and classification
  - **Date:** 22/12/2023



### Plant-View Level


 





## Authors

* **Esther Vera** - *Noumena* - [Esther Vera](https://github.com/EstherNoumena)

## Acknowledgements
This project is funded by the European Union, grant ID 101060643.

<img src="https://rea.ec.europa.eu/sites/default/files/styles/oe_theme_medium_no_crop/public/2021-04/EN-Funded%20by%20the%20EU-POS.jpg" alt="https://cordis.europa.eu/project/id/101060643" width="200"/>
