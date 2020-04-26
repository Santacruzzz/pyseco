#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils import *
from client import *
from listener import Listener

# TODO
class ServerCtx:
    pass


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
            self.client.loop()
        except KeyboardInterrupt:
            self.client.disconnect()

    def register_listener(self, listener: Listener):
        if listener not in self.listeners:
            listener.set_pyseco(self)
            self.listeners.append(listener)
        else:
            self.logger.error("Listener {} already registered.".format(listener))
