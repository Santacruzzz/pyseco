from dataclasses import dataclass
from typing import List

@dataclass
class EventPlayerConnect:
    login: str
    is_spectator: bool


@dataclass
class EventPlayerDisconnect:
    login: str


@dataclass
class EventPlayerChat:
    player_uid: int
    login: str
    text: str
    is_registered_cmd: bool


@dataclass
class EventPlayerManialinkPageAnswer:
    player_uid: int
    login: str
    answer: int


@dataclass
class EventEcho:
    internal: str
    public: str


@dataclass
class EventSChallengeInfo:
    uid: str
    name: str
    filename: str
    author: str
    environment: str
    mood: str
    bronze_time: int
    silver_time: int
    gold_time: int
    author_time: int
    copper_price: int
    lap_race: bool
    nb_laps: int
    nb_checkpoints: int


@dataclass
class EventBeginRace:
    challenge: EventSChallengeInfo


@dataclass
class EventSPlayerRanking:
    login: str
    nickname: str
    player_id: int
    rank: int
    best_time: int
    best_checkpoints: List[int]
    score: int
    nbr_laps_finished: int
    ladder_score: float


@dataclass
class EventEndRace:
    rankings: List[EventSPlayerRanking]
    challenge: EventSChallengeInfo


@dataclass
class EventBeginChallenge:
    challenge: EventSChallengeInfo
    warm_up: bool
    match_continuation: bool


@dataclass
class EventEndChallenge:
    rankings: List[EventSPlayerRanking]
    challenge: EventSChallengeInfo
    was_warm_up: bool
    match_continues_on_next_challenge: bool
    restart_challenge: bool


@dataclass
class EventStatusChanged:
    status_code: int
    status_name: str


@dataclass
class EventPlayerCheckpoint:
    player_uid: int
    login: str
    time_or_score: int
    cur_lap: int
    checkpoint_index: int


@dataclass
class EventPlayerFinish:
    player_uid: int
    login: str
    time_or_score: int


@dataclass
class EventPlayerIncoherence:
    player_uid: int
    login: str


@dataclass
class EventBillUpdated:
    bill_id: int
    state: int
    state_name: str
    transaction_id: int


# TODO add handling for base64, https://app.zenhub.com/workspaces/pyseco-5ea546214d7b49c27b6b7380/issues/santacruzzz/pyseco/19
# @dataclass
# class EventTunnelDataReceived:
#     player_uid: int
#     login: str
#     data: base64

@dataclass
class EventChallengeListModified:
    cur_challenge_index: int
    nex_challenge_index: int
    is_list_modified: bool


@dataclass
class EventSPlayerInfo:
    login: str
    nickname: str
    player_id: int
    team_id: int
    spectator_status: int
    ladder_ranking: int
    flags: int


@dataclass
class EventPlayerInfoChanged:
    player_info: EventSPlayerInfo


@dataclass
class EventManualFlowControlTransition:
    transition: str


@dataclass
class EventVoteUpdated:
    # StateName values: NewVote, VoteCancelled, VotePassed or VoteFailed
    state_name: str
    login: str
    cmd_name: str
    cmd_param: str