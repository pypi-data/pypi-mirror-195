import unittest
import sys
import order

sys.path.append("../")
from common.enums import Symbol


class TestCase(unittest.TestCase):

    resSize = order.quoteAmountToSize(symbol=Symbol['BTC/USDT:USDT'],
                                      qAmount=50,
                                      close=16000)

    print('resSize', resSize)


if __name__ == 'main':
    unittest.main()
