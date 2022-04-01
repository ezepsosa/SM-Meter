from datetime import datetime
import threading
from unittest import case
import tweepy
import time
import configparser
import praw
from langdetect import detect

from neural import load_model, predict_sentiment_twitter_eng
COORDINATES = {'AF': '33,65,5000km', 'AL': '41,20,5000km', 'DZ': '28,3,5000km', 'AS': '-14.3333,-170,5000km', 'AD': '42.5,1.6,5000km', 'AO': '-12.5,18.5,5000km', 'AI': '18.25,-63.1667,5000km', 'AQ': '-90,0,5000km', 'AG': '17.05,-61.8,5000km', 'AR': '-34,-64,5000km', 'AM': '40,45,5000km', 'AW': '12.5,-69.9667,5000km', 'AU': '-27,133,5000km', 'AT': '47.3333,13.3333,5000km', 'AZ': '40.5,47.5,5000km', 'BS': '24.25,-76,5000km', 'BH': '26,50.55,5000km', 'BD': '24,90,5000km', 'BB': '13.1667,-59.5333,5000km', 'BY': '53,28,5000km', 'BE': '50.8333,4,5000km', 'BZ': '17.25,-88.75,5000km', 'BJ': '9.5,2.25,5000km', 'BM': '32.3333,-64.75,5000km', 'BT': '27.5,90.5,5000km', 'BO': '-17,-65,5000km', 'BA': '44,18,5000km', 'BW': '-22,24,5000km', 'BV': '-54.4333,3.4,5000km', 'BR': '-10,-55,5000km', 'IO': '-6,71.5,5000km', 'BN': '4.5,114.6667,5000km', 'BG': '43,25,5000km', 'BF': '13,-2,5000km', 'BI': '-3.5,30,5000km', 'KH': '13,105,5000km', 'CM': '6,12,5000km', 'CA': '60,-95,5000km', 'CV': '16,-24,5000km', 'KY': '19.5,-80.5,5000km', 'CF': '7,21,5000km', 'TD': '15,19,5000km', 'CL': '-30,-71,5000km', 'CN': '35,105,5000km', 'CX': '-10.5,105.6667,5000km', 'CC': '-12.5,96.8333,5000km', 'CO': '4,-72,5000km', 'KM': '-12.1667,44.25,5000km', 'CG': '-1,15,5000km', 'CD': '0,25,5000km', 'CK': '-21.2333,-159.7667,5000km', 'CR': '10,-84,5000km', 'CI': '8,-5,5000km', 'HR': '45.1667,15.5,5000km', 'CU': '21.5,-80,5000km', 'CY': '35,33,5000km', 'CZ': '49.75,15.5,5000km', 'DK': '56,10,5000km', 'DJ': '11.5,43,5000km', 'DM': '15.4167,-61.3333,5000km', 'DO': '19,-70.6667,5000km', 'EC': '-2,-77.5,5000km', 'EG': '27,30,5000km', 'SV': '13.8333,-88.9167,5000km', 'GQ': '2,10,5000km', 'ER': '15,39,5000km', 'EE': '59,26,5000km', 'ET': '8,38,5000km', 'FK': '-51.75,-59,5000km', 'FO': '62,-7,5000km', 'FJ': '-18,175,5000km', 'FI': '64,26,5000km', 'FR': '46,2,5000km', 'GF': '4,-53,5000km', 'PF': '-15,-140,5000km', 'TF': '-43,67,5000km', 'GA': '-1,11.75,5000km', 'GM': '13.4667,-16.5667,5000km', 'GE': '42,43.5,5000km', 'DE': '51,9,5000km', 'GH': '8,-2,5000km', 'GI': '36.1833,-5.3667,5000km', 'GR': '39,22,5000km', 'GL': '72,-40,5000km', 'GD': '12: -21.1,55.6,5000km', 'RO': '46,25,5000km', 'RU': '60,100,5000km', 'RW': '-2,30,5000km', 'SH': '-15.9333,-5.7,5000km', 'KN': '17.3333,-62.75,5000km', 'LC': '13.8833,-61.1333,5000km', 'PM': '46.8333,-56.3333,5000km', 'VC': '13.25,-61.2,5000km', 'WS': '-13.5833,-172.3333,5000km', 'SM': '43.7667,12.4167,5000km', 'ST': '1,7,5000km', 'SA': '25,45,5000km', 'SN': '14,-14,5000km', 'RS': '44,21,5000km', 'SC': '-4.5833,55.6667,5000km', 'SL': '8.5,-11.5,5000km', 'SG': '1.3667,103.8,5000km', 'SK': '48.6667,19.5,5000km', 'SI': '46,15,5000km', 'SB': '-8,159,5000km', 'SO': '10,49,5000km', 'ZA': '-29,24,5000km', 'GS': '-54.5,-37,5000km', 'SS': '8,30,5000km', 'ES': '40,-4,5000km', 'LK': '7,81,5000km', 'SD': '15,30,5000km', 'SR': '4,-56,5000km', 'SJ': '78,20,5000km', 'SZ': '-26.5,31.5,5000km', 'SE': '62,15,5000km', 'CH': '47,8,5000km', 'SY': '35,38,5000km', 'TW': '23.5,121,5000km', 'TJ': '39,71,5000km', 'TZ': '-6,35,5000km', 'TH': '15,100,5000km', 'TL': '-8.55,125.5167,5000km', 'TG': '8,1.1667,5000km', 'TK': '-9,-172,5000km', 'TO': '-20,-175,5000km', 'TT': '11,-61,5000km', 'TN': '34,9,5000km', 'TR': '39,35,5000km', 'TM': '40,60,5000km', 'TC': '21.75,-71.5833,5000km', 'TV': '-8,178,5000km', 'UG': '1,32,5000km', 'UA': '49,32,5000km', 'AE': '24,54,5000km', 'GB': '54,-2,5000km', 'US': '38,-97,5000km', 'UM': '19.2833,166.6,5000km', 'UY': '-33,-56,5000km', 'UZ': '41,64,5000km', 'VU': '-16,167,5000km', 'VE': '8,-66,5000km', 'VN': '16,106,5000km', 'VG': '18.5,-64.5,5000km', 'VI': '18.3333,-64.8333,5000km', 'WF': '-13.3,-176.2,5000km', 'EH': '24.5,-13,5000km', 'YE': '15,48,5000km', 'ZM': '-15,30,5000km', 'ZW': '-20,30,5000km'}
NO_COUNTRY = 'Not especified'
# Subclass Stream to print IDs of Tweets received
class IDPrinter(tweepy.Stream):
    def on_status(self, status):
        if status.place:
            table_to_update.insert(parent='', index=0, text='', values=(status.text, status.user.screen_name, status.created_at, status.place.country, 'TW'))
        else:
            table_to_update.insert(parent='', index=0, text='', values=(status.text, status.user.screen_name, status.created_at, NO_COUNTRY, 'TW'))
