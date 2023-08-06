from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from datetime import datetime
from os import times
import pytz
import time
import backtrader as bt


def ts2String(timestamp, add8Hours=False, dateFormat=0):
    '''
    @brief 时间戳转北京时间 字符串
            把 timestamp 时间戳（秒/毫秒） 转为字符串
            timestamp 如果是毫秒，内部先转为秒，然后再转为字符串  YYYYMMDD HH:Mi:SS
    @param  timestamp 时间戳； 单位，秒 或者毫秒；
    @param  add8Hours 是否增加8小时，用于做兼容； True，考虑，在 timestamp加8小时；  False，不考虑，直接使用原  timestamp
    '''
    tsInSec = int(timestamp)

    strFormat = '%Y%m%d %H:%M:%S'

    if 1 == dateFormat:
        strFormat = '%Y-%m-%d %H:%M:%S'

    # 如果是毫秒格式，则转化为秒
    if tsInSec > 1000000000000:
        tsInSec = tsInSec / 1000

    if add8Hours:
        tsInSec += 3600 * 8

    tz = pytz.timezone('Asia/Shanghai')  #东八区
    return datetime.fromtimestamp(int(tsInSec), tz).strftime(strFormat)


def string2TsSec(strSec, dateFormat=0):
    '''
    @brief "YYYYMMDD HH:Mi:SS" 转换为 时间戳（秒）
    '''
    if 1 == dateFormat:
        structTime = time.strptime(strSec, "%Y-%m-%d %H:%M:%S")
    elif 2 == dateFormat:
        structTime = time.strptime(strSec, "%Y/%m/%d %H:%M")
    else:
        structTime = time.strptime(strSec, "%Y%m%d %H:%M:%S")

    timestamp = time.mktime(structTime)
    return int(timestamp)


def string2TsMs(strMs):
    '''
    @brief "YYYYMMDD HH:Mi:SS.ms" 转换为 时间戳（毫秒）
    '''

    structTime = datetime.strptime(strMs, "%Y%m%d %H:%M:%S.%f")
    timestamp = time.mktime(
        structTime.timetuple()) * 1000.0 + structTime.microsecond / 1000.0
    return int(timestamp)


def string2Datetime(strMs):
    '''
    @brief "YYYYMMDD HH:Mi:SS" 转换为 datetime
    '''
    return datetime.strptime(strMs, "%Y%m%d %H:%M:%S")


def datasDateTime2TsSec(datasDateTime):
    '''
    @brief bt.strategy self.datas[N].datetime 转换成 时间戳（秒）
          20221125 发现 datas[N].datetime 会把交易所的k线时间戳 ， 减掉 8小时，然后转换成datas[N].datetime 保存；
          调整 backtrader 时区，可能可以解决  datas[N].datetime问题；
          
          但应用跑了这么久，调整 backtrader 时区是否会矫枉过正 造成其他相关模块的时间问题，不得而知；
          因此考虑单独解析这个 datas[N].datetime，需要自行增加 8小时
    '''
    return ts2String(bt.num2date(datasDateTime).timestamp(), add8Hours=True)