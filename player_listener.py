#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from listener import *


class PlayerListener(Listener):
    def __init__(self, name: str):
        super(PlayerListener, self).__init__(name)
        self.players = {}
        self.ranks = {}
        self.cps = {}

