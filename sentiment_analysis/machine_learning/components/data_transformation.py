import os

import pandas as pd
from pydantic import BaseModel
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

from sentiment_analysis.exception import CustomException
from sentiment_analysis.logging_config import logging
from sentiment_analysis.machine_learning.components.transformers import (
    BoolValueTransformer,
    CharacterCounter,
    ColumnDropperTransformer,
    EmbedTransformer,
    LowerCaseTransformer,
    TextMissingValueTransformer,
    TokenizerTransformer,
)
from sentiment_analysis.machine_learning.utils.saver import save_object


class DataTransformationConfig(BaseModel):
    processor_file_path: str = os.path.join("artifacts", "preprocessor.pkl")


class DataTransformation(BaseModel):
    data_transformation_config: DataTransformationConfig = DataTransformationConfig()

    def init_transformer(self, data: pd.DataFrame) -> ColumnTransformer:
        """
        this function is responsible for creating the transformer object

        returns:
            processor : Sklearn ColumnTransformer

        """
        textual_columns = ["TITLE"]
        numerical_columns = ["SCORE", "NUM_COMMENTS"]
        categorical_columns = ["OVER_18"]
        drop_columns = ["POST_DATE", "id"]

        drop_transformer = Pipeline(
            [("column_dropper", ColumnDropperTransformer(drop_columns))]
        )

        num_pipeline = Pipeline(
            [
                ("imputer", SimpleImputer(strategy="mean")),
                ("scaler", MinMaxScaler()),
            ]
        )

        cat_pipeline = Pipeline(
            steps=[("bool_to_int", BoolValueTransformer(categorical_columns))]
        )

        text_pipeline = Pipeline(
            steps=[
                ("missing_values", TextMissingValueTransformer(textual_columns)),
                ("CharacterCounter", CharacterCounter()),
            ]
        )

        NLP_processing_pipeline = Pipeline(
            steps=[
                ("lower_case", LowerCaseTransformer(textual_columns)),
                ("tokenizer", TokenizerTransformer(textual_columns)),
                ("embed", EmbedTransformer()),
            ]
        )

        logging.info("Creating preprocessor object")

        preprocessor = ColumnTransformer(
            transformers=[
                ("textual", text_pipeline, textual_columns),
                ("nlp_processing", NLP_processing_pipeline, textual_columns),
                ("drop_transformer", drop_transformer, drop_columns),
                ("numerical", num_pipeline, numerical_columns),
                ("categorical", cat_pipeline, categorical_columns),
            ],
            remainder="passthrough",
        )

        logging.info("processor object created")

        return preprocessor

    def transform_df(self, data_train: pd.DataFrame, data_test: pd.DataFrame) -> tuple:
        """
        this function is responsible for transforming the data

        args :
            data_train : train data in a pandas dataframe format
            data_test : test data in a pandas dataframe format

        returns:
            train_transformed_data
            test_transformed_data
            self.data_transformation_config.processor_file_path : file path of the processor pkl

        """
        try:
            logging.info("getting transformer object")

            preprocessor = self.init_transformer(data_train)

            logging.info("preprocessing the data")
            textual_columns = ["TITLE"]
            numerical_columns = ["SCORE", "NUM_COMMENTS"]
            categorical_columns = ["OVER_18"]
            date_columns = ["YEAR", "MONTH", "DAY", "HOUR"]
            all_columns = (
                textual_columns
                + ["n_char", "tokenz", "embeddings"]
                + numerical_columns
                + categorical_columns
                + ["UPVOTE_RATIO"]
                + date_columns
            )
            train_transformed_data = preprocessor.fit_transform(data_train)
            test_transformed_data = preprocessor.transform(data_test)

            train_transformed_data = pd.DataFrame(
                train_transformed_data, columns=all_columns
            )
            test_transformed_data = pd.DataFrame(
                test_transformed_data, columns=all_columns
            )
            train_transformed_data.drop("TITLE", axis=1, inplace=True)
            train_transformed_data = train_transformed_data[
                [
                    "tokenz",
                    "embeddings",
                    "n_char",
                    "SCORE",
                    "NUM_COMMENTS",
                    "UPVOTE_RATIO",
                    "OVER_18",
                    "YEAR",
                    "MONTH",
                    "DAY",
                    "HOUR",
                ]
            ]

            test_transformed_data.drop("TITLE", axis=1, inplace=True)
            test_transformed_data = test_transformed_data[
                [
                    "tokenz",
                    "embeddings",
                    "n_char",
                    "SCORE",
                    "NUM_COMMENTS",
                    "UPVOTE_RATIO",
                    "OVER_18",
                    "YEAR",
                    "MONTH",
                    "DAY",
                    "HOUR",
                ]
            ]

            logging.info("preprocessing completed")

            save_object(
                file_path=self.data_transformation_config.processor_file_path,
                object=preprocessor,
            )

            return (
                train_transformed_data,
                test_transformed_data,
                self.data_transformation_config.processor_file_path,
            )

        except Exception as e:
            raise CustomException(e)

    def transform_csv(self, train_path: str, test_path: str):
        """
        this function is responsible for transforming the data

        args :
            train_path : train data path
            test_path : test data path

        returns:
            train_transformed_data
            test_transformed_data
            self.data_transformation_config.processor_file_path : file path of the processor pkl
        """
        try:
            logging.info("Reading train data")

            data_train = pd.read_csv(train_path)
            data_test = pd.read_csv(test_path)

            logging.info("getting transformer object")

            preprocessor = self.init_transformer(data_train)

            textual_columns = ["TITLE"]
            numerical_columns = ["SCORE", "NUM_COMMENTS"]
            categorical_columns = ["OVER_18"]
            date_columns = ["YEAR", "MONTH", "DAY", "HOUR"]

            all_columns = (
                textual_columns
                + ["n_char", "tokenz", "embeddings"]
                + numerical_columns
                + categorical_columns
                + ["UPVOTE_RATIO"]
                + date_columns
            )

            train_transformed_data = preprocessor.fit_transform(data_train)
            test_transformed_data = preprocessor.transform(data_test)

            train_transformed_data = pd.DataFrame(
                train_transformed_data, columns=all_columns
            )
            test_transformed_data = pd.DataFrame(
                test_transformed_data, columns=all_columns
            )

            train_transformed_data.drop("TITLE", axis=1, inplace=True)
            train_transformed_data = train_transformed_data[
                [
                    "tokenz",
                    "embeddings",
                    "n_char",
                    "SCORE",
                    "NUM_COMMENTS",
                    "UPVOTE_RATIO",
                    "OVER_18",
                    "YEAR",
                    "MONTH",
                    "DAY",
                    "HOUR",
                ]
            ]

            test_transformed_data.drop("TITLE", axis=1, inplace=True)
            test_transformed_data = test_transformed_data[
                [
                    "tokenz",
                    "embeddings",
                    "n_char",
                    "SCORE",
                    "NUM_COMMENTS",
                    "UPVOTE_RATIO",
                    "OVER_18",
                    "YEAR",
                    "MONTH",
                    "DAY",
                    "HOUR",
                ]
            ]

            preprocessor = self.init_transformer(data_train)

            logging.info("preprocessing the data")

            train_transformed_data = preprocessor.fit_transform(data_train)
            test_transformed_data = preprocessor.transform(data_test)

            logging.info("preprocessing completed")

            save_object(
                file_path=self.data_transformation_config.processor_file_path,
                object=preprocessor,
            )

            return (
                train_transformed_data,
                test_transformed_data,
                self.data_transformation_config.processor_file_path,
            )
        except Exception as e:
            raise CustomException(e)
