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
            {"news_csv":"TataFinalNews.csv","tweets_csv":"TataFinalTweets.csv","tech_csv":"TataFinalTech.csv","name":"TATAMOTORS","epoch":270,"lr":26},
            {"news_csv":"InfosysFinalNews.csv","tweets_csv":"InfosysFinalTweets.csv","tech_csv":"InfosysFinalTech.csv","name":"INFOSYS","epoch":150,"lr":27},
            {"news_csv":"HDFCFinalNews.csv","tweets_csv":"HDFCFinalTweets.csv","tech_csv":"HDFCFinalTech.csv","name":"HDFCBANK","epoch":400,"lr":56},
            {"news_csv":"BajajFinalNews.csv","tweets_csv":"BajajFinalTweets.csv","tech_csv":"BajajFinalTech.csv","name":"BAJAJAUTO","epoch":125,"lr":49},
            {"news_csv":"AirtelFinalNews.csv","tweets_csv":"AirtelFinalTweets.csv","tech_csv":"AirtelFinalTech.csv","name":"AIRTEL","epoch":150,"lr":0.189},
            {"news_csv":"AdaniFinalNews.csv","tweets_csv":"AdaniFinalTweets.csv","tech_csv":"AdaniFinalTech.csv","name":"ADANIPORTS","epoch":600,"lr":20}    
        ]
        data=[]
        
        for i in final_dataset:
            print('============',request.data['name'])
            print("||||||||||||||",i['name'])
            if request.data['name'] == i['name']:
                data=merge_to_final_dataset(i['news_csv'],i['tweets_csv'],i['tech_csv'],i['name'],i['epoch'],i['lr'])
                break
        # dataPred={"pred":data[0]}
        # dataActual={"actual":data[1]}
        print("+++++++++++++++",data)
        dataDict={"pred":data[0],"actual":data[1]}

        # print("[[[[[[[[[[[[[[[[",res['y_pred'])
        # serializer = StocksSerializer(data=request.data)
        # if serializer.is_valid(raise_exception=True):
        #     serializer.save()
            # return Response(serializer.data)
        return Response(data=dataDict,status=status.HTTP_200_OK)
