import numpy as np
import open3d as o3d
from pointcloud.pointcloud_loader import PointCloudLoader
from utils.utils import deserialize_line_sets



class VisualizerPointCloud:

    def __init__(self, config, base_dir): 
        self.base_dir = base_dir
        self.config = config
        self.parcel_idx = config.get("parcel_idx", 0)
        self.showcase_dates = self.config.get("showcase_dates", [])
        self.down = self.config.get("downsample", True)
        self.suffix = "_down" if self.down else ""

    def _get_3d_parcel(self, date):
        year = "20"+date[0:2]
        io_cfg = self.config["io"]
        paths_cfg = self.config["paths"]
        base_grid_paths = f"{self.base_dir}/data/grids/{year}"

        if self.down:
            cloud = o3d.io.read_point_cloud(f"{self.base_dir}/data/plant_clouds{self.suffix}/{year}/plant_cloud_{date}{self.suffix}.ply")
        else:
            cloud_path = paths_cfg["pointcloud"].format(zenodo_base=io_cfg["zenodo_base_dir"], year=year, date=date, suffix=self.suffix)
            cloud = PointCloudLoader.load_cloud(cloud_path)

        grid_path = f"{base_grid_paths}/grid_{date}.npz"
        line_sets = deserialize_line_sets(grid_path)
        
        bbox = o3d.geometry.OrientedBoundingBox.create_from_points(o3d.utility.Vector3dVector(line_sets[self.parcel_idx].points))
        parcel_3d = cloud.crop(bbox)

        return cloud, parcel_3d


    def _show_3d_parcel_comparison(self, parcel1_3d, parcel2_3d): 

        def center_pointcloud(pc):
            centroid = pc.get_center()
            return pc.translate(-centroid)

        parcel1_centered = center_pointcloud(parcel1_3d)
        parcel2_centered = center_pointcloud(parcel2_3d)

        # 2️⃣ Rotar ambos para que el eje deseado sea horizontal
        R = parcel1_centered.get_rotation_matrix_from_xyz((0, 0, np.pi / 2))
        parcel1_centered.rotate(R, center=(0,0,0))
        parcel2_centered.rotate(R, center=(0,0,0))

        # 3️⃣ Calcular el tamaño de parcel1 y trasladar parcel2 en X
        bbox1 = parcel1_centered.get_axis_aligned_bounding_box()
        extent1 = bbox1.get_extent()

        parcel2_shifted = parcel2_centered.translate((extent1[0]-4.0, extent1[1]+2.0, 0))

        # 4️⃣ Visualizar ambos alineados y “uno al lado del otro”
        o3d.visualization.draw_geometries([parcel1_centered, parcel2_shifted])


    def show_3d_parcels(self): 

        if self.showcase_dates:
            print("\n[INFO] SHOW 3D PARCEL VISUALIZATION")

            date1 = self.showcase_dates[0]
            date2 = self.showcase_dates[1]

            # Load 3D parcel clouds for two dates
            cloud1, parcel1_3d = self._get_3d_parcel(date1)
            cloud2, parcel2_3d = self._get_3d_parcel(date2)

            print(f"[INFO] Loaded clouds for {date1} and {date2}")
            print(f"  Cloud1 points: {len(cloud1.points)}")
            print(f"  Cloud2 points: {len(cloud2.points)}")
            print(f"  Parcel {self.parcel_idx} ({date1}): {len(parcel1_3d.points)} points")
            print(f"  Parcel {self.parcel_idx} ({date2}): {len(parcel2_3d.points)} points")

            # Paint and visualize comparison
            parcel1_3d.paint_uniform_color([1, 0, 0])  # red
            parcel2_3d.paint_uniform_color([0, 0, 1])  # blue
            self._show_3d_parcel_comparison(parcel1_3d, parcel2_3d)

            # Visualize clouds in Open3D
            print("[INFO] Opening 3D viewer for detailed inspection")
            cloud2.translate([25.0, 0.0, 15.0])  # offset to separate visually
            o3d.visualization.draw_geometries([cloud1, cloud2])