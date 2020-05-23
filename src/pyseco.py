import time
import traceback
from collections import defaultdict
from queue import Queue
from xmlrpc.client import loads

from pymysql import OperationalError

from src.api.tm_requests import XmlRpc
from src.errors import PlayerNotFound, NotAnEvent, EventDiscarded, PysecoException
from src.includes.config import Config
from src.includes.events_types import EventData
from src.includes.log import setup_logger
from src.includes.mysql_wrapper import MySqlWrapper
from src.player import Player
from src.server_context import ServerCtx
from src.transport import Transport
from src.utils import is_bound, strip_size

logger = setup_logger(__name__)


class Pyseco:
    def __init__(self, config_file):
        self.events_queue = Queue()
        self.config = Config(config_file)
        self.transport = Transport(self.config.rcp_ip, self.config.rcp_port, self.events_queue)
        self.rpc = XmlRpc(self.transport)

        self.events_matrix = defaultdict(set)
        self.server = ServerCtx(self.rpc, self.config)
        try:
            self.mysql = MySqlWrapper(self.config)
        except OperationalError as e:
            logger.debug(f'Cannot connect to database, error: {e}')

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.disconnect()

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
        self.server.synchronize()
        self._synchronize_game_infos()
        self._synchronize_players()
        self._synchronize_challenges()

    def _prepare_event(self, msg):
        event = EventData(*loads(msg))
        if not event.name:
            raise NotAnEvent('Not an event')

        if event.name not in self.events_matrix:
            raise EventDiscarded(f'No method registered for {event.name}')

        return event

    def start_listening(self):
        logger.info('Waiting for events...')
        while True:
            if self.events_queue.qsize():
                logger.debug(f'Handling buffered {self.events_queue.qsize()} event(s)')
                while self.events_queue.qsize():
                    self.handle_event(self.events_queue.get())
            self.handle_event(self.transport.get_any_message())

    def connect(self):
        self.transport.connect()
        status = self.rpc.get_status()
        while status.code != 4:
            time.sleep(0.5)
            new_status = self.rpc.get_status()
            if new_status != status:
                status = new_status
                logger.info(f'Server is not ready: {status.name}')

    def disconnect(self):
        self.transport.disconnect()

    def add_listener(self, class_name, listener_name):
        class_name(listener_name, self)

    def register(self, event, listener_method):
        if not is_bound(listener_method):
            logger.error(f'This is not a bound method "{listener_method.__name__}"')
            return

        logger.debug(f'Registering {listener_method.__name__} for event {event}')
        self.events_matrix[event].add(listener_method)

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
            for listener_method in self.events_matrix[event.name]:
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
