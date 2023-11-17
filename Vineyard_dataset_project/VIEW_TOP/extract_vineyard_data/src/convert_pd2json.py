import pandas as pd

	
file_path = 'labelled_parcels.csv'
output_path= 'labelled_parcels.json'

df = pd.read_csv(file_path)
df.to_json(output_path, orient='records', lines=True)

