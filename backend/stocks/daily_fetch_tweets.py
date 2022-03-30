import twint
from datetime import datetime, timedelta
import time

def scrape_all_tweets():
    tweet_data=[
        # {"csv_name":"TataFinalNews.csv","keyword":"Tata Motor"},
        # {"csv_name":"InfosysFinalNews.csv","keyword":"Infosys"},
        # {"csv_name":"HDFCFinalNews.csv","keyword":"HDFC Bank"},
        {"csv_name":"BajajFinalTweets.csv","keyword":"Bajaj Auto"},
        # {"csv_name":"AirtelFinalNews.csv","keyword":"Airtel"},
        # {"csv_name":"AdaniFinalNews.csv","keyword":"Adani port"},
    ]
    for i in tweet_data:
        scrape_tweets(i['csv_name'],i['keyword'])

def scrape_tweets(csv_name,keyword):
    # Configure
    presentday = datetime.now()
    print(presentday.strftime('%d-%m-%Y'))
    tomorrow = presentday + timedelta(1)
    print(tomorrow.strftime('%d-%m-%Y'))
    t = twint.Config()
    t.Search = keyword
    t.Store_object = True
    t.Limit = 1000
    t.Since = presentday.strftime('%Y-%m-%d')
    t.Until= tomorrow.strftime('%Y-%m-%d')
    twint.run.Search(t)
    tlist = t.search_tweet_list

    print("+++++++++++++++",tlist)
    
    return "ABC"
