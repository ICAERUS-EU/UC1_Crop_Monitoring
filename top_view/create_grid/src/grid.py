import cv2
import numpy as np
import copy 
from tqdm import tqdm

def get_coordinates(event, x, y, flags, param):
    """ """
    if event == cv2.EVENT_LBUTTONDOWN:
        coordinates = param  
        coordinates.append([x,y])


def get_coordinates_row(ortho_image_res, select_points): 

    """
    Gets the coordinates of the two points selected in the image.
    
    Args:
        ortho_image_res (numpy.ndarray): A numpy array representing the orthomosaic image.
        select_points (boolean): 
    Returns:
        coordinates (list): 
        angle (float): 
    """

    coordinates = []

    # Manual selection 
    if(select_points):
        cv2.imshow('Image', ortho_image_res)
        cv2.setMouseCallback('Image', get_coordinates, (coordinates))

        while(len(coordinates) < 1):
            cv2.waitKey(1)

        cv2.setMouseCallback('Image', get_coordinates, (coordinates))
        while(len(coordinates) < 2):
            cv2.waitKey(1)
        cv2.destroyAllWindows()

    # Automatic selection
    else:
        coordinates = [[165, 421], [783, 279]]
        coordinates = [[69, 750], [2298, 237]]   # Imagen a 50%
        coordinates = [[568, 867], [1215, 718]]  # Imagen a tamaño original


    angle = np.arctan2(coordinates[1][1] - coordinates[0][1], coordinates[1][0] - coordinates[0][0])
    print(coordinates)
    return coordinates, angle



def get_parallel_rows(ortho_image_res, mask, coordinates, VINEYARD_SEP):

    """
    Gets parallel rows that define each vineyard rows and shows them in an image.
    
    Args:
        ortho_image_res (numpy.ndarray): A numpy array representing the orthomosaic image.
        coordinates (list): list that contains the init and final coordinates of the previous selected row.
        VINEYARD_SEP (const float): value of vineyard rows separation.
    Returns:
        ortho_image_rows (numpy.ndarray): A numpy array representing the image with the vineyard rows.
    """

    # Smooth the mask
    kernel7 = np.ones((7, 7), np.uint8)
    kernel3 = np.ones((5, 5), np.uint8)
    smoothed_mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel7)
    smoothed_mask = cv2.erode(smoothed_mask, kernel3, iterations=5)
    smoothed_mask = cv2.GaussianBlur(smoothed_mask, (5, 5), 0)

    print("in parallel")

    ortho_image_rows = copy.deepcopy(ortho_image_res)
    img_height, img_width, _ = ortho_image_rows.shape

    # Added length to initial row
    added_length = 6000
    thickness = 2
    thickness = 9
    parallel_rows_points = []

    # Varible to stop drawing parallel lines
    reached = False

    #  Init and final coordinates of the selected row
    x1 = coordinates[0][0]
    y1 = coordinates[0][1]
    x2 = coordinates[1][0]
    y2 = coordinates[1][1]

    # Direction and length of the row
    v_dir = (x2 - x1, y2 - y1)
    length = (v_dir[0] ** 2 + v_dir[1] ** 2) ** 0.5
    v_dir_normalized = (v_dir[0] / length, v_dir[1] / length)
    v_perp = (-v_dir_normalized[1], v_dir_normalized[0]) 

    # Draws parallel lines until it reaches the limits of the image
    it = -1
    while True:

        # Draws the parallel lines in each direction
        if(reached):
            it -= 1
        else:
            it += 1

        # Calculates the points of the new parallel line
        x1_parallel = x1 + it * VINEYARD_SEP * v_perp[0] - added_length * v_dir_normalized[0]
        y1_parallel = y1 + it * VINEYARD_SEP * v_perp[1] - added_length * v_dir_normalized[1]
        x2_parallel = x2 + it * VINEYARD_SEP * v_perp[0] + added_length * v_dir_normalized[0]
        y2_parallel = y2 + it * VINEYARD_SEP * v_perp[1] + added_length * v_dir_normalized[1]

        point1 = (int(x1_parallel), int(y1_parallel))
        point2 = (int(x2_parallel), int(y2_parallel))

        # Check if the line is visible 
        blank_rows = np.zeros((img_height, img_width, 1), dtype=np.uint8)
        cv2.line(blank_rows, point1, point2, (255), 2)
        rows_mask = cv2.bitwise_and(blank_rows, blank_rows, mask=smoothed_mask)
        visible_pixels_yx = np.transpose(np.where(rows_mask == 255))

        if(len(visible_pixels_yx) == 0 and (not reached)):
            reached = True
            it = 0

        elif(len(visible_pixels_yx) == 0 and reached):
            break

        else: 
            # Saves parallel rows points and draw the line
            parallel_rows_points.append([point1, point2])
            cv2.line(ortho_image_rows, point1, point2, (0,0,255), thickness)


    return ortho_image_rows, parallel_rows_points
    


