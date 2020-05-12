from dataclasses import dataclass
from typing import Any


# TODO add inheritance to types returned by functions which takes compatibility version in parameter (united/nations)

from typing import List


@dataclass
class PlayerScore:
    player_id: int = 0
    score: int = 0


@dataclass
class Avatar:
    file_name: str = ''
    checksum: str = ''


@dataclass
class PackDesc:
    file_name: str = ''
    checksum: str = ''


@dataclass
class Skins:
    environment: int = 0
    pack_desc: PackDesc = PackDesc()


@dataclass
class Status:
    code: int = 0
    name: str = ''


@dataclass
class Version:
    name: str = ''
    version: str = ''
    build: str = ''


@dataclass
class CallVoteRatio:
    command: str = ''
    ratio: float = 0

    def as_dict(self):
        return {
            'Command': self.command,
            'Ratio': self.ratio
        }


@dataclass
class ManialinkPageAnswers:
    login: str = ''
    player_id: int = 0
    result: bool = True


@dataclass
class BanItem:
    login: str = ''
    client_name: str = ''
    ip_address: str = ''


@dataclass
class ForcedSkin:
    orig: str = ''
    name: str = ''
    checksum: str = ''
    url: str = ''


@dataclass
class PlayerInfo:
    login: str = ''
    nickname: str = ''
    player_id: int = 0
    team_id: int = 0
    spectator_status: int = 0
    ladder_ranking: int = 0
    flags: int = 0


@dataclass
class PlayerRanking:
    login: str = ''
    nickname: str = ''
    player_id: int = 0
    rank: int = 0
    best_time: int = 0
    best_checkpoints: int = 0
    score: int = 0
    nbr_laps_finished: int = 0
    ladder_score: int = 0


@dataclass
class CurrentCallVote:
    caller_login: str = ''
    cmd_name: str = ''
    cmd_param: str = ''


@dataclass
class StateValue:
    current_value: Any = 1
    next_value: Any = 1


@dataclass
class BillState:
    state: bool = True
    state_name: str = ''
    transaction_id: int = 0


@dataclass
class SystemInfo:
    published_ip: str = ''
    port: int = 0
    p2p_port: int = 0
    server_login: str = ''
    server_player_id: int = 0
    connection_download_rate: float = 0
    connection_upload_rate: float = 0


@dataclass
class LadderServerLimits:
    ladder_limit_min: int = 0
    ladder_limit_max: int = 0


# aligned to FOREVER version
@dataclass
class ServerOptions:
    name: str = ''
    comment: str = ''
    password: str = ''
    password_for_spectator: str = ''
    hide_server: int = 0
    current_max_players: int = 0
    next_max_players: int = 0
    current_max_spectators: int = 0
    next_max_spectators: int = 0
    is_p2p_upload: bool = True
    is_p2p_download: bool = True
    current_ladder_mode: int = 0
    next_ladder_mode: int = 0
    ladder_server_limit_max: float = 0
    ladder_server_limit_min: float = 0
    current_vehicle_net_quality: int = 0
    next_vehicle_net_quality: int = 0
    current_callvote_timeout: int = 0
    next_callvote_timeout: int = 0
    callvote_ratio: float = 0
    allow_challenge_download: bool = True
    autosave_replays: bool = True
    autosave_validation_replays: bool = True
    referee_password: str = ''
    referee_mode: int = 0
    current_use_changing_validation_seed: bool = True
    next_use_changing_validation_seed: bool = True

    def as_dict(self):
        return {
            'Name': self.name,
            'Comment': self.comment,
            'Password': self.password,
            'PasswordForSpectator': self.password_for_spectator,
            'NextMaxPlayers': self.next_max_players,
            'NextMaxSpectators': self.next_max_spectators,
            'IsP2PUpload': self.is_p2p_upload,
            'IsP2PDownload': self.is_p2p_download,
            'NextLadderMode': self.next_ladder_mode,
            'NextVehicleNetQuality': self.next_vehicle_net_quality,
            'NextCallVoteTimeOut': self.next_callvote_timeout,
            'CallVoteRatio': self.callvote_ratio,
            'AllowChallengeDownload': self.allow_challenge_download,
            'AutoSaveReplays': self.autosave_replays,
            'RefereePassword': self.referee_password,
            'RefereeMode': self.referee_mode,
            'AutoSaveValidationReplays': self.autosave_validation_replays,
            'HideServer': self.hide_server,
            'UseChangingValidationSeed': self.current_use_changing_validation_seed
        }


