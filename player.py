#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils import PlayerInfo, RankingItem


class Player(object):
    def __init__(self, player_info: PlayerInfo, player_ranking: RankingItem):
        self.info = player_info
        self.raking = player_ranking
