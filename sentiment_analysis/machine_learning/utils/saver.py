import os
import pickle

from sentiment_analysis.exception import CustomException


def save_object(file_path, object):
    """function to save an object in input into a pkl file"""
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as f:
            pickle.dump(object, f)

    except Exception as e:
        raise CustomException(e)
