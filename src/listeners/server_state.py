from src.includes.events_types import *
from src.includes.log import setup_logger
from src.pyseco import Listener

logger = setup_logger(__name__)


class ServerStateListener(Listener):
    def __init__(self, name: str, pyseco_instance):
        super(ServerStateListener, self).__init__(name, pyseco_instance)
        self.pyseco.register(EventStatusChanged.name, self.on_status_changed)
        self.pyseco.register(EventEndRound.name, self.on_end_round)
        self.pyseco.register(EventEndRace.name, self.on_end_race)
        self.pyseco.register(EventEndChallenge.name, self.on_end_challenge)
        self.pyseco.register(EventChallengeListModified.name, self.on_challenge_list_modified)
        self.pyseco.register(EventBeginChallenge.name, self.on_begin_challenge)
        self.pyseco.register(EventBeginRace.name, self.on_begin_race)
        self.pyseco.register(EventBeginRound.name, self.on_begin_round)

    def on_end_round(self):
        logger.info('EventEndRound')
        pass

    def on_end_race(self, data: EventEndRace):
        logger.info(data)
        pass

    def on_end_challenge(self, data: EventEndChallenge):
        logger.info(data)
        pass

    def on_status_changed(self, data: EventStatusChanged):
        logger.info(data)
        pass

    def on_challenge_list_modified(self, data: EventChallengeListModified):
        logger.info(data)
        pass

    def on_begin_challenge(self, data: EventBeginChallenge):
        logger.info(data)
        pass

    def on_begin_race(self, data: EventBeginRace):
        logger.info(data)
        pass

    def on_begin_round(self):
        logger.info('EventBeginRound')
        pass
