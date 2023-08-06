from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
from datetime import datetime
import math


class MathLog(bt.Indicator):
    '''
    '''
    lines = ('localline', )

    def next(self):
        self.line[0] = math.log(self.data[0])


def MathLogFunc(data=[]):
    arrRet = []
    for currItem in data:
        arrRet.append(math.log(currItem))

    return arrRet


def MathExpFunc(data=[]):
    arrRet = []
    for currItem in data:
        arrRet.append(math.exp(currItem))

    return arrRet
