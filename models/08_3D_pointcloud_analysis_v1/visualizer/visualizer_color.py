
import numpy as np 
import open3d as o3d
import matplotlib.pyplot as plt



class VisualizerColor: 

    def __init__(self, color_type, raw_data):
        self._color_type = color_type
        self._labels, self._data = self._reagroup_color_data(raw_data)
        self._color_parcel_plant_2023 = np.array(self._data['2023']['color_parcel_plant'])
        self._color_parcel_plant_2024 = np.array(self._data['2024']['color_parcel_plant'])

    def _reagroup_color_data(self, raw_data):
        labels = {}
        data_grouped = {}
        for year in ['2023', '2024']:
            data_grouped[year] = {'color_plant':[], 'color_parcel_plant':[]}
            labels[year] = []

        dates = sorted([d for d in raw_data])
        for date in dates:
            year = '20'+date[0:2]
            labels[year].append(date)
            data_grouped[year]['color_plant'].append(np.round(raw_data[date]['color_plant'], 3))
            data_grouped[year]['color_parcel_plant'].append(np.round(raw_data[date]['color_parcel_plant'], 3))
            
        return labels, data_grouped

    def show_total_color(self):
        key2 = 'color_plant'

        print(self._data['2023'][key2])

        plt.figure(figsize=(15, 6))  # Más grande que el default
        plt.plot(self._labels['2023'], self._data['2023'][key2], label=f'Mean {self._color_type} 2023', linestyle='--', marker='o')
        plt.plot(self._labels['2024'], self._data['2024'][key2], label=f'Mean {self._color_type} 2024', linestyle='--', marker='o')
        
        # Añadir valores numéricos en cada punto
        for year in ['2023', '2024']:
            for i, value in enumerate(self._data[year][key2]):
                plt.text(self._labels[year][i], value, str(value), fontsize=9, ha='right', va='bottom')

        plt.title(f"Mean {self._color_type} over time")
        plt.ylabel(f"Mean {self._color_type}")
        plt.legend()
        plt.show()


    def show_parcel_color(self, parcel_idx): 

        plt.figure(figsize=(15, 6))
        plt.plot(self._labels['2023'], self._color_parcel_plant_2023[:, parcel_idx], label=f'Mean {self._color_type} 2023', linestyle='--', marker='o')
        plt.plot(self._labels['2024'], self._color_parcel_plant_2024[:, parcel_idx], label=f'Mean {self._color_type} 2024', linestyle='--', marker='o')

        for i, value in enumerate(self._color_parcel_plant_2023[:, parcel_idx]):
            plt.text(self._labels['2023'][i], value, str(value), fontsize=9, ha='right')
        for i, value in enumerate(self._color_parcel_plant_2024[:, parcel_idx]):
            plt.text(self._labels['2024'][i], value, str(value), fontsize=9, ha='right', va='bottom')

        plt.title(f"Mean {self._color_type} for parcel {parcel_idx} over time")
        plt.ylabel(f"Mean {self._color_type}")
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
