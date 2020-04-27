from collections import defaultdict

from errors import PlayerNotFound
from player import Player
from server_context import ServerCtx
from client import *
from listener import Listener


class Pyseco(object):
    def __init__(self, login, password, ip, port, logging_mode=DEBUG):
        self.login = login
        self.password = password
        self.logger = Logger('Pyseco', logging_mode)
        self.events_map = defaultdict(set)
        self.server = ServerCtx()
        self.client = Client(ip, port, logging_mode, self.events_map)
        self.debug_data = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.client.disconnect()

    def set_debug_data(self, data):
        self.debug_data = data
        self.client.set_debug_data(data)

    def register(self, event, listener_method):
        if not is_bound(listener_method):
            self.logger.error(f'This is not a bound method "{listener_method.__name__}"')
            return
        self.events_map[event].add(listener_method)

    def run(self):
        try:
            self.client.connect()
            self.client.authenticate(self.login, self.password)
            self.client.server_message('pyseco connected')
            self.client.enable_callbacks(True)
            self.synchronize()
            self.client.loop()
        except KeyboardInterrupt:
            self.logger.info('Exiting')
        except Exception as ex:
            self.logger.error(str(ex))

    def register_listener(self, listener: Listener):
        listener.set_pyseco(self)

    def synchronize(self):
        self.logger.info('Synchronizing data')
        self._synchronize_basic_data()
        self._synchronize_game_infos()
        self._synchronize_players()
        self._synchronize_challenges()

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
        self.logger.info(self.server.current_challenge)
        self.client.server_message(f'Current map is {strip_size(self.server.current_challenge.name)}$z$s$888,'
                                  f' author: {self.server.current_challenge.author}')
        self.server.next_challenge = self.client.get_next_challenge_info()

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
            self.logger.error(f'Login "{login}" not found')
            raise PlayerNotFound(f'Login "{login}" not found')
