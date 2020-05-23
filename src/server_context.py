from dataclasses import dataclass

from src.api.tm_requests import XmlRpc
from src.api.tm_types import Version, ServerOptions, SystemInfo, StateValue, DetailedPlayerInfo, \
    LadderServerLimits, GameInfo, ChallengeInfo
from src.includes.config import Config


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
        self.version = self.rpc.get_version()
        self.options = self.rpc.get_server_options()
        self.system_info = self.rpc.get_system_info()
        self.detailed_player_info = self.rpc.get_detailed_player_info(self.config.tm_login)
        self.ladder_server_limits = self.rpc.get_ladder_server_limits()
        self.max_players = self.rpc.get_max_players()
