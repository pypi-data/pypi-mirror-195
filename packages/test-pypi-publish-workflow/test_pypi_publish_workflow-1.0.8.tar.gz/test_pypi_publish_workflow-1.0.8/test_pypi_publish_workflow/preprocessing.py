import abc
import logging
import os
from typing import Tuple

import pandas as pd

# abstract class to split data into train and test


class AbstractSplitter(abc.ABC):
    """
    An abstract method to split data into train and test.
    """

    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def load_dataframe(self, path: str) -> pd.DataFrame:
        return pd.read_csv(path)

    @abc.abstractmethod
    def split(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        pass

    def split_x_y(
        self, df_train, df_test, features, target
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        self.logger.info(
            f"""
        Splitting data into x_train, y_train, x_test, y_test
            x_train: {df_train[features].shape}
            y_train: {df_train[target].shape}
            x_test: {df_test[features].shape}
            y_test: {df_test[target].shape}
        """
        )

        data_dictionnary = {
            "x_train": df_train[features],
            "y_train": df_train[target],
            "x_test": df_test[features],
            "y_test": df_test[target],
        }

        return (
            data_dictionnary["x_train"],
            data_dictionnary["y_train"],
            data_dictionnary["x_test"],
            data_dictionnary["y_test"],
        )

    def save_data(self, data_dictionnary: dict[str, pd.DataFrame], path: str) -> None:
        self.logger.info(f"Saving data to {path}")
        self.create_folder(path)
        for key, value in data_dictionnary.items():
            save_path = os.path.join(path, f"{key}.csv")
            self.save_dataframe(value, save_path)

    def save_dataframe(self, df: pd.DataFrame, path: str) -> None:
        self.logger.info(f"Saving dataframe to {path}")
        df.to_csv(path, index=False)

    def create_folder(self, path: str) -> None:
        self.logger.info(f"Creating folder {path}")
        if not os.path.exists(path):
            os.makedirs(path)

    def log_column_info(self, df: pd.DataFrame, column: str) -> None:
        self.logger.info(
            f"""
        Giving additional information about {column}
            column: {column}
            column shape: {df[column].shape}
            unique values: {df[column].nunique()}
            min value: {df[column].min()}
            max value: {df[column].max()}
            """
        )
