import numpy as np
from talib import abstract
import math
from datetime import datetime

import sys

sys.path.append("../")

SMA = abstract.SMA
EMA = abstract.EMA

def BiasFunc(arrClose=[], period0=20, period1=60):
    '''
    @brief
    @return retCode 返回值，0 ，成功； 非0 ，失败；
    '''

    inputs = {
        'close': np.array(arrClose),
    }

    retCode = 4000
    retBias = []

    # # 规避柱子数不足，导致taLib的报错
    # #   这里的取值，跟以下 mode中的计算有关(".../2"、".../3")
    if period0 < 5 or period1 < 5:
        print(datetime.now().strftime("%Y%m%d %H:%M:%S"), "ERROR",
              'param error in BiasFunc', 'period0', period0, 'period1',
              period1)
        return retCode, retBias

    ma0 = EMA(inputs, int(period0))
    ma1 = EMA(inputs, int(period1))

    retBias = (ma0 - ma1) / ma0 * 1000
    #                   WMA(inputs, timeperiod=period),
    #                   timeperiod=int(round(math.sqrt(period))))

    # if 0 == mode:
    #     retHull = WMA(2 * WMA(inputs, timeperiod=int(period / 2)) -
    #                   WMA(inputs, timeperiod=period),
    #                   timeperiod=int(round(math.sqrt(period))))
    # elif 1 == mode:
    #     retHull = EMA(2 * EMA(inputs, timeperiod=int(period / 2)) -
    #                   EMA(inputs, timeperiod=period),
    #                   timeperiod=int(round(math.sqrt(period))))
    # elif 2 == mode:
    #     period = int(period / 2)
    #     retHull = WMA(WMA(inputs, timeperiod=int(period / 3)) * 3 -
    #                   WMA(inputs, timeperiod=int(period / 2)) -
    #                   WMA(inputs, timeperiod=period),
    #                   timeperiod=period)

    # hisNumber = 2
    # lookupNum = hisNumber + 1
    # if len(retHull) >= lookupNum and False == math.isnan(
    #         retHull[-1]) and False == math.isnan(retHull[-3]):

    #     if retHull[-1] > retHull[-3]:
    #         retColor = HullColor['green']
    #     else:
    #         retColor = HullColor['red']

    # arr = np.array([3.14], dtype=np.float64)

    retCode = 0
    return retCode, retBias.tolist()
