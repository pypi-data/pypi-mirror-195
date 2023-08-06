from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Multitimeframe test')

    parser.add_argument('--dataname',
                        default='',
                        required=False,
                        help='File Data to Load')

    parser.add_argument('--dataname2',
                        default='',
                        required=False,
                        help='Larger timeframe file to load')

    parser.add_argument('--noresample',
                        action='store_true',
                        help='Do not resample, rather load larger timeframe')

    parser.add_argument('--timeframe',
                        default='weekly',
                        required=False,
                        choices=['daily', 'weekly', 'monthly'],
                        help='Timeframe to resample to')

    parser.add_argument('--compression',
                        default=1,
                        required=False,
                        type=int,
                        help='Compress n bars into 1')

    parser.add_argument('--indicators',
                        action='store_true',
                        help='Wether to apply Strategy with indicators')

    parser.add_argument('--onlydaily',
                        action='store_true',
                        help='Indicator only to be applied to daily timeframe')

    parser.add_argument('--period',
                        default=10,
                        required=False,
                        type=int,
                        help='Period to apply to indicator')

    return parser.parse_args()
