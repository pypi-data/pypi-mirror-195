import unittest
import sys
import backtrader as bt
import numpy as np
import talib
import pandas as pd
from datetime import datetime
import time

sys.path.append("../")
from indicator.shift import ShiftFunc


class TestCase(unittest.TestCase):

    inputs = {
        'open': np.random.random(100),
        'high': np.random.random(100),
        'low': np.random.random(100),
        'close': np.random.random(100),
        'volume': np.random.random(100),
        'ts': np.random.random(100)
    }

    # print('open', inputs['open'])
    # print('open', inputs['open'].tolist())
    arrData = inputs['open'].tolist()
    print('arrData', arrData, 'len(arrData)', len(arrData))

    # resGen = ShiftFunc(data=arrData, period=1)
    resGen = ShiftFunc(data=arrData, period=0)

    print('resGen', resGen, 'len(resGen)', len(resGen))


if __name__ == 'main':
    unittest.main()
