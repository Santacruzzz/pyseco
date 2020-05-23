from dataclasses import dataclass
from xmlrpc.client import MultiCall

from src.api.tm_requests import XmlRpc
from src.api.tm_types import Version, ServerOptions, SystemInfo, StateValue, DetailedPlayerInfo, \
    LadderServerLimits, GameInfo, ChallengeInfo
from src.includes.config import Config
from src.includes.log import setup_logger

logger = setup_logger(__name__)


@dataclass
class ServerCtx:
    version: Version
    options: ServerOptions
    system_info: SystemInfo
    max_players: StateValue
    detailed_player_info: DetailedPlayerInfo
    ladder_server_limits: LadderServerLimits
    players_infos: dict
    players_rankings: dict
    current_game_info: GameInfo
    next_game_info: GameInfo
    current_challenge: ChallengeInfo
    next_challenge: ChallengeInfo

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
        multicall = MultiCall(self.rpc)
        multicall.GetVersion()
        multicall.GetServerOptions()
        multicall.GetSystemInfo()
        multicall.GetDetailedPlayerInfo(self.config.tm_login)
        multicall.GetLadderServerLimits()
        multicall.GetMaxPlayers()
        results = multicall()

        self.version = Version(*results[0].values())
        self.options = ServerOptions(*results[1].values())
        self.system_info = SystemInfo(*results[2].values())
        self.detailed_player_info = DetailedPlayerInfo(*results[3].values())
        self.ladder_server_limits = LadderServerLimits(*results[4].values())
        self.max_players = StateValue(*results[5].values())
