import unittest
import sys
import backtrader as bt
import numpy as np
import talib
import pandas as pd
from datetime import datetime

sys.path.append("../")
from indicator.crossover import CrossoverFunc


class TestCase(unittest.TestCase):

    arrLen = 8
    inputs = {
        'open': np.random.random(arrLen),
        # 'high': np.random.random(arrLen),
        # 'low': np.random.random(arrLen),
        'close': np.random.random(arrLen),
        # 'volume': np.random.random(arrLen),
        # 'ts': np.random.random(arrLen)
    }

    arrClose = inputs['close'].tolist()
    arrOpen = inputs['open'].tolist()

    print('arrClose', arrClose)
    print('arrOpen', arrOpen)
    resGen = CrossoverFunc(data0=arrClose, data1=arrOpen, period=3)
    print('resGen', resGen)


if __name__ == 'main':
    unittest.main()
