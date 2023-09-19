import os
from typing import Any, Dict, Literal, Optional

import pandas as pd
from pydantic import (
    BaseModel,
    computed_field,
    model_validator,
)
from sklearn.model_selection import train_test_split
from supabase import create_client

from sentiment_analysis.exception import CustomException
from sentiment_analysis.logging_config import logging
from sentiment_analysis.utils.utils import get_from_dict_or_env


class DataIngestionConfig(BaseModel):
    """
    class responsible for holding the paths of the data
    """

    raw_data_path: str = os.path.join("artifacts", "raw_data.csv")
    train_data_path: str = os.path.join("artifacts", "train_data.csv")
    test_data_path: str = os.path.join("artifacts", "test_data.csv")

    class ConfigDict:
        """pydantic forbidding extra parameters"""

        extra = "forbid"


class DataIngestion(BaseModel):
    DataIngestionConfig: DataIngestionConfig = DataIngestionConfig()
    """raw , train , test data paths"""

    supabase_key: Optional[str] = None
    supabase_url: Optional[str] = None
    """api keys to read data from database"""

    ingestion_type: Literal["csv", "db"]
    """either choose to ingest data from a csv or from a supabase table"""

    table_name: Optional[str] = None
    """table name in supabase database"""

    data_path: Optional[str] = None
    """path where the csv files will be stored"""

    save_csv: Literal[True, False] = True
    """whether to save the csv files or not"""

    class ConfigDict:
        """pydantic forbidding extra parameters"""

        extra = "forbid"

    @model_validator(mode="after")
    def check_tablename(self) -> "DataIngestion":
        table = self.table_name
        path = self.data_path
        if self.ingestion_type == "csv" and path is None:
            raise ValueError("table_name cannot be None when ingestion_type is 'csv")
        elif self.ingestion_type == "db" and table is None:
            raise ValueError("table_name cannot be None when ingestion_type is 'db")

        return self

    @model_validator(mode="before")
    @classmethod
    def validate_environement(cls, values: Dict) -> Dict:
        if values["ingestion_type"] == "db":
            values["supabase_key"] = get_from_dict_or_env(
                values, "supabase_key", "SUPABASE_KEY"
            )
            values["supabase_url"] = get_from_dict_or_env(
                values, "supabase_url", "SUPABASE_URL"
            )
        return values

    @computed_field
    def supabase_client(self) -> Any:
        """supabase session to query over the database's tables"""
        return create_client(str(self.supabase_url), str(self.supabase_key))

    def _read_from_db(self) -> tuple:
        """
        read data from database

        return :
            train , test data as a tuple of pandas dataframe
        """
        logging.info("read data from database")
        client = self.supabase_client
        response = client.table(self.table_name).select("*").execute()  # type: ignore
        df = pd.DataFrame(response.data)
        train, test = self._split_data(df)
        return train, test

    def _read_from_csv(self):
        """
        read data from csv

        return :
            train , test data as a tuple of pandas dataframe
        """
        logging.info("read data from csv")
        df = pd.read_csv(self.data_path)
        train, test = self._split_data(df)
        return train, test

    def _split_data(self, dataframe: pd.DataFrame) -> tuple:
        """
        split data into train and test dataframes and save as csv

        return :
            train , test data as a tuple of pandas dataframe
        """
        logging.info("split data into train and test")

        train, test = train_test_split(dataframe, test_size=0.2, random_state=42)

        if self.save_csv:
            os.makedirs(
                os.path.dirname(self.DataIngestionConfig.raw_data_path), exist_ok=True
            )

            train.to_csv(self.DataIngestionConfig.train_data_path, index=False)
            test.to_csv(self.DataIngestionConfig.test_data_path, index=False)

        return train, test

    def run_ingestion(self) -> tuple:
        """
        run the data ingestion
        """
        try:
            logging.info("running ingestion")
            if self.ingestion_type == "csv":
                train, test = self._read_from_csv()
            else:
                train, test = self._read_from_db()

            return train, test
        except Exception as e:
            raise CustomException(e)
