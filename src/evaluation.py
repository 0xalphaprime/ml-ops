import logging
from abc import ABC, abstractmethod

import numpy as np
from sklearn.metrics import mean_squared_error, r2_score

class Evaluation(ABC):
    # abstract class for defining a strategy for evaluation of models

    @abstractmethod
    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray):
        pass

class MSE(Evaluation):
    # mean squared error

    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray):
        try:
            logging.info("Calculating MSE score")
            mse = mean_squared_error(y_true, y_pred)
            logging.info("MSE score: {}".format(mse))
            return mse
        except Exception as e:
            logging.error("Error calculating MSE score: {}".format(e))
            raise e


class R2(Evaluation):
    # r2 score

    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray):
        try:
            logging.info("Calculating R2 score")
            r2 = r2_score(y_true, y_pred)
            logging.info("R2 score: {}".format(r2))
            return r2
        except Exception as e:
            logging.error("Error calculating R2 score: {}".format(e))
            raise e 
        
class RMSE(Evaluation):
    # root mean squared error

    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray):
        try:
            logging.info("Calculating RMSE score")
            rmse = mean_squared_error(y_true, y_pred, squared=False)
            logging.info("RMSE score: {}".format(rmse))
            return rmse
        except Exception as e:
            logging.error("Error calculating RMSE score: {}".format(e))
            raise e