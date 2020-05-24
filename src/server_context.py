from src.api.tm_requests import XmlRpc
from src.api.tm_types import Version, ServerOptions, SystemInfo, StateValue, DetailedPlayerInfo, \
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
        self.players_infos = dict()
        self.players_rankings = dict()
        self.current_game_info = GameInfo()
        self.next_game_info = GameInfo()
        self.current_challenge = ChallengeInfo()
        self.next_challenge = ChallengeInfo()
        self.rpc = rpc
        self.config = config

    def synchronize(self):
        multicall = self.rpc.multicall()
        multicall.get_version()
        multicall.get_server_options()
        multicall.get_system_info()
        multicall.get_detailed_player_info(self.config.tm_login)
        multicall.get_ladder_server_limits()
        multicall.get_max_players()
        multicall.exec_multicall(self.version, self.options, self.system_info,
                                 self.detailed_player_info, self.ladder_server_limits,
                                 self.max_players)
