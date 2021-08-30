#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.utils import strip_size
from src.api.tm_types import PlayerInfo, PlayerRanking


class Player(object):
    def __init__(self, player_info: PlayerInfo, player_ranking: PlayerRanking):
        self.info = player_info
        self.ranking = player_ranking

    def __str__(self) -> str:
        return strip_size(self.info.nickname)