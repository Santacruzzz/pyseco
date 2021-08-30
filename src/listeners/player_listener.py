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
        self.pyseco.register(EventPlayerFinish.name, self.on_player_finish)

    def on_player_connect(self, data: EventPlayerConnect):
        login, is_spectator = data.login, data.is_spectator
        self.pyseco.add_player(login, is_spectator)
        player = self.pyseco.get_player(login)
        self.pyseco.msg.show_welcome_message(player, self.pyseco.server.get_name())
        self.pyseco.msg.to_login(login).show_current_map_info(self.pyseco.server.current_challenge)

    def on_player_disconnect(self, data: EventPlayerDisconnect):
        login = data.login
        player = self.pyseco.get_player(login)
        self.pyseco.msg.show_player_left(player)
        self.pyseco.remove_player(login)

    def on_player_finish(self, data: EventPlayerFinish):
        pass
