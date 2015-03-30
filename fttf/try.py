import matplotlib.pyplot as plt
import numpy
import oandapy
import talib

oanda = oandapy.API(
    environment="practice",
    access_token="09e045ddd077887b7430cca657bb22cd-945b6dc2ec3fc1f43a39f6481e27cfcf")
### Get price for an instrument
response = oanda.get_prices(instruments="EUR_USD")
prices = response.get("prices")
asking_price = prices[0].get("ask")
print prices[0]
print asking_price


response = oanda.get_history(instrument="EUR_USD", count=2)
prices = response.get("candles")
print prices

class Trader(object):

    def __init__(self, oanda, granularity):
        self.oanda = oanda
        self.granularity=granularity

    def sma(self, period=50):
        response = self.oanda.get_history(
            instrument="EUR_USD",
            count=period,
            granularity=self.granularity)
        candles = response.get("candles")
        candles = numpy.array([candle['closeAsk'] for candle in candles])
        print candles, type(candles)
        sma = talib.SMA(candles, timeperiod=period)
        print sma

    def stochastic(self, fast_k=14, slow_k=3, fast_d=3, slow_d=3):
        candles = self.oanda.get_history(
            instrument="EUR_USD",
            granularity=self.granularity)['candles']
        inputs = {
            'low': numpy.array([candle['lowAsk'] for candle in candles]),
            'high': numpy.array([candle['highAsk'] for candle in candles]),
            'close': numpy.array([candle['closeAsk'] for candle in candles])
            }
        slowk, slowd = talib.abstract.STOCH(
            inputs, fast_k, slow_k, 0, slow_d, 0)
        print "SLOWK, SLOWD", slowk, slowd, type(slowk), type(slowd)
        figure = plt.figure()
        ax = figure.add_subplot(111)
        ax.plot(slowk)
        plt.show()
        print 'showing'



t = Trader(oanda, 'H1')
t.sma()
t.stochastic()


# http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:stochastic_oscillator_fast_slow_and_full
