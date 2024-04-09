from neural import load_models, predict
from datetime import datetime
from langdetect import detect
import pandas as pd
import configparser
import threading
import tweepy
import praw

""" CONSTANTS """
COORDINATES = {'AF': '33,65,5000km', 'AL': '41,20,5000km', 'DZ': '28,3,5000km', 'AS': '-14.3333,-170,5000km', 'AD': '42.5,1.6,5000km', 'AO': '-12.5,18.5,5000km', 'AI': '18.25,-63.1667,5000km', 'AQ': '-90,0,5000km', 'AG': '17.05,-61.8,5000km', 'AR': '-34,-64,5000km', 'AM': '40,45,5000km', 'AW': '12.5,-69.9667,5000km', 'AU': '-27,133,5000km', 'AT': '47.3333,13.3333,5000km', 'AZ': '40.5,47.5,5000km', 'BS': '24.25,-76,5000km', 'BH': '26,50.55,5000km', 'BD': '24,90,5000km', 'BB': '13.1667,-59.5333,5000km', 'BY': '53,28,5000km', 'BE': '50.8333,4,5000km', 'BZ': '17.25,-88.75,5000km', 'BJ': '9.5,2.25,5000km', 'BM': '32.3333,-64.75,5000km', 'BT': '27.5,90.5,5000km', 'BO': '-17,-65,5000km', 'BA': '44,18,5000km', 'BW': '-22,24,5000km', 'BV': '-54.4333,3.4,5000km', 'BR': '-10,-55,5000km', 'IO': '-6,71.5,5000km', 'BN': '4.5,114.6667,5000km', 'BG': '43,25,5000km', 'BF': '13,-2,5000km', 'BI': '-3.5,30,5000km', 'KH': '13,105,5000km', 'CM': '6,12,5000km', 'CA': '60,-95,5000km', 'CV': '16,-24,5000km', 'KY': '19.5,-80.5,5000km', 'CF': '7,21,5000km', 'TD': '15,19,5000km', 'CL': '-30,-71,5000km', 'CN': '35,105,5000km', 'CX': '-10.5,105.6667,5000km', 'CC': '-12.5,96.8333,5000km', 'CO': '4,-72,5000km', 'KM': '-12.1667,44.25,5000km', 'CG': '-1,15,5000km', 'CD': '0,25,5000km', 'CK': '-21.2333,-159.7667,5000km', 'CR': '10,-84,5000km', 'CI': '8,-5,5000km', 'HR': '45.1667,15.5,5000km', 'CU': '21.5,-80,5000km', 'CY': '35,33,5000km', 'CZ': '49.75,15.5,5000km', 'DK': '56,10,5000km', 'DJ': '11.5,43,5000km', 'DM': '15.4167,-61.3333,5000km', 'DO': '19,-70.6667,5000km', 'EC': '-2,-77.5,5000km', 'EG': '27,30,5000km', 'SV': '13.8333,-88.9167,5000km', 'GQ': '2,10,5000km', 'ER': '15,39,5000km', 'EE': '59,26,5000km', 'ET': '8,38,5000km', 'FK': '-51.75,-59,5000km', 'FO': '62,-7,5000km', 'FJ': '-18,175,5000km', 'FI': '64,26,5000km', 'FR': '46,2,5000km', 'GF': '4,-53,5000km', 'PF': '-15,-140,5000km', 'TF': '-43,67,5000km', 'GA': '-1,11.75,5000km', 'GM': '13.4667,-16.5667,5000km', 'GE': '42,43.5,5000km', 'DE': '51,9,5000km', 'GH': '8,-2,5000km', 'GI': '36.1833,-5.3667,5000km', 'GR': '39,22,5000km', 'GL': '72,-40,5000km', 'GD': '12: -21.1,55.6,5000km', 'RO': '46,25,5000km', 'RU': '60,100,5000km', 'RW': '-2,30,5000km', 'SH': '-15.9333,-5.7,5000km', 'KN': '17.3333,-62.75,5000km', 'LC': '13.8833,-61.1333,5000km', 'PM': '46.8333,-56.3333,5000km', 'VC': '13.25,-61.2,5000km', 'WS': '-13.5833,-172.3333,5000km', 'SM': '43.7667,12.4167,5000km', 'ST': '1,7,5000km', 'SA': '25,45,5000km', 'SN': '14,-14,5000km', 'RS': '44,21,5000km', 'SC': '-4.5833,55.6667,5000km', 'SL': '8.5,-11.5,5000km', 'SG': '1.3667,103.8,5000km', 'SK': '48.6667,19.5,5000km', 'SI': '46,15,5000km', 'SB': '-8,159,5000km', 'SO': '10,49,5000km', 'ZA': '-29,24,5000km', 'GS': '-54.5,-37,5000km', 'SS': '8,30,5000km', 'ES': '40,-4,5000km', 'LK': '7,81,5000km', 'SD': '15,30,5000km', 'SR': '4,-56,5000km', 'SJ': '78,20,5000km', 'SZ': '-26.5,31.5,5000km', 'SE': '62,15,5000km', 'CH': '47,8,5000km', 'SY': '35,38,5000km', 'TW': '23.5,121,5000km', 'TJ': '39,71,5000km', 'TZ': '-6,35,5000km', 'TH': '15,100,5000km', 'TL': '-8.55,125.5167,5000km', 'TG': '8,1.1667,5000km', 'TK': '-9,-172,5000km', 'TO': '-20,-175,5000km', 'TT': '11,-61,5000km', 'TN': '34,9,5000km', 'TR': '39,35,5000km', 'TM': '40,60,5000km', 'TC': '21.75,-71.5833,5000km', 'TV': '-8,178,5000km', 'UG': '1,32,5000km', 'UA': '49,32,5000km', 'AE': '24,54,5000km', 'GB': '54,-2,5000km', 'US': '38,-97,5000km', 'UM': '19.2833,166.6,5000km', 'UY': '-33,-56,5000km', 'UZ': '41,64,5000km', 'VU': '-16,167,5000km', 'VE': '8,-66,5000km', 'VN': '16,106,5000km', 'VG': '18.5,-64.5,5000km', 'VI': '18.3333,-64.8333,5000km', 'WF': '-13.3,-176.2,5000km', 'EH': '24.5,-13,5000km', 'YE': '15,48,5000km', 'ZM': '-15,30,5000km', 'ZW': '-20,30,5000km'}
NO_COUNTRY = 'Not especified'
dictionary_real_time = None
dictionary_custom_analysis = None
country_to_stream = ''
table_to_update = None
printer = None
sentiment = None
aggressive = None
stop_rd = 0
subreddit_rt = []
update_chart = True
""" CLASS SECTION """
# Subclass Stream to print IDs of Tweets received
class IDPrinter(tweepy.Stream):
    def on_status(self, status):
        global sentiment, aggressive, country_to_stream, dictionary_real_time
        if 'RT' not in status.text:
            if country_to_stream:
                if status.place and status.place.country_code == country_to_stream:
                    prediction = take_predict_tw(sentiment, aggressive, 0, status.text, status.lang)
                    table_to_update.insert(parent='', index=0, text='', values=(status.text, status.user.screen_name, status.created_at, status.place.country_code, 'TW',prediction))
            else:
                prediction = take_predict_tw(sentiment, aggressive, 0, status.text, status.lang)
                table_to_update.insert(parent='', index=0, text='', values=(status.text, status.user.screen_name, status.created_at, NO_COUNTRY, 'TW',prediction))
            add_result_to_dictionary(sentiment, aggressive, status.text, dictionary_real_time, prediction)
