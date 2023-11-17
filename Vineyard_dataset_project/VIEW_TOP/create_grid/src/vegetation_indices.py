"""
vegetation_indices.py - Vegetation Index Calculation

This module provides functions for calculating various vegetation indices from near-infrared (NIR) and red or green band images. 
These vegetation indices are commonly used in remote sensing and agriculture to assess vegetation health and vigor.

Functions:
- `ndvi(nir, r)`: Computes the Normalized Difference Vegetation Index (NDVI).
- `gndvi(nir, g)`: Computes the Green Normalized Difference Vegetation Index (GNDVI).
- `ndre(nir, re)`: Computes the Normalized Difference Red Edge Index (NDRE).
- `ndwi(nir, g)`: Computes the Normalized Difference Water Index (NDWI).

Args:
    nir (numpy.ndarray): NIR image captured by a drone or sensor.
    r (numpy.ndarray): Red or green band image captured by a drone or sensor.
    g (numpy.ndarray): Green band image captured by a drone or sensor.
    re (numpy.ndarray): Red edge band image captured by a drone or sensor.

Returns:
    numpy.ndarray: An image with computed vegetation index values.

Usage:
    import vegetation_indices

    # Example usage of NDVI calculation:
    nir_image = load_nir_image()
    red_image = load_red_image()
    ndvi_image = vegetation_indices.ndvi(nir_image, red_image)

    # Other vegetation index calculations can be performed similarly.
"""

import numpy as np
import cv2


def ndvi(nir_image, r_image): 
    """Computes the Normalized Difference Vegetation Index (NDVI),
    a measurement of vegetation health and vigor that quantifies
    the 'greenness' of plants.

    Args:
        nir numpy.ndarray: nir image captured by drone
        r numpy.ndarray: r image captured by drone

    Returns:
        numpy.ndarray: image with NDVI values
    """
    try:
        nir = np.float32(nir_image)
        r = np.float32(r_image)

        # Check for zero values in NIR and RED
        zero_mask = (nir + r) == 0

        # Calculate NDVI, but replace division by zero with 0.0
        ndvi = np.where(zero_mask, 0.0, (nir - r) / (nir + r))
        
        return ndvi

    except Exception as e:
        raise ValueError("Error computing NDVI: {}".format(str(e)))


def gndvi(nir, g): 
    """GNDVI is a variation of NDVI that uses the green band 
    instead of the red band.

    Args:
        nir numpy.ndarray: nir image captured by drone
        g numpy.ndarray: g image captured by drone

    Returns:
        numpy.ndarray: image with GNDVI values
    """
    try: 
        nir = np.float32(nir)
        g = np.float32(g)

        gndvi = (nir - g) / (nir + g) 

    except Exception as e:
        raise ValueError("Error computing NDVI: {}".format(str(e)))

    return gndvi


def ndre(nir, re): 
    """NDRE is a vegetation index that is particularly sensitive 
    to changes in chlorophyll content and canopy structure.

    Args:
        nir numpy.ndarray: nir image captured by drone
        re numpy.ndarray: re image captured by drone

    Returns:
        numpy.ndarray: image with NDRE values
    """
    try:
        nir = np.float32(nir)
        re = np.float32(re)

        ndre = (nir - re) / (nir + re)
    except Exception as e:
        raise ValueError("Error computing NDVI: {}".format(str(e)))

    return ndre


def ndwi(nir, g):  
    """NDWI is a vegetation index that is particularly sensitive 
    to changes in chlorophyll content and canopy structure.


    Args:
        nir numpy.ndarray: nir image captured by drone
        g numpy.ndarray: g image captured by drone

    Returns:
        numpy.ndarray: image with NDWI values
    """
    try: 
        nir = np.float32(nir)
        g = np.float32(g)

        ndwi = (g - nir) / (g + nir)
    except Exception as e:
        raise ValueError("Error computing NDVI: {}".format(str(e)))

    return ndwi
