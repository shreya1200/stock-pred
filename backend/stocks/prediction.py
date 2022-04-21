import pandas as pd
import numpy as np
from stocks.StockPredictor import Predictor,PredictorEntity
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time

def merge_to_final_dataset():
    final_dataset=[
        {"news_csv":"TataFinalNews.csv","tweets_csv":"TataFinalTweets.csv","tech_csv":"TataFinalTech.csv","name":"TATAMOTORS","epoch":270,"lr":26},
        {"news_csv":"InfosysFinalNews.csv","tweets_csv":"InfosysFinalTweets.csv","tech_csv":"InfosysFinalTech.csv","name":"INFOSYS","epoch":150,"lr":27},
        {"news_csv":"HDFCFinalNews.csv","tweets_csv":"HDFCFinalTweets.csv","tech_csv":"HDFCFinalTech.csv","name":"HDFCBANK","epoch":400,"lr":56},
        {"news_csv":"BajajFinalNews.csv","tweets_csv":"BajajFinalTweets.csv","tech_csv":"BajajFinalTech.csv","name":"BAJAJAUTO","epoch":125,"lr":49},
        {"news_csv":"AirtelFinalNews.csv","tweets_csv":"AirtelFinalTweets.csv","tech_csv":"AirtelFinalTech.csv","name":"AIRTEL","epoch":150,"lr":0.189},
        {"news_csv":"AdaniFinalNews.csv","tweets_csv":"AdaniFinalTweets.csv","tech_csv":"AdaniFinalTech.csv","name":"ADANIPORTS","epoch":600,"lr":20}    
    ]
    for i in final_dataset:
        news=pd.read_csv(f"stocks/datasets/{i['news_csv']}")
        tweets=pd.read_csv(f"stocks/datasets/{i['tweets_csv']}")
        technicals=pd.read_csv(f"stocks/datasets/{i['tech_csv']}")
        print(news)
        print(tweets)
        print(technicals)
        df = pd.merge(pd.merge(news,tweets,on='Date'),technicals,on='Date')
        df["Date"] = df["Date"].apply(lambda x:datetime.datetime.strptime(str(x), "%Y-%m-%d").strftime('%d-%m-%Y'))

        print("FINAL",df.columns)
        predict(df,i['name'],i['epoch'],i['lr'])

def predict(df,name,epoch,lr):
    print(name,epoch,lr)
    predictor_entity = PredictorEntity(
        name=name,
        epochs=epoch,
        lr=lr
    )

    machine = Predictor(df,predictor_entity)
    machine.compile()
    machine.test_predict()
    res = machine.res 
    # show_graph(res)
    # error_percent(res)

# # def show_res(res):
#     # print(machine.metrics())
#     plt.rcParams["figure.figsize"] = [60, 15]
#     plt.rcParams["font.size"] = 40
#     plt.rcParams["axes.labelsize"] = 60
#     plt.plot(res['y_pred'],label='y_pred',color='blue')
#     plt.plot(res['y_test'],label='y_test',color='red')
#     plt.xlim(xmin=0,xmax=len(res['y_test']))
#     plt.legend(prop={'size':30})
#     plt.show()
#     plt.rcParams.update({
#         "figure.figsize":[6.4,4.8],
#         "font.size":10,
#         "axes.labelsize":'medium',
#     })

# # def error_percent():
#     plt.rcParams["figure.figsize"] = [60, 15]
#     plt.rcParams["font.size"] = 40
#     plt.rcParams["axes.labelsize"] = 60
#     plt.plot(res['percent_error'],label='percent_error',color='blue')
#     plt.plot([10 for i in range(len(res['percent_error']))],label='10 line',color='red')
#     plt.ylabel("% Error")
#     plt.xlim(xmin=0,xmax=len(res['y_test']))
#     plt.legend(prop={'size':30})
#     plt.show()
#     plt.rcParams.update({
#         "figure.figsize":[6.4,4.8],
#         "font.size":10,
#         "axes.labelsize":'medium',
#     })

        