def mask_ortho_image_rows(ortho_image_rows, mask): 
    """
    Smoothes the mask and applies it to the input image.
    
    Args:
        ortho_image_rows (numpy.ndarray): A numpy array representing the image.
        mask (numpy.ndarray): A mask that defines the vineyard extension. 

    Returns:
        masked_rows (numpy.ndarray): A numpy array representing the image smoothed.
    """

    # Definition of kernels
    kernel7 = np.ones((7, 7), np.uint8)
    kernel3 = np.ones((5, 5), np.uint8)

    # Smooth the mask
    smoothed_mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel7)
    #smoothed_mask = cv2.erode(smoothed_mask, kernel3, iterations=2)
    smoothed_mask = cv2.erode(smoothed_mask, kernel3, iterations=5)

    smoothed_mask = cv2.GaussianBlur(smoothed_mask, (5, 5), 0)

    # Apply mask to image 
    masked_rows = cv2.bitwise_and(ortho_image_rows, ortho_image_rows, mask=smoothed_mask)

    return masked_rows



def get_filtered_rows(masked_rows_image): 
    """
    Detects red rows of masked_rows_image and smoothes the image. This will be use to split the rows in parcels.
    
    Args:
        masked_rows_image (numpy.ndarray): A numpy array representing the image with red rows for each vineyard line.

    Returns:
        filtered_rows_image (numpy.ndarray): A numpy array representing the image filtered.  
    """

    # Range for filtering red colour
    lower_red = np.array([0, 0, 250])
    upper_red = np.array([0, 0, 255])

    # Creates a red mask for extracting color red from image
    red_mask = cv2.inRange(masked_rows_image, lower_red, upper_red)

    # Applies the red mask to masked_rows_image getting the red rows and smooth
    filtered_rows_image = cv2.bitwise_and(masked_rows_image, masked_rows_image, mask=red_mask)
    filtered_rows_image = cv2.medianBlur(filtered_rows_image, 5)

    return filtered_rows_image


def get_parcel_points(k, total_parcels, all_corners, deltas, PARCEL_LEN): 
    """
    Gets the points that define each parcel of each vineyard row.

    Args:
        k (int): 
        total_parcels (int): 
        all_corners (list):
        deltas (list): 
        PARCEL_LEN (const int): 

    Returns:
        points (numpy.array): A numpy array with the four corners of the parcel.  
    """

    # Calculates the angle between the left-up corner and the right-up corner
    angle = np.arctan2(all_corners[2][1] - all_corners[0][1], all_corners[2][0] - all_corners[0][0])

    # Get parcel points depending on k, displacement and size of parcel
    p1_init_x = all_corners[0][0] + k * deltas[0]
    p1_init_y = all_corners[0][1] + k * deltas[1]
    p2_init_x = all_corners[1][0] + k * deltas[0]
    p2_init_y = all_corners[1][1] + k * deltas[1]

    p1_end_x = p1_init_x + PARCEL_LEN * np.cos(angle)
    p1_end_y = p1_init_y + PARCEL_LEN * np.sin(angle)
    p2_end_x = p2_init_x + PARCEL_LEN * np.cos(angle)
    p2_end_y = p2_init_y + PARCEL_LEN * np.sin(angle)

    p1_init = (p1_init_x, p1_init_y)
    p2_init = (p2_init_x, p2_init_y)

    # If it's the last parcel, the end points will be the ones in all_corners
    if(k == total_parcels - 1):
        p1_end = all_corners[2]
        p2_end = all_corners[3]
    else: 
        p1_end = (p1_end_x, p1_end_y)
        p2_end = (p2_end_x, p2_end_y)

    points = np.array([p1_init, p2_init, p2_end, p1_end], np.int32)

    return points



