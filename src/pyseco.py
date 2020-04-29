from collections import defaultdict
import logging
from src.errors import PlayerNotFound
from src.player import Player
from src.server_context import ServerCtx
from src.client import Client
from src.listeners.player_listener import PlayerListener
from src.utils import is_bound, strip_size

logger = logging.getLogger(__name__)


class Pyseco(object):
    def __init__(self, login, password, ip, port):
        self.login = login
        self.password = password
        self.events_map = defaultdict(set)
        self.server = ServerCtx()
        self.client = Client(ip, port, self.events_map)
        self._register_listeners()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.client.disconnect()

    def _register_listeners(self):
        PlayerListener('PlayerListener', self)
        # and so on

    def _synchronize_basic_data(self):
        self.server.version = self.client.get_version()
        self.server.system_info = self.client.get_system_info()
        self.server.detailed_player_info = self.client.get_detailed_player_info('edenik')
        self.server.ladder_server_limits = self.client.get_ladder_server_limits()
        self.server.max_players = self.client.get_max_players()

    def _synchronize_game_infos(self):
        self.server.current_game_info = self.client.get_current_game_info(0)
        self.server.next_game_info = self.client.get_next_game_info(0)

    def _synchronize_players(self):
        for player in self.client.get_player_list(self.server.max_players.current_value):
            self.add_player(login=player.login)

    def _synchronize_challenges(self):
        self.server.current_challenge = self.client.get_current_challenge_info()
        logger.info(self.server.current_challenge)
        self.client.server_message(f'Current map is {strip_size(self.server.current_challenge.name)}$z$s$888,'
                                   f' author: {self.server.current_challenge.author}')
        self.server.next_challenge = self.client.get_next_challenge_info()

    def _synchronize(self):
        logger.info('Synchronizing data')
        self._synchronize_basic_data()
        self._synchronize_game_infos()
        self._synchronize_players()
        self._synchronize_challenges()

    def register(self, event, listener_method):
        if not is_bound(listener_method):
            logger.error(f'This is not a bound method "{listener_method.__name__}"')
            return
        self.events_map[event].add(listener_method)

    def run(self):
        try:
            self.client.connect()
            self.client.authenticate(self.login, self.password)
            self.client.server_message('pyseco connected')
            self.client.enable_callbacks(True)
            self._synchronize()
            self.client.loop()
        except KeyboardInterrupt:
            logger.info('Exiting')
        except Exception as ex:
            logger.error(ex)

    def add_player(self, login: str, is_spectator: bool = False):
        if login not in self.server.playersInfos:
            self.server.playersInfos[login] = self.client.get_detailed_player_info(login)
        if login not in self.server.playersRankings:
            self.server.playersRankings[login] = self.client.get_current_ranking_for_login(login)[0]

    def remove_player(self, login: str):
        if login in self.server.playersInfos:
            del self.server.playersInfos[login]
        if login in self.server.playersRankings:
            del self.server.playersRankings[login]

    def get_player(self, login):
        try:
            return Player(self.server.playersInfos[login], self.server.playersRankings[login])
        except KeyError:
            logger.error(f'Login "{login}" not found')
            raise PlayerNotFound(f'Login "{login}" not found')

    def set_debug_data(self, data):
        self.client.set_debug_data(data)
