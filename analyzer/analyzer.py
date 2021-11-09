
""""
import library that will be used in the our code 

"""
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.svm import SVC
import nltk
from nltk.corpus import stopwords
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
import sys
import nltk
import sklearn
import pandas
import numpy as np
import os
from scipy.io import wavfile
from scipy import signal
from nltk.tokenize import word_tokenize
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# from pydub import AudioSegment
# import matplotlib.pyplot as plt
# import matplotlib.mlab as mlab


"""
    This Function called a load_data that  read a file  that contain the commints with label will return a clean commint for processing 
    
    Args:
        load_data: file path
    
    Returns : stord new clean  commint with new label 

    """
    
def load_data(path):
    df = pd.read_csv(path)
    df = df[df.labels != 'N']
    print(df.head(10))
    # print useful information about the dataset
    print(df.info())
    print(df.head())
    print(df.tail())
    print(df.columns)
    #  check class distribution  print number of postive commint and number of negative commint in our file
    classes = df['labels']
    print(classes.value_counts())
    # convert class labels to values, 0 = negative and 1 = postive
    encoder = LabelEncoder()
    Y = encoder.fit_transform(classes)
    print(Y[:10])
    #  store the commint data
    text_messages = df['comments']
    print(text_messages[:1])

     # use regular expressions to replace email addresses, URLs, phone numbers, other numbers

     # Replace email addresses with 'email'
    processed = text_messages.str.replace(r'^.+@[^\.].*\.[a-z]{2,}$', 'emailaddress')

            
     # Replace numbers with 'numbr'
    processed = processed.str.replace(r'\d+(\.\d+)?', 'numbr')

    print(df['comments'])

     # Remove punctuation
    processed = processed.str.replace(r'[^\w\d\s]', ' ')

     # Replace whitespace between terms with a single space
    processed = processed.str.replace(r'\s+', ' ')

     # Remove leading and trailing whitespace
    processed = processed.str.replace(r'^\s+|\s+?$', '')

    processed = processed.str.lower()
   # Now lets do it for all the messages
    nltk.download('stopwords')


        #  remove stop words from commint

    stop_words = set(stopwords.words('english'))

    processed = processed.apply(lambda x: " ".join(x.lower() for x in str(x).split() \
                                    if x not in stop_words))
        # print(processed)

         # Remove word stems using a Porter stemmer
    ps = nltk.PorterStemmer()

    processed = processed.apply(lambda x: ' '.join(
    ps.stem(term) for term in x.split()))


    nltk.download('punkt')  

    all_words = []
    for message in processed:
        words = word_tokenize(message)
        for w in words:
            all_words.append(w)
            
    all_words = nltk.FreqDist(all_words)


    # print the total number of words and the 15 most common words
    print('Number of words: {}'.format(len(all_words)))
    print('Most common words: {}'.format(all_words.most_common(15)))

    # use the 1500 most common words as features
    word_features = list(all_words.keys())[:1500]


    # # The find_features function will determine which of the 1500 word features are contained in the review
    def find_features(message):
        words = word_tokenize(message)
        features = {}
        for word in word_features:
            features[word] = (word in words)

        return features

    # an example!
    features = find_features(processed[8])
    for key, value in features.items():
        if value == True:
            print("The Key",key)





    messages = list(zip(processed, Y))

    # # # define a seed for reproducibility
    seed = 1
    np.random.seed = seed
    np.random.shuffle(messages)


 
    #  call find_features function for each SMS message
    featuresets = [(find_features(text), label) for (text, label) in messages]

    # # # we can split the featuresets into training and testing datasets using sklearn
    from sklearn import model_selection

# # # split the data into training and testing datasets
    training, testing = model_selection.train_test_split(featuresets, test_size = 0.25, random_state=seed)
    
    print("training len ",len(training))
    print("testing len ", len(testing))

    # # We can use sklearn algorithms in NLTK


    model = SklearnClassifier(SVC(kernel = 'linear'))

    # train the model on the training data
    model.train(training)

    # and test on the testing dataset!
    accuracy = nltk.classify.accuracy(model, testing)*100
    print("SVC Accuracy: {}".format(accuracy))




process =load_data('data/comments_classified.txt')

"""
    This Function called a remove_stopwords that  
    read that take a clean data and return new data without word stems and stopwords
    
    Args:
        remove_stopwords: data
    
    Returns :new clean data without word stems and stopwords
#     """
# def remove_stopwords(process):

#         nltk.download('stopwords')


#         #  remove stop words from commint

#         stop_words = set(stopwords.words('english'))

#         processed = process.apply(lambda x: " ".join(x.lower() for x in str(x).split() \
#                                     if x not in stop_words))
#         # print(processed)

#          # Remove word stems using a Porter stemmer
#         ps = nltk.PorterStemmer()

#         processed = processed.apply(lambda x: ' '.join(
#         ps.stem(term) for term in x.split()))

#         return(processed)

# processed =remove_stopwords(process)

# nltk.download('punkt')
#  # create bag-of-words

# """
#     This Function called a extract_features that  
#    extract the main keyword in data and save it
    
#     Args:
#         extract_features: data
    
#     Returns :features data
#     """

# def extract_features():
#     all_words = []
#     for message in processed:
#         words = word_tokenize(message)
#         for w in words:
#             all_words.append(w)
            
#     all_words = nltk.FreqDist(all_words)


#     # print the total number of words and the 15 most common words
#     print('Number of words: {}'.format(len(all_words)))
#     print('Most common words: {}'.format(all_words.most_common(15)))

#     # use the 1500 most common words as features
#     word_features = list(all_words.keys())[:1500]


#     # # The find_features function will determine which of the 1500 word features are contained in the review
#     def find_features(message):
#         words = word_tokenize(message)
#         features = {}
#         for word in word_features:
#             features[word] = (word in words)

#         return features

#     # an example!
#     features = find_features(processed[8])
#     for key, value in features.items():
#         if value == True:
#             print("The Key",key)

#    

# extract_features()











