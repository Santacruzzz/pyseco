from src.transport import Transport
from src.api.tm_requests import XmlRpc, XmlRpcMulticall
from src.api.tm_types import Version, ServerOptions, SystemInfo, StateValue, DetailedPlayerInfo, \
    LadderServerLimits, GameInfo, ChallengeInfo
from src.includes.config import Config
from src.includes.log import setup_logger

logger = setup_logger(__name__)


class ServerCtx:
    def __init__(self, transport: Transport, config: Config):
        self.version = Version()
        self.options = ServerOptions()
        self.system_info = SystemInfo()
        self.max_players = StateValue()
        self.detailed_player_info = DetailedPlayerInfo()
        self.ladder_server_limits = LadderServerLimits()
        self.current_game_info = GameInfo()
        self.next_game_info = GameInfo()
        self.current_challenge = ChallengeInfo()
        self.next_challenge = ChallengeInfo()
        self.rpc = XmlRpc(transport)
        self.rpc_multicall = XmlRpcMulticall(transport)
        self.config = config

    def _synchronize_game_infos(self):
        game_infos = self.rpc.get_game_infos()
        self.current_game_info = game_infos.current_value
        self.next_game_info = game_infos.next_value

    def _synchronize_challenges(self):
        self.current_challenge = self.rpc.get_current_challenge_info()
        self.update_next_challenge()

    def update_next_challenge(self):
        self.next_challenge = self.rpc.get_next_challenge_info()

    def synchronize(self):
        self._synchronize_game_infos()
        self._synchronize_challenges()

        self.rpc_multicall.get_version()
        self.rpc_multicall.get_server_options()
        self.rpc_multicall.get_system_info()
        self.rpc_multicall.get_detailed_player_info(self.config.tm_login)
        self.rpc_multicall.get_ladder_server_limits()
        self.rpc_multicall.get_max_players()
        self.version, self.options, self.system_info, self.detailed_player_info, self.ladder_server_limits, \
            self.max_players = self.rpc_multicall.exec(Version, ServerOptions, SystemInfo, DetailedPlayerInfo,
                                                       LadderServerLimits, StateValue)

    def get_name(self):
        return self.options.name
