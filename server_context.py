#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class ServerCtx:
    def __init__(self):
        self.version = None
        self.system_info = None
        self.detailed_player_info = None
        self.ladder_server_limits = None
        self.playersInfos = {}
        self.playersRankings = {}
        self.current_game_info = None
        self.next_game_info = None
        self.current_challenge = None
        self.next_challenge = None