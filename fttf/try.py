#!/usr/bin/env python

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


# core
from datetime import datetime

# 3rd party
import argh
import enum
from matplotlib.finance import candlestick_ohlc
import matplotlib.pyplot as plt
import matplotlib
import numpy
import oandapy
import talib

# local
import config
import savefig


oanda = None
def connect_to(env):
    global oanda
    oanda = oandapy.API(
        environment=env,
        access_token=config.access_token[env]
    )


# # Get price for an instrument
# response = oanda.get_prices(instruments="EUR_USD")
# prices = response.get("prices")
# asking_price = prices[0].get("ask")
# print asking_price

# # Get history for an instrument
# response = oanda.get_history(instrument="EUR_USD", count=2)
# prices = response.get("candles")
# print prices

def loop_forever():
    while True:
        pass


class Trend(enum.Enum):
    up = 1
    neutral = 0
    down = -1


class Trader(object):

    def __init__(self, oanda, grapher, granularity='H1', count=3500):
        self.oanda = oanda
        self.granularity = granularity
        self.count = count
        self.grapher = grapher

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
        #  print d[0]
        return d

    def sma(self, period=50):
        self.sma = talib.abstract.SMA(self._inputs, timeperiod=period)
        import numpy
        self.m_sma = numpy.diff(self.sma)  # the slope of the SMA 50
        print "SMA={0}\nM_SMA={1}".format(
            self.sma[-3:], self.m_sma[-2:])
        return self.sma

    def stochastic(self, fast_k=14, slow_k=3, fast_d=3, slow_d=3):
        candles = self.candles
        slowk, slowd = talib.abstract.STOCH(
            self.inputs,
            fast_k, slow_k, talib.MA_Type.SMA, slow_d,
            talib.MA_Type.EMA)
        #  print "SLOWK, SLOWD", slowk, slowd, type(slowk), type(slowd)
        self.stoch = slowk
        self.m_stoch = numpy.diff(slowk)
        print "stoch={0}\nM_stoch={1}".format(
            slowk[-3:], self.m_stoch[-2:])
        return slowk

    def atr(self):
        real = talib.abstract.ATR(
            self.inputs)
        return real

    # def simple_y(self, grapher):
    #     d = [c[0] for c in trading.candlestick_ohlc_data]
    #     print "Length of data={0}".format(len(d))
    #     grapher.simple_y(d)

    @property
    def overall_trend(self):
        if self.m_sma[-1] > 0:
            self.trend = Trend.up
        elif self.m_sma[-1] < 0:
            self.trend = Trend.down
        else:
            self.trend = Trend.neutral

        return self.trend

    @property
    def stochastic_trend(self):
        if self.m_stoch[-1] > 0:
            self.stoch_trend = Trend.up
        elif self.m_stoch[-1] < 0:
            self.stoch_trend = Trend.down
        else:
            self.stoch_trend = Trend.neutral

        return self.stoch_trend

    @property
    def stochastic_positioned(self):
        if self.overall_trend == Trend.up:
            if self.stoch[-2] < 50:
                return True

        if self.overall_trend == Trend.down:
            if self.stoch[-2] > 50:
                return True

        return False

    @property
    def account(self):
        aid = self.oanda.get_accounts()['accounts'][0]['accountId']
        print "Accounts: {0}".format(aid)
        return aid

    def open_trade(self):
        side = 'buy'
        if self.overall_trend == Trend.up:
            print "Opening BUY"
            side = 'buy'
        else:
            print "Opening SELL"
            side = 'sell'

        inst = 'EUR_USD'
        units = 100000 # 1 standard lot

        self.oanda.create_order(
            self.account,
            instrument=inst,
            units=units,
            side=side,
            type='market',
            trailingStop=5
        )

    def trade(self):
        print "Overall trend: {0}. Stochastic trend {1}".format(
            self.overall_trend, self.stochastic_trend)
        axis = self.grapher.axis['ohlc']
        axis.set_title("Overall: {0}".format(self.overall_trend), loc='left')
        axis.set_title("Stochastic: {0}".format(self.stochastic_trend))
        if self.overall_trend == self.stochastic_trend:
            if self.stochastic_positioned:
                print "Stochastic value of {0} is positioned".format(
                    self.stoch[-2])
                axis.set_title("Trading. Stoch={0}.".format(self.stoch[-2]),
                          loc='right')
                self.open_trade()
            else:
                print "Stochastic value of {0} is not positioned".format(
                    self.stoch[-2])
                axis.set_title("No Trade.Stoch={0}.".format(self.stoch[-2]),
                          loc='right')


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

    def draw_sma(self, seq):
        label1 = 'SMA(50)'
        self.axis['ohlc'].plot(seq, '#e1edf9', label=label1, linewidth=5)

    def draw_stochastic(self, seq):
        self.axis['stochastic'].plot(seq)

    def simple_ohlc(self, seq):
        self.axis['ohlc'].plot(seq)

    def draw_atr(self, seq):
        self.axis['atr'].plot(seq)

    def simple_y(self, seq):
        self.axis['atr'].plot(seq)


def main(
        env='practice', show_graph=False, save_graph=False,
        trade=False, stayup=False,
        timeframe='M15'):

    connect_to(env)

    grapher = Grapher()
    trading = Trader(oanda, grapher, timeframe, count=100)


    grapher.simple_ohlc(trading.inputs['close'])
    grapher.draw_stochastic(trading.stochastic())
    grapher.draw_atr(trading.atr())
    grapher.draw_sma(trading.sma())

    if trade:
        trading.trade()
        print "Trading algorithm completed."
        if show_graph:
            plt.show()
        if save_graph:
            savefig.save(
                savefig.datetime_as_file())
        if stayup:
            loop_forever()
    else:
        plt.show()
        loop_forever()


if __name__ == '__main__':
    argh.dispatch_command(main)
