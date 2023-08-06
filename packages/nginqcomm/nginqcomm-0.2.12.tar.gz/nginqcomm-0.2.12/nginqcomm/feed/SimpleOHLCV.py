from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys
import time

from datetime import datetime

import sys

sys.path.append("../")
from utils import datetimeUtil


class SimpleOHLCV:

    def __init__(self, o=[], h=[], l=[], c=[], v=[], ts=[], init=False):
        self.open = []
        self.high = []
        self.low = []
        self.close = []
        self.volume = []
        self.ts = []

        if init:
            self.open.append(0)
            self.high.append(0)
            self.low.append(0)
            self.close.append(0)
            self.volume.append(0)
            self.ts.append(datetimeUtil.ts2String(int(time.time())))

        if (len(o)):
            self.open.extend(o)
        if (len(h)):
            self.high.extend(h)
        if (len(l)):
            self.low.extend(l)
        if (len(c)):
            self.close.extend(c)
        if (len(v)):
            self.volume.extend(v)
        if (len(ts)):
            self.ts.extend(ts)

    def lastTs(self, format=0):
        '''
        @return unix时间戳，单位，秒
        '''
        ret = 0
        if self.len() > 0:
            ret = datetimeUtil.string2TsSec(self.ts[-1])

        if 1 == format:
            ret = datetimeUtil.ts2String(ret)

        return ret

    def len(self):
        print(datetime.now().strftime("%Y%m%d %H:%M:%S"), "DEBUG", 'len',
              len(self.open), len(self.high), len(self.low), len(self.close),
              len(self.volume), len(self.ts))

        # 长度判断
        #   其中的 exit（）后续应该要屏蔽
        if len(self.open) != len(self.high) or len(self.open) != len(
                self.low) or len(self.open) != len(self.close) or len(
                    self.open) != len(self.volume) or len(self.open) != len(
                        self.ts):
            print(datetime.now().strftime("%Y%m%d %H:%M:%S"), "ERROR",
                  'lenError', len(self.open), len(self.high), len(self.low),
                  len(self.close), len(self.volume), len(self.ts))
            exit()

        return len(self.open)

    def extend(self, input=None):
        strMaxTs = datetimeUtil.ts2String(0)
        if self.len() > 0:
            strMaxTs = self.ts[-1]

        maxTs = datetimeUtil.string2TsSec(strMaxTs)

        inputAfterFilter = input.tsFilter(strTs=strMaxTs)

        if inputAfterFilter.len() <= 0:
            print(
                'extend, inputAfterFilter is null',
                'strMaxTs',
                strMaxTs,
                'maxTs',
                maxTs,
            )
            return

        print('extend', 'len inputAfterFilter', inputAfterFilter.len())

        self.open.extend(inputAfterFilter.open)
        self.high.extend(inputAfterFilter.high)
        self.low.extend(inputAfterFilter.low)
        self.close.extend(inputAfterFilter.close)
        self.volume.extend(inputAfterFilter.volume)
        self.ts.extend(inputAfterFilter.ts)

    def dumps(self, index0=None, index1=None):
        return {
            'open': self.open[index0:index1],
            'high': self.high[index0:index1],
            'low': self.low[index0:index1],
            'close': self.close[index0:index1],
            'volume': self.volume[index0:index1],
            'ts': self.ts[index0:index1]
        }

    def delItems(self, index0=None, index1=None):
        del self.open[index0:index1]
        del self.high[index0:index1]
        del self.low[index0:index1]
        del self.close[index0:index1]
        del self.volume[index0:index1]
        del self.ts[index0:index1]

    def tsFilter(self, strTs=None):
        ''''
        @brief 根据时间戳过滤数据
               把小于ts的数据，都过滤掉
        '''
        i = 0
        for currTs in self.ts:
            if datetimeUtil.string2TsSec(currTs) > datetimeUtil.string2TsSec(
                    strTs):
                break
            i += 1

        return self.subset(index0=i)

    def subset(self, index0=None, index1=None):
        retOhlcv = SimpleOHLCV()

        retOhlcv.open = self.open[index0:index1]
        retOhlcv.high = self.high[index0:index1]
        retOhlcv.low = self.low[index0:index1]
        retOhlcv.close = self.close[index0:index1]
        retOhlcv.volume = self.volume[index0:index1]
        retOhlcv.ts = self.ts[index0:index1]

        return retOhlcv

    def clone(self):
        ret = SimpleOHLCV()

        ret.extend(self)

        return ret

    @staticmethod
    def convertFromDatas(feed=None, size=1000):
        '''
        @brief backtrader 的 datas转换
        '''
        # ret = SimpleOHLCV()

        arrDateTime = feed.datetime.get(size=size)
        arrTs = []
        for currDateTime in arrDateTime:
            # print(currDateTime, currDateTime)
            currTs = datetimeUtil.datasDateTime2TsSec(currDateTime)
            arrTs.append(currTs)

        ret = SimpleOHLCV(o=feed.open.get(size=size).tolist(),
                          h=feed.high.get(size=size).tolist(),
                          l=feed.low.get(size=size).tolist(),
                          c=feed.close.get(size=size).tolist(),
                          v=feed.volume.get(size=size).tolist(),
                          ts=arrTs)

        return ret
