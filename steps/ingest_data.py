import logging
import pandas as pd 
from zenml import step

class IngestData:
    # ingesting data from path
    def __init__(self, path: str):
        # initialize the path
        self.path = path

    def get_data(self):
        # read the data from the path
        logging.info(f'Ingesting data from {self.path}...')
        # return the data
        return pd.read_csv(self.path)

@step
def ingest_df(path: str) -> pd.DataFrame:
    # Instantiate the class and call the method
    try:
        ingest_data = IngestData(path)
        df = ingest_data.get_data()
        return df
    except Exception as e:
        logging.error(f'Error ingesting data: {e}')
        raise e
