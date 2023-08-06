import math
import unittest
import sys
import numpy as np
import talib

sys.path.append("../")
from indicator.bias import BiasFunc
from indicator.utils import RoundFunc, strNotNanCount


class TestCase(unittest.TestCase):

    size = 1000

    inputs = {
        'open': np.random.random(size),
        'high': np.random.random(size),
        'low': np.random.random(size),
        'close': np.random.random(size),
        'volume': np.random.random(size),
        'ts': np.random.random(size)
    }

    arrData = inputs['close'].tolist()
    # print('arrData', arrData, 'len(arrData)', len(arrData))

    retCode, retBias = BiasFunc(arrClose=arrData)

    if 0 == retCode:
        # print('retBias', retBias)
        retCode, roundBias = RoundFunc(retBias, decimal=5)
        # if 0 == retCode:
        #     print('roundBias', roundBias)

        print('BiasFunc exec ok',
              'retCode', retCode, 'strNotNanCount(retBias)',
              strNotNanCount(retBias), 'strNotNanCount(roundBias)',
              strNotNanCount(roundBias))


if __name__ == 'main':
    unittest.main()
