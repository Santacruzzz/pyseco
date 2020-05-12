from src.includes.events_types import *
from src.includes.log import setup_logger
from src.pyseco import Listener
from src.utils import strip_size

logger = setup_logger(__name__)


class PlayerListener(Listener):
    def __init__(self, name: str, pyseco_instance):
        super(PlayerListener, self).__init__(name, pyseco_instance)
        self.pyseco.register(EventPlayerConnect.name, self.on_player_connect)
        self.pyseco.register(EventPlayerDisconnect.name, self.on_player_disconnect)
        self.pyseco.register(EventPlayerCheckpoint.name, self.on_player_cp)

    def on_player_connect(self, data: EventPlayerConnect):
        login, is_spectator = data.login, data.is_spectator
        self.pyseco.add_player(login, is_spectator)
        player = self.pyseco.get_player(login)
        self.pyseco.server_message(f'{strip_size(player.info.nickname)}$z$s$888 has joined')

    def on_player_disconnect(self, data: EventPlayerDisconnect):
        login = data.login
        player = self.pyseco.get_player(login)
        self.pyseco.server_message(f'{strip_size(player.info.nickname)}$z$s$888 has left')
        self.pyseco.remove_player(login)

    def on_player_cp(self, data: EventPlayerCheckpoint):
        pass
