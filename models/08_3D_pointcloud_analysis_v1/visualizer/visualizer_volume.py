
import numpy as np 
import open3d as o3d
import matplotlib.pyplot as plt



class VisualizerVolume: 

    def __init__(self, raw_data):
        self._labels, self._data = self._reagroup_volume_data(raw_data)
        self._volume_parcel_plant_2023 = np.array(self._data['2023']['volume_parcel_plant'])
        self._volume_parcel_plant_2024 = np.array(self._data['2024']['volume_parcel_plant'])
        self._density_parcel_plant_2023 = np.array(self._data['2023']['density_parcel_plant'])
        self._density_parcel_plant_2024 = np.array(self._data['2024']['density_parcel_plant'])


    def _reagroup_volume_data(self, raw_data):

        labels = {}
        data_grouped = {}
        for year in ['2023', '2024']:
            data_grouped[year] = {'volume_plants':[], 'volume_parcel_plant':[], 'density_plants':[], 'density_parcel_plant':[]}
            labels[year] = []

        dates = sorted([d for d in raw_data])
        for date in dates:
            year = '20'+date[0:2]
            labels[year].append(date)
            data_grouped[year]['volume_plants'].append(np.round(raw_data[date]['volume_plants'], 3))
            data_grouped[year]['volume_parcel_plant'].append(np.round(raw_data[date]['volume_parcel_plant'], 3))
            data_grouped[year]['density_plants'].append(np.round(raw_data[date]['density_plants'], 3))
            data_grouped[year]['density_parcel_plant'].append(np.round(raw_data[date]['density_parcel_plant'], 3))
            
        return labels, data_grouped


    def show_total_volume(self, plant=False):
        key2 = 'volume_plants'

        plt.figure(figsize=(15, 6))  # Más grande que el default
        #plt.plot(self._labels['2023'], self._data['2023'][key2], label='Total Volume Plants 2023', linestyle='--', marker='o')
        plt.plot(self._labels['2024'], self._data['2024'][key2], label='Total Volume Plants 2024', linestyle='--', marker='o')
        
        # Añadir valores numéricos en cada punto
        for year in ['2024']:
            for i, value in enumerate(self._data[year][key2]):
                plt.text(self._labels[year][i], value, str(value), fontsize=9, ha='right', va='bottom')

        plt.title("Total volume plants over time")
        plt.ylabel('Volume')
        plt.legend()
        plt.show()


    def show_total_density(self, plant=False):
        key2 = 'density_plants'

        plt.figure(figsize=(15, 6))  # Más grande que el default
        #plt.plot(self._labels['2023'], self._data['2023'][key2], label='Total Density Plants 2023', linestyle='--', marker='o')
        plt.plot(self._labels['2024'], self._data['2024'][key2], label='Total Density Plants 2024', linestyle='--', marker='o')
        
        # Añadir valores numéricos en cada punto
        for year in ['2024']:
            for i, value in enumerate(self._data[year][key2]):
                plt.text(self._labels[year][i], value, str(value), fontsize=9, ha='right', va='bottom')

        plt.title("Total density plants over time")
        plt.ylabel('Density')
        plt.legend()
        plt.show()


    def show_parcel_volume(self, parcel_idx: int) -> None: 

        plt.figure(figsize=(15, 6))
        #plt.plot(self._labels['2023'], self._volume_parcel_plant_2023[:, parcel_idx], label='Volume Parcel Plant 2023', linestyle='--', marker='o')
        plt.plot(self._labels['2024'], self._volume_parcel_plant_2024[:, parcel_idx], label='Volume Parcel Plant 2024', linestyle='--', marker='o')

        #for i, value in enumerate(self._volume_parcel_plant_2023[:, parcel_idx]):
        #    plt.text(self._labels['2023'][i], value, str(value), fontsize=9, ha='right')
        for i, value in enumerate(self._volume_parcel_plant_2024[:, parcel_idx]):
            plt.text(self._labels['2024'][i], value, str(value), fontsize=9, ha='right', va='bottom')

        plt.title(f"Volume parcel {parcel_idx} over time")
        plt.ylabel('Volume')
        plt.show()

    def show_parcel_density(self, parcel_idx: int) -> None: 

        plt.figure(figsize=(15, 6))
        #plt.plot(self._labels['2023'], self._density_parcel_plant_2023[:, parcel_idx], label='Density Parcel Plant 2023', linestyle='--', marker='o')
        plt.plot(self._labels['2024'], self._density_parcel_plant_2024[:, parcel_idx], label='Density Parcel Plant 2024', linestyle='--', marker='o')

        #for i, value in enumerate(self._density_parcel_plant_2023[:, parcel_idx]):
        #    plt.text(self._labels['2023'][i], value, str(value), fontsize=9, ha='right')
        for i, value in enumerate(self._density_parcel_plant_2024[:, parcel_idx]):
            plt.text(self._labels['2024'][i], value, str(value), fontsize=9, ha='right', va='bottom')

        plt.title(f"Density parcel {parcel_idx} over time")
        plt.ylabel('Density')
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