# AUX: Method that updates the analysis table in real time
""" GENERAL SECTION """
def export_results(mode):
    global dictionary_real_time, dictionary_custom_analysis
    dictionary = None
    if(mode==1):
        dictionary = dictionary_real_time 
    else:
        dictionary = dictionary_custom_analysis
    if len(dictionary['Sentiment']) == 0:
        dictionary['Sentiment'] = ["Null"]*len(dictionary['Aggressive'])
    elif len(dictionary['Aggressive']) == 0:
        dictionary['Aggressive'] = ["Null"]*len(dictionary['Sentiment'])
    df = pd.DataFrame.from_dict(dictionary)
    name = "analysis/" + str(datetime.now())[:19].replace(":", ";").replace(" ", "") + ".csv"
    df.to_csv(name)

# AUX: Method that stores the user's twitter API credentials in a variable.
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

# AUX: Method that extracts the values from the map with the 'RB' key
def extract_rb_map(mapped_vars):
    return mapped_vars['RB'][0], mapped_vars['RB'][1], mapped_vars['RB'][2], mapped_vars['RB'][3], mapped_vars['RB'][4], mapped_vars['RB'][5]

# AUX: Method that extracts the values from the map with the 'EN' key. The mode value depends if its for twitter or reddit
def extract_en_map(mapped_vars, mode):
    if(mode == 0):
        return mapped_vars['EN'][0], mapped_vars['EN'][1], mapped_vars['EN'][2], mapped_vars['EN'][3], mapped_vars['EN'][3], mapped_vars['EN'][4]
    else:
        return mapped_vars['EN'][0], mapped_vars['EN'][1], mapped_vars['EN'][2]

