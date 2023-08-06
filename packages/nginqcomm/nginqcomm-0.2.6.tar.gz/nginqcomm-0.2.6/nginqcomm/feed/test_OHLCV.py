import unittest
# import OHLCV
import sys
import json

# import Test

sys.path.append("../")
from feed.SimpleOHLCV import SimpleOHLCV


class TestCase(unittest.TestCase):
    ohlcv = SimpleOHLCV()

    print('ohlcv.len', ohlcv.len(), 'ohlcv dumps', ohlcv.dumps())

    ohlcv = SimpleOHLCV(
        o=[11, 12, 13],
        h=[21, 22, 23],
        l=[31, 32, 33],
        c=[41, 42, 43],
        v=[51, 52, 53],
        ts=['20201229 00:01:00', '20201229 00:02:00', '20201229 00:03:00'])

    print('ohlcv.len', ohlcv.len(), 'ohlcv dumps', ohlcv.dumps())

    ohlcv1 = SimpleOHLCV(
        o=[14, 15, 16],
        h=[24, 25, 26],
        l=[34, 35, 36],
        c=[44, 45, 46],
        v=[54, 55, 56],
        ts=['20201229 00:04:00', '20201229 00:05:00', '20201229 00:06:00'])

    ohlcv.extend(ohlcv1)

    print('ohlcv.len', ohlcv.len(), 'ohlcv dumps', ohlcv.dumps())

    print('lastTs', ohlcv1.lastTs(format=1))

    # print(ohlcv.open.get(size=5))


#     ohlcv.delItems(-1, None)

#     print('after delItems, ohlcv.len', ohlcv.len(), 'ohlcv dumps',
#           ohlcv.dumps())

#     subOhlcv0 = ohlcv.subset(0, -1)
#     print('subOhlcv0.len', subOhlcv0.len(), 'subOhlcv0 dumps',
#           subOhlcv0.dumps())

#     tmpOhlcv = SimpleOHLCV(
#         o=[14, 15, 16],
#         h=[24, 25, 26],
#         l=[34, 35, 36],
#         c=[44, 45, 46],
#         v=[54, 55, 56],
#         ts=['20201229 00:01:00', '20201229 00:02:00', '20201229 00:03:00'])

#     print('tmpOhlcv', tmpOhlcv.dumps())

#     tmpOhlcv1 = tmpOhlcv.tsFilter(strTs='20201229 00:01:00')

#     print('tmpOhlcv1', tmpOhlcv1.dumps())

if __name__ == 'main':
    unittest.main()
