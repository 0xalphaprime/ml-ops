import logging
import pandas as pd
from zenml import step

from src.model_dev import LinearRegressionModel
from sklearn.base import RegressorMixin
from .config import ModelNameConfig

@step
def train_model(X_train: pd.DataFrame, 
    X_test: pd.DataFrame,
    y_train: pd.DataFrame, 
    y_test: pd.DataFrame,
    config: ModelNameConfig) -> RegressorMixin:
    
    
    try:
        model = None
        if config.model_name == "LinearRegression":
            model = LinearRegressionModel()
            trained_model = model.train(X_train, y_train)
            return trained_model
        else:
            logging.error("Model not implemented")
            raise NotImplementedError("Model not implemented")
    except Exception as e:
        logging.error("Error in training model: {}".format(e))
        raise e