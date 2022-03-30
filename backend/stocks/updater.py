from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from stocks import daily_fetch_news

def start():
    print('2')
    scheduler = BackgroundScheduler()
    scheduler.add_job(daily_fetch_news.scrape_all_news, 'interval', hours=12)
    scheduler.start()