#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import abstractmethod
from datetime import datetime
from collections import namedtuple
from typing import List
import inspect

# TODO add inheritance to types returned by functions which takes compatibility version in parameter (united/nations)
# TODO DetailedPlayerInfo -> class

Status = namedtuple('ServerStatus', ['code', 'name'])
Version = namedtuple('Version', ['name', 'version', 'build'])
CallVoteRatio = namedtuple('CallVoteRatio', ['command', 'ratio'])
ManialinkPageAnswers = namedtuple('ManialinkPageAnswers', ['login', 'player_id', 'result'])
BanItem = namedtuple('BanItem', ['login', 'client_name', 'ip_address'])
BlackListItem = namedtuple('BlackListItem', ['login'])
GuestListItem = namedtuple('GuestListItem', ['login'])
IgnoreListItem = namedtuple('IgnoreListItem', ['login'])
ForcedSkin = namedtuple('ForcedSkin', ['orig', 'name', 'checksum', 'url'])
Challenge = namedtuple('Challenge', ['uid', 'name', 'filename', 'environment', 'author', 'gold_time', 'copper_price'])
PlayerInfo = namedtuple('PlayerInfo', ['login', 'nickname', 'player_id', 'team_id', 'spectator_status',
                                       'ladder_ranking', 'flags'])
RankingItem = namedtuple('RankingItem', ['login', 'nickname', 'player_id', 'rank', 'best_time', 'best_checkpoints',
                                         'score', 'nbr_laps_finished', 'ladder_score'])
CurrentCallVote = namedtuple('CurrentCallVote', ['caller_login', 'cmd_name', 'cmd_param'])
StateValue = namedtuple('StateValue', ['current_value', 'next_value'])
BillState = namedtuple('BillState', ['state', 'state_name', 'transaction_id'])
SystemInfo = namedtuple('SystemInfo', ['published_ip', 'port', 'p2p_port', 'server_login', 'server_player_id',
                                       'connection_download_rate', 'connection_upload_rate'])
LadderServerLimits = namedtuple('LadderServerLimits', ['ladder_limit_min', 'ladder_limit_max'])
ServerOptions = namedtuple('ServerOptions', ['name', 'comment', 'password', 'passwordforspectator',
                                             'current_max_players', 'next_max_players', 'current_max_spectators',
                                             'next_max_spectators', 'is_p2p_upload', 'is_p2p_download',
                                             'current_ladder_mode', 'next_ladder_mode', 'current_vehicle_net_quality',
                                             'next_vehicle_net_quality', 'current_callvote_timeout',
                                             'next_callvote_timeout', 'callvote_ratio', 'allow_challenge_download',
                                             'autosave_replays', 'referee_password', 'referee_mode',
                                             'autosave_validation_replays', 'hide_server',
                                             'current_use_changing_validation_seed',
                                             'next_use_changing_validation_seed'])
ForcedMods = namedtuple('ForcedMods', ['is_override', 'mods_list'])
ForcedMusic = namedtuple('ForcedMusic', ['is_override', 'url', 'file'])
GameInfo = namedtuple('GameInfo', ['game_mode', 'chat_time', 'nb_challenge', 'rounds_points_limit',
                                   'rounds_use_new_rules', 'rounds_forced_laps', 'timeattack_limit',
                                   'timeattack_synch_start_period', 'team_points_limit',
                                   'team_max_points', 'team_use_new_rules', 'laps_nb_laps',
                                   'laps_time_limit', 'finish_timeout'])
ChallengeInfo = namedtuple('ChallengeInfo', ['name', 'uid', 'filename', 'author', 'environnement', 'mood',
                                             'bronze_time', 'silver_time', 'gold_time', 'author_time', 'copper_price',
                                             'laprace', 'nb_laps', 'nb_checkpoints'])
DetailedPlayerInfo = namedtuple('DetailedPlayerInfo', ['login', 'nickname', 'player_id', 'team_id', 'ip_address',
                                                       'download_rate', 'upload_rate', 'language', 'is_spectator',
                                                       'is_in_official_mode', 'avatar', 'skins', 'ladder_stats',
                                                       'hours_since_zone_inscription', 'online_rights'])
NetworkStats = namedtuple('NetworkStats', ['uptime', 'nbr_connection', 'mean_connection_time', 'mean_nbr_player',
                                           'recv_net_rate', 'send_net_rate', 'total_receiving_size',
                                           'total_sending_size', 'player_net_infos'])

ChatLine = str
RoundCustomPoints = int
CallVoteRatioList = List[CallVoteRatio]
ChatLinesList = List[ChatLine]
ManialinkPageAnswersList = List[ManialinkPageAnswers]
BanList = List[BanItem]
BlackList = List[BlackListItem]
GuestList = List[GuestListItem]
ForcedSkinsList = List[ForcedSkin]
RoundCustomPointsList = List[RoundCustomPoints]
ChallengeList = List[Challenge]
PlayerInfoList = List[PlayerInfo]
RankingList = List[RankingItem]
IgnoreList = List[IgnoreListItem]

# globals
DEBUG = 0
INFO = 1
NONE = 9


# classes
class EventData(object):
    def __init__(self, data, event_name: str):
        self.data = data
        self.event_name = event_name

    def __str__(self):
        return self.event_name


def _get_parent_function_name():
    # TODO sometimes throws an exception out of range blah blah
    return inspect.stack()[3][3]


class Colors(object):
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    @staticmethod
    def red(txt):
        return f'\033[91m{txt}\033[0m'

    @staticmethod
    def green(txt):
        return f'\033[92m{txt}\033[0m'

    @staticmethod
    def blue(txt):
        return f'\033[94m{txt}\033[0m'


class Logger(object):
    def __init__(self, name: str = None, logging_mode: int = 0):
        self._name = name
        self._mode = logging_mode

    def __call__(self, msg):
        self.info(msg)

    def get_logging_mode(self):
        return self._mode

    def set_logging_mode(self, logging_mode):
        self._mode = logging_mode

    def set_name(self, name):
        self._name = name

    def _show(self, tag, msg):
        function_name = _get_parent_function_name()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        try:
            if self._name:
                print(f'{current_time} {tag}/{self._name}/{function_name}: {msg}')
            else:
                print(f'{current_time} {tag}/{function_name}: {msg}')
        except Exception as ex:
            self.error(str(ex))

    def set_mode(self, mode):
        self._mode = mode

    def info(self, msg):
        if self._mode <= INFO:
            self._show(Colors.green('INF'), msg)

    def debug(self, msg):
        if self._mode <= DEBUG:
            self._show(Colors.blue('DBG'), msg)

    def error(self, msg):
        if self._mode != NONE:
            self._show(Colors.red('ERR'), msg)


