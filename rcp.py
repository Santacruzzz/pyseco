#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyseco import Pyseco
from listeners.player_listener import PlayerListener
import argparse
import logging

parser = argparse.ArgumentParser(description='Pyseco. Trackmania Server Control')
parser.add_argument('-v', '--verbose', default='DEBUG', type=str,
                    help='Logging modes: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL')
parser.add_argument('-c', '--color', default='f90', type=str, help='Debug color')

args = parser.parse_args()

"""
If you want to write logs into a file, just use param 'filename' in logging.basicConfig.
There will be logs from any logs you defined.
"""

if __name__ == '__main__':
    with Pyseco('SuperAdmin', 'optimus1', '86.106.91.148', 5002) as pyseco:
        logging.basicConfig(format='%(asctime)s:%(levelname)-8s%(name)s:%(funcName)s:%(lineno)d:%(message)s',
                            level=args.verbose,
                            datefmt='%Y-%m-%d %H:%M:%S')
        pyseco.set_debug_data({'color': args.color})
        pyseco.register_listener(PlayerListener('PlrLstnr'))
        pyseco.run()
