from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from pyrsistent import freeze

import sys
import backtrader as bt

sys.path.append("../")
from common.enums import MSTIME_MI, MSTIME_H, MSTIME_D, MSTIME_W, MSTIME_Y

# , , ,
#      , , , , NoTimeFrame
# k线周期的单位
TimeframeUni = freeze({
    'ms': bt.TimeFrame.MicroSeconds,
    's': bt.TimeFrame.Seconds,
    'mi': bt.TimeFrame.Minutes,
    'd': bt.TimeFrame.Days,
    'w': bt.TimeFrame.Weeks,
    'mo': bt.TimeFrame.Months,
    'y': bt.TimeFrame.Years
})

# k线周期
Timeframe = freeze({
    '1m': {
        'name': '1m',
        'exBar': '1m',
        'dbFieldValue': '1m',
        'msTime': 1 * MSTIME_MI['value']
    },
    '3m': {
        'name': '3m',
        'exBar': '3m',
        'dbFieldValue': '3m',
        'msTime': 3 * MSTIME_MI['value']
    },
    '5m': {
        'name': '5m',
        'exBar': '5m',
        'dbFieldValue': '5m',
        'msTime': 5 * MSTIME_MI['value']
    },
    '10m': {
        'name': '10m',
        'exBar': '10m',
        'dbFieldValue': '10m',
        'msTime': 10 * MSTIME_MI['value']
    },
    '15m': {
        'name': '15m',
        'exBar': '15m',
        'dbFieldValue': '15m',
        'msTime': 15 * MSTIME_MI['value']
    },
    '30m': {
        'name': '30m',
        'exBar': '30m',
        'dbFieldValue': '30m',
        'msTime': 30 * MSTIME_MI['value']
    },
    '1h': {
        'name': '1h',
        'exBar': '1H',
        'dbFieldValue': '1h',
        'msTime': 1 * MSTIME_H['value']
    },
    '90m': {
        'name': '90m',
        'exBar': '90m',
        'msTime': 1.5 * MSTIME_H['value']
    },
    '2h': {
        'name': '2h',
        'exBar': '2H',
        'msTime': 2 * MSTIME_H['value']
    },
    '3h': {
        'name': '3h',
        'exBar': '3H',
        'msTime': 3 * MSTIME_H['value']
    },
    '4h': {
        'name': '4h',
        'exBar': '4H',
        'dbFieldValue': '4h',
        'msTime': 4 * MSTIME_H['value']
    },
    '6h': {
        'name': '6h',
        'exBar': '6H',
        'msTime': 6 * MSTIME_H['value']
    },
    '8h': {
        'name': '8h',
        'exBar': '8H',
        'msTime': 8 * MSTIME_H['value']
    },
    '12h': {
        'name': '12h',
        'exBar': '12H',
        'msTime': 12 * MSTIME_H['value']
    },
    '1d': {
        'name': '1d',
        'exBar': '1D',
        'msTime': 1 * MSTIME_D['value']
    },
    '3d': {
        'name': '3d',
        'exBar': '3D',
        'msTime': 3 * MSTIME_D['value']
    },
    '1w': {
        'name': '1w',
        'exBar': '1W',
        'msTime': 1 * MSTIME_W['value']
    },
    '2w': {
        'name': '2w',
        'exBar': '2W',
        'msTime': 2 * MSTIME_W['value']
    },
    '1M': {
        'name': '1M',
        'exBar': '1M',
        'msTime': 1 * MSTIME_MI['value']
    },
    '3M': {
        'name': '3M',
        'exBar': '3M',
        'msTime': 3 * MSTIME_MI['value']
    },
    '6M': {
        'name': '6M',
        'exBar': '6M',
        'msTime': 6 * MSTIME_MI['value']
    },
    '1y': {
        'name': '1y',
        'exBar': '1Y',
        'msTime': 1 * MSTIME_Y['value']
    }
})
