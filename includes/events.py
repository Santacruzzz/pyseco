from includes.events_types import *


class Events:
    PLAYER_CONNECT = 'TrackMania.PlayerConnect'
    PLAYER_DISCONNECT = 'TrackMania.PlayerDisconnect'
    PLAYER_CHAT = 'TrackMania.PlayerChat'
    PLAYER_MANIALINK_PAGE_ANSWER = 'TrackMania.PlayerManialinkPageAnswer'
    ECHO = 'TrackMania.Echo'
    SERVER_START = 'TrackMania.ServerStart'
    SERVER_STOP = 'TrackMania.ServerStop'
    BEGIN_RACE = 'TrackMania.BeginRace'
    END_RACE = 'TrackMania.EndRace'
    BEGIN_CHALLENGE = 'TrackMania.BeginChallenge'
    END_CHALLENGE = 'TrackMania.EndChallenge'
    BEGIN_ROUND = 'TrackMania.BeginRound'
    END_ROUND = 'TrackMania.EndRound'
    STATUS_CHANGED = 'TrackMania.StatusChanged'
    PLAYER_CHECKPOINT = 'TrackMania.PlayerCheckpoint'
    PLAYER_FINISH = 'TrackMania.PlayerFinish'
    PLAYER_INCOHERENCE = 'TrackMania.PlayerIncoherence'
    BILL_UPDATED = 'TrackMania.BillUpdated'
    # TUNNEL_DATA_RECEIVED = 'TrackMania.TunnelDataReceived'
    CHALLENGE_LIST_MODIFIED = 'TrackMania.ChallengeListModified'
    PLAYER_INFO_CHANGED = 'TrackMania.PlayerInfoChanged'
    MANUAL_FLOW_CONTROL_TRANSITION = 'TrackMania.ManualFlowControlTransition'
    VOTE_UPDATED = 'TrackMania.VoteUpdated'


EVENTS_MAP = {
    Events.PLAYER_CONNECT: EventPlayerConnect,
    Events.PLAYER_DISCONNECT: EventPlayerDisconnect,
    Events.PLAYER_CHAT: EventPlayerChat,
    Events.PLAYER_MANIALINK_PAGE_ANSWER: EventPlayerManialinkPageAnswer,
    Events.ECHO: EventEcho,
    Events.SERVER_START: None,
    Events.SERVER_STOP: None,
    Events.BEGIN_RACE: EventBeginRace,
    Events.END_RACE: EventEndRace,
    Events.BEGIN_CHALLENGE: EventBeginChallenge,
    Events.END_CHALLENGE: EventEndChallenge,
    Events.BEGIN_ROUND: None,
    Events.END_ROUND: None,
    Events.STATUS_CHANGED: EventStatusChanged,
    Events.PLAYER_CHECKPOINT: EventPlayerCheckpoint,
    Events.PLAYER_FINISH: EventPlayerFinish,
    Events.PLAYER_INCOHERENCE: EventPlayerIncoherence,
    Events.BILL_UPDATED: EventBillUpdated,
    # Events.TUNNEL_DATA_RECEIVED: EventTunnelDataReceived,
    Events.CHALLENGE_LIST_MODIFIED: EventChallengeListModified,
    Events.PLAYER_INFO_CHANGED: EventPlayerInfoChanged,
    Events.MANUAL_FLOW_CONTROL_TRANSITION: EventManualFlowControlTransition,
    Events.VOTE_UPDATED: EventVoteUpdated
}
