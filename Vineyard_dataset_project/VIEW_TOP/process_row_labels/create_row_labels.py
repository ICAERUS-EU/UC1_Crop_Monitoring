
import numpy as np
import os 
import json

# Save row labels
base_path = './../../data/'
base_path_features = base_path + 'features/'



row_labels = [1,0,1,0,0,0,0,0,1,1,0,0,
              1,0,0,1,1,0,0,0,1,0,0,0,
              1,0,1,0,1,0,0,1,0,0,
              1,0,1,0,1,0,0,0,0,1,
              0,0,0,0,0,0,0,0,1,0]


# Savel row_labels
output_path = base_path_features + 'row_labels.json'
with open(output_path, 'w') as f:
    json.dump(row_labels, f)
