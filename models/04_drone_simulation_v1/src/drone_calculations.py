""" Class to handle the calculations to transform coordinates and move the drone """

__author__ = "Esther Vera"
__copyright__ = "Copyright 2025, Noumena"
__credits__ = ["Esther Vera, Aldo Sollazzo"]
__version__ = "1.0.0"
__maintainer__ = "Esther Vera"
__email__ = "esther@noumena.io"
__status__ = "Production"
__license__ = "MIT"


# Import python libraries
import numpy as np
from pyproj import Transformer


class DroneCalculations():
    """
    Class that handles all the calculations related to drone movements,
    including transforming GPS coordinates and calculating yaw adjustments.
    """
    def __init__(self) -> None:
        """
        Initializes the transformer for converting between different coordinate systems.
        Uses EPSG:4979 for geographic coordinates (lat, lon, alt) and EPSG:4978 for ECEF coordinates.
        """
        # Transformer for coordinates
        self.transformer = Transformer.from_crs("EPSG:4979", "EPSG:4978", always_xy=True)

    
    def transform_coordinates(self, lat: float, lon: float, alt: float) -> list:
        """
        Transforms geographic coordinates (latitude, longitude, altitude) to ECEF (Earth-Centered, Earth-Fixed) coordinates.
        
        Args:
            lat (float): Latitude in degrees.
            lon (float): Longitude in degrees.
            alt (float): Altitude in meters.
        
        Returns:
            list: Transformed coordinates as [x, y, z] in ECEF system.
        """
        xyz_coords = list(self.transformer.transform(lon, lat, alt))
        xyz_coords[2] = alt
        return xyz_coords


    def calculate_target_yaw(self, dif: list) -> float:
        """
        Calculates the yaw (heading) angle required to move towards a target from a given position.
        
        Args:
            dif (list): Difference in coordinates [dx, dy], where dx is the difference in X and dy is the difference in Y.
        
        Returns:
            float: The calculated yaw in degrees.
        """
        # Calculate yaw based on the differences in the X and Y coordinates
        target_yaw = np.rad2deg(np.arctan2(dif[1],dif[0]))

        # Adjust the yaw based on the quadrant the target is in
        if(dif[1]>0.0 and dif[0]>0.0):
            target_yaw = -180 + target_yaw
        elif(dif[1]<0.0 and dif[0]<0.0):
            target_yaw = 180 + target_yaw # target_yaw is negative
        elif(dif[1]<0.0 and dif[0]>0.0):
            target_yaw = 180 + target_yaw # target_yaw is negative
        elif(dif[1]>0.0 and dif[0]<0.0):
            target_yaw = -180 + target_yaw

        # Handle edge cases for specific yaw angles
        elif(dif[1]==0.0 and dif[0]>0.0):
            target_yaw = -90
        elif(dif[1]==0.0 and dif[0]<0.0):
            target_yaw = 90       
        elif(dif[1]>0.0 and dif[0]==0.0):
            target_yaw = 180        
        elif(dif[1]<0.0 and dif[0]==0.0):
            target_yaw = 0
        else: # When both differences are zero
            target_yaw = self.yaw   

        return target_yaw 
    

    def define_orientation_turn(self, target_yaw: float, yaw: float) -> tuple:
        """
        Determines whether to turn left or right to achieve the target yaw.
        
        Args:
            target_yaw (float): The target yaw (heading) angle.
            yaw (float): The current yaw (heading) angle of the drone.
        
        Returns:
            tuple:
                - turn_right (bool): True if the drone should turn right, False if it should turn left.
                - dyaw (float): The amount of yaw adjustment required.
        """
        # Default to turning left
        turn_right = False 
        
        # Determines whether to turn right or left based on the yaw values
        if((yaw>=0.0 and target_yaw>=0.0)
           or (yaw<0.0 and target_yaw<0.0)):
                dyaw = abs(target_yaw) - abs(yaw)
                if(yaw >= target_yaw):   # Turns right
                    turn_right = True

        elif(yaw>=0.0 and target_yaw<0.0):
            dyaw1 = abs(target_yaw) + yaw
            dyaw2 = 180 + target_yaw + 180 - yaw
            if(dyaw1<=dyaw2): # Turns right
                dyaw = abs(dyaw1)
                turn_right = True
            else:             # Turns left
                dyaw = abs(dyaw2)

        else:  # When yaw is negative and target_yaw is positive
            dyaw1 = abs(yaw) + target_yaw
            dyaw2 = 180 + yaw + 180 - target_yaw
            if(dyaw1>=dyaw2):  # Turns right
                dyaw = abs(dyaw2)
                turn_right = True
            else:              # Turns left
                dyaw = abs(dyaw1)
                
        return turn_right, dyaw 
    

    def set_straight_movement(self, vel_class, dif: list, yaw: float) -> object:
        """
        Sets the movement speed and orientation for straight movement towards a target position.
        
        Args:
            vel_class (object): The velocity control class.
            dif (list): The difference in coordinates [dx, dy, dz].
            yaw (float): The current yaw (heading) of the drone.
        
        Returns:
            object: The updated velocity class with movement instructions.
        """
        target_yaw = self.calculate_target_yaw(dif)   
        turn, dyaw = self.define_orientation_turn(target_yaw, yaw)
        vel_class.set_orientation_speed(turn, dyaw)
        print("Publishing orientation")
        print("YAW: ", yaw, " TARGET YAW: ", target_yaw, " DYAW", dyaw)

        # Set straight movement speed if the yaw adjustment is small enough
        if(abs(dyaw) < 1.5):
            print("Publishing xy-yaw velocity\n")
            vel_class.set_straight_speed(dif)

        return vel_class


    def set_parallel_movement(self, vel_class, dif: list, yaw: float) -> object:
        """
        Sets the movement speed and orientation for parallel movement (e.g., moving along a vineyard row).
        
        Args:
            vel_class (object): The velocity control class.
            dif (list): The difference in coordinates [dx, dy, dz].
            yaw (float): The current yaw (heading) of the drone.
        
        Returns:
            object: The updated velocity class with movement instructions.
        """
        target_yaw = 180  # Target yaw for parallel movement
        turn, dyaw = self.define_orientation_turn(target_yaw, yaw)
        vel_class.set_orientation_speed(turn, dyaw)
        print("Publishing orientation")
        print("YAW: ", yaw, " TARGET YAW: ", target_yaw, " DYAW", dyaw)

        # Set the parallel movement speed if the yaw adjustment is small enough
        if(abs(dyaw) < 1.5):
            print("Publishing xy-yaw velocity\n")
            vel_class.set_parallel_speed(dif)

        return vel_class
    

    def get_movement_type(self, t: int) -> bool:
        """
        Determines the type of movement based on an input parameter.
        
        Args:
            t (int): The type of movement (0 for non-parallel, non-zero for parallel).
        
        Returns:
            bool: True for parallel movement, False for non-parallel movement.
        """
        if t==0:
            return False
        else: 
            return True
