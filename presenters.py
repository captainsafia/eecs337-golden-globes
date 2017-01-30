import pandas as pd
from nltk import bigrams
import nltk
from nltk.tag.stanford import StanfordNERTagger
st = StanfordNERTagger('stanford-ner/english.all.3class.distsim.crf.ser.gz', 'stanford-ner/stanford-ner.jar')
import collections
import numpy as np


def find_tweets_with_keyword(keyword, df):

    present_tweets = df.loc[df['TweetText'].str.contains(keyword).fillna(False)]["TweetText"]
    tweet_unigrams = [t.split(' ') for t in present_tweets]
    tweet_bigrams = [list(bigrams(t)) for t in tweet_unigrams]

    return tweet_unigrams, tweet_bigrams

def get_bg_frequency_dataframe(tweet_bigrams):
    bg_count = {}
    for bg_row in tweet_bigrams:
        for bg in bg_row:
            bg_i = bg[0]+' '+bg[1]
            if bg_i in bg_count:
                bg_count[bg_i] += 1
            else:
                bg_count[bg_i] = 1

    return pd.DataFrame(list(bg_count.items()), columns=["bigrams","frequency"])


def get_most_frequent_person(bg_df):


    while bg_df.shape[0] > 0:

        max_index = bg_df["frequency"].idxmax()
        host = bg_df.loc[max_index]["bigrams"]
        print(host)
        bg_df.drop(max_index, inplace=True)
        tag = st.tag([host])[0][1]
        print("tag: ", tag)
        if tag == "PERSON":
            break

    print("Host!", host)
    return host

def main():

    data_file_path = 'data_preprocessed.p'
    df = pd.read_pickle(data_file_path)

    tweet_bigrams = find_tweets_with_keyword("presenter", df)[1]
    bg_df = get_bg_frequency_dataframe(tweet_bigrams)
    person = get_most_frequent_person(bg_df)

    return person
