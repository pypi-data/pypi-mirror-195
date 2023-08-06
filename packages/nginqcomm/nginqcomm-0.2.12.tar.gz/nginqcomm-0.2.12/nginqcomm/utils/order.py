from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys

sys.path.append("../../")

from nginqcomm.common import enums

sys.path.append("../")
from utils import maths

# @brief 报价币的数量转换为张数（size）
#        如 币对 BTC-USDT-SWAP  中的 U数量转换为 BTC的张数(size)


def quoteAmountToSize(symbol=None, qAmount=0, close=0):
    retSize = 0
    contractSize = enums.ContractSize.get(symbol)
    if 0 != close and None != contractSize:
        retSize = qAmount / close / contractSize
    return retSize


def sizeToQuoteAmount(symbol=None, size=0, close=0):
    retQuoteAmount = 0
    contractSize = enums.ContractSize.get(symbol)
    if 0 != close and None != contractSize:
        retQuoteAmount = size * close * contractSize

    return retQuoteAmount


def checkSltpParam(sltpType=None, slPercent=None, tpPercent=None):
    if enums.SltpOrderType['conditional'] != sltpType and enums.SltpOrderType[
            'oco'] != sltpType:
        return False

    if False == maths.checkPercent(slPercent) or False == maths.checkPercent(
            tpPercent):
        return False

    return True