# Method that updates the analysis table in real time
 
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
    ua = config['REDDIT']['USER_AGENT']
    return {'ck':ck,'csk':csk,'at':at,'ats':ats, 'ci':ci, 'cs':cs, 'ua':ua}

def tw_connect(keys):
    auth = tweepy.OAuthHandler(keys['ck'],keys['csk'])
    auth.set_access_token(keys['at'],keys['ats'])
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

def rd_connect(keys):
    reddit = praw.Reddit(client_id=keys['ci'], client_secret=keys['cs'], user_agent=keys['ua'])
    return reddit

def twitter_tweets(api,country, query, num_items, eng, spa):
    # QUERY
    if query:
        # If the query contains comma-separated elements we replace it to make it a multi-keyword search
        split = query.split(",")
        if len(split) > 1:
            query = query.replace(",", " OR")    
    else: 
        # q is mandatory
        query="a OR e OR i OR o OR"
        
    # LANGUAGE
    if eng + spa == 2:
        language="es OR en"
    elif spa == 1:
        language="es"
    else:
        language="en"

    # COUNTRY
    if country == '':
        tweets = tweepy.Cursor(api.search_tweets,q=query+" -filter:retweets",lang=language).items(int(num_items))
    else:
        tweets = tweepy.Cursor(api.search_tweets,q=query+" -filter:retweets",lang=language, geocode=COORDINATES[country]).items(int(num_items))
    return tweets

