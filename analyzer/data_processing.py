import os
import re
import warnings

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
import pandas as pd
from keras.layers import LSTM, Dense, Embedding, SpatialDropout1D
from keras.models import Sequential
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from nltk import tree
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from termcolor import colored
warnings.filterwarnings('ignore')
from analyzer.com_classfiction import classify_comments


class ModelCreator:
    """
    class that analyze classified data
    """

    def __init__(self, page_name):
        self.page_name = page_name
        self.model = None
        self.score = None
        self.positive_ratio = None
        self.negative_ratio = None

    # Slearn
    def page_comments(self):
        print("classifying page comments ...")
        try:
            df = classify_comments("./data/%s/comments.csv" % self.page_name, self.page_name)
            self.df_comments_list = df[df.labels != 'N']
            
            self.comments = self.df_comments_list["comments"].values
            
            impact = self.df_comments_list["labels"].value_counts().index.tolist()[0]

            results = ''
            
            if not impact :
                results = colored(("This page has NEGATIVE impact on its followers"),"red")
            else:
                results =  colored(("This page has POSITIVE impact on its followers"),"green")

            return results
            
        except Exception as e:
            raise Exception(str(e))

    def random_partitions(self):
        try:
            y = self.df_comments_list["labels"]
            (
                self.comments_train,
                self.comments_test,
                self.y_train,
                self.y_test,
            ) = train_test_split(self.comments, y, test_size=0.33, random_state=42)

            return True
        except Exception as e:
            raise Exception(str(e))

    def vectorize(self):
        try:
            self.vectorizer = CountVectorizer()
            self.vectorizer.fit(self.comments_train)

            self.X_train = self.vectorizer.transform(self.comments_train)
            self.X_test = self.vectorizer.transform(self.comments_test)

            # score
            classifier = LogisticRegression()

            classifier.fit(self.X_train, self.y_train)

            self.vscore = classifier.score(self.X_test, self.y_test)

            return True
        except Exception as e:
            raise Exception(str(e))

    # using keras
    def keras(self):
        try:
            df_comments = self.df_comments_list
            df_comments.columns = map(str.lower, df_comments.columns)
            df_comments["comments"] = df_comments["comments"].apply(lambda x: x.lower())

            self.tokenizer = Tokenizer(num_words=500, split=" ")
            self.tokenizer.fit_on_texts(df_comments["comments"].values)
            X = self.tokenizer.texts_to_sequences(df_comments["comments"].values)
            self.X = pad_sequences(X)
            self.Y = pd.get_dummies(df_comments["labels"]).values

            X_train, X_test, Y_train, Y_test = train_test_split(
                self.X, self.Y, test_size=0.40, random_state=1000
            )
            
            self.keras_rp = [X_train, X_test, Y_train, Y_test]

            return True
        except Exception as e:
            raise Exception(str(e))

    def keras_model(self):
        try:
            embed_dim = 200
            lstm_out = 200

            model = Sequential()

            model.add(Embedding(500, embed_dim, input_length= self.X.shape[1]))
            model.add(SpatialDropout1D(0.4))
            model.add(LSTM(lstm_out, dropout=0.2, recurrent_dropout=0.2))
            model.add(Dense(2, activation="softmax"))
            model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
                
            self.model = model

            return True
        except Exception as e:
            raise Exception(str(e))

    def train_model(self):
        try:

            X_train, X_test, Y_train, Y_test = self.keras_rp

            self.model.fit(X_train, Y_train, epochs=3, batch_size=15, verbose=2)

            score, acc = self.model.evaluate(X_test, Y_test)
            
            model_score = "score    --> %.2f" % score
            model_accuracy = "accuracy -->  %.2f" % acc
            print(model_score, model_accuracy)

            return model_score, model_accuracy

        except Exception as e:
            raise Exception(str(e))

    def save_the_model(self):
        try:
            self.model.save("../data/%s/" % self.page_name)
            return True
        
        except Exception as e:
            raise Exception(str(e))

    def validate_acc(self):
        try:
            X_train, X_test, Y_train, Y_test = self.keras_rp

            validation_size = 500

            X_validate = X_test[-validation_size:]
            Y_validate = Y_test[-validation_size:]
            x_test = X_test[:-validation_size]
            y_test = Y_test[:-validation_size]

            pos_cnt, neg_cnt, pos_correct, neg_correct = 0, 0, 0, 0
            for x in range(len(X_validate)):
                result = self.model.predict(
                    X_validate[x].reshape(1, x_test.shape[1]), verbose=2
                )[0]

                if np.argmax(result) == np.argmax(Y_validate[x]):

                    if np.argmax(Y_validate[x]) == 0:
                        neg_correct += 1
                    else:
                        pos_correct += 1

                if np.argmax(Y_validate[x]) == 0:
                    neg_cnt += 1
                else:
                    pos_cnt += 1

            self.keras_prediction_results = {
                "positive_acc ": str(pos_correct / pos_cnt * 100),
                "negative_acc": str(neg_correct / neg_cnt * 100),
            }

            self.save_the_model()
            return self.keras_prediction_results

        except Exception as e:
            raise Exception(str(e))
    def predict_post(self,post,model):
        sequence = self.tokenizer.texts_to_sequences([post])
        sequence = pad_sequences(sequence, maxlen=len(post), value=0)
        sentiment = model.predict(sequence, batch_size=32, verbose=2)
        return sentiment

# model = ModelCreator("cnn")
# model.page_comments()
# model.keras()
# model.keras_model()
# model.train_model()
# model.save_the_model()
