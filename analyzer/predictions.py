import re

import enchant
import numpy as np



def predict_post(post, page_name,model):
    """
    This Function predict the given post if it recommended or not based on the training and testing of the previous posts
    Args:
        post_:String
    Return:
        Recommended or Not recommended
    """

    

    english = enchant.Dict("en_US")

    clean_post = re.sub(r"[^a-zA-Z0-9 \n\.]", "", post)
    for word in post:

        list_of_words = clean_post.split()
        true_words = list()
        for word in list_of_words:
            if english.check(word):
                true_words.append(word)
            sentement = None
            if len(true_words) == len(list_of_words):
                try:
                    sentement = model.predict_post(page_name)
                except:
                    print(post, "\n", "has non english words")

        if np.argmax(sentement):
            return "Positive"
        else:
            return "negative"
