from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from datetime import datetime


def CrossoverFunc(data0=[], data1=[], period=3):
    '''
    @brief 简易的 crossover判断
    @return  0 条件不足，或者没有满足条件
             1 下穿上
            -1 上穿下
    '''
    retCode = 0
    minLen = min(len(data0), len(data1))
    minLen = min(minLen, period)

    if minLen < period:
        return retCode

    preAllSmall = True
    preAllBig = True
    currBig = False
    currSmall = False

    for i in range(minLen):
        index = -1 * (i + 1)
        if -1 == index:
            if data0[index] > data1[index]:
                currBig = True
            elif data0[index] < data1[index]:
                currSmall = True
        else:
            if data0[index] > data1[index]:
                preAllSmall = False
            elif data0[index] < data1[index]:
                preAllBig = False

        print('i', i, 'currItem@data0', data0[index], 'currItem@data1',
              data1[index])

    if preAllSmall and currBig:
        retCode = 1
    if preAllBig and currSmall:
        retCode = -1

    print('preAllBig', preAllBig, 'preAllSmall', preAllSmall, 'currBig',
          currBig, 'currSmall', currSmall)

    return retCode