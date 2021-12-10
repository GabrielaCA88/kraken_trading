import krakenex
from pykrakenapi import KrakenAPI
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

class Tradedata():

    def __init__(self, pair, since, interval):
        # initiate api
        api = krakenex.API()
        self.k = KrakenAPI(api)

        # set pair
        self.pair = pair
        # self.tz = pytz.timezone(timezone)
        self.since = since
        self.interval = interval
        

    def get_data(self):
        self.ohlc = pd.DataFrame()

        ohlc, since = self.k.get_ohlc_data(pair=self.pair, since=self.since, interval=self.interval)

        ohlc.drop(columns='vwap', inplace=True)
        v = ohlc['volume'].values
        tp = (ohlc['low'] + ohlc['close'] + ohlc['high']).div(3).values
        ohlc = ohlc.assign(vwap=(tp * v).cumsum() / v.cumsum())

        self.ohlc = ohlc

        return ohlc
  
