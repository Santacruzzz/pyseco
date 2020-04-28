#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


class Listener(object):
    def __init__(self, name: str, pyseco_instance):
        self._name = name
        self.pyseco = pyseco_instance

    def __str__(self):
        return f'Listener: {self._name}'
