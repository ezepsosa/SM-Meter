import tweepy
import json
import pandas as pd
import os
import time
import configparser

# Method that stores the user's twitter API credentials in a variable.
def take_secret_credentials():
    config = configparser.ConfigParser()
    config.read('config.ini')
    ck = config['TWITTER']['CONSUMER_KEY']
    csk = config['TWITTER']['CONSUMER_SECRET']
    at = config['TWITTER']['ACCESS_TOKEN']
    ats = config['TWITTER']['ACCESS_TOKEN_SECRET']
    ci = config['REDDIT']['CLIENT_ID']
    cs = config['REDDIT']['CLIENT_SECRET']
    return {'ck':ck,'csk':csk,'at':at,'ats':ats, 'ci':ci, 'cs':cs}

# Subclass Stream to print IDs of Tweets received
class IDPrinter(tweepy.Stream):
    def on_status(self, status):
        #print('hi')
        table.insert(parent='', index=0, text='', values=('1','Vineet','Alpha'))
        time.sleep(6)
        if status.place:
            dict_ = {'user': [], 'date': [], 'text': [], 'country': []}
            dict_['user'].append(status.user.screen_name)
            dict_['date'].append(status.created_at)
            dict_['text'].append(status.text)
            dict_['country'].append(status.place.country)

# Method that updates the analysis table in real time
def update_table(analysis):
    global table
    table = analysis
    keys = take_secret_credentials()
    printer = IDPrinter(
    keys['ck'],keys['csk'],keys['at'],keys['ats']
    )
    printer.filter(track=['a'], languages=['es'])
        
def tw_connect(keys):
    auth = tweepy.OAuthHandler(keys['ck'],keys['csk'])
    auth.set_access_token(keys['at'],keys['ats'])
    return auth

# Method that updates the custom analysis table according to the user's query
def update_table_custom(analysis, map):
    keys = take_secret_credentials()
    #Twitter
    auth = tw_connect(keys)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    tweets = twitter_tweets(api, map['EN'][1],map['EN'][2],map['EN'][3])
    #comments = reddit_comments()

    
    for tweet in tweets:
        if tweet.place:
             analysis.insert(parent='', index=0, text='', values=(tweet.text, tweet.user.screen_name, tweet.created_at, tweet.place.country))
        else:
            # If the result does not have any country set, we leave it as unspecified
             analysis.insert(parent='', index=0, text='', values=(tweet.text, tweet.user.screen_name, tweet.created_at, 'Not especified'))
#map = [entry_subreddit.get(), country_phrase.get(), query_phrase.get(), numItems.get(), start_date.get_date, end_date.get_date]}

def twitter_tweets(api,country, query, numItems):
    # If the query contains comma-separated elements we replace it to make it a multi-keyword search
    if query:
        split = query.split(",")
        if len(split) > 1:
            query = query.replace(",", " OR")    
        tweets = tweepy.Cursor(api.search_tweets,q=query,lang="es").items(int(numItems))

    # If the query is empty, it is searched by vowels, since "q" is mandatory.
    else: 
        tweets = tweepy.Cursor(api.search_tweets,q="a OR e OR i OR o OR u",lang="es").items(int(numItems))
    return tweets
