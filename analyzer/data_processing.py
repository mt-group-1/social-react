# Import needed libraries
import pandas as pd
import numpy as np
from com_classfiction import classify_comments
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
# Import needed libriries for second model
import tensorflow as tf
print(tf.__version__)
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
import re

def get_data(file_name,page_name=classify_comments()):
    """
    This Function gets a facebook page posts and likes 
    
    Args:
       File_Name: String
       page_name: String

    Returns : String contains predicted positive and negative counts
    
    """
    #Creating Csv file
    my_df=pd.read_csv(f'{file_name}.txt')
    my_df
    sentences = my_df['sentance'].values

    #Length of selected sentances
    len(sentences)
    y = my_df['race_label']

    #Spliting into test and train subsets
    sentences_train, sentences_test, y_train, y_test = train_test_split(sentences, y, test_size=0.33, random_state = 42)

    #Length of selected training sentances

    len_sentence_train = len(sentences_train)

    # Initilize vectorizer
    vectorizer = CountVectorizer()
    vectorizer.fit(sentences_train)
    X_train = vectorizer.transform(sentences_train)
    X_test  = vectorizer.transform(sentences_test)
    classifier = LogisticRegression()
    classifier.fit(X_train, y_train)
    score = classifier.score(X_test, y_test)

    #Check Score 
    print('score -> ',score)

    # Model Two
    fb_df = my_df
    fb_df.columns = map(str.lower, fb_df.columns)
    fb_df.shape

    #Training Data

    fb_df['sentance'] = fb_df['sentance'].apply(lambda x: x.lower())
    fb_df['sentance'] = fb_df['sentance'].apply((lambda x: re.sub('[^a-zA-z0-9\s]','',x)))
    max_features = 2000
    tokenizer = Tokenizer(num_words=max_features, split=' ')

    X = tokenizer.texts_to_sequences(fb_df['comment'].values)
    X = pad_sequences(X)
    fb_df.sentiment.value_counts()

    Y = pd.get_dummies(fb_df['sentiment']).values
    X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.40, random_state=1000)
    print(X_train.shape,Y_train.shape)
    print(X_test.shape,Y_test.shape)

    embed_dim = 200
    lstm_out = 200

    model = Sequential()
    model.add(Embedding(max_features, embed_dim,input_length = X.shape[1]))
    model.add(SpatialDropout1D(0.4))
    model.add(LSTM(lstm_out, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(2,activation='softmax'))
    model.compile(loss = 'categorical_crossentropy', optimizer='adam',metrics = ['accuracy'])
    print(model.summary())


    # hist = model.fit(X_train, Y_train, epochs = 7, batch_size=32, verbose = 2) It was not used in the notebook

    score,acc = model.evaluate(X_test,Y_test)

    # .2f Limiting floats to two decimal points
    print("score    --> %.2f" % (score)) 
    print("accuracy -->  %.2f" % (acc))

    # Model accuracy score in predicting (positive,negative)
    comments = list()
    for comment in fb_df["sentance"]:
        comments.append(comment)
    validation_size = len(comments)
    X_validate = X_test[-validation_size:]
    Y_validate = Y_test[-validation_size:]
    x_test = X_test[:-validation_size]
    y_test = Y_test[:-validation_size]
    X_validate

    #Specifying Parameters
    pos_cnt, neg_cnt, pos_correct, neg_correct = 0, 0, 0, 0

    for x in range(len(X_validate)):
        result = model.predict(X_validate[x].reshape(1,x_test.shape[1]),verbose = 2)[0]
        if np.argmax(result) == np.argmax(Y_validate[x]):
            if np.argmax(Y_validate[x]) == 0:
                neg_correct += 1
            else:
                pos_correct += 1
        if np.argmax(Y_validate[x]) == 0:
            neg_cnt += 1
        else:
            pos_cnt += 1
    return f'The Positive count is{pos_correct/pos_cnt*100},"%", also, The Negative count is {neg_correct/neg_cnt*100}"%"'
# print("positive_acc", pos_correct/pos_cnt*100, "%")
# print("negative_acc", neg_correct/neg_cnt*100, "%")
    