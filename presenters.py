import pandas as pd
from nltk import bigrams
import nltk
from nltk.tag.stanford import StanfordNERTagger
st = StanfordNERTagger('stanford-ner/english.all.3class.distsim.crf.ser.gz', 'stanford-ner/stanford-ner.jar')
import collections
import numpy as np
import re
import time


def find_tweets_with_keyword(keywords, df):

    for k in keywords:
        df = df.loc[df['TweetText'].str.contains(k).fillna(False)]

    return df["TweetText"]

def find_bigrams(present_tweets):

    tweet_unigrams = [t.split(' ') for t in present_tweets]
    tweet_bigrams = [list(bigrams(t)) for t in tweet_unigrams]

    return tweet_bigrams


def get_bg_frequency_dataframe(tweet_bigrams):

    # TODO: optimize by using -> http://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.value_counts.html
    bg_count = {}
    for bg_row in tweet_bigrams:
        for bg in bg_row:
            bg_i = bg[0] + ' ' + bg[1]
            if bg_i in bg_count:
                bg_count[bg_i] += 1
            else:
                bg_count[bg_i] = 1

    return pd.DataFrame(list(bg_count.items()), columns=["bigrams","frequency"])

def load_file(filename):

    lasts = []
    with open(filename,'r') as f:

        line = f.readline()
        while line:
            lasts.append(line.strip())
            line = f.readline()

    return lasts


def get_most_frequent_person(bg_df, num=50):

    p = re.compile(r'([A-Z][a-z]+\s[A-Z][a-z]+)+')
    bg_df["bigrams"] = bg_df["bigrams"].map(p.findall)

    firsts = load_file("firstnames.txt")
    lasts = load_file("surnames.txt")

    peeps = []
    for index, val in bg_df["bigrams"].iteritems():

        if len(val) == 0:
            continue

        val = val[0]

        names_list = val.split(' ')
        if names_list[0].upper() not in firsts:
            continue

        if names_list[1].upper() not in lasts:
            continue

        peeps.append(val)

    # while (bg_df.shape[0] > 0) and (num != 0):

        # max_index = bg_df["frequency"].idxmax()
        # host = bg_df.loc[max_index]["bigrams"]
        # bg_df.drop(max_index, inplace=True)
        # if host == []:
        #     continue
        # tag = st.tag(host)[0][1]
        # if tag == "PERSON":
        #     num -= 1
        #     peoples.append(host[0])
        #     print("found: ", peoples)

    return peeps


def main():

    data_file_path = 'p_data_preprocessed.p'
    df = pd.read_pickle(data_file_path)

    tweets = find_tweets_with_keyword(["present", "best"], df)
    bigrams = find_bigrams(tweets)
    frequencies = get_bg_frequency_dataframe(bigrams)
    return get_most_frequent_person(frequencies)

if __name__ == "__main__":

    presenters = main()

    print("Predicted presenters: ", presenters)
    correct = load_file("presenters.txt")
    print("Actual presenters: ", correct)

    count = 0
    for p in presenters:

        if p in correct:
            count += 1

    print("Percent found: ")
    print(count / len(correct))