def reddit_comments(reddit, subrdt, query, num_items, eng, spa):
    if subrdt != "":
        subreddit = reddit.subreddit(subrdt)
    else:
        subreddit = reddit.subreddit('all')
    comments = []
    for comment in subreddit.comments(limit=int(num_items)):
        if query in comment.body:
            print(comment.body)
            if (eng == 1 and detect(comment.body) == 'en') or (spa == 1 and detect(comment.body) == 'es'):
                comments.append(comment)
    return comments

# Method that updates the custom analysis table according to the user's query
def update_table_custom(analysis, mapped_vars):
    model = load_model('models/SA_TW_ENG')
    keys = take_secret_credentials()
    api = tw_connect(keys)
    reddit = rd_connect(keys)
    if(mapped_vars['RB'][4] == 1):
        tweets = twitter_tweets(api, mapped_vars['EN'][1],mapped_vars['EN'][2],mapped_vars['EN'][3],mapped_vars['RB'][2], mapped_vars['RB'][3])
        for tweet in tweets:
            prediction = predict_sentiment_twitter_eng(tweet.text, model)
            if tweet.place:
                analysis.insert(parent='', index=0, text='', values=(tweet.text, tweet.user.screen_name, tweet.created_at, tweet.place.country, 'TW', prediction))
            else:
                # If the result does not have any country set, we leave it as unspecified
                analysis.insert(parent='', index=0, text='', values=(tweet.text, tweet.user.screen_name, tweet.created_at, NO_COUNTRY, 'TW', prediction))
    if(mapped_vars['RB'][5] == 1):
        comments = reddit_comments(reddit,mapped_vars['EN'][0], mapped_vars['EN'][2], mapped_vars['EN'][3],mapped_vars['RB'][2], mapped_vars['RB'][3])
        for comment in comments:
            analysis.insert(parent='', index=0, text='', values=(comment.body, comment.author, datetime.utcfromtimestamp(comment.created_utc), NO_COUNTRY, 'RD'))

def update_table_real_time(table, mapped_vars):
    #model = load_model('models/SA_TW_ENG')
    keys = take_secret_credentials()
    #reddit = rd_connect(keys)
    stream_twitter(keys, table, mapped_vars['EN'][1],mapped_vars['EN'][2], mapped_vars['RB'][2], mapped_vars['RB'][3])

def stream_twitter(keys, table, country, query, eng, spa):
    # QUERY 
    global table_to_update
    table_to_update = table
    printer = IDPrinter(
    keys['ck'],keys['csk'],keys['at'],keys['ats']
    )
    if query:
        # If the query contains comma-separated elements we replace it to make it a multi-keyword search
        split = query.split(",")
        if len(split) > 1:
            query = query.replace(",", " OR")    
    else: 
        # q is mandatory
        query="a OR e OR i OR o OR"
        
    # LANGUAGE
    if eng + spa == 2:
        language="es OR en"
    elif spa == 1:
        language="es"
    else:
        language="en"
    

    # COUNTRY
    if country == '':
        print('ENTRO')
        printer.filter(track=query, languages=[language])
    else:
        printer.filter(track=query, languages=[language], geocode=COORDINATES[country])

        #FUNCIONA
        #printer.filter(track='hi')