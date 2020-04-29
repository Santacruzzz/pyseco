class PysecoException(Exception):
    pass


class PlayerNotFound(PysecoException):
    pass


class NotAnEvent(PysecoException):
    pass


class EventDiscarded(PysecoException):
    pass
