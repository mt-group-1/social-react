import pickle
import re

import enchant
import numpy as np
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer


def predict(post,model,page_name):
                
    with open('../data/%s/tokenizer.pickle' % page_name, 'rb') as handle:
        tokenizer = pickle.load(handle)
    
    sequence = tokenizer.texts_to_sequences([post])
    sequence = pad_sequences(sequence, maxlen=len(post), value=0)
    sentiment = model.predict(sequence, batch_size=32, verbose=2)
    return sentiment
    
def predict_post(post, page_name,model=None):
    """
    This Function predict the given post if it recommended or not based on the training and testing of the previous posts
    Args:
        post_:String
    Return:
        Recommended or Not recommended
    """

    

    english = enchant.Dict("en_US")

    clean_post = post
    list_of_words = clean_post.split()
    true_words = list()

    for word in list_of_words:
            if english.check(word):
                true_words.append(word)

    sentement = None
    if len(true_words) == len(list_of_words):
        true_words = " ".join(true_words)
        try:
            sentement = predict(post,page_name,model)
            if np.argmax(sentement):
                return "Positive"
            else:
                return "negative"
        except:
            print(true_words, "\n", "Has non english words")


