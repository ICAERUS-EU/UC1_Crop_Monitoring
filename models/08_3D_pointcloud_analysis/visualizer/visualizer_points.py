
import numpy as np 
import open3d as o3d
import matplotlib.pyplot as plt



class VisualizerPoints: 

    def __init__(self, raw_data):
        self._labels, self._data = self._reagroup_points_data(raw_data)
        self._points_parcel_2023 = np.array(self._data['2023']['points_parcel'])
        self._points_parcel_2024 = np.array(self._data['2024']['points_parcel'])
        self._points_parcel_plant_2023 = np.array(self._data['2023']['points_parcel_plant'])
        self._points_parcel_plant_2024 = np.array(self._data['2024']['points_parcel_plant'])


    def _reagroup_points_data(self, raw_data):

        labels = {}
        data_grouped = {}
        for year in ['2023', '2024']:
            data_grouped[year] = {'points_cloud':[], 'points_rows':[], 'points_parcel':[],
                                'points_cloud_plant':[], 'points_rows_plant':[], 'points_parcel_plant':[]
                                }
            labels[year] = []

        dates = sorted([d for d in raw_data])
        for date in dates:
            if date != '230428' and date!='230526' and date!='230728' and date!='240426':
                year = '20'+date[0:2]
                labels[year].append(date)
                data_grouped[year]['points_cloud'].append(raw_data[date]['points_cloud'])
                data_grouped[year]['points_rows'].append(raw_data[date]['points_rows'])
                data_grouped[year]['points_parcel'].append(raw_data[date]['points_parcel'])
                data_grouped[year]['points_cloud_plant'].append(raw_data[date]['points_cloud_plant'])
                data_grouped[year]['points_rows_plant'].append(raw_data[date]['points_rows_plant'])
                data_grouped[year]['points_parcel_plant'].append(raw_data[date]['points_parcel_plant'])
                
        return labels, data_grouped


    def show_total_points(self, plant=False):
        key1 = 'points_cloud' 
        key2 = 'points_cloud_plant'

        plt.figure(figsize=(15, 6))  # Más grande que el default
        plt.plot(self._labels['2023'], self._data['2023'][key1], label='Total Points 2023', marker='o')
        plt.plot(self._labels['2024'], self._data['2024'][key1], label='Total Points 2024', marker='o')
        plt.plot(self._labels['2023'], self._data['2023'][key2], label='Total Points Plants 2023', linestyle='--', marker='o')
        plt.plot(self._labels['2024'], self._data['2024'][key2], label='Total Points Plants 2024', linestyle='--', marker='o')
        
        # Añadir valores numéricos en cada punto
        for year in ['2023', '2024']:
            for i, value in enumerate(self._data[year][key1]):
                plt.text(self._labels[year][i], value, str(value), fontsize=9, ha='right')
            for i, value in enumerate(self._data[year][key2]):
                plt.text(self._labels[year][i], value, str(value), fontsize=9, ha='right', va='bottom')

        plt.title("Total points and points plants over time")
        plt.ylabel('Total points')
        plt.legend()
        plt.show()

    def show_rows_points(self) -> None:
        key1 = 'points_rows'
        key2 = 'points_rows_plant'

        plt.figure(figsize=(15, 6))
        plt.plot(self._labels['2023'], self._data['2023'][key1], label='Points Rows 2023', marker='o')  # Added marker='o'
        plt.plot(self._labels['2024'], self._data['2024'][key1], label='Points Rows 2024', marker='o')  # Added marker='o'
        plt.plot(self._labels['2023'], self._data['2023'][key2], label='Points Rows Plants 2023', linestyle='--', marker='o')  # Added marker='o'
        plt.plot(self._labels['2024'], self._data['2024'][key2], label='Points Rows Plants 2024', linestyle='--', marker='o')  # Added marker='o'

        # Añadir valores numéricos en cada punto
        for year in ['2023', '2024']:
            for i, value in enumerate(self._data[year][key1]):
                plt.text(self._labels[year][i], value, str(value), fontsize=9, ha='right')
            for i, value in enumerate(self._data[year][key2]):
                plt.text(self._labels[year][i], value, str(value), fontsize=9, ha='right', va='bottom')

        plt.title(f"Points rows and plants rows over time")
        plt.ylabel('Total points')
        plt.legend()
        plt.show()

    def show_parcel_points(self, parcel_idx: int) -> None: 

        plt.figure(figsize=(15, 6))
        plt.plot(self._labels['2023'], self._points_parcel_2023[:, parcel_idx], label='Points Parcel 2023', marker='o')
        plt.plot(self._labels['2024'], self._points_parcel_2024[:, parcel_idx], label='Points Parcel 2024', marker='o')
        plt.plot(self._labels['2023'], self._points_parcel_plant_2023[:, parcel_idx], label='Points Parcel Plant 2023', linestyle='--', marker='o')
        plt.plot(self._labels['2024'], self._points_parcel_plant_2024[:, parcel_idx], label='Points Parcel Parcel 2023', linestyle='--', marker='o')

        # Añadir valores numéricos en cada punto
        for i, value in enumerate(self._points_parcel_2023[:, parcel_idx]):
            plt.text(self._labels['2023'][i], value, str(value), fontsize=9, ha='right')
        for i, value in enumerate(self._points_parcel_2024[:, parcel_idx]):
            plt.text(self._labels['2024'][i], value, str(value), fontsize=9, ha='right', va='bottom')
        for i, value in enumerate(self._points_parcel_plant_2023[:, parcel_idx]):
            plt.text(self._labels['2023'][i], value, str(value), fontsize=9, ha='right')
        for i, value in enumerate(self._points_parcel_plant_2024[:, parcel_idx]):
            plt.text(self._labels['2024'][i], value, str(value), fontsize=9, ha='right', va='bottom')

        plt.title(f"Points parcel {parcel_idx} over time")
        plt.ylabel('Total points')
        plt.show()

    def show_3d_parcel_comparison(self, parcel1_3d, parcel2_3d): 

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
