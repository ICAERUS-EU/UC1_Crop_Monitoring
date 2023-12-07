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
For the row-view level detection, the images used are similar to the one shown below.
<p align="center">
  <img src="https://github.com/EstherNoumena/UC1_Crop_Monitoring/assets/148956768/4d0014d9-d34b-4fdb-86dd-6d3a86e71a07">
</p>
The objetive of these models is to detect if the plant row image is diseased in general or healthy. <br><br>

- _Row-view disease detection model with RF_
    - **Description:** Random forest model to detect diseased row plants
    - **Accuracy**: 0.81
    - **Dataset used:** ""
    - **Specs:**
      - **Input:** Images size (617,106,3)
      - **Output:** Labels [0 = healthy, 1 = diseased]
      - **Method:** Random Forests
      - **Type:** Classification
    - **Date:** 25/10/2023
    - **Author:** [Esther Vera](https://github.com/EstherNoumena) <br><br>

- _Row-view disease detection model with NN_



### Plant-View Level







## Authors

* **Esther Vera** - *Noumena* - [Esther Vera](https://github.com/EstherNoumena)

## Acknowledgements
This project is funded by the European Union, grant ID 101060643.

<img src="https://rea.ec.europa.eu/sites/default/files/styles/oe_theme_medium_no_crop/public/2021-04/EN-Funded%20by%20the%20EU-POS.jpg" alt="https://cordis.europa.eu/project/id/101060643" width="200"/>
