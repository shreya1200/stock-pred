from django.apps import AppConfig
from stocks.daily_fetch_news import *


class StocksConfig(AppConfig):
    name = 'stocks'

    # def ready(self):
    #     from stocks import updater
    #     print('1')
    #     updater.start()