def get_corners(contour): 

    """
    Gets the corners of the actual contour that represents a vineyard line.

    Args:
        contour (numpy.ndarray): 

    Returns:
        tuple: A tuple containing the following tuples:
        - corner_LU (tuple): 
        - corner_LD (tuple): 
        - corner_RU (tuple): 
        - corner_RD (tuple): 
    """

    # Gets the rectangle points
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    # Sorts the rectangle points
    rect_sorted = sorted(box, key=lambda x: x[0], reverse=False)
    rect_sorted_left = sorted(rect_sorted[:2], key=lambda x: x[1], reverse=False)
    rect_sorted_right = sorted(rect_sorted[2:4], key=lambda x: x[1], reverse=False)

    # Extract each corner (LU = Left Up, LD = Left Down, RU = Right Up, RD = Right Down)
    corner_LU = tuple(rect_sorted_left[0])
    corner_LD = tuple(rect_sorted_left[1])
    corner_RU = tuple(rect_sorted_right[0])
    corner_RD = tuple(rect_sorted_right[1])

    return corner_LU, corner_LD, corner_RU, corner_RD



def get_total_parcels_and_deltas(all_corners, PARCEL_LEN): 
    
    """
    Gets the corners of the actual contour that represents a vineyard line.

    Args:
        all_corners (list): 
        PARCEL_LEN (const int): 

    Returns:
        tuple: A tuple containing the following values:
          - total_parcels (int): 
          - deltas (list):  
    """

    # Calculates total length of the actual vineyard row
    dist_total = int(np.sqrt((all_corners[2][0] - all_corners[0][0])**2 + (all_corners[2][1] - all_corners[0][1])**2))
    
    # Calculates the total of parcel dividing the total distance between the length ot the parcel
    total_parcels = (dist_total/PARCEL_LEN)

    # Calculates displacement of x,y for each parcel 
    delta_x = (all_corners[2][0] - all_corners[0][0]) / total_parcels
    delta_y = (all_corners[2][1] - all_corners[0][1]) / total_parcels
    deltas = [delta_x, delta_y]

    #print(total_parcels)

    # If the total parcels is not a round number, one parcel is added (ex. 5.3 parcels >> 6 parcels)
    if(total_parcels - int(total_parcels) >=0.4):
        total_parcels = int(total_parcels) + 1
    else: 
        total_parcels = int(total_parcels)


    '''if(int(total_parcels) < total_parcels):
        total_parcels = int(total_parcels) + 1
    else: 
        total_parcels = int(total_parcels)'''

    return total_parcels, deltas



def get_all_parcel_points(filtered_rows_image, parallel_rows_points, PARCEL_LEN): 
    """
    Calculates the position for each parcel in the image.

    Args:
        filtered_rows_image (numpy.darray): image with each row.
        PARCEL_LEN (const int): size of the parcel.

    Returns:
        sorted_parcel_points (numpy.darray): array containing the coordinates for each parcel.
    """

    all_parcel_points = []

    # Detects edges and contours
    edges = cv2.Canny(filtered_rows_image,10,50) 
    contours = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[0]
    sorted_contours, rows = sort_contours(parallel_rows_points, filtered_rows_image, contours)

    # For each contour
    total = -1
    for cnt in sorted_contours: 
        
        filtered_rows_image = cv2.drawContours(filtered_rows_image, [cnt], -1, (255, 155, 0), 2)
        '''cv2.imshow("filtered_rows_image",cv2.resize(filtered_rows_image, None, fx=0.2,fy=0.2))
        cv2.waitKey(0)
        cv2.destroyAllWindows()'''

        # Get 4 corners of the rectangle that defines the contour
        all_corners = get_corners(cnt)

        # Get the total of parcels in the rows and the displacement in x,y (deltas)
        total_parcels, deltas = get_total_parcels_and_deltas(all_corners, PARCEL_LEN)


        if(total_parcels>0):
            # Saves each row independently
            all_parcel_points.append([])

        # For each parcel in the row
        for k in range(total_parcels):
            # Calculates the parcel points and draw the rectangle
            parcel = get_parcel_points(k, total_parcels, all_corners, deltas, PARCEL_LEN)
           
            # Saves parcel points
            all_parcel_points[-1].append(parcel.tolist())
        
    return all_parcel_points, rows


