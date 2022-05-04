from datetime import date,timedelta
import time
import yfinance as yf
import pandas as pd

def load_data(ticker, TODAY,TOMORROW):
    data = yf.download(ticker, TODAY.strftime('%Y-%m-%d'), TOMORROW.strftime('%Y-%m-%d'))
    data.reset_index(inplace=True)
    return data

def scrape_all_technicals():
    # START = '2000-01-01'
    TODAY = date.today()
    TOMORROW = TODAY + timedelta(1)
    technicals_data=[
        {"csv_name":"TataFinalTech.csv","keyword":"Tata Motor","url_key":"TATAMOTORS.NS"},
        {"csv_name":"InfosysFinalTech.csv","keyword":"Infosys","url_key":"INFY.NS"},
        {"csv_name":"HDFCFinalTech.csv","keyword":"HDFC Bank","url_key":"HDFCBANK.NS"},
        {"csv_name":"BajajFinalTech.csv","keyword":"Bajaj Auto","url_key":"BAJFINANCE.NS"},
        {"csv_name":"AirtelFinalTech.csv","keyword":"Airtel","url_key":"BHARTIARTL.NS"},
        {"csv_name":"AdaniFinalTech.csv","keyword":"Adani port","url_key":"ADANIPORTS.NS"},
    ]
    for i in technicals_data:
        # scrape_technicals(i['csv_name'],i['keyword'],i['url_key'])
        data = load_data(i['url_key'], TODAY,TOMORROW)
        df=pd.DataFrame(data.tail(1))
        print("*********",i['url_key'])

        if df.empty:  
            pass
        else:
            append_to_csv(df,i['csv_name'],TODAY)
            # print(df)

        # df.to_csv(f"stocks/datasets/{i['csv_name']}",index=False)


        # print(data.tail())

def append_to_csv(df,csv_name,TODAY):
    # APPEND formatted dataframe to original CSV
    df['Date'][0]=TODAY.strftime('%Y-%m-%d')
    print("CSV=====",csv_name)
    data = pd.read_csv(f"stocks/datasets/{csv_name}")    
    # check whether last entry is not of the same day to avoid redundancy
    date=data.tail(1).Date.tolist()
    if date[0] == df['Date'][0]:
        print("IN IF")
        # if the last entry is having same date then overwrite it with new data
        data.drop(index=data.index[-1], axis=0, inplace=True)
        final=pd.concat([data,df],ignore_index=True)
        final.to_csv(f"stocks/datasets/{csv_name}",index=False)
        print(final)
    else:
        print("IN ELSE")
        # append fresh data without deleting
        final=pd.concat([data,df],ignore_index=True)
        final.to_csv(f"stocks/datasets/{csv_name}",index=False)
        print(final)


def technical_data(url_key):
    TODAY = date.today()
    TOMORROW = TODAY + timedelta(1)
    data = load_data(url_key, TODAY,TOMORROW)
    print("dhfshgfjdbkjf",data)

    return data