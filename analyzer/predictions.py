import enchant
import numpy as np


def predict_post_(post,predict,model=None):
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
            sentement = predict(post,model)
            print('try')
            print(sentement)
            if np.argmax(sentement):
                return "Positive"
            else:
                return "negative"
        except Exception as e :
            print(str(e))

    else:
        print(true_words, "\n", "prediction faild, not enogh data")
