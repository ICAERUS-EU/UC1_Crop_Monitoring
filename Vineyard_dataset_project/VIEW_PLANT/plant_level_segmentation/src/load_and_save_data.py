
"""

load_and_save_data.py - Utility Functions

This module contains a collection of utility functions for common tasks in the project.
These functions include file loading data and saving the model.


Class: 
    - `Dataset`: Load imgs and masks for training. 
Functions:
    - `train_and_save`: train and save model.


Usage:
    import load_save_data

    # Example usage of Dataset class:
    Dataset(X, y, n_classes)

"""



class Dataset(torch.utils.data.Dataset):
  def __init__(self, X, y, n_classes=3):
    self.X = X
    self.y = y
    self.n_classes = n_classes

  def __len__(self):
    return len(self.X)

  def __getitem__(self, ix):
    img = self.X[ix] #np.load(self.X[ix])
    mask = self.y[ix]#np.load(self.y[ix])
    img = torch.tensor(img).unsqueeze(0) 
    mask = (np.arange(self.n_classes) == mask[...,None]).astype(np.float32) 
    return img, torch.from_numpy(mask).permute(2,0,1)
  

'''def train_and_save_model(model, X_train, y_train): 

    model.compile(optimizer=Adam(learning_rate=0.0001), loss='mse')
    model.fit(X_train, y_train, epochs=30, batch_size=4, validation_split=0.2)
    model.save("my_model.keras")

    return model'''