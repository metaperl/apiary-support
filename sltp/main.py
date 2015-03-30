#!/usr/bin/env python


from __future__ import print_function

# core
import logging

# pypi
import argh

# local

logging.basicConfig(
    format='%(lineno)s %(message)s',
    level=logging.WARN
)

def main(direction, entry, swing, atr):

    entry = float(entry)
    swing = float(swing)
    atr   = float(atr)

    if direction == 'long':
        sl = swing - atr
        tp = entry + (2 * atr)
    elif direction == 'short':
        sl = swing + atr
        tp = entry - (2 * atr)

    print("For {0} on an entry of {1}, SL={2} and TP={3}".format(
        direction, entry, sl, tp))

if __name__ == '__main__':
    argh.dispatch_command(main)
