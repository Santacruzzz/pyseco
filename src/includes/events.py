from src.includes.events_types import *

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
