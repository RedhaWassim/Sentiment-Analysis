import numpy as np
import pandas as pd
from nltk.tokenize import RegexpTokenizer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import MinMaxScaler
import spacy
nlp = spacy.load("en_core_web_sm")


class ColumnDropperTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, feature_name: list):
        self.feature_name = feature_name

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        for column in self.feature_name:
            if column in X.columns:
                X = X.drop(columns=column,axis=1)
        return X


class TextMissingValueTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, column_to_process):
        self.column_to_process = column_to_process

    def _format_deleted(self, text):
        if text == "[Deleted]":
            return None
        return text

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        # Apply missing value handling to the specified column
        for column in self.column_to_process:
            X[column] = X[column].apply(self._format_deleted)
        X = X.dropna(subset=self.column_to_process)
        return X


class BoolValueTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, column_to_process):
        self.column_to_process = column_to_process

    def _bool_to_int(self, text):
        try:
            return int(text)
        except:
            return text

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        # Apply the _bool_to_int function to the specified column
        X[self.column_to_process] = X[self.column_to_process].astype(int)
        return X


class CharacterCounter(BaseEstimator, TransformerMixin):
    """Count the number of characters in a document."""

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X["n_characters"] = X.iloc[:, 0].str.len()
        return X



class LowerCaseTransformer(BaseEstimator,TransformerMixin):
    """Count the number of characters in a document."""

    def __init__(self,columns):
        self.columns=columns

    def fit(self, X, y=None):
        return self
    def to_low(self,text):
        return text.lower()
    def transform(self, X, y=None):
        for col in self.columns:
            X[col] = X[col].apply(self.to_low)

        return X


class TokenizerTransformer(TransformerMixin):
    def __init__(self,columns):
        self.columns=columns
    def tokenize_text(self, text):
        doc = nlp(text)
        return [token.text for token in doc]
    
    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, y=None):
        # Tokenize the specified column in the DataFrame
        for col in self.columns :
            X[col] = X[col].apply(self.tokenize_text)
        return X
    

