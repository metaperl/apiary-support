import matplotlib.pyplot as plt
import numpy
import oandapy
import talib
from talib import MA_Type

oanda = oandapy.API(
    environment="practice",
    access_token="09e045ddd077887b7430cca657bb22cd-945b6dc2ec3fc1f43a39f6481e27cfcf")

# Get price for an instrument
response = oanda.get_prices(instruments="EUR_USD")
prices = response.get("prices")
asking_price = prices[0].get("ask")
print prices[0]
print asking_price

# Get history for an instrument
response = oanda.get_history(instrument="EUR_USD", count=2)
prices = response.get("candles")
print prices


class Trader(object):

    def __init__(self, oanda, granularity='H1', period=50):
        self.oanda = oanda
        self.granularity = granularity
        self.period = 50

    @property
    def candles(self):
        return self.history.get("candles")

    @property
    def history(self):
        self._history = self.oanda.get_history(
            instrument="EUR_USD",
            count=self.period,
            granularity=self.granularity)
        return self._history

    @property
    def inputs(self):
        candles = self.candles
        self._inputs = {
            'volume': numpy.array([candle['volume'] for candle in candles]),
            'open': numpy.array([candle['openAsk'] for candle in candles]),
            'low': numpy.array([candle['lowAsk'] for candle in candles]),
            'high': numpy.array([candle['highAsk'] for candle in candles]),
            'close': numpy.array([candle['closeAsk'] for candle in candles])
            }
        return self._inputs

    def sma(self, period=50):
        candles = self.candles
        close_ask = numpy.array([candle['closeAsk'] for candle in candles])
        sma = talib.SMA(close_ask, timeperiod=period)
        print "SMA=", sma

    @staticmethod
    def drawbox(a):
        figure = plt.figure()
        ax = figure.add_subplot(111)
        ax.plot(a)
        plt.show()

    def stochastic(self, fast_k=14, slow_k=3, fast_d=3, slow_d=3):
        candles = self.candles
        self.drawbox(self.inputs['high'])
        slowk, slowd = talib.abstract.STOCH(
            self.inputs, fast_k, slow_k, MA_Type.SMA, slow_d, MA_Type.EMA)
        print "SLOWK, SLOWD", slowk, slowd, type(slowk), type(slowd)
        self.drawbox(slowk)
        self.drawbox(slowd)


t = Trader(oanda, 'M15')
t.drawbox(t.inputs['close'])
t.sma()
t.stochastic()



# http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:stochastic_oscillator_fast_slow_and_full
