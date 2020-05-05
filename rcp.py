#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import logging

from src.pyseco import Pyseco

parser = argparse.ArgumentParser(description='Pyseco. Trackmania Server Control')
parser.add_argument('-l', '--loglevel', default='DEBUG', type=str,
                    help='Logging modes: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL')
parser.add_argument('-c', '--color', default='f90', type=str, help='Debug color')

args = parser.parse_args()
logging.basicConfig(level=args.loglevel, datefmt='%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    with Pyseco('SuperAdmin', 'optimus1', '86.106.91.148', 5002) as pyseco:
        pyseco.set_debug_data({'color': args.color})
        pyseco.run()
