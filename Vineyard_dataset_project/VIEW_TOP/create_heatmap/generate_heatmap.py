
import numpy as np 
import matplotlib.pyplot as plt 

# Create a random 2D array for demonstration
data = np.random.random((10, 10))

# Create a heatmap
plt.imshow(data, cmap='viridis')#, interpolation='nearest')
plt.colorbar()  # Add colorbar on the right side

# Show the plot
plt.show()