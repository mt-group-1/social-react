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
        DataFrames: contains classified data with positive | negative | nutral  labels for each comment
    """

    # nltk.download("vader_lexicon")

    df = pd.read_csv("%s" % text_file, names=["comments"], sep="\t")

    # Cleaning data from emails,number and special characters to be more accurate

    df["comments"] = df["comments"].str.replace("^\d+\s|\s\d+\s|\s\d+$", " ")
    df["comments"] = df["comments"].str.replace('"', "")
    df["comments"] = df["comments"].str.replace("*", "")
    df["comments"] = df["comments"].str.replace("/[^@\s]*@[^@\s]*\.[^@\s]*/", "")
    df["comments"] = df["comments"].str.replace(
        '"/[a-zA-Z]*[:\/\/]*[A-Za-z0-9\-_]+\.+[A-Za-z0-9\.\/%&=\?\-_]+/i"', ""
    )
    df["comments"] = df["comments"].str.replace(
        "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))",
        "",
    )
    df["comments"] = df["comments"].str.replace("https://", "")
    df["comments"] = df["comments"].str.replace(r"\d+(\.\d+)?", "")
    sid = SentimentIntensityAnalyzer()

    new_words = {
        "over": -0.5,
        "garbage": -2.0,
        "dumpster": -3.1,
        ":(": -1,
        "refuses": -1,
        "down": -1,
        "crashed": -2,
        "Amen": 1,
        "Available": 1,
        "#Save": 1,
        "always": 0.5,
    }

    sid.lexicon.update(new_words)
    # Create new coloums for positive and negative percentages
    df["impactPers"] = df["comments"].apply(
        lambda comments: sid.polarity_scores(comments)
    )
    df["posPers"] = df["impactPers"].apply(lambda score_dict: score_dict["pos"])
    df["negPers"] = df["impactPers"].apply(lambda score_dict: score_dict["neg"])
    df["neuPers"] = df["impactPers"].apply(lambda score_dict: score_dict["neu"])
    df["comPers"] = df["impactPers"].apply(lambda score_dict: score_dict["compound"])

    # Labeling the data depending on the above persentages
    def label_race(row):
        """
        This is a helper function that gives a positive or negative impact for each comment based on the persentages
        Args:
            row :String
        Returns:
            String (N) or Integer
        """
        if row["comPers"] >= 0.02:
            return 1
        elif row["comPers"] <= -0.02:
            return 0
        else:
            return "N"

    # Create new coloumn for the final labels
    df["labels"] = df.apply(lambda row: label_race(row), axis=1)
    
    # Create new file containing two coloumns
    new_df = df[["comments", "labels"]]
    create_dir(page_name)
    new_df.to_csv("./data/%s/classified_comments.txt" % page_name)

    return new_df


def create_dir(page_name):
    import os

    dir_path = "./data/%s" % page_name.lower()
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
        return True
    else:
        return False