@dataclass
class Mods:
    env_name: str = ''
    url: str = ''


@dataclass
class ForcedMods:
    is_override: bool = True
    mods_list: list = list


@dataclass
class ForcedMusic:
    is_override: bool = True
    url: str = ''
    file: str = ''


@dataclass
class GameInfo:
    game_mode: int = 0
    chat_time: int = 0
    nb_challenge: str = ''
    rounds_points_limit: int = 0
    rounds_use_new_rules: int = 0
    rounds_forced_laps: int = 0
    timeattack_limit: int = 0
    timeattack_synch_start_period: int = 0
    team_points_limit: int = 0
    team_max_points: int = 0
    team_use_new_rules: int = 0
    laps_nb_laps: int = 0
    laps_time_limit: int = 0
    finish_timeout: int = 0

    def as_dict(self):
        return {
            'GameMode': self.game_mode,
            'ChatTime': self.chat_time,
            'RoundsPointsLimit': self.rounds_points_limit,
            'RoundsUseNewRules': self.rounds_use_new_rules,
            'RoundsForcedLaps': self.rounds_forced_laps,
            'TimeAttackLimit,': self.timeattack_limit,
            'TimeAttackSynchStartPeriod': self.timeattack_synch_start_period,
            'TeamPointsLimit': self.team_points_limit,
            'TeamMaxPoints': self.team_max_points,
            'TeamUseNewRules': self.team_use_new_rules,
            'LapsNbLaps': self.laps_nb_laps,
            'LapsTimeLimit': self.laps_time_limit,
            'FinishTimeout': self.finish_timeout
        }


@dataclass
class ChallengeInfo:
    uid: int = 0
    name: str = ''
    filename: str = ''
    author: str = ''
    environment: int = 0
    mood: int = 0
    bronze_time: int = 0
    silver_time: int = 0
    gold_time: int = 0
    author_time: int = 0
    copper_price: int = 0
    lap_race: int = 0
    nb_laps: int = 0
    nb_checkpoints: int = 0


@dataclass
class LadderRanking:
    path: str = ''
    score: float = 0
    ranking: int = 0
    total_count: int = 0


@dataclass
class LadderStats:
    last_match_score: float = 0
    nbr_match_wins: int = 0
    nbr_match_draws: int = 0
    nbr_match_losses: int = 0
    team_name: str = ''
    player_rankings: List[LadderRanking] = list
    TeamRankings: list = list


@dataclass
class DetailedPlayerInfo:
    login: str = ''
    nickname: str = ''
    player_id: int = 0
    team_id: int = 0
    path: str = ''
    language: str = ''
    client_version: str = ''
    ip_address: str = ''
    download_rate: float = 0
    upload_rate: float = 0
    is_spectator: bool = True
    is_in_official_mode: bool = True
    is_referee: bool = True
    avatar: Avatar = Avatar()
    skins: Skins = Skins()
    ladder_stats: LadderStats = LadderStats()
    hours_since_zone_inscription: int = 0
    online_rights: int = 0


@dataclass
class PlayerNetInfos:
    login: str = ''
    ip_address: str = ''
    last_transfer_time: int = 0
    delta_between_two_last_net_state: int = 0
    packet_loss_rate: float = 0


@dataclass
class NetworkStats:
    uptime: int = 0
    nbr_connection: int = 0
    mean_connection_time: float = 0
    mean_nbr_player: float = 0
    recv_net_rate: float = 0
    send_net_rate: float = 0
    total_receiving_size: int = 0
    total_sending_size: int = 0
    player_net_infos: PlayerNetInfos = PlayerNetInfos()


@dataclass
class TextWithLanguage:
    lang: str = ''
    text: str = ''

    def as_dict(self):
        return {
            'Lang': self.lang,
            'Text': self.text
        }
