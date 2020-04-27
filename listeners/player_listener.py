#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from listener import Listener
from utils import strip_size


class PlayerListener(Listener):
    def __init__(self, name: str):
        super(PlayerListener, self).__init__(name)

    def PlayerConnect(self, login, isspectator):
        self.pyseco.add_player(login, isspectator)
        player = self.pyseco.get_player(login)
        self.pyseco.client.serverMessage(f'{strip_size(player.info.nickname)}$z$s$888 has joined')

    def PlayerDisconnect(self, login):
        player = self.pyseco.get_player(login)
        self.pyseco.client.serverMessage(f'{strip_size(player.info.nickname)}$z$s$888 has left')
        self.pyseco.remove_player(login)

    def PlayerCheckpoint(self, playeruid, login, timeorscore, curlap, checkpointindex):
        pass

    def PlayerFinish(self, playeruid, login, timeorscore):
        pass

    def PlayerIncoherence(self, playeruid, login):
        pass

    def PlayerInfoChanged(self, playerinfo):
        pass

