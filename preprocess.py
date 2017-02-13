import sys
import pandas as pd
import numpy as np
import re

import nltk
#nltk.download()
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
import string

DATA_FRAME = None

st = LancasterStemmer()

tokens_re_string = [
    r'<[^>]+>',
    r'(?:@[\w_]+)',
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens = re.compile(r'('+'|'.join(tokens_re_string)+')', re.VERBOSE | re.IGNORECASE)

def tokenize(text):
    punctuation = list(string.punctuation)
    tokens = []
    stop = stopwords.words('english') + punctuation + ['rt','RT', 'via']
    if isinstance(text, str):
        for word in text.split(' '):
            if word not in stop:
                tokens.append(word)
    return tokens

def process_data_file(filename):
   DATA_FRAME = pd.read_table(filename, names = [
       'TweetText',
       'TweetUserName',
       'UserIDString',
       'TweetIDString',
       'Timestamp'
    ])
   DATA_FRAME['tokens'] = DATA_FRAME['TweetText'].map(tokenize)
   DATA_FRAME.to_pickle('data_preprocessed.p')

if __name__ == '__main__':
    filename = sys.argv[1]
    process_data_file(filename)
