import re

import enchant
import numpy as np



def predict_post(post, pagename,model):
    """
    This Function predict the given post if it recommended or not based on the training and testing of the previous posts
    Args:
        post:String
    Return:
        Recommended or Not recommended
    """
    


    english = enchant.Dict("en_US")

    clean_post = post
    

    list_of_words = clean_post.split()
    print("List of words",list_of_words)
    true_words = list()
    for word in list_of_words:
        if english.check(word):
            true_words.append(word)     
            continue     
    if len(true_words) == len(list_of_words):
        x=" ".join(true_words)
        sentement = model.predict()
        if np.argmax(sentement):
            print('inside')
            return "Positive"
        else:
            print('outside')
            return "negative"
    else:
        print(true_words, "\n", "Has non english words")