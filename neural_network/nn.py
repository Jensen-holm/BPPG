from typing import Callable
from sklearn.preprocessing import StandardScaler
import pandas as pd


class NN:
    def __init__(
        self,
        epochs: int,
        hidden_size: int,
        learning_rate: float,
        test_size: float,
        activation: str,
        features: list[str],
        target: str,
        data: pd.DataFrame,
    ):
        self.epochs = epochs
        self.hidden_size = hidden_size
        self.learning_rate = learning_rate
        self.test_size = test_size
        self.activation = activation
        self.features = features
        self.target = target
        self.data = data

        self.loss_hist: list[float] = None
        self.func_prime: Callable = None
        self.func: Callable = None
        self.X: pd.DataFrame = None
        self.y: pd.DataFrame = None
        self.y_dummy: pd.DataFrame = None
        self.input_size: int = None
        self.output_size: int = None

    def set_df(self, df: pd.DataFrame) -> None:
        assert isinstance(df, pd.DataFrame)
        x = df[self.features]
        y = df[self.target]
        self.X = pd.get_dummies(x, columns=self.features)
        self.y_dummy = pd.get_dummies(y, columns=self.target)
        self.input_size = len(self.X.columns)
        self.output_size = len(self.y_dummy.columns)

    def normalize(self):
        scaler = StandardScaler()
        self.y_dummy = scaler.fit_transform(self.y_dummy)
        self.X = scaler.fit_transform(self.X)

    def set_func(self, f: Callable) -> None:
        assert isinstance(f, Callable)
        self.func = f

    def set_func_prime(self, f: Callable) -> None:
        assert isinstance(f, Callable)
        self.func_prime = f

    @classmethod
    def from_dict(cls, dct):
        """ Creates an instance of NN given a dictionary
        we can use this to make sure that the arguments are right
        """
        return cls(**dct)