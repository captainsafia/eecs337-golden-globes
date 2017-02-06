import pandas as pd

from nltk import bigrams
from nltk.tag.stanford import StanfordNERTagger
st = StanfordNERTagger('stanford-ner/english.all.3class.distsim.crf.ser.gz', 'stanford-ner/stanford-ner.jar')

"""
Implementation Notes
This script finds the names of the award winners for a particular ceremony.
It does so by extracting tweets with the action verb "wins" to limit the 
scope of the tweets that have to be searched through to those that are most
relevant to the context. Afterwards, bigrams are generated from the text of
these tweets. The bigrams contain tuples like ('best', 'actor') or ('Emma', 'Stone').
These bigrams are then passed to a Parts-of-Speeech tagger. The POS tagger will
tag bigrams with names of individuals with the 'PERSON' tag and generate a
new tuple like ('Emma', 'Person'). The tagged bigrams are then filtered to exclude
any that don't contain 'PERSON' as the tag for both words in the bigram and
the extracted words are treated as the names of the winner and printed out.

Note that this implementation does take a while to run. The bulk of the compute
time is spent tagging the bigrams using the Stanford POS Tagger.
"""


PREPROCESSED_DATA_FILE = 'data_preprocessed.p'
PREPROCESSED_DF = pd.read_pickle(PREPROCESSED_DATA_FILE)

def filter_dataframe():
    """
    Extract the tweets that contain verbs relevant to winning.
    """
    df_remove_null = PREPROCESSED_DF.dropna()
    return df_remove_null[df_remove_null['TweetText'].str.contains("wins")]

def extract_names(bigrams):
    """
    Tag each of the bigram tuples with the appropriate Part of Speech.
    """
    named_bigrams = []
    NUM_BIGRAMS = len(bigrams)
    for index, bigram in enumerate(bigrams):
        print("Processing bigram", index + 1, "of", NUM_BIGRAMS)
        tagged = st.tag(bigram)

        # This fixes a weird bug where the tagger will pick up
        # an empty string and not tag it
        if len(tagged) == 1:
            tagged.append((None, None))
        if len(tagged) == 0:
            tagged.append((None, None))
            tagged.append((None, None))

        tags = [tagged[0][1], tagged[1][1]]
        if tags[0] == 'PERSON' and tags[1] == 'PERSON':
            person = " ".join(bigrams[index])
            # If a winner is already on the list, don't add them
            if person not in named_bigrams:
                named_bigrams.append(person)

    return named_bigrams

def get_bigrams(tweets):
    """
    Generate bigrams for each tweet.
    """
    split_tweets = [tweet.split(" ") for tweet in tweets]
    tweet_bigrams = []
    for tweet in split_tweets:
        tweet_bigrams.extend(list(bigrams(tweet)))
    return list(set(tweet_bigrams))

def find_award_winners():
    """
    Main function that runs through the process of filtering the dataframe,
    extracting bigrams, tagging the bigrams using POS, and then filtering the
    tags that are labelled 'PERSON'.
    """
    df = filter_dataframe()
    bigrams = get_bigrams(df['TweetText'].tolist())
    named_bigrams = extract_names(bigrams)
    print("Award Winners")
    # Remove duplicate names in winners list
    for index, name in named_bigrams:
        print(index + 1, ".", name)

if __name__ == '__main__':
    find_award_winners()
