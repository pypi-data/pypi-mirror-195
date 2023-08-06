from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


def checkPercent(paramPercent):
    if paramPercent <= 0 or paramPercent > 100:
        return False

    return True