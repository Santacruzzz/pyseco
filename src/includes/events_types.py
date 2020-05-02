from dataclasses import dataclass
from typing import List


def event_decorator(cls):
    cls.name = cls.__name__
    return cls


class EventData:
    def __init__(self, payload, name: str):
        self.type = EVENTS_MAP[name]
        self.name = self.type.name
        self.data = self._parse_data(payload)

    def _parse_data(self, payload):
        if payload:
            return self.type(*payload)
        return None


@event_decorator
@dataclass
class EventPlayerConnect:
    login: str
    is_spectator: bool


@event_decorator
@dataclass
class EventPlayerDisconnect:
    login: str


@event_decorator
@dataclass
class EventPlayerChat:
    player_uid: int
    login: str
    text: str
    is_registered_cmd: bool


@event_decorator
@dataclass
class EventPlayerManialinkPageAnswer:
    player_uid: int
    login: str
    answer: int


@event_decorator
@dataclass
class EventEcho:
    internal: str
    public: str


@event_decorator
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


@event_decorator
@dataclass
class EventBeginRace:
    challenge: EventSChallengeInfo


@event_decorator
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


@event_decorator
@dataclass
class EventEndRace:
    rankings: List[EventSPlayerRanking]
    challenge: EventSChallengeInfo


@event_decorator
@dataclass
class EventBeginChallenge:
    challenge: EventSChallengeInfo
    warm_up: bool
    match_continuation: bool


@event_decorator
@dataclass
class EventEndChallenge:
    rankings: List[EventSPlayerRanking]
    challenge: EventSChallengeInfo
    was_warm_up: bool
    match_continues_on_next_challenge: bool
    restart_challenge: bool


@event_decorator
@dataclass
class EventStatusChanged:
    status_code: int
    status_name: str


@event_decorator
@dataclass
class EventPlayerCheckpoint:
    player_uid: int
    login: str
    time_or_score: int
    cur_lap: int
    checkpoint_index: int


@event_decorator
@dataclass
class EventPlayerFinish:
    player_uid: int
    login: str
    time_or_score: int


@event_decorator
@dataclass
class EventPlayerIncoherence:
    player_uid: int
    login: str


@event_decorator
@dataclass
class EventBillUpdated:
    bill_id: int
    state: int
    state_name: str
    transaction_id: int


# TODO add handling for base64, https://app.zenhub.com/workspaces/pyseco-5ea546214d7b49c27b6b7380/issues/santacruzzz/pyseco/19
# @event_decorator
@dataclass
# class EventTunnelDataReceived:
#     player_uid: int
#     login: str
#     data: base64

@event_decorator
@dataclass
class EventChallengeListModified:
    cur_challenge_index: int
    nex_challenge_index: int
    is_list_modified: bool


@event_decorator
@dataclass
class EventSPlayerInfo:
    login: str
    nickname: str
    player_id: int
    team_id: int
    spectator_status: int
    ladder_ranking: int
    flags: int


@event_decorator
@dataclass
class EventPlayerInfoChanged:
    player_info: EventSPlayerInfo


@event_decorator
@dataclass
class EventManualFlowControlTransition:
    transition: str


@event_decorator
@dataclass
class EventVoteUpdated:
    # StateName values: NewVote, VoteCancelled, VotePassed or VoteFailed
    state_name: str
    login: str
    cmd_name: str
    cmd_param: str


@event_decorator
@dataclass
class EventServerStart:
    pass


@event_decorator
@dataclass
class EventServerStop:
    pass


@event_decorator
@dataclass
class EventBeginRound:
    pass


@event_decorator
@dataclass
class EventEndRound:
    pass


EVENTS_MAP = {
    'TrackMania.PlayerConnect': EventPlayerConnect,
    'TrackMania.PlayerDisconnect': EventPlayerDisconnect,
    'TrackMania.PlayerChat': EventPlayerChat,
    'TrackMania.PlayerManialinkPageAnswer': EventPlayerManialinkPageAnswer,
    'TrackMania.Echo': EventEcho,
    'TrackMania.ServerStart': EventServerStart,
    'TrackMania.ServerStop': EventServerStop,
    'TrackMania.BeginRace': EventBeginRace,
    'TrackMania.EndRace': EventEndRace,
    'TrackMania.BeginChallenge': EventBeginChallenge,
    'TrackMania.EndChallenge': EventEndChallenge,
    'TrackMania.BeginRound': EventBeginRound,
    'TrackMania.EndRound': EventEndRound,
    'TrackMania.StatusChanged': EventStatusChanged,
    'TrackMania.PlayerCheckpoint': EventPlayerCheckpoint,
    'TrackMania.PlayerFinish': EventPlayerFinish,
    'TrackMania.PlayerIncoherence': EventPlayerIncoherence,
    'TrackMania.BillUpdated': EventBillUpdated,
    # 'TrackMania.TunnelDataReceived': EventTunnelDataReceived,
    'TrackMania.ChallengeListModified': EventChallengeListModified,
    'TrackMania.PlayerInfoChanged': EventPlayerInfoChanged,
    'TrackMania.ManualFlowControlTransition': EventManualFlowControlTransition,
    'TrackMania.VoteUpdated': EventVoteUpdated
}