#!/usr/bin/env python


from __future__ import print_function
import os
import sys
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

# core
import logging
import pprint
import re
import sys
import time


# pypi
import argh


# local


logging.basicConfig(
    format='%(lineno)s %(message)s',
    level=logging.WARN
)


def main(direction, entry, atr):

    entry = float(entry)
    atr   = float(atr)

    if direction == 'long':
        sl = entry - atr
        tp = entry + (2 * atr)
    elif direction == 'short':
        sl = entry + atr
        tp = entry - (2 * atr)

    print("For {0} on an entry of {1}, SL={2} and TP={3}".format(
        direction, entry, sl, tp))

if __name__ == '__main__':
    argh.dispatch_command(main)
