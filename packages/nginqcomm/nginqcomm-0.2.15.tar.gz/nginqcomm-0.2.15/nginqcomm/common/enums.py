from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import sys
from pyrsistent import freeze

sys.path.append("../")
from infra.pyEnv import env

# 币对
Symbol = freeze({
    'BTC/USDT:USDT': 'BTC/USDT:USDT',
    'ETH/USDT:USDT': 'ETH/USDT:USDT',
    'XRP/USDT:USDT': 'XRP/USDT:USDT',
    'OP/USDT:USDT': 'OP/USDT:USDT',
    'OKT/USDT:USDT': 'OKT/USDT:USDT',
    'DYDX/USDT:USDT': 'DYDX/USDT:USDT',
    'GMT/USDT:USDT': 'GMT/USDT:USDT',
})

# 合约张数
ContractSize = None
if env.proEnv():
    ContractSize = freeze({
        Symbol['BTC/USDT:USDT']: 0.01,
        Symbol['ETH/USDT:USDT']: 0.1,
        Symbol['XRP/USDT:USDT']: 100,
        Symbol['OP/USDT:USDT']: 1,
        Symbol['OKT/USDT:USDT']: 0,
        Symbol['DYDX/USDT:USDT']: 1,
        Symbol['GMT/USDT:USDT']: 1,
    })
else:
    ContractSize = freeze({
        Symbol['BTC/USDT:USDT']: 0.001,
        Symbol['ETH/USDT:USDT']: 0.01,
        Symbol['XRP/USDT:USDT']: 100,
        Symbol['OP/USDT:USDT']: 1,
        Symbol['OKT/USDT:USDT']: 0,
        Symbol['DYDX/USDT:USDT']: 0,
        Symbol['GMT/USDT:USDT']: 0.1
    })

# 产品ID
InstId = freeze({
    Symbol['BTC/USDT:USDT']: 'BTC-USDT-SWAP',
    Symbol['ETH/USDT:USDT']: 'ETH-USDT-SWAP',
    Symbol['XRP/USDT:USDT']: 'XRP-USDT-SWAP',
    Symbol['OP/USDT:USDT']: 'OP-USDT-SWAP',
    Symbol['OKT/USDT:USDT']: 'OKT-USDT-SWAP',
    Symbol['DYDX/USDT:USDT']: 'DYDX-USDT-SWAP',
    Symbol['GMT/USDT:USDT']: 'GMT-USDT-SWAP',
})

# 持仓方向
PosSide = freeze({'LONG': 'long', 'SHORT': 'short'})

# 止盈止损 订单类型
SltpOrderType = freeze({
    'conditional': 'conditional',  # 单向止盈止损
    'oco': 'oco',  # 双向止盈止损
})

# 交易模式
TdMode = freeze({
    'isolated': 'isolated',  # 逐仓
    'cross': 'cross'  # 全仓
})

# 订单方向
Side = freeze({'buy': 'buy', 'sell': 'sell'})

# 时间（以毫秒为单位)
MSTIME_MS = freeze({'value': 1})
MSTIME_S = freeze({'value': 1000 * MSTIME_MS['value']})
MSTIME_MI = freeze({'value': 60 * MSTIME_S['value']})
MSTIME_H = freeze({'value': 3600 * MSTIME_S['value']})
MSTIME_D = freeze({'value': 24 * MSTIME_H['value']})
MSTIME_W = freeze({'value': 7 * MSTIME_D['value']})
MSTIME_MO = freeze({'value': 30 * MSTIME_D['value']})
MSTIME_Y = freeze({'value': 365 * MSTIME_D['value']})

# 交易所缩写
Exchange = freeze({'OKX': 'OKX', 'Binance': 'Binance'})

# 交易所Api参数接口信息
ExangeApiParamInfo = freeze({
    # exchange ID
    'exId': {
        'OKX': 1
    },

    # k线历史查询单页最大记录个数s
    'ohlcvHisPageLimit': {
        'OKX': 100
    },
})
