from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
from datetime import datetime
import math


class Shift(bt.indicators.PeriodN):
    '''
    '''
    lines = ('localline', )

    def next(self):
        self.line[0] = self.data[-1 * self.p.period]

        # print(
        #     'Shift next()',
        #     'period',
        #     self.p.period,
        #     'self.data.get(size=20)',
        #     self.data.get(size=20),
        # )


def ShiftFunc(data=[], period=1):
    return data[:len(data) - period]
