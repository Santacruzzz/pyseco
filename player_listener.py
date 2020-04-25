#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from listener import *


class PlayerListener(Listener):
    def __init__(self, name: str):
        super(PlayerListener, self).__init__(name)
        self.players = {}
        self.ranks = {}
        self.cps = {}

    def PlayerConnect(self, login, isspectator):
        player_info = self.pyseco.client.getPlayerInfo(login)
        self.players[login] = player_info
        self.ranks[login] = self.pyseco.client.getCurrentRankingForLogin(login)[0]
        self.cps[login] = self.ranks[login].best_checkpoints
        if len(self.cps[login]) == 0:
            self.cps[login] = [-1] * 50

        spec = ''
        if isspectator:
            spec = ' jako obserwator'
        self.pyseco.client.serverMessage('Gracz: {}$z$s$888 dołączył{}'.format(player_info.login, spec))
        self.pyseco.client.serverMessage('CPki: {}'.format(str(self.ranks[login].best_checkpoints)))

    def PlayerDisconnect(self, login):
        del self.players[login]
        del self.ranks[login]

    def PlayerManialinkPageAnswer(self, playeruid, login, answer):
        pass

    def PlayerCheckpoint(self, playeruid, login, timeorscore, curlap, checkpointindex):
        cps = self.cps[login]

        def_sec = 0
        def_millis = 0
        plus_minus = '='

        if cps[checkpointindex] == -1:
            cps[checkpointindex] = timeorscore
        else:
            old_cp_time = cps[checkpointindex]
            if old_cp_time > timeorscore:
                plus_minus = '$00f-$z$s$888'
                cps[checkpointindex] = timeorscore
            else:
                plus_minus = '$f00+$z$s$888'
            new_time = abs(timeorscore - old_cp_time)
            def_sec, def_millis = self._parse_time(new_time)

        seconds, millis = self._parse_time(timeorscore)
        self.pyseco.client.serverMessage(f'{self.players[login].nickname}$z$s$888 at cp: {checkpointindex + 1}: {seconds}.{millis} ({plus_minus}{def_sec}.{def_millis})')

    @staticmethod
    def _parse_time(time_in_millis):
        seconds = time_in_millis // 1000
        millis = (time_in_millis % 1000) // 10
        if millis < 10:
            millis = f'0{millis}'
        return seconds, millis

    def PlayerFinish(self, playeruid, login, timeorscore):
        if timeorscore > 0:
            seconds, millis = self._parse_time(timeorscore)
            self.pyseco.client.serverMessage('{} time: {}.{}'.format(login, seconds, millis))

    def PlayerIncoherence(self, playeruid, login):
        pass

    def PlayerInfoChanged(self, playerinfo):
        pass

