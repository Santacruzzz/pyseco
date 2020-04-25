#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils import *
from client import *
from listener import Listener


class Pyseco(object):
    def __init__(self, login, password, ip, port, logging_mode=DEBUG):
        self.login = login
        self.password = password
        self.logger = Logger('Pyseco', logging_mode)
        self.listeners = []
        self.server = ServerCtx()
        self.client = Client(ip, port, logging_mode, self.listeners)
        self.debug_data = None

    def set_debug_data(self, data):
        self.debug_data = data
        self.client.set_debug_data(data)

    def run(self):
        try:
            self.client.connect()
            self.client.authenticate(self.login, self.password)
            self.client.serverMessage('pyseco connected')
            self.client.enable_callbacks(True)
            self.synchronize()

            for player in self.server.playersRankings.values():
                for listener in self.listeners:
                    if "PlayerConnect" in dir(listener):
                        listener.PlayerConnect(player.login, False)

            self.client.loop()
        except KeyboardInterrupt:
            self.logger.info('Exiting')
        except Exception as ex:
            self.logger.error(str(ex))

    def register_listener(self, listener: Listener):
        if listener not in self.listeners:
            listener.set_pyseco(self)
            self.listeners.append(listener)
        else:
            self.logger.error("Listener {} already registered.".format(listener))

    def synchronize(self):
        self.logger.info('Synchronizing data')
        self._synchronize_basic_data()
        self._synchronize_game_infos()
        self._synchronize_players()
        self._synchronize_challenges()

    def _synchronize_basic_data(self):
        self.server.version = self.client.getVersion()
        self.server.system_info = self.client.getSystemInfo()
        self.server.detailed_player_info = self.client.getDetailedPlayerInfo('edenik')
        self.server.ladder_server_limits = self.client.getLadderServerLimits()

    def _synchronize_game_infos(self):
        self.server.current_game_info = self.client.getCurrentGameInfo()
        self.server.next_game_info = self.client.getNextGameInfo()
        self.server.challenge = self.client.getCurrentChallengeInfo()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.client.disconnect()

    def _synchronize_players(self):
        for player in self.client.getPlayerList(50, 0):
            self.server.playersInfos[player.login] = self.client.getDetailedPlayerInfo(player.login)
            self.server.playersRankings[player.login] = self.client.getCurrentRankingForLogin(player.login)[0]

    def _synchronize_challenges(self):
        self.server.challenge = self.client.getCurrentChallengeInfo()
        self.server.next_challenge = self.client.getNextChallengeInfo()
