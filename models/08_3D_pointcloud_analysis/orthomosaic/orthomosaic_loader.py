import cv2
import sys
import rasterio
import numpy as np 
import open3d as o3d
from utils.utils import rotation_matrix_from_vectors

class OrthomosaicLoader:
    """
    Handles loading and processing of orthomosaic images
    """
    
    @staticmethod
    def load_orthomosaic(tif_path):
        """
        Load orthomosaic from TIFF file and convert to RGB
        """
        try:
            with rasterio.open(tif_path) as src:
                red_band = src.read(1)
                green_band = src.read(2)
                blue_band = src.read(3)
                ortho_image = cv2.merge([blue_band, green_band, red_band])
                rgb_image = OrthomosaicLoader.adjust_orthomosaic(ortho_image)
            return rgb_image
        except Exception as e:
            print(f"❌ Failed to load orthomosaic: {tif_path}")
            print(f"   Error: {e}")
            sys.exit(1)

    @staticmethod
    def adjust_orthomosaic(ortho_image):
        """
        Adjust orthomosaic image size and apply masking

        """
        if ortho_image.shape[0] == 14441: 
            # Resize image
            ortho_image = cv2.resize(ortho_image, (4692, 3610))

            # Apply thresholding and masking
            _, binary_mask = cv2.threshold(
                cv2.cvtColor(ortho_image, cv2.COLOR_BGR2GRAY), 
                254, 255, cv2.THRESH_BINARY_INV
            )
            kernel = cv2.getStructuringElement(
                shape=cv2.MORPH_ELLIPSE, 
                ksize=(35, 35)
            )
            binary_mask = cv2.erode(binary_mask, kernel)
            ortho_image_masked = cv2.bitwise_and(
                ortho_image, ortho_image, mask=binary_mask
            )

            # Replace black pixels with white
            black_pixels = np.all(ortho_image_masked == [0, 0, 0], axis=-1)
            ortho_image_masked[black_pixels] = [255, 255, 255]

            # Convert to RGB and clean up
            img_rgb = cv2.cvtColor(ortho_image_masked, cv2.COLOR_BGR2RGB)
            del ortho_image
            return img_rgb

        return ortho_image

    @staticmethod
    def create_color_plane_from_image(img_rgb, resolution = 0.038):
        """
        Create a 3D color plane point cloud from RGB image
        """
        h, w, _ = img_rgb.shape
        
        # Generate 3D points for each pixel
        xx, yy = np.meshgrid(np.arange(w), np.arange(h))
        x = xx.flatten() * resolution
        y = (h - yy.flatten()) * resolution  # invert Y axis for Open3D
        z = np.zeros_like(x)
        
        points = np.vstack((x, y, z)).T
        colors = img_rgb.reshape(-1, 3) / 255.0
        
        # Create point cloud
        cloud = o3d.geometry.PointCloud()
        cloud.points = o3d.utility.Vector3dVector(points)
        cloud.colors = o3d.utility.Vector3dVector(colors)

        # Mask: True where color is NOT white
        not_white_mask = ~np.all(colors == 1.0, axis=1)

        # Create filtered point cloud without white pixels
        filtered_cloud = o3d.geometry.PointCloud()
        filtered_cloud.points = o3d.utility.Vector3dVector(points[not_white_mask])
        filtered_cloud.colors = o3d.utility.Vector3dVector(colors[not_white_mask])

        return filtered_cloud

    @staticmethod
    def compute_plane_orientation(cloud):
        """
        Compute plane orientation using PCA
        """
        pts = np.asarray(cloud.points)
        centroid = np.mean(pts, axis=0)
        pts_centered = pts - centroid
        cov = np.cov(pts_centered.T)
        eigvals, eigvecs = np.linalg.eigh(cov)
        normal_vector = eigvecs[:, 0]  # normal vector to the plane
        
        # Rotation matrix that aligns Z (0,0,1) with normal vector
        R = rotation_matrix_from_vectors(np.array([0, 0, 1]), normal_vector)
        
        return normal_vector, R, centroid
