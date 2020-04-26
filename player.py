#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from includes.trackmania_types import PlayerInfo, PlayerRanking


class Player(object):
    def __init__(self, player_info: PlayerInfo, player_ranking: PlayerRanking):
        self.info = player_info
        self.raking = player_ranking
