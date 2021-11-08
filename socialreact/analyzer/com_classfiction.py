import pandas as pd
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
def labeling(text_file):
    """
    Description:
    This function recives a text file and convert it into csv file to enable to label the comments inside that file, also this function use the nltk library whuch called vader to be enable to give percentages for positive,negative and neutral impact 

    Args:
        text_file:text file

    Returns:
        new_text_file: text file with labeled data
    """
    data={
        'comments':f'{text_file}.txt',
    }

    for source,filepath in data.items():
        df=pd.read_csv(filepath,names=['comments'],sep='\t')
    # Cleaning data from emails,number and special characters
    df['comments'] = df['comments'].str.replace('[^a-zA-Z]', ' ')
    df['comments'] = df['comments'].str.replace('@[A-Za-z0-9]+', ' ')
    df['comments'] = df['comments'].str.lower()
    sid = SentimentIntensityAnalyzer()
    # Create new coloums for positive and negative percentages
    df['impactPers'] = df['comments'].apply(lambda sentance: sid.polarity_scores(sentance))
    df['posPers']  = df['impactPers'].apply(lambda score_dict: score_dict['pos'])
    df['negPers']  = df['impactPers'].apply(lambda score_dict: score_dict['neg'])
    df['neuPers']  = df['impactPers'].apply(lambda score_dict: score_dict['neu'])
    #Labeling the data depending on the above persentages
    def label_race (row):
        if row['neuPers']  > 0.65:
            return 'N'
        if row['posPers']  > 0.5 :
            return 1
        if row['posPers']  < 0.5:
            return 0
        return 'Other'
    # Create new coloumn for the final labels
    df['labels'] = df.apply (lambda row: label_race(row), axis=1)
    # Create new file containing two coloumns
    new_df = df[['comments', 'labels']]
    new_file=new_df.to_csv('labeled_comments.txt')
    return new_file

labeling("Google_comments")