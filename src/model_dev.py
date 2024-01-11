import logging
from abc import ABC, abstractmethod
from sklearn.linear_model import LinearRegression

class Model(ABC):
    # Abstract class for models
    @abstractmethod
    def train(self, X_train, y_train):
        pass

class LinearRegressionModel(Model):
    # Linear Regression model
    def train(self, X_train, y_train, **kwargs):
        try:
            model = LinearRegression(**kwargs)
            model.fit(X_train, y_train)
            logging.info("Model training complete!")
            return model
        except Exception as e:
            logging.error("Error in training model: {}".format(e))
            raise e
        