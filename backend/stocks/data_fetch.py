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

def scrape_news(csv_name,keyword):
    headline_data=[]
    dates = []
    headlines = []

    for i in range(44648,44650):   
        url_date= 'https://economictimes.indiatimes.com/archivelist/year-2022,month-1,starttime-'+str(i)+'.cms'
        print(url_date)
        monthwise = requests.get(url_date)
        content_monthwise = monthwise.text
        soup=BeautifulSoup(content_monthwise,'lxml')

        # to collect date of news
        table=soup.table
        for tag in table.descendants:
            if ',' in tag:
                date=tag.string

        news=soup.section
        for headline in news.descendants:
            if keyword in headline: #change keyword acc to company and corresponding data
                headline_data.append(headline.string)

        dates += [date for _ in range(0, len(headline_data))]
        headlines += headline_data

    empty = pd.DataFrame({'Date': dates, 'Headline': headlines})
    format_data_news(empty,csv_name)



def format_data_news(df1,csv_name):
    # drop duplicates
    df1 =df1.drop_duplicates()
    df1=df1.reset_index(drop=True)

    # change date format:
    months = {
        'Jan':'01',
        'Feb':'02',
        'Mar':'03',
        'Apr':'04',
        'May':'05',
        'Jun':'06',
        'Jul':'07',
        'Aug':'08',
        'Sep':'09',
        'Oct':'10',
        'Nov':'11',
        'Dec':'12',
    }

    def getDate(date):
        date=date.replace(",","")
        date = date.split(' ')
        return f"{date[2]}-{months.get(date[1])}-{date[0]}"

    len=df1["Date"].shape[0]
    # print(len)

    for i in range(len):
        df1.loc[i,"Date"]=getDate(df1.loc[i,"Date"])
    
    merge_data(df1,csv_name)



def merge_data(df1,csv_name):
    df1 = df1.groupby(['Date'])['Headline'].apply(':: '.join).reset_index()
    df1=df1.reset_index(drop=True)
    # print (df1[['Date','Headline']])

    vaders(df1,csv_name)

def vaders(df1,csv_name):
    print("Jai bajrang bali")
    df1.dropna(inplace=True)

    blanks = []  # start with an empty list

    for i,lb,rv in df1.itertuples():  
        if type(rv)==str:            
            if rv.isspace():        
                blanks.append(i)     

    df1.drop(blanks, inplace=True)
    # print(df1)

    scores=[]
    for i in range (0,len(df1)):
        sentence=df1.loc[i,'Headline']
        scores.append(sid.polarity_scores(sentence))
    
    # print(scores)

    df1['Scores']=scores
    # print(df1)

    df_separated=df1.copy()
    df_separated['Comp_News']  = df_separated['Scores'].apply(lambda score_dict: score_dict['compound'])
    df_separated['Pos_News']  = df_separated['Scores'].apply(lambda score_dict: score_dict['pos'])
    df_separated['Neu_News']  = df_separated['Scores'].apply(lambda score_dict: score_dict['neu'])
    df_separated['Neg_News']  = df_separated['Scores'].apply(lambda score_dict: score_dict['neg'])

    # print(df_separated)

    df_separated=df_separated.drop(['Headline','Scores'],axis=1)
    # df_separated["Date"] = df_separated["Date"].apply(lambda x:datetime.datetime.strptime(x, "%Y-%m-%d").strftime('%d-%m-%Y'))

    # print(df_separated)

   
    data = fetch_data(csv_name)
    append_csv(data,df_separated,csv_name)
    # data = fetch_data("HDFCFinal.csv")
    # append_csv(data,df_separated,"HDFCFinal.csv")

def fetch_data(a):
    data = pd.read_csv(f"stocks/datasets/{a}")
    # Sort csv in ascending order
    df= data.copy()
    # df["Date"] = df["Date"].apply(lambda x:datetime.datetime.strptime(str(x), "%d-%m-%Y").strftime('%Y-%m-%d'))
    df.sort_values(by='Date', inplace=True)
    df=df.reset_index(drop=True)
    print(df)
    # print(df)
    return df

def append_csv(data,df_separated,a):
    final=pd.concat([data,df_separated],ignore_index=True)
    data1=pd.read_csv(f"stocks/datasets/{a}")
    final.to_csv(f"stocks/datasets/{a}",index=False)



   




