class PysecoException(Exception):
    pass


class PlayerNotFound(PysecoException):
    pass


class NotAnEvent(PysecoException):
    pass


class EventDiscarded(PysecoException):
    pass


class WrongCommand(PysecoException):
    pass


class WrongNumberOfParams(PysecoException):
    pass


class InconsistentTypesError(PysecoException):
    pass