def sort_contours(parallel_rows_points, filtered_rows_image, contours): 
    # Sort contours
    rows = []
    sorted_contours = []
    for points in tqdm(parallel_rows_points):
        appended_contours = []
        blank1 = np.zeros_like(filtered_rows_image)
        blank1 = cv2.line(blank1, points[0], points[1], (255,255,255), 9)

        for cnt in contours: 
            blank2 = np.zeros_like(filtered_rows_image)
            blank2 = cv2.drawContours(blank2, [cnt], -1, (255, 255, 255), -1)
            mask = cv2.bitwise_and(blank1, blank2)

            if np.any(mask): 
                appended_contours.append(cnt)
                    
        appended_contours = sorted(appended_contours, key=lambda c: cv2.boundingRect(c)[0])
        rect = cv2.minAreaRect(appended_contours[0])
        box = np.int0(cv2.boxPoints(rect))
        rows.append(box[0])
        for appended_cnt in appended_contours: 
            sorted_contours.append(appended_cnt)

    return sorted_contours, rows


def get_all_centers_parcels(sorted_parcel_points):

    n = 4
    centers_parcels = []
    
    for k1, row in enumerate(sorted_parcel_points):
        centers_parcels.append([])
        for k2, parcel in enumerate(row):

            closed_parcel = parcel + [parcel[0]]

            A = 0
            C_x = 0
            C_y = 0

            for i in range(n):
                factor = closed_parcel[i][0] * closed_parcel[i + 1][1] - closed_parcel[i + 1][0] * closed_parcel[i][1]
                A += factor
                C_x += (closed_parcel[i][0] + closed_parcel[i + 1][0]) * factor
                C_y += (closed_parcel[i][1] + closed_parcel[i + 1][1]) * factor

            A = A / 2
            C_x = C_x / (6 * A)
            C_y = C_y / (6 * A)

            centers_parcels[-1].append([C_x, C_y])

    return centers_parcels



def draw_parcels(ortho_image_res, sorted_parcel_points, rows):
    """
    Draws parcel rectangles in each vineyard row.

    Args:
        ortho_image_res (numpy.darray): orthomosaic image to draw the parcels in. 
        sorted_parcel_points (numpy.darray): array containing the coordinates for the parcels.
    Returns:
        parcel_rows_image (numpy.darray): image with the parcels drawn.
    """

    # Copy image and detects edges and contours
    parcel_rows_image = copy.deepcopy(ortho_image_res)
    parcel_rows_image = np.full_like(ortho_image_res, 255)

    gris = cv2.cvtColor(ortho_image_res, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gris, 200, 255, cv2.THRESH_BINARY)

    padding = 50
    #thresh = cv2.copyMakeBorder(thresh, padding, padding, padding, padding, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    thresh = cv2.bitwise_not(thresh)
    contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    #area_min = 80000
    for contorno in contornos:
        #if cv2.contourArea(contorno) > area_min :
        print(cv2.contourArea(contorno) )
        parcel_rows_image = cv2.drawContours(parcel_rows_image, [contorno], -1, (0, 0, 0), 2)
        '''cv2.imshow("parcel_rows_image",cv2.resize(parcel_rows_image, None, fx=0.2,fy=0.2))
        cv2.waitKey(0)
        cv2.destroyAllWindows()'''


    # For each parcel in the row
    total = 0
    for k1, row in enumerate(sorted_parcel_points):
        for k2, parcel in enumerate(row):
            total = total + 1

            #cv2.polylines(parcel_rows_image, [np.array(parcel)], isClosed=True, color=[0,170,255], thickness=2)
            cv2.polylines(parcel_rows_image, [np.array(parcel)], isClosed=True, color=[0,0,0], thickness=2)

            center_x = int((parcel[0][0] + parcel[2][0]) / 2) - 2
            center_y = int((parcel[0][1] + parcel[2][1]) / 2) + 2
            center = (center_x, center_y)

            #cv2.putText(parcel_rows_image, str(total), center, cv2.FONT_HERSHEY_SIMPLEX, 0.23, (255,255,255), 1)
            cv2.putText(parcel_rows_image, str(total), center, cv2.FONT_HERSHEY_SIMPLEX, 0.23, (0,0,0), 1)
   

            '''
            # Write row number
            if (k2 == 0):
                center_x = int((parcel[0][0] + parcel[2][0]) / 2) - 50
                center_y = int((parcel[0][1] + parcel[2][1]) / 2) + 14
                center = (center_x, center_y)
                cv2.putText(parcel_rows_image, str(k1+1), center, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 1)'''
    

    padding_left = 100
    parcel_rows_image = cv2.copyMakeBorder(parcel_rows_image, 0, 0, padding_left, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    for k1, center in enumerate(rows):
        cv2.putText(parcel_rows_image, str(k1), (10, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)



    return parcel_rows_image
    
