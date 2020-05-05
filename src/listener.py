from src.includes.log import setup_logger

logger = setup_logger(__name__)


class Listener(object):
    def __init__(self, name: str, pyseco_instance):
        self._name = name
        self.pyseco = pyseco_instance
        logger.debug(f'{name} registered')

    def __str__(self):
        return f'Listener: {self._name}'
