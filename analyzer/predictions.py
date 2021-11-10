import re

import enchant
from keras.layers import LSTM, Dense, Embedding, SpatialDropout1D
from keras.models import Sequential
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer


def predict_post(post_):
    """
    This Function predict the given post if it recommended or not based on the training and testing of the previous posts
    Args:
        post_:String
    Return:
        Recommended or Not recommended
    """
    pass
