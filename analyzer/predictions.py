import re
import enchant
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
def predict_post(post_):
    """
    This Function predict the given post if it recommended or not based on the training and testing of the previous posts

    Args:
        post_:String
    Return:
        Recommended or Not recommended
    """
    max_features=2000
    english = enchant.Dict("en_US")
    tokenizer = Tokenizer(num_words=max_features, split=' ')
    sequence__ = tokenizer.texts_to_sequences([post_])

    sequence = pad_sequences(sequence__, maxlen=len(post_), value=0)

    #Needed for model
    embed_dim = 200
    lstm_out = 200

    model = Sequential()
    model.add(Embedding(max_features, embed_dim,input_length = X.shape[1]))
    model.add(SpatialDropout1D(0.4))
    model.add(LSTM(lstm_out, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(2,activation='softmax'))
    model.compile(loss = 'categorical_crossentropy', optimizer='adam',metrics = ['accuracy'])

    sentiment = model.predict(sequence, batch_size=32, verbose=2)

    

    clean_post = re.sub(r"[^a-zA-Z0-9 \n\.]", "", post_)
    list_of_words = clean_post.split()
    true_words = list()
    for word in list_of_words:
        if english.check(word):
            true_words.append(word)

    if len(true_words) == len(list_of_words):
        try:
            print(predict_post(post_), post_[:30])
        except:
            print(post_, "\n", "has non english words")
    # return "Positive" if np.argmax(sentiment) else "negative"
    # [post_prediction(post) for post in post_sample]
    # return 'Recommended'