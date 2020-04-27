#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from listener import Listener
from includes.events import Events
from utils import strip_size


class PlayerListener(Listener):
    def __init__(self, name: str):
        super(PlayerListener, self).__init__(name)

    def set_pyseco(self, pyseco_instance):
        super().set_pyseco(pyseco_instance)
        self.pyseco.register(Events.PLAYER_CONNECT, self.on_player_connect)
        self.pyseco.register(Events.PLAYER_DISCONNECT, self.on_player_disconnect)
        self.pyseco.register(Events.PLAYER_CHECKPOINT, self.on_player_checkpoint)

    def on_player_connect(self, data: Events.PLAYER_CONNECT.type):
        login, is_spectator = data.login, data.is_spectator
        self.pyseco.add_player(login, is_spectator)
        player = self.pyseco.get_player(login)
        self.pyseco.client.server_message(f'{strip_size(player.info.nickname)}$z$s$888 has joined')

    def on_player_disconnect(self, data: Events.PLAYER_DISCONNECT.type):
        login = data.login
        player = self.pyseco.get_player(login)
        self.pyseco.client.server_message(f'{strip_size(player.info.nickname)}$z$s$888 has left')
        self.pyseco.remove_player(login)

    def on_player_checkpoint(self, data: Events.PLAYER_CHECKPOINT.type):
        player_uid = data.player_uid
        login = data.login
        time_or_score = data.time_or_score
        cur_lap = data.cur_lap
        checkpoint_index = data.checkpoint_index
        player = self.pyseco.get_player(login)
        self.pyseco.client.server_message(f'{strip_size(player.info.nickname)}$z$s$888 on cp')
