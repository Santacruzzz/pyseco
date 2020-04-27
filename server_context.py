#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# TODO change it to dataclass
class ServerCtx:
    def __init__(self):
        self.version = None
        self.system_info = None
        self.max_players = None
        self.detailed_player_info = None
        self.ladder_server_limits = None
        self.playersInfos = {}
        self.playersRankings = {}
        self.current_game_info = None
        self.next_game_info = None
        self.current_challenge = None
        self.next_challenge = None
