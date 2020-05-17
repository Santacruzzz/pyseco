from dataclasses import dataclass
from typing import List

from src.APIs.method_types import Version, ServerOptions, SystemInfo, StateValue, DetailedPlayerInfo, \
    LadderServerLimits, PlayerInfo, PlayerRanking, GameInfo, ChallengeInfo


@dataclass
class ServerCtx:
    version: Version
    options: ServerOptions
    system_info: SystemInfo
    max_players: StateValue
    detailed_player_info: DetailedPlayerInfo
    ladder_server_limits: LadderServerLimits
    players_infos: List[PlayerInfo]
    players_rankings: List[PlayerRanking]
    current_game_info: GameInfo
    next_game_info: GameInfo
    current_challenge: ChallengeInfo
    next_challenge: ChallengeInfo

    def __init__(self):
        pass
