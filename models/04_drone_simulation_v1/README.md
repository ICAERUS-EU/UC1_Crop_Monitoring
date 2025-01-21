# 04 - DRONE SIMULATION WITH ROS2 AND SPHINX IN A VINEYARD MODEL

## 🌿 Overview

 This repository contains the code for navigating with the Anafi Parrot drone in the Sphinx simulation with ROS2 over a vineyard model. The workflow includes several key features: transforming GPS coordinates for precise movement, adjusting the drone's velocities and gimbal, capturing plant images at specific intervals, orienting the drone based on the type of movement and providing battery status alerts.


 ## 🗂️ Structure

- **src:** 
  - **drone_calculations.py**: class to calculate drone target locations, transform coordinates and set movements. 
  - **drone_publisher.py**: class to publish velocities and orientations of the drone and the gimbal. 
- **README.md**: explanation of the repository and usage. 
- **drone_main.py**: main code to execute. It handles the suscriptions to GPS information, the yaw orientation of the drone, the camera and the battery level. It decides the type of movement of the drone and the calls to publish velocities. 
- **requirements.txt**: file to easily install the libraries. 
- **coordinates.yaml**: it contains the coordinates in GPS that define the drone path. 
- **config.yaml**: it contains the path to the vineyard model to load it in the simulation. 


## 📄 Dataset 

The data needed is in the [drone_sim_folder](https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/tree/main/data/drone_sim_model) inside the data folder of this repository. It contains the model _whole_vineyard.fbx_ that is used for the simulation. 


## 💻 Requirements

- **Environment configuration**: There is no specific environment needed, the libraries should be installed inside ros2. 
- **Data**: Download the [whole_vineyard.fbx](https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/blob/main/data/drone_sim_model/whole_vineyard.fbx) model from this repository and change the _config.yaml_ model path to your specific route. 

## ⚙️ Parameters

The parameters are defined directly in the code. 

- **Data paths**: 
- **Variables**: 


## 🚀 Usage

For using the model,

```

```



## 📊 Results

<p align="center">
  <img src="" width=769 height=590>
</p>




## Authors

* **Esther Vera** - *Noumena* - [Esther Vera](https://github.com/EstherNoumena)

## Acknowledgements
This project is funded by the European Union, grant ID 101060643.

<img src="https://rea.ec.europa.eu/sites/default/files/styles/oe_theme_medium_no_crop/public/2021-04/EN-Funded%20by%20the%20EU-POS.jpg" alt="https://cordis.europa.eu/project/id/101060643" width="200"/>
