# 02 - PLANT LOCATOR FROM ROW-VIEW TO GLOBAL-VIEW -> GRID

- **Description:** This algorithm contains the complete workflow from detecting a plant in an image to locate this plant in the global-view orthomosaic following a predefined grid to visualize its health status. It locates also the drone position.

    *Please download the [Yolov8 model](https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/blob/main/models/01_plant_disease_detection_yolov8_v1/best.pt) to perform the plant detection and be able to execute the code*
- **Dataset:** [UC1 GITHUB DATA FOLDER](https://zenodo.org/records/11195994)
- **Input:** Image size (800,800,3)
- **Output:** Global orthomosaic with plant location, health status and drone location following a grid layout
- **Method:** Algorithmic approach
- **Type:** Detection, classification, global localization 
- **Date:** 09/04/2024


In this image is shown the detection of a plant that will be marked in the global-view. The drone location of this visualization is extracted and transformed to the orthomosaic view. 

<p align="center">
  <img src="https://github.com/user-attachments/assets/5d6a953b-b82b-4b3d-8b7b-e5b7ec3c204d" width=700 height=396>
</p>


After processing all the row images, it is obtained the global visualization of the vineyards where the drones' positions are marked as blue triangles, and the health status of the plants are shown as green rectangles (healthy) or red rectangles (unhealthy): 

<p align="center">
  <img src="https://github.com/user-attachments/assets/651b875e-fac6-4b35-9c35-cf24758487a3" width=769 height=590>
</p>




## Authors

* **Esther Vera** - *Noumena* - [Esther Vera](https://github.com/EstherNoumena)

## Acknowledgements
This project is funded by the European Union, grant ID 101060643.

<img src="https://rea.ec.europa.eu/sites/default/files/styles/oe_theme_medium_no_crop/public/2021-04/EN-Funded%20by%20the%20EU-POS.jpg" alt="https://cordis.europa.eu/project/id/101060643" width="200"/>