# TODO add ABC meta
class BaseClient(object):
    def __init__(self):
        pass

    @abstractmethod
    def __getattr__(self, item):
        pass

    def authenticate(self, *data) -> bool:
        """Allow user authentication by specifying a login and a password, to gain access to the set of
        functionalities corresponding to this authorization level. """
        if len(data) > 0:
            return bool(getattr(self, 'Authenticate')(*data))
        return bool(getattr(self, 'Authenticate')())

    def changeAuthPassword(self, *data) -> bool:
        """Change the password for the specified login/user. Only available to SuperAdmin."""
        if len(data) > 0:
            return bool(getattr(self, 'ChangeAuthPassword')(*data))
        return bool(getattr(self, 'ChangeAuthPassword')())

    def enableCallbacks(self, *data) -> bool:
        """Allow the GameServer to call you back."""
        if len(data) > 0:
            return bool(getattr(self, 'EnableCallbacks')(*data))
        return bool(getattr(self, 'EnableCallbacks')())

    def getVersion(self, *data) -> Version:
        """Returns a struct with the Name, Version and Build of the application remotely controled."""
        if len(data) > 0:
            return Version(*getattr(self, 'GetVersion')(*data).values())
        return Version(*getattr(self, 'GetVersion')().values())

    def callVote(self, *data) -> bool:
        """Call a vote for a cmd. The command is a XML string corresponding to an XmlRpc request.
        Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'CallVote')(*data))
        return bool(getattr(self, 'CallVote')())

    def callVoteEx(self, *data) -> bool:
        """Extended call vote. Same as CallVote, but you can additionally supply specific parameters for this vote:
        a ratio, a time out and who is voting. Special timeout values: a timeout of '0' means default,
        '1' means indefinite; a ratio of '-1' means default; Voters values: '0' means only active players,
        '1' means any player, '2' is for everybody, pure spectators included. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'CallVoteEx')(*data))
        return bool(getattr(self, 'CallVoteEx')())

    def internalCallVote(self, *data) -> bool:
        """Used internally by game."""
        if len(data) > 0:
            return bool(getattr(self, 'InternalCallVote')(*data))
        return bool(getattr(self, 'InternalCallVote')())

    def cancelVote(self, *data) -> bool:
        """Cancel the current vote. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'CancelVote')(*data))
        return bool(getattr(self, 'CancelVote')())

    def getCurrentCallVote(self, *data) -> CurrentCallVote:
        """Returns the vote currently in progress. The returned structure is { CallerLogin, CmdName, CmdParam }."""
        if len(data) > 0:
            return CurrentCallVote(*getattr(self, 'GetCurrentCallVote')(*data).values())
        return CurrentCallVote(*getattr(self, 'GetCurrentCallVote')().values())

    def setCallVoteTimeOut(self, *data) -> bool:
        """Set a new timeout for waiting for votes. A zero value disables callvote. Only available to Admin.
        Requires a challenge restart to be taken into account."""
        if len(data) > 0:
            return bool(getattr(self, 'SetCallVoteTimeOut')(*data))
        return bool(getattr(self, 'SetCallVoteTimeOut')())

    def getCallVoteTimeOut(self, *data) -> StateValue:
        """Get the current and next timeout for waiting for votes. The struct returned contains two
        fields 'CurrentValue' and 'NextValue'."""
        if len(data) > 0:
            return StateValue(*getattr(self, 'GetCallVoteTimeOut')(*data).values())
        return StateValue(*getattr(self, 'GetCallVoteTimeOut')().values())

    def setCallVoteRatio(self, *data) -> bool:
        """Set a new default ratio for passing a vote. Must lie between 0 and 1. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SetCallVoteRatio')(*data))
        return bool(getattr(self, 'SetCallVoteRatio')())

    def getCallVoteRatio(self, *data) -> float:
        """Get the current default ratio for passing a vote. This value lies between 0 and 1."""
        if len(data) > 0:
            return float(*getattr(self, 'GetCallVoteRatio')(*data).values())
        return float(*getattr(self, 'GetCallVoteRatio')().values())

    def setCallVoteRatios(self, *data) -> bool:
        """Set new ratios for passing specific votes. The parameter is an array of structs {string Command,
        double Ratio}, ratio is in [0,1] or -1 for vote disabled. Only available to Admin. """
        if len(data) > 0:
            return bool(getattr(self, 'SetCallVoteRatios')(*data))
        return bool(getattr(self, 'SetCallVoteRatios')())

    def getCallVoteRatios(self, *data) -> CallVoteRatioList:
        """Get the current ratios for passing votes."""
        if len(data) > 0:
            return [CallVoteRatio(*result.values()) for result in getattr(self, 'GetCallVoteRatios')(*data)]
        return [CallVoteRatio(*result.values()) for result in getattr(self, 'GetCallVoteRatios')()]

    def chatSendServerMessage(self, *data) -> bool:
        """Send a text message to all clients without the server login. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'ChatSendServerMessage')(*data))
        return bool(getattr(self, 'ChatSendServerMessage')())

    def chatSendServerMessageToLanguage(self, *data) -> bool:
        """Send a localised text message to all clients without the server login, or optionally to a Login (which can
        be a single login or a list of comma-separated logins). The parameter is an array of structures {Lang='??',
        Text='...'}. If no matching language is found, the last text in the array is used. Only available to Admin. """
        if len(data) > 0:
            return bool(getattr(self, 'ChatSendServerMessageToLanguage')(*data))
        return bool(getattr(self, 'ChatSendServerMessageToLanguage')())

    def chatSendServerMessageToId(self, *data) -> bool:
        """Send a text message without the server login to the client with the specified PlayerId.
        Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'ChatSendServerMessageToId')(*data))
        return bool(getattr(self, 'ChatSendServerMessageToId')())

    def chatSendServerMessageToLogin(self, *data) -> bool:
        """Send a text message without the server login to the client with the specified login.
        Login can be a single login or a list of comma-separated logins. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'ChatSendServerMessageToLogin')(*data))
        return bool(getattr(self, 'ChatSendServerMessageToLogin')())

    def chatSend(self, *data) -> bool:
        """Send a text message to all clients. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'ChatSend')(*data))
        return bool(getattr(self, 'ChatSend')())

    def chatSendToLanguage(self, *data) -> bool:
        """Send a localised text message to all clients, or optionally to a Login (which can be a single
        login or a list of comma-separated logins). The parameter is an array of structures {Lang='??', Text='...'}.
        If no matching language is found, the last text in the array is used. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'ChatSendToLanguage')(*data))
        return bool(getattr(self, 'ChatSendToLanguage')())

    def chatSendToLogin(self, *data) -> bool:
        """Send a text message to the client with the specified login. Login can be a single
        login or a list of comma-separated logins. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'ChatSendToLogin')(*data))
        return bool(getattr(self, 'ChatSendToLogin')())

    def chatSendToId(self, *data) -> bool:
        """Send a text message to the client with the specified PlayerId. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'ChatSendToId')(*data))
        return bool(getattr(self, 'ChatSendToId')())

    def getChatLines(self, *data) -> ChatLinesList:
        """Returns the last chat lines. Maximum of 40 lines. Only available to Admin."""
        if len(data) > 0:
            return [ChatLine(*result.values()) for result in getattr(self, 'GetChatLines')(*data)]
        return [ChatLine(*result.values()) for result in getattr(self, 'GetChatLines')()]

    def chatEnableManualRouting(self, *data) -> bool:
        """The chat messages are no longer dispatched to the players, they only go to the rpc callback
        and the controller has to manually forward them. The second (optional) parameter allows all messages from
        the server to be automatically forwarded. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'ChatEnableManualRouting')(*data))
        return bool(getattr(self, 'ChatEnableManualRouting')())

    def chatForwardToLogin(self, *data) -> bool:
        """(Text, SenderLogin, DestLogin) Send a text message to the specified DestLogin (or everybody if empty)
        on behalf of SenderLogin. DestLogin can be a single login or a list of comma-separated logins.
        Only available if manual routing is enabled. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'ChatForwardToLogin')(*data))
        return bool(getattr(self, 'ChatForwardToLogin')())

    def sendNotice(self, *data) -> bool:
        """Display a notice on all clients. The parameters are the text message to display, and the login
        of the avatar to display next to it (or '' for no avatar), and an optional 'max duration'
        in seconds (default: 3). Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SendNotice')(*data))
        return bool(getattr(self, 'SendNotice')())

    def sendNoticeToId(self, *data) -> bool:
        """Display a notice on the client with the specified UId. The parameters are the Uid of the client
        to whom the notice is sent, the text message to display, and the UId of the avatar to display
        next to it (or '255' for no avatar), and an optional 'max duration' in seconds (default: 3).
        Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SendNoticeToId')(*data))
        return bool(getattr(self, 'SendNoticeToId')())

    def sendNoticeToLogin(self, *data) -> bool:
        """Display a notice on the client with the specified login. The parameters are the login of the client
        to whom the notice is sent, the text message to display, and the login of the avatar to display
        next to it (or '' for no avatar), and an optional 'max duration' in seconds (default: 3).
        Login can be a single login or a list of comma-separated logins.  Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SendNoticeToLogin')(*data))
        return bool(getattr(self, 'SendNoticeToLogin')())

    def sendDisplayManialinkPage(self, *data) -> bool:
        """Display a manialink page on all clients. The parameters are the xml description of the page to display,
        a timeout to autohide it (0 = permanent), and a boolean to indicate whether the page must be hidden
        as soon as the user clicks on a page option. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SendDisplayManialinkPage')(*data))
        return bool(getattr(self, 'SendDisplayManialinkPage')())

    def sendDisplayManialinkPageToId(self, *data) -> bool:
        """Display a manialink page on the client with the specified UId. The first parameter is the UId of the player,
        the other are identical to 'SendDisplayManialinkPage'. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SendDisplayManialinkPageToId')(*data))
        return bool(getattr(self, 'SendDisplayManialinkPageToId')())

    def sendDisplayManialinkPageToLogin(self, *data) -> bool:
        """Display a manialink page on the client with the specified login. The first parameter is the
        login of the player, the other are identical to 'SendDisplayManialinkPage'.
        Login can be a single login or a list of comma-separated logins. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SendDisplayManialinkPageToLogin')(*data))
        return bool(getattr(self, 'SendDisplayManialinkPageToLogin')())

    def sendHideManialinkPage(self, *data) -> bool:
        """Hide the displayed manialink page on all clients. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SendHideManialinkPage')(*data))
        return bool(getattr(self, 'SendHideManialinkPage')())

    def sendHideManialinkPageToId(self, *data) -> bool:
        """Hide the displayed manialink page on the client with the specified UId. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SendHideManialinkPageToId')(*data))
        return bool(getattr(self, 'SendHideManialinkPageToId')())

    def sendHideManialinkPageToLogin(self, *data) -> bool:
        """Hide the displayed manialink page on the client with the specified login. Login can be a single
        login or a list of comma-separated logins. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SendHideManialinkPageToLogin')(*data))
        return bool(getattr(self, 'SendHideManialinkPageToLogin')())

    def getManialinkPageAnswers(self, *data) -> ManialinkPageAnswersList:
        """Returns the latest results from the current manialink page, as an array of structs {string Login,
        int PlayerId, int Result} Result==0 -> no answer, Result>0.... -> answer from the player."""
        if len(data) > 0:
            return [ManialinkPageAnswers(*result.values()) for result in getattr(self, 'GetManialinkPageAnswers')(*data)]
        return [ManialinkPageAnswers(*result.values()) for result in getattr(self, 'GetManialinkPageAnswers')()]

    def kick(self, *data) -> bool:
        """Kick the player with the specified login, with an optional message. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'Kick')(*data))
        return bool(getattr(self, 'Kick')())

    def kickId(self, *data) -> bool:
        """Kick the player with the specified PlayerId, with an optional message. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'KickId')(*data))
        return bool(getattr(self, 'KickId')())

    def ban(self, *data) -> bool:
        """Ban the player with the specified login, with an optional message. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'Ban')(*data))
        return bool(getattr(self, 'Ban')())

    def banAndBlackList(self, *data) -> bool:
        """Ban the player with the specified login, with a message. Add it to the black list,
        and optionally save the new list. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'BanAndBlackList')(*data))
        return bool(getattr(self, 'BanAndBlackList')())

    def banId(self, *data) -> bool:
        """Ban the player with the specified PlayerId, with an optional message. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'BanId')(*data))
        return bool(getattr(self, 'BanId')())

    def unBan(self, *data) -> bool:
        """Unban the player with the specified client name. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'UnBan')(*data))
        return bool(getattr(self, 'UnBan')())

    def cleanBanList(self, *data) -> bool:
        """Clean the ban list of the server. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'CleanBanList')(*data))
        return bool(getattr(self, 'CleanBanList')())

    def getBanList(self, *data) -> BanList:
        """Returns the list of banned players. This method takes two parameters. The first parameter
        specifies the maximum number of infos to be returned, and the second one the starting index in the list.
        The list is an array of structures. Each structure contains the following fields :
        Login, ClientName and IPAddress."""
        if len(data) > 0:
            return [BanItem(*result.values()) for result in getattr(self, 'GetBanList')(*data)]
        return [BanItem(*result.values()) for result in getattr(self, 'GetBanList')()]

    def blackList(self, *data) -> bool:
        """Blacklist the player with the specified login. Only available to SuperAdmin."""
        if len(data) > 0:
            return bool(getattr(self, 'BlackList')(*data))
        return bool(getattr(self, 'BlackList')())

    def blackListId(self, *data) -> bool:
        """Blacklist the player with the specified PlayerId. Only available to SuperAdmin."""
        if len(data) > 0:
            return bool(getattr(self, 'BlackListId')(*data))
        return bool(getattr(self, 'BlackListId')())

    def unBlackList(self, *data) -> bool:
        """UnBlackList the player with the specified login. Only available to SuperAdmin."""
        if len(data) > 0:
            return bool(getattr(self, 'UnBlackList')(*data))
        return bool(getattr(self, 'UnBlackList')())

    def cleanBlackList(self, *data) -> bool:
        """Clean the blacklist of the server. Only available to SuperAdmin."""
        if len(data) > 0:
            return bool(getattr(self, 'CleanBlackList')(*data))
        return bool(getattr(self, 'CleanBlackList')())

    def getBlackList(self, *data) -> BlackList:
        """Returns the list of blacklisted players. This method takes two parameters.
        The first parameter specifies the maximum number of infos to be returned,
        and the second one the starting index in the list. The list is an array of structures.
        Each structure contains the following fields : Login."""
        if len(data) > 0:
            return [BlackListItem(*result.values()) for result in getattr(self, 'GetBlackList')(*data)]
        return [BlackListItem(*result.values()) for result in getattr(self, 'GetBlackList')()]

    def loadBlackList(self, *data) -> bool:
        """Load the black list file with the specified file name. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'LoadBlackList')(*data))
        return bool(getattr(self, 'LoadBlackList')())

    def saveBlackList(self, *data) -> bool:
        """Save the black list in the file with specified file name. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SaveBlackList')(*data))
        return bool(getattr(self, 'SaveBlackList')())

    def addGuest(self, *data) -> bool:
        """Add the player with the specified login on the guest list. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'AddGuest')(*data))
        return bool(getattr(self, 'AddGuest')())

    def addGuestId(self, *data) -> bool:
        """Add the player with the specified PlayerId on the guest list. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'AddGuestId')(*data))
        return bool(getattr(self, 'AddGuestId')())

    def removeGuest(self, *data) -> bool:
        """Remove the player with the specified login from the guest list. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'RemoveGuest')(*data))
        return bool(getattr(self, 'RemoveGuest')())

    def removeGuestId(self, *data) -> bool:
        """Remove the player with the specified PlayerId from the guest list. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'RemoveGuestId')(*data))
        return bool(getattr(self, 'RemoveGuestId')())

    def cleanGuestList(self, *data) -> bool:
        """Clean the guest list of the server. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'CleanGuestList')(*data))
        return bool(getattr(self, 'CleanGuestList')())

    def getGuestList(self, *data) -> GuestList:
        """Returns the list of players on the guest list. This method takes two parameters.
        The first parameter specifies the maximum number of infos to be returned, and the second one
        the starting index in the list. The list is an array of structures.
        Each structure contains the following fields : Login."""
        if len(data) > 0:
            return [GuestListItem(*result.values()) for result in getattr(self, 'GetGuestList')(*data)]
        return [GuestListItem(*result.values()) for result in getattr(self, 'GetGuestList')()]

    def loadGuestList(self, *data) -> bool:
        """Load the guest list file with the specified file name. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'LoadGuestList')(*data))
        return bool(getattr(self, 'LoadGuestList')())

    def saveGuestList(self, *data) -> bool:
        """Save the guest list in the file with specified file name. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SaveGuestList')(*data))
        return bool(getattr(self, 'SaveGuestList')())

    def setBuddyNotification(self, *data) -> bool:
        """Sets whether buddy notifications should be sent in the chat. login is the login of the player,
        or '' for global setting, and enabled is the value. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SetBuddyNotification')(*data))
        return bool(getattr(self, 'SetBuddyNotification')())

    def getBuddyNotification(self, *data) -> bool:
        """Gets whether buddy notifications are enabled for login, or '' to get the global setting."""
        if len(data) > 0:
            return bool(getattr(self, 'GetBuddyNotification')(*data))
        return bool(getattr(self, 'GetBuddyNotification')())

    def writeFile(self, *data) -> bool:
        """Write the data to the specified file. The filename is relative to the Tracks path.
        Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'WriteFile')(*data))
        return bool(getattr(self, 'WriteFile')())

    def tunnelSendDataToId(self, *data) -> bool:
        """Send the data to the specified player. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'TunnelSendDataToId')(*data))
        return bool(getattr(self, 'TunnelSendDataToId')())

    def tunnelSendDataToLogin(self, *data) -> bool:
        """Send the data to the specified player. Login can be a single login or a list of comma-separated logins.
        Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'TunnelSendDataToLogin')(*data))
        return bool(getattr(self, 'TunnelSendDataToLogin')())

    def echo(self, *data) -> bool:
        """Just log the parameters and invoke a callback. Can be used to talk to other xmlrpc clients connected,
        or to make custom votes. If used in a callvote, the first parameter will be used as the vote
        message on the clients. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'Echo')(*data))
        return bool(getattr(self, 'Echo')())

    def ignore(self, *data) -> bool:
        """Ignore the player with the specified login. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'Ignore')(*data))
        return bool(getattr(self, 'Ignore')())

    def ignoreId(self, *data) -> bool:
        """Ignore the player with the specified PlayerId. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'IgnoreId')(*data))
        return bool(getattr(self, 'IgnoreId')())

    def unIgnore(self, *data) -> bool:
        """Unignore the player with the specified login. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'UnIgnore')(*data))
        return bool(getattr(self, 'UnIgnore')())

    def unIgnoreId(self, *data) -> bool:
        """Unignore the player with the specified PlayerId. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'UnIgnoreId')(*data))
        return bool(getattr(self, 'UnIgnoreId')())

    def cleanIgnoreList(self, *data) -> bool:
        """Clean the ignore list of the server. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'CleanIgnoreList')(*data))
        return bool(getattr(self, 'CleanIgnoreList')())

    def getIgnoreList(self, *data) -> IgnoreList:
        """Returns the list of ignored players. This method takes two parameters.
        The first parameter specifies the maximum number of infos to be returned, and the second one
        the starting index in the list. The list is an array of structures. Each structure contains
        the following fields : Login."""
        if len(data) > 0:
            return [IgnoreListItem(*result.values()) for result in getattr(self, 'GetIgnoreList')(*data)]
        return [IgnoreListItem(*result.values()) for result in getattr(self, 'GetIgnoreList')()]

    def pay(self, *data) -> int:
        """Pay coppers from the server account to a player, returns the BillId.
        This method takes three parameters: Login of the payee, Coppers to pay and a Label to send with the payment.
        The creation of the transaction itself may cost coppers, so you need to have coppers on the server account.
        Only available to Admin."""
        if len(data) > 0:
            return int(getattr(self, 'Pay')(*data))
        return int(getattr(self, 'Pay')())

    def sendBill(self, *data) -> int:
        """Create a bill, send it to a player, and return the BillId. This method takes four parameters:
        LoginFrom of the payer, Coppers the player has to pay, Label of the transaction and an optional
        LoginTo of the payee (if empty string, then the server account is used).
        The creation of the transaction itself may cost coppers, so you need to have coppers on the server account.
        Only available to Admin."""
        if len(data) > 0:
            return int(getattr(self, 'SendBill')(*data))
        return int(getattr(self, 'SendBill')())

    def getBillState(self, *data) -> BillState:
        """Returns the current state of a bill. This method takes one parameter, the BillId.
        Returns a struct containing State, StateName and TransactionId.
        Possible enum values are: CreatingTransaction, Issued, ValidatingPayement, Payed, Refused, Error."""
        if len(data) > 0:
            return BillState(*getattr(self, 'GetBillState')(*data).values())
        return BillState(*getattr(self, 'GetBillState')().values())

    def getServerCoppers(self, *data) -> int:
        """Returns the current number of coppers on the server account."""
        if len(data) > 0:
            return int(getattr(self, 'GetServerCoppers')(*data))
        return int(getattr(self, 'GetServerCoppers')())

    def getSystemInfo(self, *data) -> SystemInfo:
        """Get some system infos, including connection rates (in kbps)."""
        if len(data) > 0:
            return SystemInfo(*getattr(self, 'GetSystemInfo')(*data).values())
        return SystemInfo(*getattr(self, 'GetSystemInfo')().values())

    def setConnectionRates(self, *data) -> bool:
        """Set the download and upload rates (in kbps)."""
        if len(data) > 0:
            return bool(getattr(self, 'SetConnectionRates')(*data))
        return bool(getattr(self, 'SetConnectionRates')())

    def setServerName(self, *data) -> bool:
        """Set a new server name in utf8 format. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SetServerName')(*data))
        return bool(getattr(self, 'SetServerName')())

    def getServerName(self, *data) -> str:
        """Get the server name in utf8 format."""
        if len(data) > 0:
            return str(getattr(self, 'GetServerName')(*data))
        return str(getattr(self, 'GetServerName')())

    def setServerComment(self, *data) -> bool:
        """Set a new server comment in utf8 format. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SetServerComment')(*data))
        return bool(getattr(self, 'SetServerComment')())

    def getServerComment(self, *data) -> str:
        """Get the server comment in utf8 format."""
        if len(data) > 0:
            return str(getattr(self, 'GetServerComment')(*data))
        return str(getattr(self, 'GetServerComment')())

    def setHideServer(self, *data) -> bool:
        """Set whether the server should be hidden from the public server list
        (0 = visible, 1 = always hidden, 2 = hidden from nations). Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SetHideServer')(*data))
        return bool(getattr(self, 'SetHideServer')())

    def getHideServer(self, *data) -> int:
        """Get whether the server wants to be hidden from the public server list."""
        if len(data) > 0:
            return int(getattr(self, 'GetHideServer')(*data))
        return int(getattr(self, 'GetHideServer')())

    def isRelayServer(self, *data) -> bool:
        """Returns true if this is a relay server."""
        if len(data) > 0:
            return bool(getattr(self, 'IsRelayServer')(*data))
        return bool(getattr(self, 'IsRelayServer')())

    def setServerPassword(self, *data) -> bool:
        """Set a new password for the server. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SetServerPassword')(*data))
        return bool(getattr(self, 'SetServerPassword')())

    def getServerPassword(self, *data) -> str:
        """Get the server password if called as Admin or Super Admin, else returns if a password is needed or not."""
        if len(data) > 0:
            return str(getattr(self, 'GetServerPassword')(*data))
        return str(getattr(self, 'GetServerPassword')())

    def setServerPasswordForSpectator(self, *data) -> bool:
        """Set a new password for the spectator mode. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SetServerPasswordForSpectator')(*data))
        return bool(getattr(self, 'SetServerPasswordForSpectator')())

    def getServerPasswordForSpectator(self, *data) -> str:
        """Get the password for spectator mode if called as Admin or Super Admin, else returns if a password
        is needed or not."""
        if len(data) > 0:
            return str(getattr(self, 'GetServerPasswordForSpectator')(*data))
        return str(getattr(self, 'GetServerPasswordForSpectator')())

    def setMaxPlayers(self, *data) -> bool:
        """Set a new maximum number of players. Only available to Admin. Requires a challenge restart to be
        taken into account."""
        if len(data) > 0:
            return bool(getattr(self, 'SetMaxPlayers')(*data))
        return bool(getattr(self, 'SetMaxPlayers')())

    def getMaxPlayers(self, *data) -> StateValue:
        """Get the current and next maximum number of players allowed on server. The struct returned contains
        two fields CurrentValue and NextValue."""
        if len(data) > 0:
            return StateValue(*getattr(self, 'GetMaxPlayers')(*data).values())
        return StateValue(*getattr(self, 'GetMaxPlayers')().values())

    def setMaxSpectators(self, *data) -> bool:
        """Set a new maximum number of Spectators. Only available to Admin. Requires a challenge restart to be
        taken into account."""
        if len(data) > 0:
            return bool(getattr(self, 'SetMaxSpectators')(*data))
        return bool(getattr(self, 'SetMaxSpectators')())

    def getMaxSpectators(self, *data) -> StateValue:
        """Get the current and next maximum number of Spectators allowed on server. The struct returned contains
        two fields CurrentValue and NextValue."""
        if len(data) > 0:
            return StateValue(*getattr(self, 'GetMaxSpectators')(*data).values())
        return StateValue(*getattr(self, 'GetMaxSpectators')().values())

    def enableP2PUpload(self, *data) -> bool:
        """Enable or disable peer-to-peer upload from server. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'EnableP2PUpload')(*data))
        return bool(getattr(self, 'EnableP2PUpload')())

    def isP2PUpload(self, *data) -> bool:
        """Returns if the peer-to-peer upload from server is enabled."""
        if len(data) > 0:
            return bool(getattr(self, 'IsP2PUpload')(*data))
        return bool(getattr(self, 'IsP2PUpload')())

    def enableP2PDownload(self, *data) -> bool:
        """Enable or disable peer-to-peer download for server. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'EnableP2PDownload')(*data))
        return bool(getattr(self, 'EnableP2PDownload')())

    def isP2PDownload(self, *data) -> bool:
        """Returns if the peer-to-peer download for server is enabled."""
        if len(data) > 0:
            return bool(getattr(self, 'IsP2PDownload')(*data))
        return bool(getattr(self, 'IsP2PDownload')())

    def allowChallengeDownload(self, *data) -> bool:
        """Allow clients to download challenges from the server. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'AllowChallengeDownload')(*data))
        return bool(getattr(self, 'AllowChallengeDownload')())

    def isChallengeDownloadAllowed(self, *data) -> bool:
        """Returns if clients can download challenges from the server."""
        if len(data) > 0:
            return bool(getattr(self, 'IsChallengeDownloadAllowed')(*data))
        return bool(getattr(self, 'IsChallengeDownloadAllowed')())

    def autoSaveReplays(self, *data) -> bool:
        """Enable the autosaving of all replays (vizualisable replays with all players, but not validable)
        on the server. Only available to SuperAdmin."""
        if len(data) > 0:
            return bool(getattr(self, 'AutoSaveReplays')(*data))
        return bool(getattr(self, 'AutoSaveReplays')())

    def autoSaveValidationReplays(self, *data) -> bool:
        """Enable the autosaving on the server of validation replays, every time a player makes a new time.
        Only available to SuperAdmin."""
        if len(data) > 0:
            return bool(getattr(self, 'AutoSaveValidationReplays')(*data))
        return bool(getattr(self, 'AutoSaveValidationReplays')())

    def isAutoSaveReplaysEnabled(self, *data) -> bool:
        """Returns if autosaving of all replays is enabled on the server."""
        if len(data) > 0:
            return bool(getattr(self, 'IsAutoSaveReplaysEnabled')(*data))
        return bool(getattr(self, 'IsAutoSaveReplaysEnabled')())

    def isAutoSaveValidationReplaysEnabled(self, *data) -> bool:
        """Returns if autosaving of validation replays is enabled on the server."""
        if len(data) > 0:
            return bool(getattr(self, 'IsAutoSaveValidationReplaysEnabled')(*data))
        return bool(getattr(self, 'IsAutoSaveValidationReplaysEnabled')())

    def saveCurrentReplay(self, *data) -> bool:
        """Saves the current replay (vizualisable replays with all players, but not validable).
        Pass a filename, or '' for an automatic filename. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SaveCurrentReplay')(*data))
        return bool(getattr(self, 'SaveCurrentReplay')())

    def saveBestGhostsReplay(self, *data) -> bool:
        """Saves a replay with the ghost of all the players' best race. First parameter is the login of the player
        (or '' for all players), Second parameter is the filename, or '' for an automatic filename.
        Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SaveBestGhostsReplay')(*data))
        return bool(getattr(self, 'SaveBestGhostsReplay')())

    # def getValidationReplay(self, *data) -> base64 GetValidationReplay:
    #     '''Returns a replay containing the data needed to validate the current best time of the player.
    #     The parameter is the login of the player.'''
    #     if len(data) > 0:
    #         return ValidationReplay(*getattr(self, 'GetValidationReplay')(*data).values())
    #     return ValidationReplay(*getattr(self, 'GetValidationReplay')().values())

    def setLadderMode(self, *data) -> bool:
        """Set a new ladder mode between ladder disabled (0) and forced (1). Only available to Admin.
        Requires a challenge restart to be taken into account."""
        if len(data) > 0:
            return bool(getattr(self, 'SetLadderMode')(*data))
        return bool(getattr(self, 'SetLadderMode')())

    def getLadderMode(self, *data) -> StateValue:
        """Get the current and next ladder mode on server. The struct returned contains two fields CurrentValue
        and NextValue."""
        if len(data) > 0:
            return StateValue(*getattr(self, 'GetLadderMode')(*data).values())
        return StateValue(*getattr(self, 'GetLadderMode')().values())

    def getLadderServerLimits(self, *data) -> LadderServerLimits:
        """Get the ladder points limit for the players allowed on this server. The struct returned contains
        two fields LadderServerLimitMin and LadderServerLimitMax."""
        if len(data) > 0:
            return LadderServerLimits(*getattr(self, 'GetLadderServerLimits')(*data).values())
        return LadderServerLimits(*getattr(self, 'GetLadderServerLimits')().values())

    def setVehicleNetQuality(self, *data) -> bool:
        """Set the network vehicle quality to Fast (0) or High (1). Only available to Admin.
        Requires a challenge restart to be taken into account."""
        if len(data) > 0:
            return bool(getattr(self, 'SetVehicleNetQuality')(*data))
        return bool(getattr(self, 'SetVehicleNetQuality')())

    def getVehicleNetQuality(self, *data) -> StateValue:
        """Get the current and next network vehicle quality on server. The struct returned contains two fields
        CurrentValue and NextValue."""
        if len(data) > 0:
            return StateValue(*getattr(self, 'GetVehicleNetQuality')(*data).values())
        return StateValue(*getattr(self, 'GetVehicleNetQuality')().values())

    def setServerOptions(self, *data) -> bool:
        """Set new server options using the struct passed as parameters. This struct must contain the following fields:
        Name, Comment, Password, PasswordForSpectator, NextMaxPlayers, NextMaxSpectators, IsP2PUpload, IsP2PDownload,
        NextLadderMode, NextVehicleNetQuality, NextCallVoteTimeOut, CallVoteRatio, AllowChallengeDownload,
        AutoSaveReplays, and optionally for forever: RefereePassword, RefereeMode, AutoSaveValidationReplays,
        HideServer, UseChangingValidationSeed. Only available to Admin. A change of NextMaxPlayers, NextMaxSpectators,
        NextLadderMode, NextVehicleNetQuality, NextCallVoteTimeOut or UseChangingValidationSeed
        requires a challenge restart to be taken into account."""
        if len(data) > 0:
            return bool(getattr(self, 'SetServerOptions')(*data))
        return bool(getattr(self, 'SetServerOptions')())

    def getServerOptions(self, *data) -> ServerOptions:
        """Optional parameter for compatibility: struct version (0 = united, 1 = forever).
        Returns a struct containing the server options: Name, Comment, Password, PasswordForSpectator,
        CurrentMaxPlayers, NextMaxPlayers, CurrentMaxSpectators, NextMaxSpectators, IsP2PUpload, IsP2PDownload,
        CurrentLadderMode, NextLadderMode, CurrentVehicleNetQuality, NextVehicleNetQuality, CurrentCallVoteTimeOut,
        NextCallVoteTimeOut, CallVoteRatio, AllowChallengeDownload and AutoSaveReplays, and additionally for forever:
        RefereePassword, RefereeMode, AutoSaveValidationReplays, HideServer, CurrentUseChangingValidationSeed,
        NextUseChangingValidationSeed."""
        if len(data) > 0:
            return ServerOptions(*getattr(self, 'GetServerOptions')(*data).values())
        return ServerOptions(*getattr(self, 'GetServerOptions')().values())

    def setServerPackMask(self, *data) -> bool:
        """Defines the packmask of the server. Can be 'United', 'Nations', 'Sunrise', 'Original', or any of the
        environment names. (Only challenges matching the packmask will be allowed on the server, so that player
        connecting to it know what to expect.) Only available when the server is stopped. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SetServerPackMask')(*data))
        return bool(getattr(self, 'SetServerPackMask')())

    def getServerPackMask(self, *data) -> str:
        """Get the packmask of the server."""
        if len(data) > 0:
            return str(getattr(self, 'GetServerPackMask')(*data))
        return str(getattr(self, 'GetServerPackMask')())

    def setForcedMods(self, *data) -> bool:
        """Set the mods to apply on the clients. Parameters: Override, if true even the challenges with a mod will
        be overridden by the server setting; and Mods, an array of structures [{EnvName, Url}, ...].
        Requires a challenge restart to be taken into account. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SetForcedMods')(*data))
        return bool(getattr(self, 'SetForcedMods')())

    def getForcedMods(self, *data) -> ForcedMods:
        """Get the mods settings."""
        if len(data) > 0:
            return ForcedMods(*getattr(self, 'GetForcedMods')(*data).values())
        return ForcedMods(*getattr(self, 'GetForcedMods')().values())

    def setForcedMusic(self, *data) -> bool:
        """Set the music to play on the clients. Parameters: Override, if true even the challenges with a
        custom music will be overridden by the server setting, and a UrlOrFileName for the music. Requires a
        challenge restart to be taken into account. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SetForcedMusic')(*data))
        return bool(getattr(self, 'SetForcedMusic')())

    def getForcedMusic(self, *data) -> ForcedMusic:
        """Get the music setting."""
        if len(data) > 0:
            return ForcedMusic(*getattr(self, 'GetForcedMusic')(*data).values())
        return ForcedMusic(*getattr(self, 'GetForcedMusic')().values())

    def setForcedSkins(self, *data) -> bool:
        """Defines a list of remappings for player skins. It expects a list of structs Orig, Name, Checksum, Url.
        Orig is the name of the skin to remap, or '*' for any other. Name, Checksum, Url define the skin to use.
        (They are optional, you may set value '' for any of those. All 3 null means same as Orig). Will only affect
        players connecting after the value is set. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SetForcedSkins')(*data))
        return bool(getattr(self, 'SetForcedSkins')())

    def getForcedSkins(self, *data) -> ForcedSkinsList:
        """Get the current forced skins."""
        if len(data) > 0:
            return [ForcedSkin(*result.values()) for result in getattr(self, 'GetForcedSkins')(*data)]
        return [ForcedSkin(*result.values()) for result in getattr(self, 'GetForcedSkins')()]

    def getLastConnectionErrorMessage(self, *data) -> str:
        """Returns the last error message for an internet connection. Only available to Admin."""
        if len(data) > 0:
            return str(getattr(self, 'GetLastConnectionErrorMessage')(*data))
        return str(getattr(self, 'GetLastConnectionErrorMessage')())

    def setRefereePassword(self, *data) -> bool:
        """Set a new password for the referee mode. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SetRefereePassword')(*data))
        return bool(getattr(self, 'SetRefereePassword')())

    def getRefereePassword(self, *data) -> str:
        """Get the password for referee mode if called as Admin or Super Admin, else returns if a password is
        needed or not."""
        if len(data) > 0:
            return str(getattr(self, 'GetRefereePassword')(*data))
        return str(getattr(self, 'GetRefereePassword')())

    def setRefereeMode(self, *data) -> bool:
        """Set the referee validation mode. 0 = validate the top3 players, 1 = validate all players.
        Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SetRefereeMode')(*data))
        return bool(getattr(self, 'SetRefereeMode')())

    def getRefereeMode(self, *data) -> int:
        """Get the referee validation mode."""
        if len(data) > 0:
            return int(getattr(self, 'GetRefereeMode')(*data))
        return int(getattr(self, 'GetRefereeMode')())

    def setUseChangingValidationSeed(self, *data) -> bool:
        """Set whether the game should use a variable validation seed or not. Only available to Admin.
        Requires a challenge restart to be taken into account."""
        if len(data) > 0:
            return bool(getattr(self, 'SetUseChangingValidationSeed')(*data))
        return bool(getattr(self, 'SetUseChangingValidationSeed')())

    def getUseChangingValidationSeed(self, *data) -> StateValue:
        """Get the current and next value of UseChangingValidationSeed. The struct returned contains two fields
        CurrentValue and NextValue."""
        if len(data) > 0:
            return StateValue(*getattr(self, 'GetUseChangingValidationSeed')(*data).values())
        return StateValue(*getattr(self, 'GetUseChangingValidationSeed')().values())

    def setWarmUp(self, *data) -> bool:
        """Sets whether the server is in warm-up phase or not. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SetWarmUp')(*data))
        return bool(getattr(self, 'SetWarmUp')())

    def getWarmUp(self, *data) -> bool:
        """Returns whether the server is in warm-up phase."""
        if len(data) > 0:
            return bool(getattr(self, 'GetWarmUp')(*data))
        return bool(getattr(self, 'GetWarmUp')())

    def challengeRestart(self, *data) -> bool:
        """Restarts the challenge, with an optional boolean parameter DontClearCupScores (only available in cup mode).
        Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'ChallengeRestart')(*data))
        return bool(getattr(self, 'ChallengeRestart')())

    def restartChallenge(self, *data) -> bool:
        """Restarts the challenge, with an optional boolean parameter DontClearCupScores (only available in cup mode).
        Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'RestartChallenge')(*data))
        return bool(getattr(self, 'RestartChallenge')())

    def nextChallenge(self, *data) -> bool:
        """Switch to next challenge, with an optional boolean parameter DontClearCupScores (only available in cup mode).
        Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'NextChallenge')(*data))
        return bool(getattr(self, 'NextChallenge')())

    def stopServer(self, *data) -> bool:
        """Stop the server. Only available to SuperAdmin."""
        if len(data) > 0:
            return bool(getattr(self, 'StopServer')(*data))
        return bool(getattr(self, 'StopServer')())

    def forceEndRound(self, *data) -> bool:
        """In Rounds or Laps mode, force the end of round without waiting for all players to giveup/finish.
        Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'ForceEndRound')(*data))
        return bool(getattr(self, 'ForceEndRound')())

    def setGameInfos(self, *data) -> bool:
        """Set new game settings using the struct passed as parameters. This struct must contain the following fields :
        GameMode, ChatTime, RoundsPointsLimit, RoundsUseNewRules, RoundsForcedLaps, TimeAttackLimit,
        TimeAttackSynchStartPeriod, TeamPointsLimit, TeamMaxPoints, TeamUseNewRules, LapsNbLaps, LapsTimeLimit,
        FinishTimeout, and optionally: AllWarmUpDuration, DisableRespawn, ForceShowAllOpponents,
        RoundsPointsLimitNewRules, TeamPointsLimitNewRules, CupPointsLimit, CupRoundsPerChallenge, CupNbWinners,
        CupWarmUpDuration. Only available to Admin. Requires a challenge restart to be taken into account."""
        if len(data) > 0:
            return bool(getattr(self, 'SetGameInfos')(*data))
        return bool(getattr(self, 'SetGameInfos')())

    def getCurrentGameInfo(self, *data) -> GameInfo:
        """Optional parameter for compatibility: struct version (0 = united, 1 = forever). Returns a struct containing
        the current game settings, ie: GameMode, ChatTime, NbChallenge, RoundsPointsLimit, RoundsUseNewRules,
        RoundsForcedLaps, TimeAttackLimit, TimeAttackSynchStartPeriod, TeamPointsLimit, TeamMaxPoints, TeamUseNewRules,
        LapsNbLaps, LapsTimeLimit, FinishTimeout, and additionally for version 1: AllWarmUpDuration, DisableRespawn,
        ForceShowAllOpponents, RoundsPointsLimitNewRules, TeamPointsLimitNewRules, CupPointsLimit,
        CupRoundsPerChallenge, CupNbWinners, CupWarmUpDuration."""
        if len(data) > 0:
            return GameInfo(*getattr(self, 'GetCurrentGameInfo')(*data).values())
        return GameInfo(*getattr(self, 'GetCurrentGameInfo')().values())

    def getNextGameInfo(self, *data) -> GameInfo:
        """Optional parameter for compatibility: struct version (0 = united, 1 = forever).
        Returns a struct containing the game settings for the next challenge, ie: GameMode, ChatTime, NbChallenge,
        RoundsPointsLimit, RoundsUseNewRules, RoundsForcedLaps, TimeAttackLimit, TimeAttackSynchStartPeriod,
        TeamPointsLimit, TeamMaxPoints, TeamUseNewRules, LapsNbLaps, LapsTimeLimit, FinishTimeout,
        and additionally for version 1: AllWarmUpDuration, DisableRespawn, ForceShowAllOpponents,
        RoundsPointsLimitNewRules, TeamPointsLimitNewRules, CupPointsLimit, CupRoundsPerChallenge, CupNbWinners,
        CupWarmUpDuration."""
        if len(data) > 0:
            return GameInfo(*getattr(self, 'GetNextGameInfo')(*data).values())
        return GameInfo(*getattr(self, 'GetNextGameInfo')().values())

    def getGameInfos(self, *data) -> StateValue:
        """Optional parameter for compatibility: struct version (0 = united, 1 = forever).
        Returns a struct containing two other structures, the first containing the current game settings and
        the second the game settings for next challenge. The first structure is named CurrentGameInfos and the
        second NextGameInfos."""
        if len(data) > 0:
            return StateValue(*getattr(self, 'GetGameInfos')(*data).values())
        return StateValue(*getattr(self, 'GetGameInfos')().values())

    def setGameMode(self, *data) -> bool:
        """Set a new game mode between Rounds (0), TimeAttack (1), Team (2), Laps (3), Stunts (4) and Cup (5).
        Only available to Admin. Requires a challenge restart to be taken into account."""
        if len(data) > 0:
            return bool(getattr(self, 'SetGameMode')(*data))
        return bool(getattr(self, 'SetGameMode')())

    def getGameMode(self, *data) -> int:
        """Get the current game mode."""
        if len(data) > 0:
            return int(getattr(self, 'GetGameMode')(*data))
        return int(getattr(self, 'GetGameMode')())

    def setChatTime(self, *data) -> bool:
        """Set a new chat time value in milliseconds (actually 'chat time' is the duration of the end race podium,
        0 means no podium displayed.). Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SetChatTime')(*data))
        return bool(getattr(self, 'SetChatTime')())

    def getChatTime(self, *data) -> StateValue:
        """Get the current and next chat time. The struct returned contains two fields CurrentValue and NextValue."""
        if len(data) > 0:
            return StateValue(*getattr(self, 'GetChatTime')(*data).values())
        return StateValue(*getattr(self, 'GetChatTime')().values())

    def setFinishTimeout(self, *data) -> bool:
        """Set a new finish timeout (for rounds/laps mode) value in milliseconds. 0 means default.
        1 means adaptative to the duration of the challenge. Only available to Admin.
        Requires a challenge restart to be taken into account."""
        if len(data) > 0:
            return bool(getattr(self, 'SetFinishTimeout')(*data))
        return bool(getattr(self, 'SetFinishTimeout')())

    def getFinishTimeout(self, *data) -> StateValue:
        """Get the current and next FinishTimeout. The struct returned contains two fields CurrentValue and
        NextValue."""
        if len(data) > 0:
            return StateValue(*getattr(self, 'GetFinishTimeout')(*data).values())
        return StateValue(*getattr(self, 'GetFinishTimeout')().values())

    def setAllWarmUpDuration(self, *data) -> bool:
        """Set whether to enable the automatic warm-up phase in all modes. 0 = no, otherwise it's the duration
        of the phase, expressed in number of rounds (in rounds/team mode), or in number of times the gold medal
        time (other modes). Only available to Admin. Requires a challenge restart to be taken into account."""
        if len(data) > 0:
            return bool(getattr(self, 'SetAllWarmUpDuration')(*data))
        return bool(getattr(self, 'SetAllWarmUpDuration')())

    def getAllWarmUpDuration(self, *data) -> StateValue:
        """Get whether the automatic warm-up phase is enabled in all modes. The struct returned contains two
        fields CurrentValue and NextValue."""
        if len(data) > 0:
            return StateValue(*getattr(self, 'GetAllWarmUpDuration')(*data).values())
        return StateValue(*getattr(self, 'GetAllWarmUpDuration')().values())

    def setDisableRespawn(self, *data) -> bool:
        """Set whether to disallow players to respawn. Only available to Admin. Requires a challenge restart to
        be taken into account."""
        if len(data) > 0:
            return bool(getattr(self, 'SetDisableRespawn')(*data))
        return bool(getattr(self, 'SetDisableRespawn')())

    def getDisableRespawn(self, *data) -> StateValue:
        """Get whether players are disallowed to respawn. The struct returned contains two fields CurrentValue
        and NextValue."""
        if len(data) > 0:
            return StateValue(*getattr(self, 'GetDisableRespawn')(*data).values())
        return StateValue(*getattr(self, 'GetDisableRespawn')().values())

    def setForceShowAllOpponents(self, *data) -> bool:
        """Set whether to override the players preferences and always display all opponents (0=no override,
        1=show all, other value=minimum number of opponents). Only available to Admin. Requires a challenge restart
        to be taken into account."""
        if len(data) > 0:
            return bool(getattr(self, 'SetForceShowAllOpponents')(*data))
        return bool(getattr(self, 'SetForceShowAllOpponents')())

    def getForceShowAllOpponents(self, *data) -> StateValue:
        """Get whether players are forced to show all opponents. The struct returned contains two fields CurrentValue
        and NextValue."""
        if len(data) > 0:
            return StateValue(*getattr(self, 'GetForceShowAllOpponents')(*data).values())
        return StateValue(*getattr(self, 'GetForceShowAllOpponents')().values())

    def setTimeAttackLimit(self, *data) -> bool:
        """Set a new time limit for time attack mode. Only available to Admin. Requires a challenge restart to be
        taken into account."""
        if len(data) > 0:
            return bool(getattr(self, 'SetTimeAttackLimit')(*data))
        return bool(getattr(self, 'SetTimeAttackLimit')())

    def getTimeAttackLimit(self, *data) -> StateValue:
        """Get the current and next time limit for time attack mode. The struct returned contains two fields
        CurrentValue and NextValue."""
        if len(data) > 0:
            return StateValue(*getattr(self, 'GetTimeAttackLimit')(*data).values())
        return StateValue(*getattr(self, 'GetTimeAttackLimit')().values())

    def setTimeAttackSynchStartPeriod(self, *data) -> bool:
        """Set a new synchronized start period for time attack mode. Only available to Admin. Requires a challenge
        restart to be taken into account."""
        if len(data) > 0:
            return bool(getattr(self, 'SetTimeAttackSynchStartPeriod')(*data))
        return bool(getattr(self, 'SetTimeAttackSynchStartPeriod')())

    def getTimeAttackSynchStartPeriod(self, *data) -> StateValue:
        """Get the current and synchronized start period for time attack mode. The struct returned contains two
        fields CurrentValue and NextValue."""
        if len(data) > 0:
            return StateValue(*getattr(self, 'GetTimeAttackSynchStartPeriod')(*data).values())
        return StateValue(*getattr(self, 'GetTimeAttackSynchStartPeriod')().values())

    def setLapsTimeLimit(self, *data) -> bool:
        """Set a new time limit for laps mode. Only available to Admin. Requires a challenge restart to be taken
        into account."""
        if len(data) > 0:
            return bool(getattr(self, 'SetLapsTimeLimit')(*data))
        return bool(getattr(self, 'SetLapsTimeLimit')())

    def getLapsTimeLimit(self, *data) -> StateValue:
        """Get the current and next time limit for laps mode. The struct returned contains two fields CurrentValue
        and NextValue."""
        if len(data) > 0:
            return StateValue(*getattr(self, 'GetLapsTimeLimit')(*data).values())
        return StateValue(*getattr(self, 'GetLapsTimeLimit')().values())

    def setNbLaps(self, *data) -> bool:
        """Set a new number of laps for laps mode. Only available to Admin. Requires a challenge restart to be
        taken into account."""
        if len(data) > 0:
            return bool(getattr(self, 'SetNbLaps')(*data))
        return bool(getattr(self, 'SetNbLaps')())

    def getNbLaps(self, *data) -> StateValue:
        """Get the current and next number of laps for laps mode. The struct returned contains two fields
        CurrentValue and NextValue."""
        if len(data) > 0:
            return StateValue(*getattr(self, 'GetNbLaps')(*data).values())
        return StateValue(*getattr(self, 'GetNbLaps')().values())

    def setRoundForcedLaps(self, *data) -> bool:
        """Set a new number of laps for rounds mode (0 = default, use the number of laps from the challenges,
        otherwise forces the number of rounds for multilaps challenges). Only available to Admin. Requires a
        challenge restart to be taken into account."""
        if len(data) > 0:
            return bool(getattr(self, 'SetRoundForcedLaps')(*data))
        return bool(getattr(self, 'SetRoundForcedLaps')())

    def getRoundForcedLaps(self, *data) -> StateValue:
        """Get the current and next number of laps for rounds mode. The struct returned contains two fields
        CurrentValue and NextValue."""
        if len(data) > 0:
            return StateValue(*getattr(self, 'GetRoundForcedLaps')(*data).values())
        return StateValue(*getattr(self, 'GetRoundForcedLaps')().values())

    def setRoundPointsLimit(self, *data) -> bool:
        """Set a new points limit for rounds mode (value set depends on UseNewRulesRound). Only available to Admin.
        Requires a challenge restart to be taken into account."""
        if len(data) > 0:
            return bool(getattr(self, 'SetRoundPointsLimit')(*data))
        return bool(getattr(self, 'SetRoundPointsLimit')())

    def getRoundPointsLimit(self, *data) -> StateValue:
        """Get the current and next points limit for rounds mode (values returned depend on UseNewRulesRound).
        The struct returned contains two fields CurrentValue and NextValue."""
        if len(data) > 0:
            return StateValue(*getattr(self, 'GetRoundPointsLimit')(*data).values())
        return StateValue(*getattr(self, 'GetRoundPointsLimit')().values())

    def setRoundCustomPoints(self, *data) -> bool:
        """Set the points used for the scores in rounds mode. Points is an array of decreasing integers for the
        players from the first to last. And you can add an optional boolean to relax the constraint checking
        on the scores. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SetRoundCustomPoints')(*data))
        return bool(getattr(self, 'SetRoundCustomPoints')())

    def getRoundCustomPoints(self, *data) -> RoundCustomPointsList:
        """Gets the points used for the scores in rounds mode."""
        if len(data) > 0:
            return [RoundCustomPoints(*result.values()) for result in getattr(self, 'GetRoundCustomPoints')(*data)]
        return [RoundCustomPoints(*result.values()) for result in getattr(self, 'GetRoundCustomPoints')()]

    def setUseNewRulesRound(self, *data) -> bool:
        """Set if new rules are used for rounds mode. Only available to Admin. Requires a challenge restart to be
        taken into account."""
        if len(data) > 0:
            return bool(getattr(self, 'SetUseNewRulesRound')(*data))
        return bool(getattr(self, 'SetUseNewRulesRound')())

    def getUseNewRulesRound(self, *data) -> StateValue:
        """Get if the new rules are used for rounds mode (Current and next values). The struct returned contains
        two fields CurrentValue and NextValue."""
        if len(data) > 0:
            return StateValue(*getattr(self, 'GetUseNewRulesRound')(*data).values())
        return StateValue(*getattr(self, 'GetUseNewRulesRound')().values())

    def setTeamPointsLimit(self, *data) -> bool:
        """Set a new points limit for team mode (value set depends on UseNewRulesTeam). Only available to Admin.
        Requires a challenge restart to be taken into account."""
        if len(data) > 0:
            return bool(getattr(self, 'SetTeamPointsLimit')(*data))
        return bool(getattr(self, 'SetTeamPointsLimit')())

    def getTeamPointsLimit(self, *data) -> StateValue:
        """Get the current and next points limit for team mode (values returned depend on UseNewRulesTeam).
        The struct returned contains two fields CurrentValue and NextValue."""
        if len(data) > 0:
            return StateValue(*getattr(self, 'GetTeamPointsLimit')(*data).values())
        return StateValue(*getattr(self, 'GetTeamPointsLimit')().values())

    def setMaxPointsTeam(self, *data) -> bool:
        """Set a new number of maximum points per round for team mode. Only available to Admin. Requires a
        challenge restart to be taken into account."""
        if len(data) > 0:
            return bool(getattr(self, 'SetMaxPointsTeam')(*data))
        return bool(getattr(self, 'SetMaxPointsTeam')())

    def getMaxPointsTeam(self, *data) -> StateValue:
        """Get the current and next number of maximum points per round for team mode. The struct returned contains
        two fields CurrentValue and NextValue."""
        if len(data) > 0:
            return StateValue(*getattr(self, 'GetMaxPointsTeam')(*data).values())
        return StateValue(*getattr(self, 'GetMaxPointsTeam')().values())

    def setUseNewRulesTeam(self, *data) -> bool:
        """Set if new rules are used for team mode. Only available to Admin. Requires a challenge restart to be
        taken into account."""
        if len(data) > 0:
            return bool(getattr(self, 'SetUseNewRulesTeam')(*data))
        return bool(getattr(self, 'SetUseNewRulesTeam')())

    def getUseNewRulesTeam(self, *data) -> StateValue:
        """Get if the new rules are used for team mode (Current and next values). The struct returned contains
        two fields CurrentValue and NextValue."""
        if len(data) > 0:
            return StateValue(*getattr(self, 'GetUseNewRulesTeam')(*data).values())
        return StateValue(*getattr(self, 'GetUseNewRulesTeam')().values())

    def setCupPointsLimit(self, *data) -> bool:
        """Set the points needed for victory in Cup mode. Only available to Admin. Requires a challenge restart
        to be taken into account."""
        if len(data) > 0:
            return bool(getattr(self, 'SetCupPointsLimit')(*data))
        return bool(getattr(self, 'SetCupPointsLimit')())

    def getCupPointsLimit(self, *data) -> StateValue:
        """Get the points needed for victory in Cup mode. The struct returned contains two fields CurrentValue
        and NextValue."""
        if len(data) > 0:
            return StateValue(*getattr(self, 'GetCupPointsLimit')(*data).values())
        return StateValue(*getattr(self, 'GetCupPointsLimit')().values())

    def setCupRoundsPerChallenge(self, *data) -> bool:
        """Sets the number of rounds before going to next challenge in Cup mode. Only available to Admin.
        Requires a challenge restart to be taken into account."""
        if len(data) > 0:
            return bool(getattr(self, 'SetCupRoundsPerChallenge')(*data))
        return bool(getattr(self, 'SetCupRoundsPerChallenge')())

    def getCupRoundsPerChallenge(self, *data) -> StateValue:
        """Get the number of rounds before going to next challenge in Cup mode. The struct returned contains
        two fields CurrentValue and NextValue."""
        if len(data) > 0:
            return StateValue(*getattr(self, 'GetCupRoundsPerChallenge')(*data).values())
        return StateValue(*getattr(self, 'GetCupRoundsPerChallenge')().values())

    def setCupWarmUpDuration(self, *data) -> bool:
        """Set whether to enable the automatic warm-up phase in Cup mode. 0 = no, otherwise it's the duration of
        the phase, expressed in number of rounds. Only available to Admin. Requires a challenge restart to be
        taken into account."""
        if len(data) > 0:
            return bool(getattr(self, 'SetCupWarmUpDuration')(*data))
        return bool(getattr(self, 'SetCupWarmUpDuration')())

    def getCupWarmUpDuration(self, *data) -> StateValue:
        """Get whether the automatic warm-up phase is enabled in Cup mode. The struct returned contains two fields
        CurrentValue and NextValue."""
        if len(data) > 0:
            return StateValue(*getattr(self, 'GetCupWarmUpDuration')(*data).values())
        return StateValue(*getattr(self, 'GetCupWarmUpDuration')().values())

    def setCupNbWinners(self, *data) -> bool:
        """Set the number of winners to determine before the match is considered over. Only available to Admin.
        Requires a challenge restart to be taken into account."""
        if len(data) > 0:
            return bool(getattr(self, 'SetCupNbWinners')(*data))
        return bool(getattr(self, 'SetCupNbWinners')())

    def getCupNbWinners(self, *data) -> StateValue:
        """Get the number of winners to determine before the match is considered over. The struct returned contains
        two fields CurrentValue and NextValue."""
        if len(data) > 0:
            return StateValue(*getattr(self, 'GetCupNbWinners')(*data).values())
        return StateValue(*getattr(self, 'GetCupNbWinners')().values())

    def getCurrentChallengeIndex(self, *data) -> int:
        """Returns the current challenge index in the selection, or -1 if the challenge is no longer in the
        selection."""
        if len(data) > 0:
            return int(getattr(self, 'GetCurrentChallengeIndex')(*data))
        return int(getattr(self, 'GetCurrentChallengeIndex')())

    def getNextChallengeIndex(self, *data) -> int:
        """Returns the challenge index in the selection that will be played next (unless the current one is
        restarted...)"""
        if len(data) > 0:
            return int(getattr(self, 'GetNextChallengeIndex')(*data))
        return int(getattr(self, 'GetNextChallengeIndex')())

    def setNextChallengeIndex(self, *data) -> bool:
        """Sets the challenge index in the selection that will be played next (unless the current one is
        restarted...)"""
        if len(data) > 0:
            return bool(getattr(self, 'SetNextChallengeIndex')(*data))
        return bool(getattr(self, 'SetNextChallengeIndex')())

    def getCurrentChallengeInfo(self, *data) -> ChallengeInfo:
        """Returns a struct containing the infos for the current challenge. The struct contains the following
        fields : Name, UId, FileName, Author, Environnement, Mood, BronzeTime, SilverTime, GoldTime, AuthorTime,
        CopperPrice, LapRace, NbLaps and NbCheckpoints."""
        if len(data) > 0:
            return ChallengeInfo(*getattr(self, 'GetCurrentChallengeInfo')(*data).values())
        return ChallengeInfo(*getattr(self, 'GetCurrentChallengeInfo')().values())

    def getNextChallengeInfo(self, *data) -> ChallengeInfo:
        """Returns a struct containing the infos for the next challenge. The struct contains the following fields:
        Name, UId, FileName, Author, Environnement, Mood, BronzeTime, SilverTime, GoldTime, AuthorTime, CopperPrice
        and LapRace. (NbLaps and NbCheckpoints are also present but always set to -1)"""
        if len(data) > 0:
            return ChallengeInfo(*getattr(self, 'GetNextChallengeInfo')(*data).values())
        return ChallengeInfo(*getattr(self, 'GetNextChallengeInfo')().values())

    def getChallengeInfo(self, *data) -> ChallengeInfo:
        """Returns a struct containing the infos for the challenge with the specified filename. The struct contains
        the following fields : Name, UId, FileName, Author, Environnement, Mood, BronzeTime, SilverTime, GoldTime,
        AuthorTime, CopperPrice and LapRace. (NbLaps and NbCheckpoints are also present but always set to -1)"""
        if len(data) > 0:
            return ChallengeInfo(*getattr(self, 'GetChallengeInfo')(*data).values())
        return ChallengeInfo(*getattr(self, 'GetChallengeInfo')().values())

    def checkChallengeForCurrentServerParams(self, *data) -> bool:
        """Returns a boolean if the challenge with the specified filename matches the current server settings."""
        if len(data) > 0:
            return bool(getattr(self, 'CheckChallengeForCurrentServerParams')(*data))
        return bool(getattr(self, 'CheckChallengeForCurrentServerParams')())

    def getChallengeList(self, *data) -> ChallengeList:
        """Returns a list of challenges among the current selection of the server. This method take two parameters.
        The first parameter specifies the maximum number of infos to be returned, and the second one the starting
        index in the selection. The list is an array of structures. Each structure contains the following fields :
        Name, UId, FileName, Environnement, Author, GoldTime and CopperPrice."""
        if len(data) > 0:
            return [Challenge(*result.values()) for result in getattr(self, 'GetChallengeList')(*data)]
        return [Challenge(*result.values()) for result in getattr(self, 'GetChallengeList')()]

    def addChallenge(self, *data) -> bool:
        """Add the challenge with the specified filename at the end of the current selection.
        Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'AddChallenge')(*data))
        return bool(getattr(self, 'AddChallenge')())

    def addChallengeList(self, *data) -> int:
        """Add the list of challenges with the specified filenames at the end of the current selection.
        The list of challenges to add is an array of strings. Only available to Admin."""
        if len(data) > 0:
            return int(getattr(self, 'AddChallengeList')(*data))
        return int(getattr(self, 'AddChallengeList')())

    def removeChallenge(self, *data) -> bool:
        """Remove the challenge with the specified filename from the current selection. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'RemoveChallenge')(*data))
        return bool(getattr(self, 'RemoveChallenge')())

    def removeChallengeList(self, *data) -> int:
        """Remove the list of challenges with the specified filenames from the current selection.
        The list of challenges to remove is an array of strings. Only available to Admin."""
        if len(data) > 0:
            return int(getattr(self, 'RemoveChallengeList')(*data))
        return int(getattr(self, 'RemoveChallengeList')())

    def insertChallenge(self, *data) -> bool:
        """Insert the challenge with the specified filename after the current challenge. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'InsertChallenge')(*data))
        return bool(getattr(self, 'InsertChallenge')())

    def insertChallengeList(self, *data) -> int:
        """Insert the list of challenges with the specified filenames after the current challenge.
        The list of challenges to insert is an array of strings. Only available to Admin."""
        if len(data) > 0:
            return int(getattr(self, 'InsertChallengeList')(*data))
        return int(getattr(self, 'InsertChallengeList')())

    def chooseNextChallenge(self, *data) -> bool:
        """Set as next challenge the one with the specified filename, if it is present in the selection.
        Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'ChooseNextChallenge')(*data))
        return bool(getattr(self, 'ChooseNextChallenge')())

    def chooseNextChallengeList(self, *data) -> int:
        """Set as next challenges the list of challenges with the specified filenames,
        if they are present in the selection. The list of challenges to choose is an array of strings.
        Only available to Admin."""
        if len(data) > 0:
            return int(getattr(self, 'ChooseNextChallengeList')(*data))
        return int(getattr(self, 'ChooseNextChallengeList')())

    def loadMatchSettings(self, *data) -> int:
        """Set a list of challenges defined in the playlist with the specified filename as the current selection
        of the server, and load the gameinfos from the same file. Only available to Admin."""
        if len(data) > 0:
            return int(getattr(self, 'LoadMatchSettings')(*data))
        return int(getattr(self, 'LoadMatchSettings')())

    def appendPlaylistFromMatchSettings(self, *data) -> int:
        """Add a list of challenges defined in the playlist with the specified filename at the end of the current
        selection. Only available to Admin."""
        if len(data) > 0:
            return int(getattr(self, 'AppendPlaylistFromMatchSettings')(*data))
        return int(getattr(self, 'AppendPlaylistFromMatchSettings')())

    def saveMatchSettings(self, *data) -> int:
        """Save the current selection of challenge in the playlist with the specified filename,
        as well as the current gameinfos. Only available to Admin."""
        if len(data) > 0:
            return int(getattr(self, 'SaveMatchSettings')(*data))
        return int(getattr(self, 'SaveMatchSettings')())

    def insertPlaylistFromMatchSettings(self, *data) -> int:
        """Insert a list of challenges defined in the playlist with the specified filename after the current challenge.
        Only available to Admin."""
        if len(data) > 0:
            return int(getattr(self, 'InsertPlaylistFromMatchSettings')(*data))
        return int(getattr(self, 'InsertPlaylistFromMatchSettings')())

    def getPlayerInfo(self, *data) -> PlayerInfo:
        """
        Returns a struct containing the infos on the player with the specified login, with an optional parameter for
        compatibility: struct version (0 = united, 1 = forever). The structure is identical to the ones from
        GetPlayerList. Forever PlayerInfo struct is: Login, NickName, PlayerId, TeamId, SpectatorStatus,
        LadderRanking, and LadderRanking is 0 when not in official mode,
        Flags = ForceSpectator(0,1,2) + IsReferee * 10 + IsPodiumReady * 100 + IsUsingStereoscopy * 1000 +
        IsManagedByAnOtherServer * 10000 + IsServer * 100000 + HasPlayerSlot * 1000000
        SpectatorStatus = Spectator + TemporarySpectator * 10 + PureSpectator * 100 + AutoTarget * 1000 +
        CurrentTargetId * 10000
        """
        if len(data) > 0:
            return PlayerInfo(*getattr(self, 'GetPlayerInfo')(*data).values())
        return PlayerInfo(*getattr(self, 'GetPlayerInfo')().values())

    def getDetailedPlayerInfo(self, *data) -> DetailedPlayerInfo:
        """Returns a struct containing the infos on the player with the specified login.
        The structure contains the following fields : Login, NickName, PlayerId, TeamId, IPAddress,
        DownloadRate, UploadRate, Language, IsSpectator, IsInOfficialMode, a structure named Avatar,
        an array of structures named Skins, a structure named LadderStats, HoursSinceZoneInscription
        and OnlineRights (0: nations account, 3: united account). Each structure of the array Skins contains
        two fields Environnement and a struct PackDesc. Each structure PackDesc, as well as the struct Avatar,
        contains two fields FileName and Checksum."""
        if len(data) > 0:
            return DetailedPlayerInfo(*getattr(self, 'GetDetailedPlayerInfo')(*data).values())
        return DetailedPlayerInfo(*getattr(self, 'GetDetailedPlayerInfo')().values())

    def getPlayerList(self, *data) -> PlayerInfoList:
        """
        Returns the list of players on the server. This method take two parameters.
        The first parameter specifies the maximum number of infos to be returned, and the second one the starting
        index in the list, an optional 3rd parameter is used for compatibility: struct version (0 = united,
        1 = forever, 2 = forever, including the servers).
        The list is an array of PlayerInfo structures.
        Forever PlayerInfo struct is: Login, NickName, PlayerId, TeamId, SpectatorStatus, LadderRanking, and
        Flags = ForceSpectator(0,1,2) + IsReferee * 10 + IsPodiumReady * 100 + IsUsingStereoscopy * 1000 +
        IsManagedByAnOtherServer * 10000 + IsServer * 100000 + HasPlayerSlot * 1000000
        LadderRanking is 0 when not in official mode,
        SpectatorStatus = Spectator + TemporarySpectator * 10 + PureSpectator * 100 + AutoTarget * 1000 +
        CurrentTargetId * 10000
        """
        if len(data) > 0:
            return [PlayerInfo(*result.values()) for result in getattr(self, 'GetPlayerList')(*data)]
        return [PlayerInfo(*result.values()) for result in getattr(self, 'GetPlayerList')()]

    def getMainServerPlayerInfo(self, *data) -> PlayerInfo:
        """
        Returns a struct containing the player infos of the game server (ie: in case of a basic server, itself;
        in case of a relay server, the main server),
        with an optional parameter for compatibility: struct version (0 = united, 1 = forever). The structure is
        identical to the ones from GetPlayerList.
        Forever PlayerInfo struct is: Login, NickName, PlayerId, TeamId, SpectatorStatus, LadderRanking, and
        LadderRanking is 0 when not in official mode,
        Flags = ForceSpectator(0,1,2) + IsReferee * 10 + IsPodiumReady * 100 + IsUsingStereoscopy * 1000 +
        IsManagedByAnOtherServer * 10000 + IsServer * 100000 + HasPlayerSlot * 1000000
        SpectatorStatus = Spectator + TemporarySpectator * 10 + PureSpectator * 100 + AutoTarget * 1000 +
        CurrentTargetId * 10000
        """
        if len(data) > 0:
            return PlayerInfo(*getattr(self, 'GetMainServerPlayerInfo')(*data).values())
        return PlayerInfo(*getattr(self, 'GetMainServerPlayerInfo')().values())

    def getCurrentRanking(self, *data) -> RankingList:
        """Returns the current rankings for the race in progress. (in team mode, the scores for the two
        teams are returned. In other modes, it's the individual players' scores) This method take two parameters.
        The first parameter specifies the maximum number of infos to be returned, and the second one the starting
        index in the ranking. The ranking returned is a list of structures. Each structure contains the following
        fields : Login, NickName, PlayerId, Rank, BestTime, Score, NbrLapsFinished and LadderScore.
        It also contains an array BestCheckpoints that contains the checkpoint times for the best race."""
        if len(data) > 0:
            return [RankingItem(*result.values()) for result in getattr(self, 'GetCurrentRanking')(*data)]
        return [RankingItem(*result.values()) for result in getattr(self, 'GetCurrentRanking')()]

    def getCurrentRankingForLogin(self, *data) -> RankingList:
        """Returns the current ranking for the race in progressof the player with the specified login
        (or list of comma-separated logins). The ranking returned is a list of structures, that contains the
        following fields : Login, NickName, PlayerId, Rank, BestTime, Score, NbrLapsFinished and LadderScore.
        It also contains an array BestCheckpoints that contains the checkpoint times for the best race."""
        if len(data) > 0:
            return [RankingItem(*result.values()) for result in getattr(self, 'GetCurrentRankingForLogin')(*data)]
        return [RankingItem(*result.values()) for result in getattr(self, 'GetCurrentRankingForLogin')()]

    def forceScores(self, *data) -> bool:
        """Force the scores of the current game. Only available in rounds and team mode. You have to pass an
        array of structs {int PlayerId, int Score}. And a boolean SilentMode - if true, the scores are silently
        updated (only available for SuperAdmin), allowing an external controller to do its custom counting...
        Only available to Admin/SuperAdmin."""
        if len(data) > 0:
            return bool(getattr(self, 'ForceScores')(*data))
        return bool(getattr(self, 'ForceScores')())

    def forcePlayerTeam(self, *data) -> bool:
        """Force the team of the player. Only available in team mode. You have to pass the login and the
        team number (0 or 1). Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'ForcePlayerTeam')(*data))
        return bool(getattr(self, 'ForcePlayerTeam')())

    def forcePlayerTeamId(self, *data) -> bool:
        """Force the team of the player. Only available in team mode. You have to pass the playerid and the
        team number (0 or 1). Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'ForcePlayerTeamId')(*data))
        return bool(getattr(self, 'ForcePlayerTeamId')())

    def forceSpectator(self, *data) -> bool:
        """Force the spectating status of the player. You have to pass the login and the spectator mode
        (0: user selectable, 1: spectator, 2: player). Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'ForceSpectator')(*data))
        return bool(getattr(self, 'ForceSpectator')())

    def forceSpectatorId(self, *data) -> bool:
        """Force the spectating status of the player. You have to pass the playerid and the spectator mode
        (0: user selectable, 1: spectator, 2: player). Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'ForceSpectatorId')(*data))
        return bool(getattr(self, 'ForceSpectatorId')())

    def forceSpectatorTarget(self, *data) -> bool:
        """Force spectators to look at a specific player. You have to pass the login of the spectator
        (or '' for all) and the login of the target (or '' for automatic), and an integer for the camera type to use
        (-1 = leave unchanged, 0 = replay, 1 = follow, 2 = free). Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'ForceSpectatorTarget')(*data))
        return bool(getattr(self, 'ForceSpectatorTarget')())

    def forceSpectatorTargetId(self, *data) -> bool:
        """Force spectators to look at a specific player. You have to pass the id of the spectator (or -1 for all)
        and the id of the target (or -1 for automatic), and an integer for the camera type to use
        (-1 = leave unchanged, 0 = replay, 1 = follow, 2 = free). Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'ForceSpectatorTargetId')(*data))
        return bool(getattr(self, 'ForceSpectatorTargetId')())

    def spectatorReleasePlayerSlot(self, *data) -> bool:
        """Pass the login of the spectator. A spectator that once was a player keeps his player slot,
        so that he can go back to race mode. Calling this function frees this slot for another player to connect.
        Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SpectatorReleasePlayerSlot')(*data))
        return bool(getattr(self, 'SpectatorReleasePlayerSlot')())

    def spectatorReleasePlayerSlotId(self, *data) -> bool:
        """Pass the playerid of the spectator. A spectator that once was a player keeps his player slot,
        so that he can go back to race mode. Calling this function frees this slot for another player to connect.
        Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'SpectatorReleasePlayerSlotId')(*data))
        return bool(getattr(self, 'SpectatorReleasePlayerSlotId')())

    def manualFlowControlEnable(self, *data) -> bool:
        """Enable control of the game flow: the game will wait for the caller to validate state transitions.
        Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'ManualFlowControlEnable')(*data))
        return bool(getattr(self, 'ManualFlowControlEnable')())

    def manualFlowControlProceed(self, *data) -> bool:
        """Allows the game to proceed. Only available to Admin."""
        if len(data) > 0:
            return bool(getattr(self, 'ManualFlowControlProceed')(*data))
        return bool(getattr(self, 'ManualFlowControlProceed')())

    def manualFlowControlIsEnabled(self, *data) -> int:
        """Returns whether the manual control of the game flow is enabled. 0 = no, 1 = yes by the xml-rpc
        client making the call, 2 = yes, by some other xml-rpc client. Only available to Admin."""
        if len(data) > 0:
            return int(getattr(self, 'ManualFlowControlIsEnabled')(*data))
        return int(getattr(self, 'ManualFlowControlIsEnabled')())

    def manualFlowControlGetCurTransition(self, *data) -> str:
        """Returns the transition that is currently blocked, or '' if none.
        (That's exactly the value last received by the callback.) Only available to Admin."""
        if len(data) > 0:
            return str(getattr(self, 'ManualFlowControlGetCurTransition')(*data))
        return str(getattr(self, 'ManualFlowControlGetCurTransition')())

    def checkEndMatchCondition(self, *data) -> str:
        """Returns the current match ending condition. Return values are: 'Playing', 'ChangeMap' or 'Finished'."""
        if len(data) > 0:
            return str(getattr(self, 'CheckEndMatchCondition')(*data))
        return str(getattr(self, 'CheckEndMatchCondition')())

    def getNetworkStats(self, *data) -> NetworkStats:
        """Returns a struct containing the networks stats of the server. The structure contains the following fields :
        Uptime, NbrConnection, MeanConnectionTime, MeanNbrPlayer, RecvNetRate, SendNetRate, TotalReceivingSize,
        TotalSendingSize and an array of structures named PlayerNetInfos. Each structure of the array PlayerNetInfos
        contains the following fields : Login, IPAddress, LastTransferTime, DeltaBetweenTwoLastNetState,
        PacketLossRate. Only available to SuperAdmin."""
        if len(data) > 0:
            return NetworkStats(*getattr(self, 'GetNetworkStats')(*data).values())
        return NetworkStats(*getattr(self, 'GetNetworkStats')().values())

    def startServerLan(self, *data) -> bool:
        """Start a server on lan, using the current configuration. Only available to SuperAdmin."""
        if len(data) > 0:
            return bool(getattr(self, 'StartServerLan')(*data))
        return bool(getattr(self, 'StartServerLan')())

    def startServerInternet(self, *data) -> bool:
        """Start a server on internet using the 'Login' and 'Password' specified in the struct passed as parameters.
        Only available to SuperAdmin."""
        if len(data) > 0:
            return bool(getattr(self, 'StartServerInternet')(*data))
        return bool(getattr(self, 'StartServerInternet')())

    def getStatus(self, *data) -> Status:
        """Returns the current status of the server."""
        if len(data) > 0:
            return Status(*getattr(self, 'GetStatus')(*data).values())
        return Status(*getattr(self, 'GetStatus')().values())

    def quitGame(self, *data) -> bool:
        """Quit the application. Only available to SuperAdmin."""
        if len(data) > 0:
            return bool(getattr(self, 'QuitGame')(*data))
        return bool(getattr(self, 'QuitGame')())

    def gameDataDirectory(self, *data) -> str:
        """Returns the path of the game datas directory. Only available to Admin."""
        if len(data) > 0:
            return str(getattr(self, 'GameDataDirectory')(*data))
        return str(getattr(self, 'GameDataDirectory')())

    def getTracksDirectory(self, *data) -> str:
        """Returns the path of the tracks directory. Only available to Admin."""
        if len(data) > 0:
            return str(getattr(self, 'GetTracksDirectory')(*data))
        return str(getattr(self, 'GetTracksDirectory')())

    def getSkinsDirectory(self, *data) -> str:
        """Returns the path of the skins directory. Only available to Admin."""
        if len(data) > 0:
            return str(getattr(self, 'GetSkinsDirectory')(*data))
        return str(getattr(self, 'GetSkinsDirectory')())
