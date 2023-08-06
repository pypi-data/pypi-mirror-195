from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import unittest
import sys

from datetimeUtil import *


class TestCase(unittest.TestCase):
    tsInMs = 1668222660000
    str0 = ts2String(tsInMs)
    print('tsInMs', tsInMs, 'str0', str0)

    strSec = "20201005 10:12:56"
    print('strSec', strSec, 'string2TsSec(strSec)', string2TsSec(strSec))

    strMs = '20190114 15:22:18.123'
    print('strMs', strMs, 'string2TsMs(strMs)', string2TsMs(strMs))

    tsInSec = string2TsSec(str0)
    print('str0', str0, 'tsInSec', tsInSec)
    assert tsInMs / 1000 == tsInSec

    tsInSec = 1669345200
    str1 = ts2String(tsInSec)
    str2 = ts2String(tsInSec, add8Hours=True, dateFormat=1)
    print('tsInSec', tsInSec, 'str1', str1, 'str2', str2)

    datasDateTime = 738484.4583333334

    str3 = datasDateTime2TsSec(datasDateTime)
    print('datasDateTime', datasDateTime, 'str3', str3)

    print('time()', time.time())

    tsInMs = 0
    str0 = ts2String(tsInMs)
    print('tsInMs', tsInMs, 'str0', str0)


if __name__ == 'main':
    unittest.main()
