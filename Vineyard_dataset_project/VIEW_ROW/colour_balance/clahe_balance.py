import cv2
import numpy as np




def white_balance_with_marker(image_path, marker_coords):
    # Read the image
    img = cv2.imread(image_path)

    # Convert the image from BGR to LAB color space
    lab_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    # Extract the L channel (luminance)
    l_channel = lab_img[:, :, 0]

    # Calculate the average luminance of the marker region
    marker_avg_luminance = np.mean(l_channel[marker_coords[0]:marker_coords[1], marker_coords[2]:marker_coords[3]])

    # Calculate the scaling factor based on the average luminance of the marker
    scaling_factor = 128 / marker_avg_luminance

    # Apply the scaling factor to the L channel
    balanced_l_channel = cv2.multiply(l_channel, scaling_factor)

    # Replace the original L channel with the balanced one
    lab_img[:, :, 0] = balanced_l_channel

    # Convert the LAB image back to BGR
    balanced_img = cv2.cvtColor(lab_img, cv2.COLOR_LAB2BGR)

    # Display the original and balanced images
    cv2.imwrite('balanced_img_V1_2.png', balanced_img)
    
    
    cv2.imshow('Original Image', img)
    cv2.imshow('Balanced Image', balanced_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
image_path = 'IMG_0133.tif'
image_path = 'IMG_0068.tif'

# Define the coordinates of the marker region (top-left and bottom-right)
marker_coordinates = [590, 928, 600, 938]
marker_coordinates = [285, 407, 295, 417]


white_balance_with_marker(image_path, marker_coordinates)


