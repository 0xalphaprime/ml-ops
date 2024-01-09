import logging
from abc import ABC, abstractmethod
from typing import Union
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

class DataStrategy(ABC):
    # abstract class for handling data
    @abstractmethod
    def handle_data(self, df: pd.DataFrame) -> Union[pd.DataFrame, pd.Series]:
        pass


class DataPreProcessStrategy(DataStrategy):
    # class for preprocessing data

    def handle_data(self, df: pd.DataFrame) ->pd.DataFrame:
        try:
            df = df.drop(
                [
                    'order_approved_at',
                    'order_delivered_carrier_date',
                    'order_delivered_customer_date',
                    'order_estimated_delivery_date',
                    'order_purchase_timestamp',
                ],
                axis=1,
            )
            df["product_weight_g"].fillna(df["product_weight_g"].median(), inplace=True)
            df["product_length_cm"].fillna(df["product_length_cm"].median(), inplace=True)
            df["product_height_cm"].fillna(df["product_height_cm"].median(), inplace=True)
            df["product_width_cm"].fillna(df["product_width_cm"].median(), inplace=True)
            # write "No review" in review_comment_message column
            df["review_comment_message"].fillna("No review", inplace=True)

            df = df.select_dtypes(include=[np.number])
            columns_to_drop = ['customer_zip_code_prefix', 'order_item_id']
            df = df.drop(columns_to_drop, axis=1)
            return df
        except Exception as e:
            logging.error(e)
            raise e
        
class DataSplitStrategy(DataStrategy):
    # class for splitting our data
    pass