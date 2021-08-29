from src.transport import Transport
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
from src.utils import is_bound, strip_size

logger = setup_logger(__name__)


class Pyseco:
    def __init__(self, config_file):
        self.events_queue = Queue()
        self.config = Config(config_file)
        self.transport = Transport(self.config, self.events_queue)
        self.rpc = XmlRpc(self.transport)
        self.events_matrix = defaultdict(set)
        self.server = ServerCtx(self.transport, self.config)
        self.players = dict()
        try:
            self.mysql = MySqlWrapper(self.config)
        except OperationalError as e:
            logger.debug(f'Cannot connect to database, error: {e}')

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.disconnect()

    def _prepare_event(self, msg):
        event = EventData(*loads(msg))
        if not event.name:
            raise NotAnEvent('Not an event')

        if event.name not in self.events_matrix:
            raise EventDiscarded(f'No method registered for {event.name}')

        return event

    def synchronize_players(self):
        for player in self.rpc.get_player_list(self.server.max_players.current_value):
            self.add_player(login=player.login)

    def start_listening(self):
        logger.info('Waiting for events...')
        while True:
            if self.events_queue.qsize():
                logger.debug(
                    f'Handling buffered {self.events_queue.qsize()} event(s)')
                while self.events_queue.qsize():
                    self.handle_event(self.events_queue.get())
            self.handle_event(self.rpc.get_any_message())

    def connect(self):
        self.rpc.connect()
        status = self.rpc.get_status()
        while status.code != 4:
            time.sleep(0.5)
            new_status = self.rpc.get_status()
            if new_status != status:
                status = new_status
                logger.info(f'Server is not ready: {status.name}')

    def disconnect(self):
        self.rpc.disconnect()

    def register_listener(self, class_name, listener_name):
        class_name(listener_name, self)

    def register(self, event, listener_method):
        if not is_bound(listener_method):
            logger.error(
                f'This is not a bound method "{listener_method.__name__}"')
            return

        logger.debug(
            f'Registering {listener_method.__name__} for event {event}')
        self.events_matrix[event].add(listener_method)

    def run(self):
        try:
            self.connect()
            self.rpc.authenticate(self.config.rcp_login,
                                  self.config.rcp_password)
            self.server_message('pyseco connected')
            self.rpc.enable_callbacks(True)
            self.server.synchronize()
            self.synchronize_players()
            self.start_listening()
        except KeyboardInterrupt:
            logger.info('Exiting')
        except Exception as ex:
            logger.error(traceback.format_exc())
            raise
        finally:
            self.rpc.disconnect()

    def add_player(self, login: str, is_spectator: bool = False):
        self.players[login] = Player(self.rpc.get_detailed_player_info(login),
                                     self.rpc.get_current_ranking_for_login(login)[0])

    def remove_player(self, login: str):
        if login in self.players:
            del self.players[login]

    def get_player(self, login: str) -> Player:
        try:
            return self.players[login]
        except KeyError:
            logger.warn(f'Login "{login}" not found')
            raise PlayerNotFound(f'Login "{login}" not found')

    def is_player_on_server(self, login):
        return login in self.players

    def server_message(self, msg):
        self.rpc.chat_send_server_message(
            f'{self.config.color}{self.config.prefix}~ $888{msg}')

    def server_message_to_login(self, login, msg):
        self.rpc.chat_send_server_message_to_login(
            f'{self.config.color}{self.config.prefix}~ $888{msg}', login)

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
            logger.debug(f'Event dropped. {ex}')
        except UnicodeDecodeError as ex:
            logger.error(f'Parsing xml failed. ({ex})')


class Listener(object):
    def __init__(self, name: str, pyseco_instance: Pyseco):
        self._name = name
        self.pyseco = pyseco_instance
        logger.debug(f'{name} registered')

    def __str__(self):
        return f'Listener: {self._name}'
