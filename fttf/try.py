#!/usr/bin/env python

# core
from datetime import datetime

# 3rd party
from matplotlib.finance import candlestick_ohlc
import matplotlib.pyplot as plt
import matplotlib
import numpy
import oandapy
import talib


# local

oanda = oandapy.API(
    environment="practice",
    access_token="09e045ddd077887b7430cca657bb22cd-945b6dc2ec3fc1f43a39f6481e27cfcf")

# # Get price for an instrument
# response = oanda.get_prices(instruments="EUR_USD")
# prices = response.get("prices")
# asking_price = prices[0].get("ask")
# print asking_price

# # Get history for an instrument
# response = oanda.get_history(instrument="EUR_USD", count=2)
# prices = response.get("candles")
# print prices


class Trader(object):

    def __init__(self, oanda, granularity='H1', count=3500):
        self.oanda = oanda
        self.granularity = granularity
        self.count = count

    @property
    def candles(self):
        return self.history.get("candles")

    @property
    def history(self):
        self._history = self.oanda.get_history(
            instrument="EUR_USD",
            count=self.count,
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

    @property
    def candlestick_ohlc_data(self):
        d = [
            (matplotlib.dates.date2num(
                datetime.strptime(candle['time'], '%Y-%m-%dT%X.%fZ')),
             candle['openAsk'], candle['highAsk'],
             candle['lowAsk'], candle['closeAsk'],
             candle['volume'])
            for candle in self.candles]
        #print d[0]
        return d

    def sma(self, period=50):
        candles = self.candles
        close_ask = numpy.array([candle['closeAsk'] for candle in candles])
        sma = talib.SMA(close_ask, timeperiod=period)
        print "SMA=", sma

    def stochastic(self, fast_k=14, slow_k=3, fast_d=3, slow_d=3):
        candles = self.candles
        slowk, slowd = talib.abstract.STOCH(
            self.inputs,
            fast_k, slow_k, talib.MA_Type.SMA, slow_d,
            talib.MA_Type.EMA)
        #print "SLOWK, SLOWD", slowk, slowd, type(slowk), type(slowd)
        return slowk

    def atr(self):
        real = talib.abstract.ATR(
            self.inputs)
        return real

    def simple_y(self, grapher):
        d = [c[0] for c in trading.candlestick_ohlc_data]
        print "Length of data={0}".format(len(d))
        grapher.simple_y(d)


class Grapher(object):
    def __init__(self):
        self.figure = plt.figure()
        gs = (6, 4)
        self.axis = dict()
        self.axis['ohlc'] = plt.subplot2grid(gs, (0, 0), rowspan=4, colspan=4)
        self.axis['stochastic'] = plt.subplot2grid(gs, (4, 0), colspan=4)
        self.axis['atr'] = plt.subplot2grid(gs, (5, 0), colspan=4)

    def draw_ohlc(self, quotes):
        candlestick_ohlc(
            self.axis['ohlc'],
            quotes, width=0.6)

    def draw_stochastic(self, seq):
        self.axis['stochastic'].plot(seq)

    def simple_ohlc(self, seq):
        self.axis['ohlc'].plot(seq)

    def draw_atr(self, seq):
        self.axis['atr'].plot(seq)

    def simple_y(self, seq):
        self.axis['atr'].plot(seq)


#t = Trader(oanda, 'M15')
trading = Trader(oanda, 'H1', count=250)
grapher = Grapher()

grapher.simple_ohlc(trading.inputs['close'])
grapher.draw_stochastic(trading.stochastic())
grapher.draw_atr(trading.atr())

plt.show()

while True:
    pass

# Goal: A graph similar to what I have at Oanda visually
# Main graph is candlesticks with 50 SMA
# subplot2grid( (y_cells, x_cells), (y_upper_left,x_upper_left) )
# subplot2grid( (6,4), (0,0), rowspan=4, colspan=4)

# below main is Stochastic
# subplot2grid( (6,4), (4,0), rowspan=1, colspan=4)

# below that is ATR
# subplot2grid( (6,4), (5,0), rowspan=1, colspan=4)



# http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:stochastic_oscillator_fast_slow_and_full

# Notes:
# http://matplotlib.org/users/gridspec.html
# subplot2grid((ygrid,xgrid), (y,x))  # takes rowspan and colspan args which
                                      # which default to 1
