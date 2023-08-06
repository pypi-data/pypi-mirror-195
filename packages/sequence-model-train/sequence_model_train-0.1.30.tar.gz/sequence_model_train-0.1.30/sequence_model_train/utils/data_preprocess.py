import pandas as pd


# load data
def load_dataset(data_path=None, dtype='pandas'):
    data = pd.read_csv(data_path)
    return data


# Split the dataset into training and validation sets
def split_train_valid(data):
    '''
    Split the dataset into training and validation sets
    where 80% of the data is used for training
    and 20% is used for validation.
    '''
    train_size = int(data.shape[0] * 0.8)
    train_dataset, valid_dataset = data[0:train_size], data[train_size:]
    return train_dataset, valid_dataset
