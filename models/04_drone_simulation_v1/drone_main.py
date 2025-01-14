""" Node class that completely handles the simulation of the drone in the vineyard model using ROS2 and Sphinx """

__author__ = "Esther Vera"
__copyright__ = "Copyright 2025, Noumena"
__credits__ = ["Esther Vera, Aldo Sollazzo"]
__version__ = "1.0.0"
__maintainer__ = "Esther Vera"
__email__ = "esther@noumena.io"
__status__ = "Production"
__license__ = "MIT"

# Import python libraries
import sys
import os
import cv2 
import yaml
import numpy as np

# Import ROS2 libraries
import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from std_msgs.msg import UInt8
from sensor_msgs.msg import NavSatFix, Image 
from geometry_msgs.msg import Vector3Stamped
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSDurabilityPolicy

# Import custom libraries
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from src.drone_publisher import DroneVelocityPublisher, GimbalOrientationPublisher
from src.drone_calculationsdrone_calculations import DroneCalculations

# ====================================================================================       

# To handle cv2 images
bridge = CvBridge()

# QOS definition to get topics information
qos_profile = QoSProfile(
    reliability=QoSReliabilityPolicy.BEST_EFFORT, 
    durability=QoSDurabilityPolicy.VOLATILE, 
    depth=10  
)

# Config file with coordinates to move the drone
with open("/home/noumena/ros2_ws/src/py_pubsub/coordinates.yaml", 'r') as file:
    coord_yaml = yaml.safe_load(file)

# ====================================================================================       

