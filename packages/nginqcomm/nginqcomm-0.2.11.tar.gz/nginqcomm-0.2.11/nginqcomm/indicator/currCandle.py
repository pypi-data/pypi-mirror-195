from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
from datetime import datetime
import math
import numpy
import pandas as pd
import sys
import time

sys.path.append("../")
from utils import datetimeUtil
from indicator.heikin_ashi import HA
from feed.SimpleOHLCV import SimpleOHLCV


class LastHourAvgInd(bt.Indicator):
    '''
    @brief 计算一个小时内的平均值
            该指标当前未考虑通用型，暂时只能用在 1m 周期上
    '''
    lines = ('localline', )

    def next(self):
        # 需要计算的柱子数
        #   按当前的分钟数来计算，综合考虑当前已有的柱子数（len(self.data.datetime)）

        lastHourCandleNum = 60  # 默认是60根柱子

        # 第0~59分的赋值
        if datetime.now().minute > 0:
            lastHourCandleNum = min(datetime.now().minute,
                                    len(self.data.datetime))

        retAvg = math.fsum(
            self.data.get(size=lastHourCandleNum)) / lastHourCandleNum

        print(datetime.now().strftime("%Y%m%d %H:%M:%S"), "DEBUG",
              'LastHourAvgInd', 'lastHourCandleNum', lastHourCandleNum,
              'retAvg', retAvg)

        self.line[0] = retAvg


class LastNAvg(bt.indicators.PeriodN):
    '''
    @brief 计算 N个柱子内的平均值
    '''
    lines = ('localline', )

    def next(self):

        print(datetime.now().strftime("%Y%m%d %H:%M:%S"), "DEBUG",
              'LastNAvg next() 000000', 'period', self.p.period)

        if (self.p.period <= 0):
            return

        print(datetime.now().strftime("%Y%m%d %H:%M:%S"), "DEBUG",
              'LastNAvg next() 111111', 'self.data.get(size=self.p.period)',
              self.data.get(size=self.p.period))

        retAvg = math.fsum(self.data.get(size=self.p.period)) / self.p.period

        print(datetime.now().strftime("%Y%m%d %H:%M:%S"), "DEBUG",
              'LastNAvg next()', 'period', self.p.period, 'retAvg', retAvg)

        self.line[0] = retAvg


def ConvertDateTime(feed=None, size=1000):
    arrDateTime = feed.datetime.get(size=size)
    arrTs = []
    for currDateTime in arrDateTime:
        # print(currDateTime, currDateTime)
        currTs = datetimeUtil.datasDateTime2TsSec(currDateTime)
        arrTs.append(currTs)

    return {
        'open': feed.open.get(size=size),
        'high': feed.high.get(size=size),
        'low': feed.low.get(size=size),
        'close': feed.close.get(size=size),
        'volume': feed.volume.get(size=size),
        'ts': arrTs
    }


def appendOhlcv(src=None, appendItem=None):
    print(
        'appendOhlcv',
        # 'src', src,
        'typeOf(src[open])',
        type(src['open']),
        #   'appendItem',
        #       appendItem
    )
    # print('src[open] len', len(src['open']))

    src['open'].append(appendItem['open'])
    src['high'].append(appendItem['high'])
    src['low'].append(appendItem['low'])
    src['close'].append(appendItem['close'])
    src['volume'].append(appendItem['volume'])
    src['ts'].append(appendItem['ts'])

    return src


def OhlcvHA(ohlcv=None):
    return HA(o=ohlcv.open,
              h=ohlcv.high,
              l=ohlcv.low,
              c=ohlcv.close,
              v=ohlcv.volume,
              ts=ohlcv.ts)


def FeedHA(feed=None, size=1000, inputResConvert=None):
    resConvert = None
    if (None != feed):
        resConvert = ConvertDateTime(feed, size)
    else:
        resConvert = inputResConvert

    return HA(o=resConvert['open'],
              h=resConvert['high'],
              l=resConvert['low'],
              c=resConvert['close'],
              v=resConvert['volume'],
              ts=resConvert['ts'])


def OhlcvAvg(ohlcv=None):
    retAvg = SimpleOHLCV(init=True)

    size = ohlcv.len()
    if ohlcv.len() <= 0:
        return retAvg

    print(
        # 'dataFeed', dataFeed,
        'FeedAvg',
        'size',
        size)

    for i in range(size):
        retAvg.open[0] += ohlcv.open[i]
        retAvg.high[0] += ohlcv.high[i]
        retAvg.low[0] += ohlcv.low[i]
        retAvg.close[0] += ohlcv.close[i]
        retAvg.volume[0] += ohlcv.volume[i]

    retAvg.open[0] = retAvg.open[0] / size
    retAvg.high[0] = retAvg.high[0] / size
    retAvg.low[0] = retAvg.low[0] / size
    retAvg.close[0] = retAvg.close[0] / size
    retAvg.volume[0] = retAvg.volume[0] / size

    return retAvg


def FeedAvg(localFeed=None, size=1000):
    retAvg = {
        'open': 0,
        'high': 0,
        'low': 0,
        'close': 0,
        'volume': 0,
        'ts': datetimeUtil.ts2String(int(time.time()))
    }

    if size <= 0:
        return retAvg

    dataFeed = {
        'open': localFeed['open'][-1 * size:],
        'high': localFeed['high'][-1 * size:],
        'low': localFeed['low'][-1 * size:],
        'close': localFeed['close'][-1 * size:],
        'volume': localFeed['volume'][-1 * size:]
    }

    print(
        # 'dataFeed', dataFeed,
        'FeedAvg',
        'size',
        size)

    for i in range(size):
        retAvg['open'] += dataFeed['open'][i]
        retAvg['high'] += dataFeed['high'][i]
        retAvg['low'] += dataFeed['low'][i]
        retAvg['close'] += dataFeed['close'][i]
        retAvg['volume'] += dataFeed['volume'][i]

    retAvg['open'] = retAvg['open'] / size
    retAvg['high'] = retAvg['high'] / size
    retAvg['low'] = retAvg['low'] / size
    retAvg['close'] = retAvg['close'] / size
    retAvg['volume'] = retAvg['volume'] / size

    return retAvg
