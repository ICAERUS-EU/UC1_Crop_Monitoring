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
- **Data**: Download the [whole_vineyard.fbx](https://github.com/ICAERUS-EU/UC1_Crop_Monitoring/blob/main/data/drone_sim_model/whole_vineyard.fbx) model from this repository and change the **config.yaml** model path to your specific route. 

## ⚙️ Parameters

The parameters are defined directly in the code. 

- **Data paths**: define the data path to **coordinates.yaml** inside **drone_main.py**.
- **Variables**: variables are defined inside the code and you should be modified carefully. 


## 🚀 Usage

To start the parrot drone simulation follow the next steps: 

- Install ROS2. In this case, ROS2 Humble is been used. 
- Install Sphinx following the webpage [documentation](https://developer.parrot.com/docs/sphinx/installation.html). 
- To start the simulation:
   - In one CMD write:  
   ```
   sudo systemctl start firmwared.service
   ```
   - Add your password and run: 
   ```
   sudo systemctl start firmwared.service
   ```
   - Open another CMD and write:
   ```
   sphinx "/opt/parrot-sphinx/usr/share/sphinx/drones/anafi.drone"::firmware="https://firmware.parrot.com/Versions/anafi/pc/%23latest/images/anafi- pc.ext2.zip"
   ```
   - To define the environment you should open a new CMD and run the next command. This defines the route to config.yaml that will load the vineyards model and also specifies the gps coordinates where the simulation will take place.. 
   ```
   parrot-ue4-empty -config-file=Documents/config.yaml -gps-json='{"lat_deg":41.288745, "lng_deg":1.712019, "elevation":0.0}'
   ```
   <details>
   <summary>NOTE</summary>
   This command loads everything, to test without the model and coordinates just use: <code>parrot-ue4-empty</code>
   </details>

Once the simulation is running you should see an image like this: 

<p align="center">
  <img src="https://github.com/user-attachments/assets/d9316da3-45ca-471a-b186-3cf4043e32e2" style="width: 75%; height: auto;">
</p>

Let's take off the drone but first we need to establish the connection with ROS2: 

- Open a new CMD and add the next command to enter into your ros workspace (change name to yours), source the ros2 environment and launch the nodes communication with the Anafi drone: 
   ```
   cd ros2_ws/
   ```
   ```
   source install/setup.bash
   ```
   ```
   ros2 launch anafi_ros_nodes anafi_launch.py ip:='10.202.0.1' model:='4k'
   ```
- If everthing works smooth, you should be able to perform take off and move the drone. In a new CMD run:
   ```
   cd ros2_ws/
   ```
   ```
   source install/setup.bash
   ```
   ```
   source /opt/ros/humble/setup.bash 
   ```
   ```
   ros2 service call /anafi/drone/takeoff std_srvs/srv/Trigger {}\ 
   ```
- If you want to land the drone just call the service:
   ```
   ros2 service call /anafi/drone/land std_srvs/srv/Trigger {}\ 
   ```   
To this point there is another clarification to be made. ROS2 works with packages that contains the code that define the nodes. In the case of this simulation, it was reutilize the **py_pubsub** (example package) from ROS2 and the code and files where substituted per **drone_main.py** and the ones in **src** folder. You can create your own package or reutilized one from ROS2. Once the code is correctly located in and referenced:

- Open a terminal and run the next command to update the workspace with the new codes: 
   ```
   cd ros2_ws/
   ```
   ```
   source install/setup.bash
   ```
   ```
   source /opt/ros/humble/setup.bash 
   ```
   ```
   colcon build
   ```
- After the drone take off, run the **drone_main.py** code to make the drone move between the defined GPS coordinates (changing the package name accordingly):
   ```
   ros2 run py_pubsub drone_main
   ```    

Then the drone will start moving towards the GPS coordinates defined in order. It will perform two types of movements: 

- **Straight movement**: a direct movement from the actual position to the next one where the drone faces the GPS final position that it is directing.
- **Parallel movement**: a parallel movement to capture photos from the vineyard plants. In this case, the drone moves parallel to the vineyard row and the next GPS coordinates. Its mark with a 1 in the last parameter after each set of coordinates in **coordinates.yaml**. During this movement, the drone will take photos after a certain distance.

 
### Drone suscriptions

| **Component**           | **Topic**                        | **Description**                           |
|-------------------------|----------------------------------|-------------------------------------------|
| GPS location           | `/anafi/drone/gps/location`       | GPS location of the drone                 |
| Orientation            | `/anafi/drone/rpy_slow`           | To extract the yaw of the drone           |
| Camera                 | `/anafi/camera/image`             | To get the captured images by the camera  |
| Battery level          | `/anafi/battery/percentage`       | Battery level of the drone                |


  
### Drone publishers

| **Component**           | **Topic**                        | **Description**                             |
|-------------------------|----------------------------------|---------------------------------------------|
| Angular velocity        | `/anafi/drone/gps/location`      | To specify the pitch, roll and yaw velocity |
| Altitude velocity       | `/anafi/drone/rpy_slow`          | To move the drone up and down               |
| Gimbal orientation      | `/anafi/camera/image`            | To adjust the gimbal orientation            |




## 📊 Results

During the flight of the drone you could appreaciate the next environment:  

<p align="center">
  <img src="https://github.com/user-attachments/assets/dc4cdf4b-6fd8-4c92-9c87-0053435706af" style="width: 75%; height: auto;">
</p>



<details>
<summary>SPHINX SPECIFICATIONS</summary>
Sphinx is very useful if you have an Anafi drone and want to customize the programming. 
The Sphinx simulation has limitations of space, speed, publishing an reaction time. 
</details>

> [!TIP]
> [Setting GPS coordinates in Sphinx](https://developer.parrot.com/docs/sphinx/launcher_api.html)
> 
> [Customize 3D models in Sphinx](https://developer.parrot.com/docs/sphinx/customize_the_environment.html)
> 
> [3D scenes available in Sphinx](https://developer.parrot.com/docs/sphinx/available_worlds.html)


## Authors

* **Esther Vera** - *Noumena* - [Esther Vera](https://github.com/EstherNoumena)

## Acknowledgements
This project is funded by the European Union, grant ID 101060643.

<img src="https://rea.ec.europa.eu/sites/default/files/styles/oe_theme_medium_no_crop/public/2021-04/EN-Funded%20by%20the%20EU-POS.jpg" alt="https://cordis.europa.eu/project/id/101060643" width="200"/>
