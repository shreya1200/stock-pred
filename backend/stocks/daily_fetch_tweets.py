import pandas as pd
from datetime import datetime, timedelta
import time
import twint
import os
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()
from stocks.daily_fetch_news import append_to_csv


def scrape_all_tweets():
    tweet_data=[
        {"csv_name":"TataFinalTweets.csv","keyword":"Tata Motors Stocks"},
        {"csv_name":"InfosysFinalTweets.csv","keyword":"INFY Stocks"},
        {"csv_name":"HDFCFinalTweets.csv","keyword":"HDFC Bank Stocks"},
        {"csv_name":"BajajFinalTweets.csv","keyword":"Bajaj Auto Stocks"},
        {"csv_name":"AirtelFinalTweets.csv","keyword":"Airtel Stocks"},
        {"csv_name":"AdaniFinalTweets.csv","keyword":"Adani port Stocks"},
    ]
    for i in tweet_data:
        scrape_tweets(i['csv_name'],i['keyword'])

def scrape_tweets(csv_name,keyword):
    tweets_list = []
    print("[[[[[[[[[[[[[[[[",keyword)
    # Configure
    presentday = datetime.now()
    tomorrow = presentday + timedelta(1)
    presentday=presentday.strftime('%Y-%m-%d')
    tomorrow=tomorrow.strftime('%Y-%m-%d')
    print("++++++",presentday)
    print(tomorrow)

    t = twint.Config()
    t.Search = keyword
    t.Store_object = True
    # t.Limit=1000
    t.Since = presentday
    t.Until= tomorrow
    t.Store_csv = True
    t.Output = 'tweet_results.csv'
    twint.run.Search(t)

    # DROP DUPLICATES
    df=pd.read_csv("tweet_results.csv")
    print(df)
    if df.empty:  
        pass
    else:  
        df =df.drop_duplicates(['tweet'])
        df=df.reset_index(drop=True)

        # CREATE LIST TO PERFORM VADERS
        tweets_list.extend(df['tweet'].tolist()) 
        scores = vaders_scores(tweets_list)
        print("=====",scores)

    # GET DATE in final
        final_date=presentday

        # make dataframe
        scraped_data = [[final_date,scores]]
        df=pd.DataFrame(scraped_data,columns=['Date','Scores'])
        
        # separate every score into separate columns
        df['Comp_Social']  = df['Scores'].apply(lambda score_dict: score_dict['compound'])
        df['Pos_Social']  = df['Scores'].apply(lambda score_dict: score_dict['pos'])
        df['Neu_Social']  = df['Scores'].apply(lambda score_dict: score_dict['neu'])
        df['Neg_Social']  = df['Scores'].apply(lambda score_dict: score_dict['neg'])

    # drop scores column
        df=df.drop(['Scores'],axis=1)
        print(df)

    # APPEND TO MAIN CSV
        append_to_csv(df,csv_name,final_date)

        # delete contents of  csv
        # os.remove("tweet_results{csv_name}.csv")
        # f = open("tweet_results.csv", "w")
        # f.truncate()
        # f.close() 
        # with open('tweet_results.csv', 'r+') as f:
        #     next(f) # read one line
        #     f.truncate() # terminate the file her
        with open('tweet_results.csv', 'r+',errors='ignore') as f:
            f.readline() # read one line
            f.truncate(f.tell()) # terminate the file here



    # print("+++++++++++++++",tlist)
    
    return "ABC"

def vaders_scores(headlines):
    # generate scores for headlines : SENTIMENT ANALYSIS
    scores=[]
    headlines_final="".join(map(str,headlines))
    scores = sid.polarity_scores(headlines_final)
    return scores 