# AUX: Method that returns the state of the global variable "update_chart"
def should_update_chart():
    global update_chart
    return update_chart

# AUX: Method that returns the state of the global variable "dictionary_real_time"
def update_to_real_time_dictionary():
    global dictionary_real_time
    return dictionary_real_time

""" CUSTOM """
# AUX: Method that adds the results to the dictionary passed by parameters. The parameters text, sentiment and aggressiveness are added.
def add_result_to_dictionary(sentiment, aggressive, text, dictionary_custom_results, prediction):
    dictionary_custom_results['text'].append(text)
    if (sentiment * aggressive == 1):
        prediction = prediction.split("\n")
        dictionary_custom_results['Aggressive'].append(prediction[0])
        dictionary_custom_results['Sentiment'].append(prediction[1])
    elif(sentiment == 1):
        dictionary_custom_results['Sentiment'].append(prediction)
    else:
        dictionary_custom_results['Aggressive'].append(prediction)
    return dictionary_custom_results

# AUX: Method that inserts the tweet in the table passed by parameters.
def insert_tweet(tweets, sentiment, aggressive, analysis, dictionary_custom_results):
    for tweet in tweets:
        prediction = take_predict_tw(sentiment, aggressive, 0, tweet.text, tweet.lang)
        if tweet.place:
            analysis.insert(parent='', index=0, text='', values=(tweet.text, tweet.user.screen_name, tweet.created_at, tweet.place.country, 'TW', prediction))
        else:
            # If the result does not have any country set, we leave it as unspecified
            analysis.insert(parent='', index=0, text='', values=(tweet.text, tweet.user.screen_name, tweet.created_at, NO_COUNTRY, 'TW', prediction))
        add_result_to_dictionary(sentiment, aggressive, tweet.text, dictionary_custom_results, prediction)
    return dictionary_custom_results

# AUX: Method that inserts the comments in the table passed by parameters.
def insert_comments(comments, sentiment, aggressive, analysis, dictionary_custom_results):
    for comment in comments:
        try:
            prediction = take_predict_rd(sentiment, aggressive, 1, comment.body, False)
            analysis.insert(parent='', index=0, text='', values=(comment.body, comment.author, datetime.utcfromtimestamp(comment.created_utc), NO_COUNTRY, 'RD', prediction))
            add_result_to_dictionary(sentiment, aggressive, comment.body, dictionary_custom_results, prediction)
        except:
            print("There's was an error in a sentence analysis")
    return dictionary_custom_results
    
# Method that updates the custom analysis table according to the user's query
def update_table_custom(analysis, mapped_vars):
    global dictionary_custom_analysis
    dictionary_custom_analysis = {'text':[],'Sentiment':[], 'Aggressive':[]}
    sentiment, aggressive, english, spanish, twt, rdt = extract_rb_map(mapped_vars)
    subrdt, country, query, numItms, after, before = extract_en_map(mapped_vars, 0)
    if(sentiment + aggressive > 0):
        load_models(spanish, english, twt, rdt, sentiment, aggressive)
        keys = take_secret_credentials()
        if(twt == 1):
            api = tw_connect(keys)
            tweets = twitter_tweets(api, country,query,numItms,english, spanish, after, before)
            dictionary_custom_analysis = insert_tweet(tweets, sentiment, aggressive, analysis, dictionary_custom_analysis)      
        if(rdt == 1):
            reddit = rd_connect(keys)
            comments = reddit_comments(reddit,subrdt, query, int(numItms),english, spanish)
            dictionary_custom_analysis = insert_comments(comments, sentiment, aggressive, analysis, dictionary_custom_analysis)
    return dictionary_custom_analysis

""" REAL TIME """
# Method that for twitter printer, reddit and graph updates. 
def stop_real_time_analysis():
    global printer, subreddit_rt, update_chart
    if printer:
        printer.running = False
    subreddit_rt = []
    update_chart = False

# Method that updates the table in real time with the searched data. 
def update_table_real_time(table, mapped_vars):
    global stop_rd, dictionary_real_time, update_chart, dictionary_real_time
    dictionary_real_time = {'text':[],'Sentiment':[], 'Aggressive':[]}
    update_chart, stop_rd, keys = True, 0, take_secret_credentials()
    subrdt, country, query = extract_en_map(mapped_vars, 1)
    sentiment, aggressive, english, spanish, twt, rdt = extract_rb_map(mapped_vars)
    load_models(spanish, english, twt, rdt, sentiment, aggressive)
    if(rdt==1):
        threading.Thread(target=stream_reddit, args=[keys, table, subrdt,query, english, spanish, sentiment, aggressive]).start()
    if(twt==1):
        threading.Thread(target=stream_twitter, args=[keys, table, country, query, english, spanish, sentiment, aggressive]).start()
    
   
