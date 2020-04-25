#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyseco import Pyseco
from player_listener import PlayerListener
import argparse

parser = argparse.ArgumentParser(description='Pyseco. Trackmania Server Control')
parser.add_argument('-v', '--verbose', default=1, type=int, help='Logging mode. 0 - DEBUG, 1 - INFO, 9 - NONE')
parser.add_argument('-c', '--color', default='f90', type=str, help='Debug color')

args = parser.parse_args()

if __name__ == '__main__':
    with Pyseco('SuperAdmin', 'optimus1', '86.106.91.148', 5002, args.varbose) as pyseco:
        pyseco.set_debug_data({'color': args.color})
        pyseco.register_listener(PlayerListener('PlrLstnr'))
        pyseco.run()
