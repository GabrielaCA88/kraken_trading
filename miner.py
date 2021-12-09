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
    # def plot_data(self):
    #     # first declare an empty figure
    #     fig = go.Figure()
    #
    #     # declare subplots
    #     fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
    #                         vertical_spacing=0.01,
    #                         row_heights=[0.5, 0.1])
    #
    #     # set up the candlestick bar
    #     fig.add_trace(go.Candlestick(x=self.ohlc.index,
    #                                  open=self.ohlc[('open')],
    #                                  high=self.ohlc[('high')],
    #                                  low=self.ohlc[('low')],
    #                                  close=self.ohlc[('close')],
    #                                  showlegend=False))
    #     # set up the vwap line
    #     fig.add_trace(go.Scatter(
    #         x=self.ohlc.index,
    #         y=self.ohlc['vwap'],
    #         mode='lines',
    #         name='vwap1',
    #         line=dict(color='royalblue', width=2),
    #         showlegend=False
    #     ))
    #
    #     # include a volume bar
    #     colors = ['green' if row['open'] - row['close'] >= 0
    #               else 'red' for index, row in self.ohlc.iterrows()]
    #     fig.add_trace(go.Bar(x=self.ohlc.index,
    #                          y=self.ohlc['volume'],
    #                          marker_color=colors,
    #                          showlegend=False
    #                          ), row=2, col=1)
    #
    #     # remove rangeslider
    #     fig.update_layout(xaxis_rangeslider_visible=False)
    #
    #     fig.update_yaxes(title_text="Price", row=1, col=1)
    #     fig.update_yaxes(title_text="Volume", row=2, col=1)
    #
    #     fig.show()

#Execute

#d=Tradedata ('BTCUSD', '1607188303', '1440')
#d.get_data()
# d.plot_data()


