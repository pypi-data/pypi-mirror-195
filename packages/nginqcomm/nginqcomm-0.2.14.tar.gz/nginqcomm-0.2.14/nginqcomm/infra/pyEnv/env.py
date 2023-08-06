from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os


def proEnv():
    return 'pro' == instPyEnv.pyEnv


def devEnv():
    return 'dev' == instPyEnv.pyEnv


class PyEnv():

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            # print(datetime.now().strftime("%Y%m%d %H:%M:%S"), "DEBUG",
            #       "Creating the object")
            cls._instance = super(PyEnv, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance

    def __init__(self):
        self.pyEnv = os.environ.get("PYTHON_ENV")
        print('pyEnv', self.pyEnv)


instPyEnv = PyEnv()