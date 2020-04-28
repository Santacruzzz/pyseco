#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyseco import Pyseco
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
    logging.basicConfig(format='%(asctime)s.%(msecs)03d:%(levelname)-8s%(name)s:%(funcName)s:%(lineno)d:%(message)s',
                        level=args.verbose,
                        datefmt='%Y-%m-%d %H:%M:%S')
    with Pyseco('SuperAdmin', 'optimus1', '86.106.91.148', 5002) as pyseco:
        pyseco.set_debug_data({'color': args.color})
        pyseco.run()