""" TWITTER SECTION """
# Method that creates a connection with twitter.
def tw_connect(keys):
    auth = tweepy.OAuthHandler(keys['ck'],keys['csk'])
    auth.set_access_token(keys['at'],keys['ats'])
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

# Method that obtains tweets from twitter.
def twitter_tweets(api,country, query, num_items, eng, spa, after, before):
    query, language, country = define_twitter_search(query, eng, spa, country)
    if country == '':
        tweets = tweepy.Cursor(api.search_tweets,q=query+" -filter:retweets",lang=language).items(int(num_items))
    else:
        
        tweets = tweepy.Cursor(api.search_tweets,q=query+" -filter:retweets",lang=language, geocode=COORDINATES[country]).items(int(num_items))
    return tweets

# Method to create a twitter stream.
def stream_twitter(keys, table, country, query, eng, spa, sntm, aggrs):
    #GLOBAL VARS
    global table_to_update, country_to_stream, printer, sentiment, aggressive
    sentiment, aggressive, table_to_update, country_to_stream = sntm, aggrs, table, ''
    #CREATING OBJECTS
    printer = IDPrinter(
    keys['ck'],keys['csk'],keys['at'],keys['ats']
    )
    query, language, country = define_twitter_search(query, eng, spa, country)
    if "OR" in query:
        query = query.split(" OR ")
    else:
        query = [query]
    if(eng*spa==1):
        printer.filter(track=query, languages=language.split(" OR "))
    else:
        printer.filter(track=query, languages=[language])

# Method that deefine a twitter search with the inputs params.
def define_twitter_search(query, eng, spa, country):
    # QUERY 
    global country_to_stream
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
    if country:
        country_to_stream = country

    return query, language, country_to_stream

""" REDDIT SECTION """
# Method that creates a connection with reddit.
def rd_connect(keys):
    reddit = praw.Reddit(client_id=keys['ci'], client_secret=keys['cs'], user_agent=keys['ua'])
    return reddit

# Method to create a reddit stream.
def stream_reddit(keys, table, subrdt, query, eng, spa, sentiment, aggressive):
    global subreddit_rt, dictionary_real_time
    reddit = rd_connect(keys)
    if subrdt != "":
        subreddit_rt = reddit.subreddit(subrdt)
    else:
        subreddit_rt = reddit.subreddit('all')
    for comment in subreddit_rt.comments():
        try:
            if query in comment.body and comment.body and ((eng == 1 and detect(comment.body) == 'en') or (spa == 1 and detect(comment.body) == 'es')):
                prediction = take_predict_rd(sentiment, aggressive, 1, comment.body, False)
                table.insert(parent='', index=0, text='', values=(comment.body, comment.author, datetime.utcfromtimestamp(comment.created_utc), NO_COUNTRY, 'RD',prediction))
                add_result_to_dictionary(sentiment, aggressive, comment.body, dictionary_real_time, prediction)
        except:
            print("Detected one comment with no valid characters")

# Method that returns reddit comments.
def reddit_comments(reddit, subrdt, query, num_items, eng, spa):
    if subrdt != "":
        subreddit = reddit.subreddit(subrdt)
    else:
        subreddit = reddit.subreddit('all')
    comments = []
    #api_praw = PushshiftAPI(praw=reddit)
    for comment in subreddit.comments(limit=int(num_items)):
        if query in comment.body:
            try:
                if (eng == 1 and detect(comment.body) == 'en') or (spa == 1 and detect(comment.body) == 'es'):
                    comments.append(comment)
            except:
                print("This comment doesn't fit in the rules of detecting languages")
        if len(comments) > int(num_items) -1:
            break
    return comments

# Method that predict a tweet. Mode is for social media.
def take_predict_tw(sa, aa, mode, text, lang):
    if (lang =='en'):
        return predict(sa, aa, 1, mode, text)
    else:
        return predict(sa, aa, 0, mode, text)

# Method that predict a comment. Mode is for social media.
def take_predict_rd(sa, aa, mode, text, forced):
    if (detect(text) == 'en' or forced):
        return predict(sa, aa, 1, mode, text)
    else:
        return predict(sa, aa, 0, mode, text)
