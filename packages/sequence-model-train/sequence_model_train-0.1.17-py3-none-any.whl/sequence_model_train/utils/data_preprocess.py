import pandas as pd
from ..data import data_pipeline


# load data
def load_dataset(data_path=None, dtype='pandas'):
    data = pd.read_csv(data_path)
    return data


# processinig_data
def process_data(data):
    pipeline = data_pipeline.get_pipeline()
    pipeline.fit(data)
    data = pipeline.transform(data)
    data = data.drop(columns='DATE')
    return data
