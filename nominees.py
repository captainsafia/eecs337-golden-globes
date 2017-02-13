import pandas as pd

import os
import pickle

PREPROCESSED_DATA_FILE = 'data_preprocessed.p' #Referring to the preprocessed data file created from preprocess.py
PREPROCESSED_DF = pd.read_pickle(PREPROCESSED_DATA_FILE)  #Convert back to dataframe

nominees = []

def filter_dataframe():
    
    #Extract the tweets that contain the root of the verb and noun forms ("nominated" and "nominee") relevant to winning.
    
    no_nulls = PREPROCESSED_DF.dropna()
    return no_nulls[no_nulls['TweetText'].str.contains("nomin")]

def processnamelist():

#Take in the census data first names and convert them to a list

    firstnames = pd.read_csv('firstnames.txt', sep = " ", header = none)
    firstnames.columns = ["names"]
    namelist = firstnames["names"].tolist()

def findname(target):

#Takes in a tweet in the form of a list of words, and goes through each word to see if it's a first name.
#If it is a first name, then assume that the next word is the last name and add the two words in the form
#of a list to the namepairs list. When done, return name pairs found from the tweet.

    namepairs = [] #list within list
    for name in namelist:
        if name in target:
            lastname.append([name, target[target.index(name)+1]])
    return namepairs

def processtweet(tweets):
    
#Takes in the filtered tweets dataframe, splits into words, and finds names using the attached first name list
#Adds found names into list of nominees in the form of "firstname lastname" in one string.

    for tweet in tweets:
        temp = [tweet.split(" ") for tweet in tweets]
        temp2 = findname(temp)
        for pair in temp2:
            nominees.extend(pair[0] + " " + pair[1])

def findnominees():
    
    #Main function --> filters the tweet data, breaks down into words and finds names, and adds them to nominee list.
    
    filteredtweets = filter_dataframe()
    processtweet(filteredtweets['TweetText'].tolist())

    # Remove duplicate names in winners list
    for name in nominees:
        if nominees.count(name) > 1:
            list.clear(name)
            list.append(name)

    return nominees