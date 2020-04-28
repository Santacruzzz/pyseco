#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class PysecoException(Exception):
    pass


class PlayerNotFound(PysecoException):
    pass


class NotAnEvent(PysecoException):
    pass


class EventDiscarded(PysecoException):
    pass
