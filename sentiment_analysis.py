import pandas as pd
import sys
from nltk.sentiment.vader import SentimentIntensityAnalyzer

PREPROCESSED_DATA_FILE = 'data_preprocessed.p'
PREPROCESSED_DF = pd.read_pickle(PREPROCESSED_DATA_FILE)

def get_sentiment(filter_word):
    df_remove_null = PREPROCESSED_DF.dropna()
    filtered = df_remove_null[df_remove_null['TweetText'].str.contains(filter_word)]
    print(len(filtered), 'tweets found for', filter_word)
    analyzer = SentimentIntensityAnalyzer()
    overall_sentiment = []
    for tweet in filtered['TweetText'].tolist():
        ss = analyzer.polarity_scores(tweet)
        overall_sentiment.append(ss['compound'])
    print('Overall sentiment for', filter_word)
    print(sum(overall_sentiment) / len(overall_sentiment))

if __name__ == '__main__':
    filter_word = sys.argv[1]
    get_sentiment(filter_word)
