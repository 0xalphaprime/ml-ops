import logging
import pandas as pd
from zenml import step
from src.data_cleaning import DataCleaning, DataPreProcessStrategy, DataSplitStrategy
from typing_extensions import Annotated
from typing import Tuple


@step
def clean_df(df: pd.DataFrame) -> Tuple[
    Annotated[pd.DataFrame, "X_train"],
    Annotated[pd.DataFrame, "X_test"],
    Annotated[pd.DataFrame, "y_train"],
    Annotated[pd.DataFrame, "y_test"],
]:
    try:
        # instantiate strategy
        process_strategy = DataPreProcessStrategy()
        # instantiate data cleaning class
        data_cleaning = DataCleaning(df, process_strategy)
        # call handle_data method
        processed_data = data_cleaning.handle_data()

        split_strategy = DataSplitStrategy()
        data_cleaning = DataCleaning(processed_data, split_strategy)
        X_train, X_test, y_train, y_test = data_cleaning.handle_data()
        return X_train, X_test, y_train, y_test
        logging.info("Data cleaning complete!")
    except Exception as e:
        logging.error("Error in cleaning data: {}".format(e))
        raise e

