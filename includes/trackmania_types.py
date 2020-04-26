from dataclasses import dataclass


# TODO add inheritance to types returned by functions which takes compatibility version in parameter (united/nations)
# TODO DetailedPlayerInfo -> class

@dataclass
class PlayerScore:
    player_id: int
    score: int


@dataclass
class Avatar:
    file_name: str
    checksum: str


@dataclass
class PackDesc:
    file_name: str
    checksum: str


@dataclass
class Skins:
    environment: int
    pack_desc: PackDesc


@dataclass
class Status:
    code: int
    name: str


@dataclass
class Version:
    name: str
    version: str
    build: str


@dataclass
class CallVoteRatio:
    command: str
    ratio: float


@dataclass
class ManialinkPageAnswers:
    login: str
    player_id: int
    result: bool


@dataclass
class BanItem:
    login: str
    client_name: str
    ip_address: str


@dataclass
class ForcedSkin:
    orig: str
    name: str
    checksum: str
    url: str


@dataclass
class PlayerInfo:
    login: str
    nickname: str
    player_id: int
    team_id: int
    spectator_status: int
    ladder_ranking: int
    flags: int


@dataclass
class PlayerRanking:
    login: str
    nickname: str
    player_id: int
    rank: int
    best_time: int
    best_checkpoints: int
    score: int
    nbr_laps_finished: int
    ladder_score: int


@dataclass
class CurrentCallVote:
    caller_login: str
    cmd_name: str
    cmd_param: str


@dataclass
class StateValue:
    current_value: bool
    next_value: bool


@dataclass
class BillState:
    state: bool
    state_name: str
    transaction_id: int


@dataclass
class SystemInfo:
    published_ip: str
    port: int
    p2p_port: int
    server_login: str
    server_player_id: int
    connection_download_rate: float
    connection_upload_rate: float


@dataclass
class LadderServerLimits:
    ladder_limit_min: int
    ladder_limit_max: int


@dataclass
class ServerOptions:
    name: str
    comment: str
    password: str
    password_for_spectator: str
    current_max_players: int
    next_max_players: int
    current_max_spectators: int
    next_max_spectators: int
    is_p2p_upload: bool
    is_p2p_download: bool
    current_ladder_mode: int
    next_ladder_mode: int
    current_vehicle_net_quality: int
    next_vehicle_net_quality: int
    current_callvote_timeout: int
    next_callvote_timeout: int
    callvote_ratio: float
    allow_challenge_download: bool
    autosave_replays: bool
    referee_password: str
    referee_mode: int
    autosave_validation_replays: bool
    hide_server: int
    current_use_changing_validation_seed: bool
    next_use_changing_validation_seed: bool


@dataclass
class Mods:
    env_name: str
    url: str


@dataclass
class ForcedMods:
    is_override: bool
    mods_list: list


@dataclass
class ForcedMusic:
    is_override: bool
    url: str
    file: str


@dataclass
class GameInfo:
    game_mode: int
    chat_time: int
    nb_challenge: str
    rounds_points_limit: int
    rounds_use_new_rules: int
    rounds_forced_laps: int
    timeattack_limit: int
    timeattack_synch_start_period: int
    team_points_limit: int
    team_max_points: int
    team_use_new_rules: int
    laps_nb_laps: int
    laps_time_limit: int
    finish_timeout: int


@dataclass
class ChallengeInfo:
    uid: int
    name: str
    filename: str
    author: str
    environment: int
    mood: int
    bronze_time: int
    silver_time: int
    gold_time: int
    author_time: int
    copper_price: int
    lap_race: int
    nb_laps: int
    nb_checkpoints: int


@dataclass
class DetailedPlayerInfo:
    login: str
    nickname: str
    player_id: int
    team_id: int
    ip_address: str
    download_rate: float
    upload_rate: float
    language: str
    is_spectator: bool
    is_in_official_mode: bool
    avatar: Avatar
    skins: Skins
    ladder_stats: int
    hours_since_zone_inscription: int
    online_rights: int


@dataclass
class PlayerNetInfos:
    login: str
    ip_address: str
    last_transfer_time: int
    delta_between_two_last_net_state: int
    packet_loss_rate: float


@dataclass
class NetworkStats:
    uptime: int
    nbr_connection: int
    mean_connection_time: float
    mean_nbr_player: float
    recv_net_rate: float
    send_net_rate: float
    total_receiving_size: int
    total_sending_size: int
    player_net_infos: PlayerNetInfos


@dataclass
class TextWithLanguage:
    lang: str
    text: str
