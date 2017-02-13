import pandas as pd

import os
import pickle

PREPROCESSED_DATA_FILE = 'data_preprocessed.p' #Referring to the preprocessed data file created from preprocess.py
PREPROCESSED_DF = pd.read_pickle(PREPROCESSED_DATA_FILE)  #Convert back to dataframe

nominees = []
namelist = []
tweetstatus = []
alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def filter_dataframe():
    
#Mark the tweets that contain the words 'nominee' and 'nominated'.
    
    global tweetstatus

    tweetstatus = PREPROCESSED_DF['TweetText'].str.contains("nominee|nominated")
    return PREPROCESSED_DF


def processnamelist():

#Take in the census data first names and convert them to a list

    global namelist

    names = pd.read_csv("firstnames.txt")
    names.columns = ['a']
    namelist = names['a'].tolist()

def findname(target):

#Takes in a tweet in the form of a list of words, and goes through each word to see if it's a first name.
#If it is a first name, then assume that the next word is the last name and add the two words in the form
#of a list to the namepairs list. When done, return name pairs found from the tweet.

    namepairs = [] #list within list
    index = 0
    for token in target:
        token = token.upper()
        for name in namelist:
            name = name[:-1]
            if name == token and (name != "IN" and name != "AN" and name != "SO" and name != "SEE" and name != "MY"):
                if index < len(target)-1:
                    namepairs.append([target[index], target[index+1]])
                else:
                    namepairs.append([target[index]])
        index += 1      
    return namepairs

def processtweet(tweets):
    
#Takes in the list of all tweet text, splits into words, and finds names using the attached first name list
#Adds found names into list of nominees in the form of "firstname lastname" in one string.

    global nominees
    global alphabet

    count = 0
    for tweet in tweets:
        if tweetstatus[count] == True:
            temp = tweet.split(" ")
            temp2 = findname(temp)
            for pair in temp2:
                if len(pair) == 2:
                    if(pair[0][0] in alphabet and pair[1][0] in alphabet):
                        nominees.append(pair[0] + " " + pair[1])
            count += 1
        else:
            count += 1

def findnominees():
    
    #Main function --> filters the tweet data, breaks down into words and finds names, and adds them to nominee list.
    
    alltweets = filter_dataframe()
    processnamelist()
    processtweet(alltweets['TweetText'].tolist())

    # Remove duplicate names in winners list
    for name in nominees:

        # Remove all strings with numbers
        if any(character.isdigit() for character in name):
            nominees.remove(name)

        # Remove all punctuation-containing names
        if ("!" in name or "." in name or "?" in name or "\\" in name):
            nominees.remove(name)

        # Remove all duplicates
        go = nominees.count(name)
        if go > 1:
            while go > 1:
                nominees.remove(name)
                go -= 1

    return nominees