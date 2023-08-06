import numpy as np
import math
from datetime import datetime

import sys

sys.path.append("../")


def RoundFunc(arrClose=[], decimal=3):
    '''
    @brief
    @return retCode 返回值，0 ，成功； 非0 ，失败；
    '''

    inputs = {
        'close': np.array(arrClose),
    }

    retCode = 4000
    retArr = np.round(inputs['close'], decimal)

    retCode = 0
    return retCode, retArr.tolist()


import math


def notNanCount(data=[]):
    count = 0
    for currItem in data:
        # print('currItem', currItem)
        if True != math.isnan(currItem):
            count += 1

    return count


def strNotNanCount(data=[]):
    count = notNanCount(data)
    return str(count) + "/" + str(len(data))
