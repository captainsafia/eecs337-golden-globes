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

def contains_number(word):
    return any(char.isdigit() for char in word)

def contains_punctuation(word):
    punctuation = list(string.punctuation)
    return any(char in punctuation for char in word)

def tokenize(text):
    tokens = []
    stop = stopwords.words('english') + ['rt','RT', 'via']
    if isinstance(text, str):
        for word_ in text.split(' '):
            word = word_.lower().strip()
            if (word not in stop and
                not contains_punctuation(word) and
                not word.startswith('http') and
                not contains_number(word)):
                tokens.append(word)
    return ' '.join(tokens)

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
