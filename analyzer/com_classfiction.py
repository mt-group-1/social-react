import warnings

import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

warnings.filterwarnings("ignore")


def classify_comments(text_file, page_name):

    """
    Description:
    This function recives a text file and convert it into csv file to enable to label the comments inside that file, also this function use the nltk library whuch called vader to be enable to give percentages for positive,negative and neutral impact

    Args:
        text_file:text file
    Returns:
        new_text_file: text file with labeled data
    """
    nltk.download("vader_lexicon")

    df = pd.read_csv("%s" % text_file, names=["comments"], sep="\t")

    # Cleaning data from emails,number and special characters to be more accurate
    
    df['sentance'] = df['sentance'].str.replace("^\d+\s|\s\d+\s|\s\d+$", ' ')
    df['sentance'] = df['sentance'].str.replace('"', '')
    df['sentance'] = df['sentance'].str.replace('*', '')
    df['sentance'] = df['sentance'].str.replace('/[^@\s]*@[^@\s]*\.[^@\s]*/', '')
    df['sentance'] = df['sentance'].str.replace('"/[a-zA-Z]*[:\/\/]*[A-Za-z0-9\-_]+\.+[A-Za-z0-9\.\/%&=\?\-_]+/i"', '')
    df['sentance'] = df['sentance'].str.replace('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))', '')
    df['sentance'] = df['sentance'].str.replace('https://', '')

    sid = SentimentIntensityAnalyzer()
    new_words = {
    'over': -0.5,
    'garbage': -2.0,
    'dumpster': -3.1,
    ':(':-1,
    'refuses':-1,
    'down':-1,
    'crashed':-2,
    'Amen':1,
    'Available':1,
    '#Save':1,
    'always':0.5
                }
    sid.lexicon.update(new_words)
    # Create new coloums for positive and negative percentages
    df['impactPers'] = df['sentance'].apply(lambda sentance: sid.polarity_scores(sentance))
    df['posPers']  = df['impactPers'].apply(lambda score_dict: score_dict['pos'])
    df['negPers']  = df['impactPers'].apply(lambda score_dict: score_dict['neg'])
    df['neuPers']  = df['impactPers'].apply(lambda score_dict: score_dict['neu'])
    df['comPers']  = df['impactPers'].apply(lambda score_dict: score_dict['compound'])

    # Labeling the data depending on the above persentages
    def label_race(row):
        """
        This is a helper function that gives a positive or negative impact for each comment based on the persentages

        Args:
            row :String

        Returns:
            String (N) or Integer 
        """
        if row['comPers']  >= 0.02 :
            return 1
        elif row['comPers']  <= -0.02:
            return -1
        else:
            return 0

    # Create new coloumn for the final labels
    df["labels"] = df.apply(lambda row: label_race(row), axis=1)

    # Create new file containing two coloumns
    new_df = df[["comments", "labels"]]

    new_df.to_csv("./data/%s_comments.txt" % page_name)

    return new_df
