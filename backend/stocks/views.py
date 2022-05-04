from django.shortcuts import render
from rest_framework.views import APIView
from . models import *
from rest_framework.response import Response
from . serializer import *
import pandas as pd
# from stocks.data_fetch import *
from stocks.daily_fetch_news import *
from stocks.daily_fetch_tweets import *
from stocks.daily_fetch_technicals import *
# from stocks.prediction import predicted,actual
from stocks.prediction import *
import schedule
from rest_framework import status
from rest_framework.permissions import AllowAny

# Create your views here.


class StocksView(APIView):
    # fetch_data("InfosysFinal.csv")
    # stock_data={"csv_name":{"TataFinal.csv","InfosysFinal.csv","HDFCFinal.csv","BajajFinal.csv","AirtelFinal.csv","AdaniFinal.csv"}}

    # scrape_news_now()

    scrape_all_news()

    scrape_all_tweets()

    scrape_all_technicals()

    # merge_to_final_dataset()

    # SCHEDULE SCRAPE FOR EVERYDAY
    # schedule.every().day.at("14:10").do(scrape_all_news)# change 10:30 to time of your choice
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    # scrape_news(i['csv_name'],i['keyword'])
    # scrape()

    serializer_class = StocksSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        detail = [{"name": detail.name, "detail": detail.detail}
                  for detail in Stocks.objects.all()]
        return Response(detail)

    def post(self, request):
        print("============+++++++++",request.data['name'])
        final_dataset=[
            {
                "news_csv":"TataFinalNews.csv",
                "tweets_csv":"TataFinalTweets.csv",
                "tech_csv":"TataFinalTech.csv",
                "name":"TATAMOTORS",
                "epoch":270,
                "lr":26,
                "keyword_news":"Tata Motor",
                "keyword_tweets":"Tata Motors Stocks",
                "url_key":"TATAMOTORS.NS"
            },
            {
                "news_csv":"InfosysFinalNews.csv",
                "tweets_csv":"InfosysFinalTweets.csv",
                "tech_csv":"InfosysFinalTech.csv",
                "name":"INFOSYS",
                "epoch":150,
                "lr":27,
                "keyword_news":"Infosys",
                "keyword_tweets":"INFY Stocks",
                "url_key":"INFY.NS"
                
            },
            {
                "news_csv":"HDFCFinalNews.csv",
                "tweets_csv":"HDFCFinalTweets.csv",
                "tech_csv":"HDFCFinalTech.csv",
                "name":"HDFCBANK",
                "epoch":400,
                "lr":56,
                "keyword_news":"HDFC Bank",
                "keyword_tweets":"HDFC Bank Stocks",
                "url_key":"HDFCBANK.NS"
            },
            {
                "news_csv":"BajajFinalNews.csv",
                "tweets_csv":"BajajFinalTweets.csv",
                "tech_csv":"BajajFinalTech.csv",
                "name":"BAJAJAUTO",
                "epoch":125,
                "lr":49,
                "keyword_news":"Bajaj Auto",
                "keyword_tweets":"Bajaj Auto Stocks",
                "url_key":"BAJFINANCE.NS"
            },
            {
                "news_csv":"AirtelFinalNews.csv",
                "tweets_csv":"AirtelFinalTweets.csv",
                "tech_csv":"AirtelFinalTech.csv",
                "name":"AIRTEL",
                "epoch":150,
                "lr":0.189,
                "keyword_news":"Airtel",
                "keyword_tweets":"Airtel Stocks",
                "url_key":"BHARTIARTL.NS"
            },
            {
                "news_csv":"AdaniFinalNews.csv",
                "tweets_csv":"AdaniFinalTweets.csv",
                "tech_csv":"AdaniFinalTech.csv",
                "name":"ADANIPORTS",
                "epoch":600,
                "lr":20,
                "keyword_news":"Adani port",
                "keyword_tweets":"Adani port Stocks",
                "url_key":"ADANIPORTS.NS"
            }    
        ]
        data=[]
        
        for i in final_dataset:
            print('============',request.data['name'])
            print("||||||||||||||",i['name'])
            if request.data['name'] == i['name']:
                data=merge_to_final_dataset(i['news_csv'],i['tweets_csv'],i['tech_csv'],i['name'],i['epoch'],i['lr'])
                newsData=news_headlines(i['keyword_news'])
                print("=-=-==-=-=-=-=-=-=-=",newsData)
                tweetData=tweets_data(i['keyword_tweets'])
                print("||||||++++++++||||||||",tweetData)
                techData=technical_data(i["url_key"])
                print("||||||+++++++++++++___________________________++++++++++++++||||||",techData)
                break
        dataPred={"pred":data[0]}
        print("::::::::::",dataPred)
        # dataActual={"actual":data[1]}
        # print("+++++++++++++++",data)
        tomorrowsPred=data[0][-1]-techData['Close']
        if tomorrowsPred[0]>0:
            trend="Positive"
        else:
            trend="Negative"
        dataDict={"pred":data[0],"actual":data[1],"news":newsData,"tweets":tweetData,"technicals":{"open":techData['Open'],"low":techData['Low'],"high":techData['High'],"close":techData['Close'],"adjClose":techData['Adj Close'],"vol":techData['Volume'],"tomorrowsPred":trend}}
        # print("apoorva",dataDict)
    

        # print("[[[[[[[[[[[[[[[[",res['y_pred'])
        # serializer = StocksSerializer(data=request.data)
        # if serializer.is_valid(raise_exception=True):
        #     serializer.save()
            # return Response(serializer.data)
        return Response(data=dataDict,status=status.HTTP_200_OK)
