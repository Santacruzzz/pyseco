#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from listener import Listener
from includes.trackmania_types import Events
from utils import strip_size


class PlayerListener(Listener):
    def __init__(self, name: str):
        super(PlayerListener, self).__init__(name)

    def set_pyseco(self, pyseco_instance):
        super().set_pyseco(pyseco_instance)
        self.pyseco.register(Events.PLAYER_CONNECT, self.on_player_connect)
        self.pyseco.register(Events.PLAYER_DISCONNECT, self.on_player_disconnect)
        self.pyseco.register(Events.PLAYER_CHECKPOINT, self.on_player_checkpoint)

    # TODO create dedicated types to each event, e.g. here will be data: EventPlayerConnect
    def on_player_connect(self, data):
        login, is_spectator = data
        self.pyseco.add_player(login, is_spectator)
        player = self.pyseco.get_player(login)
        self.pyseco.client.server_message(f'{strip_size(player.info.nickname)}$z$s$888 has joined')

    def on_player_disconnect(self, data):
        login = data[0]
        player = self.pyseco.get_player(login)
        self.pyseco.client.server_message(f'{strip_size(player.info.nickname)}$z$s$888 has left')
        self.pyseco.remove_player(login)

    def on_player_checkpoint(self, data):
        playeruid, login, timeorscore, curlap, checkpointindex = data
        player = self.pyseco.get_player(login)
        self.pyseco.client.server_message(f'{strip_size(player.info.nickname)}$z$s$888 on cp')
