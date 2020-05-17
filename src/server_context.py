from dataclasses import dataclass

from src.APIs.method_types import Version, ServerOptions, SystemInfo, StateValue, DetailedPlayerInfo, \
    LadderServerLimits, GameInfo, ChallengeInfo


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

    def __init__(self):
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
