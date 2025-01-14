""" Classes to manage the publication of velocities to move the drone in the simulation """

__author__ = "Esther Vera"
__copyright__ = "Copyright 2025, Noumena"
__credits__ = ["Esther Vera, Aldo Sollazzo"]
__version__ = "1.0.0"
__maintainer__ = "Esther Vera"
__email__ = "esther@noumena.io"
__status__ = "Production"
__license__ = "MIT"


import numpy as np 
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from anafi_ros_interfaces.msg import MoveByCommand, PilotingCommand, GimbalCommand 

qos_profile = QoSProfile(depth=10)  # QoS configuration

class DroneVelocityPublisher(Node):
    """
    Class for publishing drone velocity commands, including straight and parallel movement, 
    altitude adjustments and orientation adjustments.
    """
    def __init__(self) -> None: 
        """
        Initializes the DroneVelocityPublisher, setting up publishers for drone velocity and altitude commands.
        """
        super().__init__('drone_vel_publisher')

        # Publisher for drone movement commands
        self.publisher = self.create_publisher(
            PilotingCommand,
            '/anafi/drone/command',
            qos_profile
        )
        # Publisher for altitude movement commands
        self.publisher_altitude = self.create_publisher(
            MoveByCommand,
            '/anafi/drone/moveby',
            qos_profile
        )

        # Movement limits and speeds
        self.limits = [0.04,0.1,0.3,0.5]
        self.speed = 3.0
        self.speed_yaw = 9.0
        self.vel = PilotingCommand()
        self.vel_alt = MoveByCommand()
        self.prev_vel_alt = np.nan # Stores the previous altitude velocity to detect changes

        self.set_zero_speed()


    def set_zero_speed(self) -> None:
        """
        Sets the drone's linear and yaw velocities to zero.
        """
        self.vel.roll = 0.0
        self.vel.pitch = 0.0
        self.vel.gaz = 0.0
        self.vel.yaw = 0.0


    def set_zero_moveby_speed(self):
        """
        Sets the drone's altitude and yaw velocities to zero.
        """
        self.vel_alt.dx = 0.0
        self.vel_alt.dy = 0.0
        self.vel_alt.dz = 0.0
        self.vel_alt.dyaw = 0.0


    def set_straight_speed(self, dif: list) -> None:
        """
        Sets the pitch speed for straight-line movement based on the distance to the target.
        
        Args:
            dif (list): A list containing the differences [dx, dy, dz] between current and target positions.
        """
        dist = np.linalg.norm(dif[0:2])
        if(dist>self.limits[1]):
            self.vel.pitch = 0.1* dist
            if(dist < 1.5):
                self.vel.pitch = 0.2
            elif(dist < 10.0):
                self.vel.pitch = 0.5
            elif(dist >= 10.0):
                self.vel.pitch = 0.5

        elif(dist<-self.limits[1]):
            self.vel.pitch = -0.1* dist
            if(dist > -1.5):
                self.vel.pitch = -0.2
            elif(dist > -10.0):
                self.vel.pitch = -0.5
            elif(dist <= -10.0):
                self.vel.pitch = -0.5


    def set_parallel_speed(self, dif: list) -> None:
        """
        Sets the roll and pitch speeds for parallel movement based on the difference in coordinates.
        
        Args:
            dif (list): A list containing the differences [dx, dy, dz] between current and target positions.
        """
        dist = np.linalg.norm(dif[0:2])

        if(abs(dif[0]) < 0.15):
            if(dif[1] > self.limits[1]):
                self.vel.roll = -self.speed * dist
                if(self.vel.roll < -2.0):
                    self.vel.roll = -0.5
                if(dif[1] < 1.5): 
                    self.vel.roll = -0.2 
                if(dif[1] < 7.0):
                    self.vel.roll = -0.5  
                
            elif(dif[1] < -self.limits[1]):
                self.vel.roll = self.speed * dist
                if(self.vel.roll > 2.0):
                    self.vel.roll = 0.5
                if(dif[1] < 1.5):  
                    self.vel.roll = 0.2
                if(dif[1] < 7.0):
                    self.vel.roll = 0.5 
                
        if(dif[0] > self.limits[0]):
            self.vel.pitch = 0.5
            if(dif[0] < 0.15):
                self.vel.pitch = 0.06
            elif(dif[0] < 1.0):
                self.vel.pitch = 0.2

        elif(dif[0] < -self.limits[0]):
            self.vel.pitch = -0.5
            if(dif[0] > -0.15):
                self.vel.pitch = -0.06
            elif(dif[0] > -1.0):
                self.vel.pitch = -0.2


    def set_altitude_speed(self, dif: list) -> None:
        """
        Sets the vertical speed for altitude adjustments.
        
        Args:
            dif (list): A list containing the differences [dx, dy, dz] between current and target positions.
        """
        self.vel_alt.dx = 0.0
        self.vel_alt.dy = 0.0
        self.vel_alt.dz = -dif[2]
        self.vel_alt.dyaw = 0.0        


    def set_orientation_speed(self, turn_right: bool, dyaw: float) -> None:
        """
        Sets the yaw speed for orientation adjustments.
        
        Args:
            turn_right (bool): True if the drone should turn right, False for left.
            dyaw (float): The difference between current and target yaw.
        """
        if(abs(dyaw)>self.limits[3]):
            if(turn_right == True): # Turn right
                self.vel.yaw = -self.speed_yaw
                if(abs(dyaw)<8.0):
                    self.vel.yaw = -2.0
                elif(abs(dyaw)<25.0):
                    self.vel.yaw = -3.0
    
            else: # Turn left
                self.vel.yaw = self.speed_yaw
                if(abs(dyaw)<8.0):
                    self.vel.yaw = 2.0
                elif(abs(dyaw)<25.0):
                    self.vel.yaw = 3.0


    def custom_speed(self, vx: float, vy: float, vz: float, vyaw: float) -> None:
        """
        Sets custom speeds for roll, pitch, gaz and yaw.
        
        Args:
            vx (float): Roll speed.
            vy (float): Pitch speed.
            vz (float): Vertical speed.
            vyaw (float): Yaw speed.
        """
        self.vel.roll = vx
        self.vel.pitch = vy
        self.vel.gaz = vz
        self.vel.yaw = vyaw


    def publish(self)-> None:
        """
        Publishes the velocity commands to the appropriate ROS2 topics.
        """
        if(self.prev_vel_alt != 0.0 or self.vel_alt.dz!=0.0):  # Publish altitude velocity
            self.vel_alt.header.stamp = self.get_clock().now().to_msg() 
            self.vel_alt.header.frame_id = ''
            self.publisher_altitude.publish(self.vel_alt)
            self.prev_vel_alt = self.vel_alt.dz
            self.get_logger().info(f"HEIGHT SPEED: {self.vel_alt.dz}")

        elif(self.vel != None):  # Publish xy yaw velocity
            self.vel.header.stamp = self.get_clock().now().to_msg() 
            self.vel.header.frame_id = ''
            self.publisher.publish(self.vel)
            self.get_logger().info(f"VELOCITIES\n  - Roll: {self.vel.roll}\n  - Pitch: {self.vel.pitch}\n  - Gaz: {self.vel.gaz}\n  - Yaw: {self.vel.yaw}")
        
        else: 
            self.get_logger().warning(f'Velocity couldnt be published: {self.vel}\n')



class GimbalOrientationPublisher(Node):
    """
    Class for publishing gimbal orientation commands.
    """
    def __init__(self): 
        """
        Initializes the GimbalOrientationPublisher, setting up the gimbal command publisher.
        """
        super().__init__('gimbal_orientation_publisher')

        self.publisher_gimbal = self.create_publisher(
            GimbalCommand,
            '/anafi/gimbal/command',
            qos_profile
        )
        self.gimbal = GimbalCommand()
        

    def publish(self, gimbal_angle: float) -> None:
        """
        Publishes a command to set the gimbal's orientation.

        Args:
            gimbal_angle (float): The desired pitch angle for the gimbal in degrees.
        """    
        self.gimbal.header.stamp = self.get_clock().now().to_msg() 
        self.gimbal.header.frame_id = ''
        self.gimbal.pitch = gimbal_angle
        self.publisher_gimbal.publish(self.gimbal)
        self.get_logger().info(f"GIMBAL ORIENTATION: {self.gimbal.pitch}")

     