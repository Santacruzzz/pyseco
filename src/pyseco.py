import traceback
from collections import defaultdict
from xmlrpc.client import loads
from pymysql import OperationalError

from src.APIs.trackmania_api import XmlRpc
from src.client import Client
from src.errors import PlayerNotFound, NotAnEvent, EventDiscarded, PysecoException
from src.includes.config import Config
from src.includes.events_types import EventData
from src.includes.log import setup_logger
from src.includes.mysql_wrapper import MySqlWrapper
from src.player import Player
from src.server_context import ServerCtx
from src.utils import is_bound, strip_size

logger = setup_logger(__name__)


class Pyseco:
    def __init__(self, config_file):
        self.config = Config(config_file)
        self.client = Client(self.config.rcp_ip, self.config.rcp_port, self)
        self.rpc = XmlRpc(self.client)

        self.events_map = defaultdict(set)
        self.server = ServerCtx()
        try:
            self.mysql = MySqlWrapper(self.config)
        except OperationalError as e:
            logger.debug(f'Cannot connect to database, error: {e}')

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.disconnect()

    def _synchronize_basic_data(self):
        self.server.version = self.rpc.get_version()
        self.server.options = self.rpc.get_server_options()
        self.server.system_info = self.rpc.get_system_info()
        self.server.detailed_player_info = self.rpc.get_detailed_player_info(self.config.tm_login)
        self.server.ladder_server_limits = self.rpc.get_ladder_server_limits()
        self.server.max_players = self.rpc.get_max_players()

    def _synchronize_game_infos(self):
        game_infos = self.rpc.get_game_infos()
        self.server.current_game_info = game_infos.current_value
        self.server.next_game_info = game_infos.next_value

    def _synchronize_players(self):
        for player in self.rpc.get_player_list(self.server.max_players.current_value):
            self.add_player(login=player.login)

    def _synchronize_challenges(self):
        self.server.current_challenge = self.rpc.get_current_challenge_info()
        logger.info(self.server.current_challenge)
        self.server_message(f'Current map is {strip_size(self.server.current_challenge.name)}$z$s$888,'
                            f' author: {self.server.current_challenge.author}')
        self.server.next_challenge = self.rpc.get_next_challenge_info()

    def _synchronize(self):
        logger.info('Synchronizing data')
        self._synchronize_basic_data()
        self._synchronize_game_infos()
        self._synchronize_players()
        self._synchronize_challenges()

    def _prepare_event(self, msg):
        event = EventData(*loads(msg))
        if not event.name:
            raise NotAnEvent('Not an event')

        if event.name not in self.events_map:
            raise EventDiscarded(f'No method registered for {event.name}')

        return event

    def start_listening(self):
        self.client.loop()

    def connect(self):
        self.client.connect()

    def disconnect(self):
        self.client.disconnect()

    def add_listener(self, class_name, listener_name):
        class_name(listener_name, self)

    def register(self, event, listener_method):
        if not is_bound(listener_method):
            logger.error(f'This is not a bound method "{listener_method.__name__}"')
            return

        logger.debug(f'Registering {listener_method.__name__} for event {event}')
        self.events_map[event].add(listener_method)

    def run(self):
        try:
            self.connect()
            self.rpc.authenticate(self.config.rcp_login, self.config.rcp_password)
            self.server_message('pyseco connected')
            self.rpc.enable_callbacks(True)
            self._synchronize()
            self.start_listening()
        except KeyboardInterrupt:
            logger.info('Exiting')
        except Exception as ex:
            logger.error(traceback.format_exc())
            raise

    def add_player(self, login: str, is_spectator: bool = False):
        if login not in self.server.players_infos:
            self.server.players_infos[login] = self.rpc.get_detailed_player_info(login)
        if login not in self.server.players_rankings:
            self.server.players_rankings[login] = self.rpc.get_current_ranking_for_login(login)[0]

    def remove_player(self, login: str):
        if login in self.server.players_infos:
            del self.server.players_infos[login]
        if login in self.server.players_rankings:
            del self.server.players_rankings[login]

    def get_player(self, login: str) -> Player:
        try:
            return Player(self.server.players_infos[login], self.server.players_rankings[login])
        except KeyError:
            logger.error(f'Login "{login}" not found')
            raise PlayerNotFound(f'Login "{login}" not found')

    def server_message(self, msg):
        self.rpc.chat_send_server_message(f'{self.config.color}{self.config.prefix}~ $888{msg}')

    def handle_event(self, event):
        try:
            event = self._prepare_event(event)
            logger.debug(f'{event.name} Data: {event.data}')
            for listener_method in self.events_map[event.name]:
                if event.data:
                    listener_method(event.data)
                else:
                    listener_method()

        except PysecoException as ex:
            logger.debug(f'Event discarded: {ex}')
        except UnicodeDecodeError as ex:
            logger.error(f'Parsing xml failed. ({ex})')


class Listener(object):
    def __init__(self, name: str, pyseco_instance: Pyseco):
        self._name = name
        self.pyseco = pyseco_instance
        logger.debug(f'{name} registered')

    def __str__(self):
        return f'Listener: {self._name}'
