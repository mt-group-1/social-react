""""
import library that will be used in the our code 
"""
import os
import sys
import warnings

import nltk
import numpy as np
import pandas
import pandas as pd
import sklearn
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.corpus import stopwords
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.tokenize import word_tokenize
from scipy import signal
from scipy.io import wavfile
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

warnings.filterwarnings('ignore')

def load_data(path):
    
    # nltk.download('punkt') 
    # nltk.download('stopwords')
    """
    This function is called load_data which reads a file containing  comments and it has a label for each comment .
    then  Processing and organizing data through a set of operations, then  extract the features from the comments
    Then divide the data into training and test data, and then get accuracy using machine learning model.
        
        Args:
            load_data: file path
        Process Done Inside the load_data Function:
        1. read the txt file
        2. process data and clean it 
        3. extract feature in the data and save it
        4. split the data in the train and test 
        5. use a SCV model for tran data and get accurcy
        
        Returns :   
        Accuracy of classification the commit
        """

    df = pd.read_csv(path)

    df = df[df.labels != 'N']

    classes = df['labels']

    encoder = LabelEncoder()

    Y = encoder.fit_transform(classes)

    text_messages = df['comments']

    processed = text_messages.str.replace(r'^.+@[^\.].*\.[a-z]{2,}$', 'emailaddress')
    processed = processed.str.replace(r'\d+(\.\d+)?', 'numbr')
    processed = processed.str.replace(r'[^\w\d\s]', ' ')
    processed = processed.str.replace(r'\s+', ' ')
    processed = processed.str.replace(r'^\s+|\s+?$', '')
    processed = processed.str.lower()

    stop_words = set(stopwords.words('english'))
    processed = processed.apply(lambda x: " ".join(x.lower() for x in str(x).split() \
                                    if x not in stop_words))
    ps = nltk.PorterStemmer()
    

    processed = processed.apply(lambda x: ' '.join(
    ps.stem(term) for term in x.split()))

    all_words = []
    
    for message in processed:
        words = word_tokenize(message)
        for w in words:
            all_words.append(w)
    all_words = nltk.FreqDist(all_words)
    # print('Number of words: {}'.format(len(all_words)))
    # print('Most common words: {}'.format(all_words.most_common(15)))
    word_features = list(all_words.keys())[:1500]
    
    def find_features(message):
        words = word_tokenize(message)
        features = {}
        for word in word_features:
            features[word] = (word in words)
        return features
 
    # features = find_features(processed[8])
    
    # for key, value in features.items():

    #     if value == True:

    #         print("The Key",key)





    messages = list(zip(processed, Y))
    seed = 1
    np.random.seed = seed
    np.random.shuffle(messages)
    featuresets = [(find_features(text), label) for (text, label) in messages]
    from sklearn import model_selection
    training, testing = model_selection.train_test_split(featuresets, test_size = 0.25, random_state=seed)
    # print("training len ",len(training))
    # print("testing len ", len(testing))
    
    model = SklearnClassifier(SVC(kernel = 'linear'))

   
    model.train(training)

   
    accuracy = nltk.classify.accuracy(model, testing)*100
    # print("SVC Accuracy: {}".format(accuracy))
    return accuracy
    

# process = load_data('./data/google/classified_comments.txt')

# df = pd.read_csv('../data/google/comments.txt')
# df = df[df.labels != '
# load_data("./data/google/classified_comments.txt")