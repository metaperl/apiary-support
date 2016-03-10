#!/usr/bin/env python


from __future__ import print_function

# core
import logging
import decimal

# pypi
import argh

# local

logging.basicConfig(
    format='%(lineno)s %(message)s',
    level=logging.WARN
)

one_percent = 1.0 / 100.0
two_percent = 2.0 / 100.0

decimal.getcontext().prec = 8

def main(entry, percent=6):

    entry = decimal.Decimal(entry)
    x_percent = decimal.Decimal(percent / 100.0)

    tp = entry * x_percent + entry

    print("On an entry of {0:f}, TP={1:.8f} for a {2} percent gain".format(
        entry, tp, percent))


if __name__ == '__main__':
    argh.dispatch_command(main)
