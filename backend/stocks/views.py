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
import schedule

# Create your views here.
  
class StocksView(APIView):
    # fetch_data("InfosysFinal.csv")
    # stock_data={"csv_name":{"TataFinal.csv","InfosysFinal.csv","HDFCFinal.csv","BajajFinal.csv","AirtelFinal.csv","AdaniFinal.csv"}}
    
    # scrape_all_news()

    scrape_all_tweets()

    scrape_all_technicals()

    # SCHEDULE SCRAPE FOR EVERYDAY
    # schedule.every().day.at("14:10").do(scrape_all_news)# change 10:30 to time of your choice
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    
        # scrape_news(i['csv_name'],i['keyword'])
        # scrape()
    
    serializer_class = StocksSerializer
  
    def get(self, request):
        detail = [ {"name": detail.name,"detail": detail.detail} 
        for detail in Stocks.objects.all()]
        return Response(detail)
  
    def post(self, request):  
        serializer = StocksSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return  Response(serializer.data)