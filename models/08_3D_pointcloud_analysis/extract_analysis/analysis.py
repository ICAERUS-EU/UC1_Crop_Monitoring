import cv2
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt


# =========================
# COLOR ANALYSIS
# =========================
class ColorAnalysis:
    @staticmethod
    def get_color_analysis(pointcloud, grayscale=True):
        """
        Analyze the color distribution of a point cloud.
        """
        if len(pointcloud.colors) == 0:
            print("The point cloud has no color information.")
            return

        colors = np.asarray(pointcloud.colors)

        if grayscale:
            # Convert RGB to grayscale using luminosity method (REC 601)
            gray_values = 0.299 * colors[:, 0] + 0.587 * colors[:, 1] + 0.114 * colors[:, 2]

            plt.figure(figsize=(10, 5))
            plt.hist(gray_values, bins=30, color='gray', alpha=0.7, label='Grayscale')
            plt.title('Grayscale Intensity Histogram')
            plt.xlabel('Intensity [0-1]')
            plt.ylabel('Frequency')

            print(f"Mean intensity: {np.mean(gray_values):.3f}")
            print(f"Standard deviation: {np.std(gray_values):.3f}")
        else:
            # RGB channels
            plt.figure(figsize=(10, 5))
            plt.hist(colors[:, 0], bins=30, color='red', alpha=0.5, label='Red')
            plt.hist(colors[:, 1], bins=30, color='green', alpha=0.5, label='Green')
            plt.hist(colors[:, 2], bins=30, color='blue', alpha=0.5, label='Blue')
            plt.title('RGB Color Histogram')

            print(f"Color means - R: {np.mean(colors[:,0]):.3f}, G: {np.mean(colors[:,1]):.3f}, B: {np.mean(colors[:,2]):.3f}")

        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def mean_health_per_parcel(cloud, line_sets):
        """
        Compute a vegetation health proxy per parcel using the green channel.
        """
        health_parcels = []

        for cube in line_sets:
            bbox = o3d.geometry.OrientedBoundingBox.create_from_points(o3d.utility.Vector3dVector(cube.points))
            mask = bbox.get_point_indices_within_bounding_box(cloud.points)
            
            if len(mask) == 0:
                health_parcels.append(np.nan)
                continue

            cloud_in_cube = cloud.select_by_index(mask)
            colors = np.asarray(cloud_in_cube.colors)
            mean_green = np.mean(colors[:, 1])
            health_parcels.append(mean_green)

        return health_parcels

    # VARI ANALYSIS
    # ========================
    @staticmethod
    def compute_vari(colors):
        """
        Calculate VARI from RGB colors normalized in [0,1].
        """
        R = colors[:, 0]
        G = colors[:, 1]
        B = colors[:, 2]
        denom = (G + R - B) + 1e-6  # avoid division by zero
        vari = (G - R) / denom
        return vari

    @staticmethod
    def vari_per_parcel(cloud, line_sets):
        """
        Calculate mean VARI per parcel from point cloud colors.
        
        Returns:
            vari_parcels: list of VARI per parcel
            mean_vari: overall mean VARI
        """
        vari_parcels = []

        for cube in line_sets:
            bbox = o3d.geometry.OrientedBoundingBox.create_from_points(
                o3d.utility.Vector3dVector(cube.points)
            )
            mask = bbox.get_point_indices_within_bounding_box(cloud.points)
            if len(mask) == 0:
                vari_parcels.append(np.nan)
                continue

            cloud_in_cube = cloud.select_by_index(mask)
            colors = np.asarray(cloud_in_cube.colors)

            vari_vals = ColorAnalysis.compute_vari(colors)
            vari_parcels.append(np.nanmean(vari_vals))

        mean_vari = np.nanmean(vari_parcels)
        return vari_parcels, mean_vari
    
    # NDVI ANALYSIS
    # =========================
    @staticmethod
    def build_rainbow_lut():
        """
        Build a 256-color RGB LUT from OpenCV Rainbow colormap.
        """
        lut = np.zeros((256, 3), dtype=np.uint8)
        for i in range(256):
            lut[i] = cv2.applyColorMap(np.array([[i]], dtype=np.uint8), cv2.COLORMAP_RAINBOW)[0, 0]
        return lut

    @staticmethod
    def rgb_to_ndvi(colors, lut):
        """
        Convert RGB colors (Nx3 [0,1]) to approximate NDVI using the LUT.
        """
        rgb_255 = (colors * 255).astype(np.uint8)
        ndvi_est = []

        for c in rgb_255:
            dists = np.linalg.norm(lut - c, axis=1)
            idx = np.argmin(dists)
            ndvi_val = (idx / 255.0) * 2 - 1  # map index to [-1, 1]
            ndvi_est.append(ndvi_val)

        return np.array(ndvi_est)

    @staticmethod
    def mean_ndvi_per_parcel(cloud, line_sets, lut):
        """
        Compute mean NDVI per parcel.
        """
        ndvi_parcels = []

        for cube in line_sets:
            bbox = o3d.geometry.OrientedBoundingBox.create_from_points(
                o3d.utility.Vector3dVector(cube.points)
            )
            mask = bbox.get_point_indices_within_bounding_box(cloud.points)
            if len(mask) == 0:
                ndvi_parcels.append(np.nan)
                continue

            cloud_in_cube = cloud.select_by_index(mask)
            colors = np.asarray(cloud_in_cube.colors)
            ndvi_vals = ColorAnalysis.rgb_to_ndvi(colors, lut)
            ndvi_parcels.append(np.mean(ndvi_vals))

        mean_ndvi = np.nanmean(ndvi_parcels)
        return ndvi_parcels, mean_ndvi

