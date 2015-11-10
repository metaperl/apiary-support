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

one_percent = 1.0 / 100.0

def main(entry):

    entry = float(entry)
    tp = entry * one_percent + entry

    print("On an entry of {0}, TP={1}".format(entry, tp))


if __name__ == '__main__':
    argh.dispatch_command(main)