class DroneNode(Node):
    """
    A ROS2 Node class for managing drone operations including navigation, 
    sensor data processing and image capture.
    """
    def __init__(self) -> None:
        """
        Initializes the DroneNode instance and sets up publishers, 
        subscriptions, and internal variables.
        """
        super().__init__('drone_node')

        # Create classes 
        self.velocity = DroneVelocityPublisher()
        self.gimbal = GimbalOrientationPublisher()
        self.calc = DroneCalculations()
        self.gimbal.publish(20.0)

        # Generate subscriptions
        self.subscription_gps = self.create_subscription(
            NavSatFix,
            '/anafi/drone/gps/location',
            self.gps_callback,
            qos_profile)
        
        self.subscription_rpy = self.create_subscription(
            Vector3Stamped,
            '/anafi/drone/rpy_slow',
            self.orientation_callback,
            qos_profile)

        self.subscription_cam = self.create_subscription(
            Image,
            '/anafi/camera/image',
            self.camera_callback,
            qos_profile)
        
        self.subscription_bat = self.create_subscription(
            UInt8,
            '/anafi/battery/percentage',
            self.battery_callback,
            qos_profile)
        
        # Timer to call publish function
        self.timer = self.create_timer(0.1, self.velocity.publish)   # Timer that calls the publish function every 0.1s
        
        # Init internal variables
        self.id = 0
        self.photo_id = 0          # Number of images taken
        self.prev_first_digit = '0'
        self.parallel_movement = False  # Parallel movement: drone in vineyard row, not parallel movement: going to certain position
        
        self.yaw = np.nan        
        self.target_yaw = np.nan
        self.target_reached = 100  # Counter to wait between drone actions
        self.previous_xyz = None
        self.current_xyz = None

        # Load target GPS coordinates
        self.targets_gps = coord_yaml.get('targets_gps', [])
        lat, lon, alt, _ = self.targets_gps[self.id]
        self.target_xyz = self.calc.transform_coordinates(lat, lon, alt)

        self.names = ["pos_down1", "pos_up1", "pos_up2", "pos_down2", "pos_down3", "pos_up3", "home"]

    
    def gps_callback(self, msg: NavSatFix) -> None:
        """
        Handles incoming GPS data, calculates differences to target coordinates
        and determines movements for the drone.

        Args:
            - msg (NavSatFix): The GPS data received from the '/anafi/drone/gps/location' topic.
        """
        self.get_logger().info(f'GPS received: latitud={msg.latitude}, longitud={msg.longitude}, altitud={msg.altitude}')

        # Transform GPS coordinates to xyz coordinates
        self.current_xyz = self.calc.transform_coordinates(msg.latitude, msg.longitude, msg.altitude)
        
        # Calculate difference between current and target coordinates
        dif = [self.target_xyz[i] - self.current_xyz[i] for i in range(3)]            
        print(f"\nDifferences: \n  ΔX: {dif[0]} m \n  ΔY: {dif[1]} m \n  ΔZ: {dif[2]} m\n")

        # Set velocity to 0 by default
        self.velocity.set_zero_speed()
        self.velocity.set_zero_moveby_speed()
        
        # Counter to wait between drone movements
        if(self.target_reached >= 5): 

            # Correct altitude difference
            if(abs(dif[2])>0.6):
                print("\nPublishing altitude")
                self.velocity.set_altitude_speed(dif)

            # If drone yaw is known
            elif(not np.isnan(self.yaw)):
                # If position hasnt been reached yet
                if(abs(dif[0])>0.35 or abs(dif[1])>0.35):
                    if(not self.parallel_movement):
                        print("Straight movement")
                        self.velocity = self.calc.set_straight_movement(self.velocity, dif, self.yaw)
                        
                    else: 
                        print("Parallel movement")
                        self.velocity = self.calc.set_parallel_movement(self.velocity, dif, self.yaw)

                else: # If position reached, go to new target or end node
                    self.get_logger().info(f'DEFINING NEW TARGET, {self.names[self.id]}')
                    self.id = self.id + 1
                    self.target_reached = 0 

                    if(self.id < len(self.targets_gps)) :
                        lat, lon, alt, t = self.targets_gps[self.id]
                        self.target_xyz = self.calc.transform_coordinates(lat, lon, alt)
                        self.parallel_movement = self.calc.get_movement_type(t)
                    else: 
                        self.destroy_node()
                        rclpy.shutdown()
        else: 
            self.target_reached += 1

        self.velocity.publish()
        print("\n\n----------------------------------------------------------\n")


    def orientation_callback(self, msg: Vector3Stamped) -> None:
        """
        Handles incoming orientation data, updating the drone's current yaw.

        Args:
            - msg (Vector3Stamped): Orientation data received from the '/anafi/drone/rpy_slow' topic.
        """
        self.yaw = msg.vector.z

    
    def battery_callback(self, msg: UInt8) -> None:
        """
        Manages "come home" action based on battery level.

        Args:
            - msg (UInt8): The battery level received from the '/anafi/battery/percentage' topic.
        """
        battery_level = int(msg.data)  

        # Print battery level when last digit is 0 
        if(str(battery_level)[-1] == '0' and self.prev_first_digit != str(battery_level)[0]):
            self.get_logger().info(f'Battery level: {battery_level}%')
            self.prev_first_digit = str(battery_level)[0]

        # Return home if battery level <= 25
        if battery_level <= 25:
            self.id = len(self.targets_gps) - 1
            lat, lon, alt, _ = self.targets_gps[self.id]
            self.target_xyz = self.calc.transform_coordinates(lat, lon, alt)
            self.parallel_movement = False
            self.target_reached = 100 
            self.get_logger().info(f'Battery level: {battery_level}%')
            self.get_logger().warn("¡Low battery! Returning home")


    def camera_callback(self, msg: Image) -> None:
        """
        Handles incoming camera data and processes images when drone is moving in a vineyard row (parallel movement).

        Args:
        - msg (Image): The camera image data received from the '/anafi/camera/image' topic.
        """
        # Only uses the camera when path is parallel to the vineyards
        if(self.parallel_movement==True and (self.yaw < -160 or self.yaw > 160) and self.current_xyz[-1]<2.2):
            if(self.previous_xyz != None and self.current_xyz != None):
                self.distance_travel = np.linalg.norm(np.array(self.current_xyz[0:2]) - np.array(self.previous_xyz[0:2]))
                if(self.distance_travel >= 1.0):
                    cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')  # Adjust encoding as necessary
                    cv2.imshow("data", cv_image)
                    cv2.waitKey(600)
                    cv2.destroyAllWindows()
                    cv2.imwrite(f"/home/noumena/Documents/images_drone/frame_{self.photo_id}.jpg", cv_image)
                    self.photo_id += 1
                    self.previous_xyz = self.current_xyz
                    self.get_logger().info(f'Photo taken: frame_{self.photo_id}.jpg')
            elif(self.previous_xyz == None and self.current_xyz != None):
                self.previous_xyz = self.current_xyz

# ====================================================================================       

def main() -> None:
    """
    Main entry point of the script. Initializes the ROS2 node, spins the event loop, 
    and shuts down the node upon termination.
    """
    rclpy.init()
    drone_node = DroneNode()
    rclpy.spin(drone_node)
    drone_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()