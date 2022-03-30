import pandas as pd
from rest_framework.response import Response
import datetime
import time
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

def scrape_all_news():
    print("3_Start_now")
    stock_data=[
        {"csv_name":"TataFinalNews.csv","keyword":"Tata Motor"},
        {"csv_name":"InfosysFinalNews.csv","keyword":"Infosys"},
        {"csv_name":"HDFCFinalNews.csv","keyword":"HDFC Bank"},
        {"csv_name":"BajajFinalNews.csv","keyword":"Bajaj Auto"},
        {"csv_name":"AirtelFinalNews.csv","keyword":"Airtel"},
        {"csv_name":"AdaniFinalNews.csv","keyword":"Adani port"},
    ]
    for i in stock_data:
        scrape(i['csv_name'],i['keyword'])

def scrape(csv_name,keyword):
    # print(keyword)
    headlines = []
    scores=[]

    # your web scraping code here
    print('web scraping')
    url_data= 'https://economictimes.indiatimes.com/headlines.cms'
    print(url_data)
    daily = requests.get(url_data)
    print(daily)
    content_daily = daily.text
    soup=BeautifulSoup(content_daily,'lxml')

    # Fetch Date from headlines page
    date_data = soup.find_all("span",{"class":"dib time"})
    arg=date_data[0].string
    date= arg[:-14]
    # print("***",date)

    # Change date format
    final_date=format_date(date)
    # print("--",final_date)

    # Fetch Headlines as list
    headline_data = soup.findAll("a")
    # arg=headline_data

    for texts in headline_data:
        # print(texts)
        if keyword in texts.text:
            headlines.append(texts.string)
    
    # apply Vader's algorithm
    scores=vaders_scores(headlines)
    # print(scores)

    # CREATE DATAFRAME
    # Add scraped data to dataframe
    scraped_data = [[final_date,scores]]
    # print(scraped_data)
    df=pd.DataFrame(scraped_data,columns=['Date','Scores'])
    
    # separate every score into separate columns
    df['Comp_News']  = df['Scores'].apply(lambda score_dict: score_dict['compound'])
    df['Pos_News']  = df['Scores'].apply(lambda score_dict: score_dict['pos'])
    df['Neu_News']  = df['Scores'].apply(lambda score_dict: score_dict['neu'])
    df['Neg_News']  = df['Scores'].apply(lambda score_dict: score_dict['neg'])

    # drop scores column
    df=df.drop(['Scores'],axis=1)

    # append DataFrame to respective csv
    append_to_csv(df,csv_name,final_date)   



def format_date(date):
    # change date format: to yyyy-mm-dd
    months = {
        'January':'01',
        'February':'02',
        'March':'03',
        'April':'04',
        'May':'05',
        'June':'06',
        'July':'07',
        'August':'08',
        'September':'09',
        'October':'10',
        'November':'11',
        'December':'12',
    }

    date=date.replace(",","")
    date = date.split(' ')
    return f"{date[2]}-{months.get(date[1])}-{date[0]}"
        
def vaders_scores(headlines):
    # generate scores for headlines : SENTIMENT ANALYSIS
    scores=[]
    headlines_final="".join(map(str,headlines))
    scores = sid.polarity_scores(headlines_final)
    return scores
    

def append_to_csv(df,csv_name,final_date):
    # APPEND formatted dataframe to original CSV
    data = pd.read_csv(f"stocks/datasets/{csv_name}")    

    # check whether last entry is not of the same day to avoid redundancy
    date=data.tail(1).Date.tolist()

    if date[0] == final_date:
        # if the last entry is having same date then overwrite it with new data
        data.drop(index=data.index[-1], axis=0, inplace=True)
        final=pd.concat([data,df],ignore_index=True)
        final.to_csv(f"stocks/datasets/{csv_name}",index=False)
        print(final)
    else:
        # append fresh data without deleting
        final=pd.concat([data,df],ignore_index=True)
        final.to_csv(f"stocks/datasets/{csv_name}",index=False)
        print(final)

