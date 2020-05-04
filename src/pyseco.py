import logging
import traceback
from collections import defaultdict
from xmlrpc.client import loads
from src.APIs.trackmania_api import TrackmaniaAPI, StateValue
from src.errors import PlayerNotFound, NotAnEvent, EventDiscarded, PysecoException
from src.listeners.player_listener import PlayerListener, EventData
from src.listeners.chat_listener import ChatListener
from src.player import Player
from src.server_context import ServerCtx
from src.utils import is_bound, strip_size

logger = logging.getLogger(__name__)


class Pyseco(TrackmaniaAPI):
    def __init__(self, login, password, ip, port):
        super().__init__(ip, port, self)
        self.login = login
        self.password = password
        self.events_map = defaultdict(set)
        self.server = ServerCtx()
        self._register_listeners()
        self.debug_data = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.disconnect()

    def _register_listeners(self):
        PlayerListener('PlayerListener', self)
        ChatListener('ChatListener', self)
        # and so on

    def _synchronize_basic_data(self):
        self.server.version = self.get_version()
        self.server.system_info = self.get_system_info()
        self.server.detailed_player_info = self.get_detailed_player_info('edenik')
        self.server.ladder_server_limits = self.get_ladder_server_limits()
        # self.server.max_players = self.get_max_players()
        self.server.max_players = StateValue(50, 50)

    def _synchronize_game_infos(self):
        game_infos = self.get_game_infos(1)
        self.server.current_game_info = game_infos.current_value
        self.server.next_game_info = game_infos.next_value

    def _synchronize_players(self):
        for player in self.get_player_list(self.server.max_players.current_value):
            self.add_player(login=player.login)

    def _synchronize_challenges(self):
        self.server.current_challenge = self.get_current_challenge_info()
        logger.info(self.server.current_challenge)
        self.server_message(f'Current map is {strip_size(self.server.current_challenge.name)}$z$s$888,'
                            f' author: {self.server.current_challenge.author}')
        self.server.next_challenge = self.get_next_challenge_info()

    def _synchronize(self):
        logger.info('Synchronizing data')
        self._synchronize_basic_data()
        self._synchronize_game_infos()
        self._synchronize_players()
        self._synchronize_challenges()

    def _prepare_event(self, msg):
        event = EventData(*loads(msg))
        if not event.name:
            # TODO this is an side effect of noresponse method which should be deleted
            # if parsed xml has no "methodName" (second field in tuple) then this is a response
            # which belongs to noresponse.Request and should be discarded
            raise NotAnEvent('Not an event')

        if event.name not in self.events_map:
            raise EventDiscarded(f'No method registered for {event.name}')

        return event

    def register(self, event, listener_method):
        if not is_bound(listener_method):
            logger.error(f'This is not a bound method "{listener_method.__name__}"')
            return

        logger.debug(f'Registering {listener_method.__name__} for event {event}')
        self.events_map[event].add(listener_method)

    def run(self):
        try:
            self.connect()
            self.authenticate(self.login, self.password)
            self.server_message('pyseco connected')
            self.enable_callbacks(True)
            self._synchronize()
            self.start_listening()
        except KeyboardInterrupt:
            logger.info('Exiting')
        except Exception as ex:
            logger.error(traceback.format_exc())
            raise

    def add_player(self, login: str, is_spectator: bool = False):
        if login not in self.server.playersInfos:
            self.server.playersInfos[login] = self.get_detailed_player_info(login)
        if login not in self.server.playersRankings:
            self.server.playersRankings[login] = self.get_current_ranking_for_login(login)[0]

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

    def server_message(self, msg):
        self.ChatSendServerMessage(f'${self.debug_data["color"]}~ $888{msg}')

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

    def set_debug_data(self, data):
        self.debug_data = data
