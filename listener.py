#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from utils import Logger


class Listener(object):
    def __init__(self, name: str):
        self.logger = Logger(name)
        self._name = name
        self.pyseco = None

    def __str__(self):
        return f'Listener: {self._name}'

    def set_logging_mode(self, logging_mode: int):
        self.logger.set_logging_mode(logging_mode)

    def set_pyseco(self, pyseco_instance):
        self.pyseco = pyseco_instance
