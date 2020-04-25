#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils import *
from pyseco import Pyseco
from player_listener import PlayerListener

if __name__ == '__main__':
    pyseco = Pyseco('SuperAdmin', 'optimus1', '86.106.91.148', 5002, DEBUG)
    pyseco.register_listener(PlayerListener('PlrLstnr'))
    pyseco.run()