# =========================
# VOLUME ANALYSIS
# =========================
class VolumeAnalysis:
    @staticmethod
    def get_total_points(cloud, line_sets):
        """
        Count total points and points per parcel.
        """
        total_points = 0
        points_per_parcel = []

        for cube in line_sets:
            bbox = o3d.geometry.OrientedBoundingBox.create_from_points(o3d.utility.Vector3dVector(cube.points))
            mask = bbox.get_point_indices_within_bounding_box(cloud.points)
            num_points = len(mask)

            total_points += num_points
            points_per_parcel.append(num_points)

        return total_points, points_per_parcel

    @staticmethod
    def volume_and_density_per_plant(cloud, line_sets, voxel_size=0.05, padding=0.0):
        """
        Compute volume, density, and porosity per plant.
        """
        volumes = []
        densities = []
        porosities = []

        for cube in line_sets:
            bbox_cube = o3d.geometry.OrientedBoundingBox.create_from_points(o3d.utility.Vector3dVector(cube.points))
            mask = bbox_cube.get_point_indices_within_bounding_box(cloud.points)

            if len(mask) == 0:
                volumes.append(0.0)
                densities.append(0.0)
                porosities.append(1.0)
                continue

            cloud_in_cube = cloud.select_by_index(mask)
            voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(cloud_in_cube, voxel_size=voxel_size)
            n_voxels_ocupados = len(voxel_grid.get_voxels())
            vol = n_voxels_ocupados * voxel_size**3
            volumes.append(vol)

            bbox = cloud_in_cube.get_axis_aligned_bounding_box()
            if padding > 0:
                bbox = bbox.expand(padding)
            extent = bbox.get_extent()
            vol_prisma = extent[0] * extent[1] * extent[2]

            n_voxels_totales = max(vol_prisma / (voxel_size**3), 1)
            density = min(n_voxels_ocupados / n_voxels_totales, 1.0)
            porosity = 1 - density

            densities.append(density)
            porosities.append(porosity)

        return volumes, densities, porosities


# =========================
# HEIGHT ANALYSIS
# =========================
class HeightAnalysis:
    @staticmethod
    def calculate_height(points):
        """
        Compute the 99th percentile height of points relative to minimum Z.
        """
        if len(points) == 0:
            return 0.0

        z = points[:, 2]
        z_norm = z - np.min(z)
        height = np.percentile(z_norm, 99)
        return height

    @staticmethod
    def get_height_points(cloud, line_sets):
        """
        Compute height per parcel and overall 99th percentile.
        """
        height_parcels = []

        for cube in line_sets:
            bbox = o3d.geometry.OrientedBoundingBox.create_from_points(o3d.utility.Vector3dVector(cube.points))
            mask = bbox.get_point_indices_within_bounding_box(cloud.points)
            cloud_in_cube = cloud.select_by_index(mask)

            height = HeightAnalysis.calculate_height(np.asarray(cloud_in_cube.points))
            height_parcels.append(height)

        height_rows = np.percentile(height_parcels, 99)
        return height_rows, height_parcels
