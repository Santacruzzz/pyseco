from src.api.tm_requests import XmlRpc
from src.api.tm_types import TmStr, Version, ServerOptions, SystemInfo, StateValue, DetailedPlayerInfo, \
    LadderServerLimits, GameInfo, ChallengeInfo
from src.includes.config import Config
from src.includes.log import setup_logger

logger = setup_logger(__name__)


class ServerCtx:
    def __init__(self, rpc: XmlRpc, config: Config):
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
        self.rpc = rpc
        self.config = config

    def _synchronize_game_infos(self):
        game_infos = self.rpc.get_game_infos()
        self.current_game_info = game_infos.current_value
        self.next_game_info = game_infos.next_value

    def _synchronize_challenges(self):
        self.current_challenge = self.rpc.get_current_challenge_info()
        self.next_challenge = self.rpc.get_next_challenge_info()

    def synchronize(self):
        self._synchronize_game_infos()
        self._synchronize_challenges()

        multicall = self.rpc.getMulticallRpc()
        multicall.get_version()
        multicall.get_server_options()
        multicall.get_system_info()
        multicall.get_detailed_player_info(self.config.tm_login)
        multicall.get_ladder_server_limits()
        multicall.get_max_players()
        self.version, self.options, self.system_info, self.detailed_player_info, self.ladder_server_limits, \
            self.max_players = multicall.exec_multicall(Version, ServerOptions, SystemInfo, DetailedPlayerInfo,
                                                        LadderServerLimits, StateValue)

    def get_name(self) -> TmStr:
        return TmStr(self.options.name)
