import unittest
import sys
import backtrader as bt
import numpy as np
import talib
import pandas as pd
from datetime import datetime
import time

sys.path.append("../")
from indicator.heikin_ashi import HA


class TestCase(unittest.TestCase):

    inputs = {
        'open': np.random.random(100),
        'high': np.random.random(100),
        'low': np.random.random(100),
        'close': np.random.random(100),
        'volume': np.random.random(100),
        'ts': np.random.random(100)
    }

    # dfTmp = pd.DataFrame(
    #     data=inputs, columns=['open', 'high', 'low', 'close', 'volume', 'ts'])
    # dfTmp = dfTmp.set_index('ts')

    ha = HA(o=inputs['open'],
            h=inputs['high'],
            l=inputs['low'],
            c=inputs['close'],
            v=inputs['volume'],
            ts=inputs['ts'])
    print('ha', ha)
    
    print('ha_close', ha['close'])
    print('len(ha_close)', len(ha['close']))
    print('type(ha)', type(ha))

    # inputs = {
    #     'open': [1, 2, 3, 4, 5],
    #     'high': [1, 2, 3, 4, 5],
    #     'low': [1, 2, 3, 4, 5],
    #     'close': [1, 2, 3, 4, 5],
    #     'volume': [1, 2, 3, 4, 5],
    #     'ts': [1, 2, 3, 4, 5]
    # }

    # ha = HA(o=inputs['open'],
    #         h=inputs['high'],
    #         l=inputs['low'],
    #         c=inputs['close'],
    #         v=inputs['volume'],
    #         ts=inputs['ts'])
    # print('ha', ha)
    # print('ha_close', ha['close'])
    # print('len(ha_close)', len(ha['close']))
    # print('type(ha)', type(ha))

    # ha = ha.shift(periods=1, freq="infer")
    ha = ha.shift(periods=-1)

    print('ha_close', ha['close'])
    print('len(ha_close)', len(ha['close']))
    # periods=3, freq="infer"


if __name__ == 'main':
    unittest.main()
