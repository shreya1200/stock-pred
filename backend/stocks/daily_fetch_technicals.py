from datetime import date
# import yfinance as yf




def scrape_all_technicals():
    START = '2000-01-01'
    TODAY = date.today().strftime("%Y-%m-%d")
    tweet_data=[
        # {"csv_name":"TataFinalNews.csv","keyword":"Tata Motor"},
        # {"csv_name":"InfosysFinalNews.csv","keyword":"Infosys"},
        # {"csv_name":"HDFCFinalNews.csv","keyword":"HDFC Bank"},
        {"csv_name":"BajajFinalTweets.csv","keyword":"Bajaj Auto"},
        # {"csv_name":"AirtelFinalNews.csv","keyword":"Airtel"},
        # {"csv_name":"AdaniFinalNews.csv","keyword":"Adani port"},
    ]
    for i in tweet_data:
        scrape_technicals(i['csv_name'],i['keyword'])

def scrape_technicals(csv_name,keyword):
    # Configure
    return "ABC"