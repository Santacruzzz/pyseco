#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import logging
import os

from src.listeners.server_state import ServerStateListener
from src.pyseco import Pyseco
from src.listeners.chat_listener import ChatListener
from src.listeners.player_listener import PlayerListener

parser = argparse.ArgumentParser(description='Pyseco. Trackmania Server Control')
parser.add_argument('-l', '--loglevel', default='DEBUG', type=str,
                    help='Logging modes: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL')
parser.add_argument('-s', '--settings', default='config.yaml', type=str,
                    help='Filename with config')

args = parser.parse_args()
logging.basicConfig(level=args.loglevel, datefmt='%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    settings = os.path.join(os.path.dirname(os.path.realpath(__file__)), args.settings)
    with Pyseco(settings) as pyseco:
        pyseco.add_listener(ServerStateListener, 'ServerStateListener')
        pyseco.add_listener(PlayerListener, 'PlayerListener')
        pyseco.add_listener(ChatListener, 'ChatListener')
        pyseco.run()
