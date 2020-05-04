from src.APIs.method_types import *
from src.client import Client


class TrackmaniaAPI(object):
    def __init__(self, ip, port, pyseco):
        self._client = Client(ip, port, pyseco)

    def __getattr__(self, name):
        method = Method(self._client.request, name)
        if name == 'noresponse':
            method.set_send(self._client.no_response_request)
        return method

    def start_listening(self):
        self._client.loop()

    def connect(self):
        self._client.connect()

    def disconnect(self):
        self._client.disconnect()

    def authenticate(self, login: str, password: str) -> bool:
        """Allow user authentication by specifying a login and a password, to gain access to the set of
        functionalities corresponding to this authorization level. """
        return self.Authenticate(login, password)

    def change_auth_password(self, login: str, password: str) -> bool:
        """Change the password for the specified login/user. Only available to SuperAdmin."""
        return self.ChangeAuthPassword(login, password)

    def enable_callbacks(self, callback: bool) -> bool:
        """Allow the GameServer to call you back."""
        return self.EnableCallbacks(callback)

    def get_version(self) -> Version:
        """Returns a struct with the Name, Version and Build of the application remotely controled."""
        return Version(*self.GetVersion().values())

    def call_vote(self, vote: str) -> bool:
        """Call a vote for a cmd. The command is a XML string corresponding to an XmlRpc request.
        Only available to Admin."""
        return self.CallVote(vote)

    def call_vote_ex(self, vote: str, ratio: float, time_out: int, voter: int) -> bool:
        """Extended call vote. Same as CallVote, but you can additionally supply specific parameters for this vote:
        a ratio, a time out and who is voting. Special timeout values: a timeout of 0 means default,
        1 means indefinite; a ratio of -1 means default; Voters values: 0 means only active players,
        1 means any player, 2 is for everybody, pure spectators included. Only available to Admin."""
        return self.CallVoteEx(vote, ratio, time_out, voter)

    def internal_call_vote(self) -> bool:
        """Used internally by game."""
        return self.InternalCallVote()

    def cancel_vote(self) -> bool:
        """Cancel the current vote. Only available to Admin."""
        return self.CancelVote()

    def get_current_call_vote(self) -> CurrentCallVote:
        """Returns the vote currently in progress. The returned structure is { CallerLogin, CmdName, CmdParam }."""
        return CurrentCallVote(*self.GetCurrentCallVote().values())

    def set_call_vote_time_out(self, timeout: int) -> bool:
        """Set a new timeout for waiting for votes. A zero value disables callvote. Only available to Admin.
        Requires a challenge restart to be taken into account."""
        return self.SetCallVoteTimeOut(timeout)

    def get_call_vote_timeout(self) -> StateValue:
        """Get the current and next timeout for waiting for votes. The struct returned contains two
        fields CurrentValue and NextValue."""
        return StateValue(*self.GetCallVoteTimeOut().values())

    def set_call_vote_ratio(self, ratio: float) -> bool:
        """Set a new default ratio for passing a vote. Must lie between 0 and 1. Only available to Admin."""
        return self.SetCallVoteRatio(ratio)

    def get_call_vote_ratio(self) -> float:
        """Get the current default ratio for passing a vote. This value lies between 0 and 1."""
        return self.GetCallVoteRatio()

    def set_call_vote_ratios(self, vote_ratios: List[CallVoteRatio]) -> bool:
        """Set new ratios for passing specific votes. The parameter is an array of structs {string Command,
        double Ratio}, ratio is in [0,1] or -1 for vote disabled. Only available to Admin. """
        return self.SetCallVoteRatios(vote_ratios)

    def get_call_vote_ratios(self) -> List[CallVoteRatio]:
        """Get the current ratios for passing votes."""
        return [CallVoteRatio(*result.values()) for result in self.GetCallVoteRatios()]

    def chat_send_server_message(self, message: str) -> bool:
        """Send a text message to all clients without the server login. Only available to Admin."""
        return self.ChatSendServerMessage(message)

    def chat_send_server_message_to_language(self, messages: List[TextWithLanguage], logins: str) -> bool:
        """Send a localised text message to all clients without the server login, or optionally to a Login (which can
        be a single login or a list of comma-separated logins). The parameter is an array of structures {Lang=??,
        Text=...}. If no matching language is found, the last text in the array is used. Only available to Admin. """
        return self.ChatSendServerMessageToLanguage(messages, logins)

    def chat_send_server_message_to_id(self, message: str, player_id: int) -> bool:
        """Send a text message without the server login to the client with the specified PlayerId.
        Only available to Admin."""
        return self.ChatSendServerMessageToId(message, player_id)

    def chat_send_server_message_to_login(self, message: str, logins: str) -> bool:
        """Send a text message without the server login to the client with the specified login.
        Login can be a single login or a list of comma-separated logins. Only available to Admin."""
        return self.ChatSendServerMessageToLogin(message, logins)

    def chat_send(self, message: str) -> bool:
        """Send a text message to all clients. Only available to Admin."""
        return self.ChatSend(message)

    def chat_send_to_language(self, messages: List[TextWithLanguage], login: str) -> bool:
        """Send a localised text message to all clients, or optionally to a Login (which can be a single
        login or a list of comma-separated logins). The parameter is an array of structures {Lang=??, Text=...}.
        If no matching language is found, the last text in the array is used. Only available to Admin."""
        return self.ChatSendToLanguage(messages, login)

    def chat_send_to_login(self, message: str, logins: str) -> bool:
        """Send a text message to the client with the specified login. Login can be a single
        login or a list of comma-separated logins. Only available to Admin."""
        return self.ChatSendToLogin(message, logins)

    def chat_send_to_id(self, message: str, player_id: int) -> bool:
        """Send a text message to the client with the specified PlayerId. Only available to Admin."""
        return self.ChatSendToId(message, player_id)

    def get_chat_lines(self) -> List[str]:
        """Returns the last chat lines. Maximum of 40 lines. Only available to Admin."""
        return self.GetChatLines()

    def chat_enable_manual_routing(self, manual_forward: bool, automatic_forward: bool) -> bool:
        """The chat messages are no longer dispatched to the players, they only go to the rpc callback
        and the controller has to manually forward them. The second (optional) parameter allows all messages from
        the server to be automatically forwarded. Only available to Admin."""
        return self.ChatEnableManualRouting(manual_forward, automatic_forward)

    def chat_forward_to_login(self, message: str, login_from: str, login_to: str) -> bool:
        """(Text, SenderLogin, DestLogin) Send a text message to the specified DestLogin (or everybody if empty)
        on behalf of SenderLogin. DestLogin can be a single login or a list of comma-separated logins.
        Only available if manual routing is enabled. Only available to Admin."""
        return self.ChatForwardToLogin(message, login_from, login_to)

    def send_notice(self, message: str, avatar_login: str, max_duration: int) -> bool:
        """Display a notice on all clients. The parameters are the text message to display, and the login
        of the avatar to display next to it (or  for no avatar), and an optional max duration
        in seconds (default: 3). Only available to Admin."""
        return self.SendNotice(message, avatar_login, max_duration)

    def send_notice_to_id(self, player_id: int, message: str, avatar_login: str, max_duration: int) -> bool:
        """Display a notice on the client with the specified UId. The parameters are the Uid of the client
        to whom the notice is sent, the text message to display, and the UId of the avatar to display
        next to it (or 255 for no avatar), and an optional max duration in seconds (default: 3).
        Only available to Admin."""
        return self.SendNoticeToId(player_id, message, avatar_login, max_duration)

    def send_notice_to_login(self, login: str, message: str, avatar_login: str, max_duration: int) -> bool:
        """Display a notice on the client with the specified login. The parameters are the login of the client
        to whom the notice is sent, the text message to display, and the login of the avatar to display
        next to it (or  for no avatar), and an optional max duration in seconds (default: 3).
        Login can be a single login or a list of comma-separated logins.  Only available to Admin."""
        return self.SendNoticeToLogin(login, message, avatar_login, max_duration)

    def send_display_manialink_page(self, xml_description: str, timeout: int, page_hidden: bool) -> bool:
        """Display a manialink page on all clients. The parameters are the xml description of the page to display,
        a timeout to autohide it (0 = permanent), and a boolean to indicate whether the page must be hidden
        as soon as the user clicks on a page option. Only available to Admin."""
        return self.SendDisplayManialinkPage(xml_description, timeout, page_hidden)

    def send_display_manialink_page_to_id(self, player_id: int, xml_description: str, timeout: int,
                                          page_hidden: bool) -> bool:
        """Display a manialink page on the client with the specified UId. The first parameter is the UId of the player,
        the other are identical to SendDisplayManialinkPage. Only available to Admin."""
        return self.SendDisplayManialinkPageToId(player_id, xml_description, timeout, page_hidden)

    def send_display_manialink_page_to_login(self, login: str, xml_description: str, timeout: int,
                                             page_hidden: bool) -> bool:
        """Display a manialink page on the client with the specified login. The first parameter is the
        login of the player, the other are identical to SendDisplayManialinkPage.
        Login can be a single login or a list of comma-separated logins. Only available to Admin."""
        return self.SendDisplayManialinkPageToLogin(login, xml_description, timeout, page_hidden)

    def send_hide_manialink_page(self) -> bool:
        """Hide the displayed manialink page on all clients. Only available to Admin."""
        return self.SendHideManialinkPage()

    def send_hide_manialink_page_to_id(self, player_id: int) -> bool:
        """Hide the displayed manialink page on the client with the specified UId. Only available to Admin."""
        return self.SendHideManialinkPageToId(player_id)

    def send_hide_manialink_page_to_login(self, logins: str) -> bool:
        """Hide the displayed manialink page on the client with the specified login. Login can be a single
        login or a list of comma-separated logins. Only available to Admin."""
        return self.SendHideManialinkPageToLogin(logins)

    def get_manialink_page_answers(self) -> List[ManialinkPageAnswers]:
        """Returns the latest results from the current manialink page, as an array of structs {string Login,
        int PlayerId, int Result} Result==0 -> no answer, Result>0.... -> answer from the player."""
        return [ManialinkPageAnswers(*result.values()) for result in self.GetManialinkPageAnswers()]

    def kick(self, login: str, message='') -> bool:
        """Kick the player with the specified login, with an optional message. Only available to Admin."""
        return self.Kick(login, message)

    def kick_id(self, player_id: int, message: str) -> bool:
        """Kick the player with the specified PlayerId, with an optional message. Only available to Admin."""
        return self.KickId(player_id, message)

    def ban(self, login: str, message: str) -> bool:
        """Ban the player with the specified login, with an optional message. Only available to Admin."""
        return self.Ban(login, message)

    def ban_and_black_list(self, login: str, message: str, save: bool) -> bool:
        """Ban the player with the specified login, with a message. Add it to the black list,
        and optionally save the new list. Only available to Admin."""
        return self.BanAndBlackList(login, message, save)

    def ban_id(self, player_id: int, message: str) -> bool:
        """Ban the player with the specified PlayerId, with an optional message. Only available to Admin."""
        return self.BanId(player_id, message)

    def un_ban(self, login: str) -> bool:
        """Unban the player with the specified client name. Only available to Admin."""
        return self.UnBan(login)

    def clean_ban_list(self) -> bool:
        """Clean the ban list of the server. Only available to Admin."""
        return self.CleanBanList()

    def get_ban_list(self, max_number_of_infos: int, starting_index: int) -> List[BanItem]:
        """Returns the list of banned players. This method takes two parameters. The first parameter
        specifies the maximum number of infos to be returned, and the second one the starting index in the list.
        The list is an array of structures. Each structure contains the following fields :
        Login, ClientName and IPAddress."""
        return [BanItem(*result.values()) for result in
                self.GetList[BanItem](max_number_of_infos, starting_index)]

    def black_list(self, login: str) -> bool:
        """Blacklist the player with the specified login. Only available to SuperAdmin."""
        return self.BlackList(login)

    def black_list_id(self, player_id) -> bool:
        """Blacklist the player with the specified PlayerId. Only available to SuperAdmin."""
        return self.BlackListId(player_id)

    def un_black_list(self, login: str) -> bool:
        """UnBlackList the player with the specified login. Only available to SuperAdmin."""
        return self.UnBlackList(login)

    def clean_black_list(self) -> bool:
        """Clean the blacklist of the server. Only available to SuperAdmin."""
        return self.CleanBlackList()

    def get_black_list(self, max_number_of_infos: int, starting_index: int) -> List[str]:
        """Returns the list of blacklisted players. This method takes two parameters.
        The first parameter specifies the maximum number of infos to be returned,
        and the second one the starting index in the list. The list is an array of structures.
        Each structure contains the following fields : Login."""
        return self.GetBlackList(max_number_of_infos, starting_index)

    def load_black_list(self, filename: str) -> bool:
        """Load the black list file with the specified file name. Only available to Admin."""
        return self.LoadBlackList(filename)

    def save_black_list(self, filename: str) -> bool:
        """Save the black list in the file with specified file name. Only available to Admin."""
        return self.SaveBlackList(filename)

    def add_guest(self, login: str) -> bool:
        """Add the player with the specified login on the guest list. Only available to Admin."""
        return self.AddGuest(login)

    def add_guest_id(self, player_id: int) -> bool:
        """Add the player with the specified PlayerId on the guest list. Only available to Admin."""
        return self.AddGuestId(player_id)

    def remove_guest(self, login: str) -> bool:
        """Remove the player with the specified login from the guest list. Only available to Admin."""
        return self.RemoveGuest(login)

    def remove_guest_id(self, player_id: int) -> bool:
        """Remove the player with the specified PlayerId from the guest list. Only available to Admin."""
        return self.RemoveGuestId(player_id)

    def clean_guest_list(self) -> bool:
        """Clean the guest list of the server. Only available to Admin."""
        return self.CleanGuestList()

    def get_guest_list(self, max_number_of_infos: int, starting_index: int) -> List[str]:
        """Returns the list of players on the guest list. This method takes two parameters.
        The first parameter specifies the maximum number of infos to be returned, and the second one
        the starting index in the list. The list is an array of structures.
        Each structure contains the following fields : Login."""
        return self.GetGuestList(max_number_of_infos, starting_index)

    def load_guest_list(self, filename: str) -> bool:
        """Load the guest list file with the specified file name. Only available to Admin."""
        return self.LoadGuestList(filename)

    def save_guest_list(self, filename: str) -> bool:
        """Save the guest list in the file with specified file name. Only available to Admin."""
        return self.SaveGuestList(filename)

    def set_buddy_notification(self, login: str, enabled: bool) -> bool:
        """Sets whether buddy notifications should be sent in the chat. login is the login of the player,
        or  for global setting, and enabled is the value. Only available to Admin."""
        return self.SetBuddyNotification(login, enabled)

    def get_buddy_notification(self, login: str) -> bool:
        """Gets whether buddy notifications are enabled for login, or  to get the global setting."""
        return self.GetBuddyNotification(login)

    # def write_file(self, *data) -> bool:
    #     """Write the data to the specified file. The filename is relative to the Tracks path.
    #     Only available to Admin."""
    #     return self.WriteFile(*data)
    #
    # def tunnel_send_data_to_id(self, *data) -> bool:
    #     """Send the data to the specified player. Only available to Admin."""
    #     return self.TunnelSendDataToId(*data)
    #
    # def tunnel_send_data_to_login(self, *data) -> bool:
    #     """Send the data to the specified player. Login can be a single login or a list of comma-separated logins.
    #     Only available to Admin."""
    #     return self.TunnelSendDataToLogin(*data)

    def echo(self, internal: str, public: str) -> bool:
        """Just log the parameters and invoke a callback. Can be used to talk to other xmlrpc clients connected,
        or to make custom votes. If used in a callvote, the first parameter will be used as the vote
        message on the clients. Only available to Admin."""
        return self.Echo(internal, public)

    def ignore(self, login: str) -> bool:
        """Ignore the player with the specified login. Only available to Admin."""
        return self.Ignore(login)

    def ignore_id(self, player_id: int) -> bool:
        """Ignore the player with the specified PlayerId. Only available to Admin."""
        return self.IgnoreId(player_id)

    def un_ignore(self, login: str) -> bool:
        """Unignore the player with the specified login. Only available to Admin."""
        return self.UnIgnore(login)

    def un_ignore_id(self, player_id: int) -> bool:
        """Unignore the player with the specified PlayerId. Only available to Admin."""
        return self.UnIgnoreId(player_id)

    def clean_ignore_list(self, max_number_of_infos: int, starting_index: int) -> bool:
        """Clean the ignore list of the server. Only available to Admin."""
        return self.CleanIgnoreList(max_number_of_infos, starting_index)

    def get_ignore_list(self, max_number_of_infos: int, starting_index: int) -> List[str]:
        """Returns the list of ignored players. This method takes two parameters.
        The first parameter specifies the maximum number of infos to be returned, and the second one
        the starting index in the list. The list is an array of structures. Each structure contains
        the following fields : Login."""
        return self.GetIgnoreList(max_number_of_infos, starting_index)

    def pay(self, login: str, coppers: int, label: str) -> int:
        """Pay coppers from the server account to a player, returns the BillId.
        This method takes three parameters: Login of the payee, Coppers to pay and a Label to send with the payment.
        The creation of the transaction itself may cost coppers, so you need to have coppers on the server account.
        Only available to Admin."""
        return self.Pay(login, coppers, label)

    def send_bill(self, login_from: str, coppers: int, label: str, login_to: str) -> int:
        """Create a bill, send it to a player, and return the BillId. This method takes four parameters:
        LoginFrom of the payer, Coppers the player has to pay, Label of the transaction and an optional
        LoginTo of the payee (if empty string, then the server account is used).
        The creation of the transaction itself may cost coppers, so you need to have coppers on the server account.
        Only available to Admin."""
        return self.SendBill(login_from, coppers, label, login_to)

    def get_bill_state(self, state: int) -> BillState:
        """Returns the current state of a bill. This method takes one parameter, the BillId.
        Returns a struct containing State, StateName and TransactionId.
        Possible enum values are: CreatingTransaction, Issued, ValidatingPayement, Payed, Refused, Error."""
        return BillState(*self.GetBillState(state).values())

    def get_server_coppers(self) -> int:
        """Returns the current number of coppers on the server account."""
        return self.GetServerCoppers()

    def get_system_info(self) -> SystemInfo:
        """Get some system infos, including connection rates (in kbps)."""
        return SystemInfo(*self.GetSystemInfo().values())

    def set_connection_rates(self, connection_rate: int) -> bool:
        """Set the download and upload rates (in kbps)."""
        return self.SetConnectionRates(connection_rate)

    def set_server_name(self, name: str) -> bool:
        """Set a new server name in utf8 format. Only available to Admin."""
        return self.SetServerName(name)

    def get_server_name(self) -> str:
        """Get the server name in utf8 format."""
        return self.GetServerName()

    def set_server_comment(self, comment: str) -> bool:
        """Set a new server comment in utf8 format. Only available to Admin."""
        return self.SetServerComment(comment)

    def get_server_comment(self) -> str:
        """Get the server comment in utf8 format."""
        return self.GetServerComment()

    def set_hide_server(self, hidden: bool) -> bool:
        """Set whether the server should be hidden from the public server list
        (0 = visible, 1 = always hidden, 2 = hidden from nations). Only available to Admin."""
        return self.SetHideServer(hidden)

    def get_hide_server(self) -> int:
        """Get whether the server wants to be hidden from the public server list."""
        return self.GetHideServer()

    def is_relay_server(self) -> bool:
        """Returns true if this is a relay server."""
        return self.IsRelayServer()

    def set_server_password(self, password: str) -> bool:
        """Set a new password for the server. Only available to Admin."""
        return self.SetServerPassword(password)

    def get_server_password(self) -> str:
        """Get the server password if called as Admin or Super Admin, else returns if a password is needed or not."""
        return self.GetServerPassword()

    def set_server_password_for_spectator(self, password: str) -> bool:
        """Set a new password for the spectator mode. Only available to Admin."""
        return self.SetServerPasswordForSpectator(password)

    def get_server_password_for_spectator(self) -> str:
        """Get the password for spectator mode if called as Admin or Super Admin, else returns if a password
        is needed or not."""
        return self.GetServerPasswordForSpectator()

    def set_max_players(self, max_players: int) -> bool:
        """Set a new maximum number of players. Only available to Admin. Requires a challenge restart to be
        taken into account."""
        return self.SetMaxPlayers(max_players)

    def get_max_players(self) -> StateValue:
        """Get the current and next maximum number of players allowed on server. The struct returned contains
        two fields CurrentValue and NextValue."""
        return StateValue(*self.GetMaxPlayers().values())

    def set_max_spectators(self, number_of_spectators: int) -> bool:
        """Set a new maximum number of Spectators. Only available to Admin. Requires a challenge restart to be
        taken into account."""
        return self.SetMaxSpectators(number_of_spectators)

    def get_max_spectators(self) -> StateValue:
        """Get the current and next maximum number of Spectators allowed on server. The struct returned contains
        two fields CurrentValue and NextValue."""
        return StateValue(*self.GetMaxSpectators().values())

    def enable_p2p_upload(self, p2p: bool) -> bool:
        """Enable or disable peer-to-peer upload from server. Only available to Admin."""
        return self.EnableP2PUpload(p2p)

    def is_p2p_upload(self) -> bool:
        """Returns if the peer-to-peer upload from server is enabled."""
        return self.IsP2PUpload()

    def enable_p2p_download(self, p2p: bool) -> bool:
        """Enable or disable peer-to-peer download for server. Only available to Admin."""
        return self.EnableP2PDownload(p2p)

    def is_p2p_download(self) -> bool:
        """Returns if the peer-to-peer download for server is enabled."""
        return self.IsP2PDownload()

    def allow_challenge_download(self, allowed: bool) -> bool:
        """Allow clients to download challenges from the server. Only available to Admin."""
        return self.AllowChallengeDownload(allowed)

    def is_challenge_download_allowed(self) -> bool:
        """Returns if clients can download challenges from the server."""
        return self.IsChallengeDownloadAllowed()

    def auto_save_replays(self, auto_save: bool) -> bool:
        """Enable the autosaving of all replays (vizualisable replays with all players, but not validable)
        on the server. Only available to SuperAdmin."""
        return self.AutoSaveReplays(auto_save)

    def auto_save_validation_replays(self, auto_save: bool) -> bool:
        """Enable the autosaving on the server of validation replays, every time a player makes a new time.
        Only available to SuperAdmin."""
        return self.AutoSaveValidationReplays(auto_save)

    def is_auto_save_replays_enabled(self) -> bool:
        """Returns if autosaving of all replays is enabled on the server."""
        return self.IsAutoSaveReplaysEnabled()

    def is_auto_save_validation_replays_enabled(self) -> bool:
        """Returns if autosaving of validation replays is enabled on the server."""
        return self.IsAutoSaveValidationReplaysEnabled()

    def save_current_replay(self, filename: str) -> bool:
        """Saves the current replay (vizualisable replays with all players, but not validable).
        Pass a filename, or  for an automatic filename. Only available to Admin."""
        return self.SaveCurrentReplay(filename)

    def save_best_ghosts_replay(self, login: str, filename: str) -> bool:
        """Saves a replay with the ghost of all the players best race. First parameter is the login of the player
        (or  for all players), Second parameter is the filename, or  for an automatic filename.
        Only available to Admin."""
        return self.SaveBestGhostsReplay(login, filename)

    # def getValidationReplay(self, *data) -> base64 GetValidationReplay:
    #     Returns a replay containing the data needed to validate the current best time of the player.
    #     The parameter is the login of the player.
    #         retur ValidationReplay(*self.GetValidationReplay(*data).values())

    def set_ladder_mode(self, ladder_mode: int) -> bool:
        """Set a new ladder mode between ladder disabled (0) and forced (1). Only available to Admin.
        Requires a challenge restart to be taken into account."""
        return self.SetLadderMode(ladder_mode)

    def get_ladder_mode(self) -> StateValue:
        """Get the current and next ladder mode on server. The struct returned contains two fields CurrentValue
        and NextValue."""
        return StateValue(*self.GetLadderMode().values())

    def get_ladder_server_limits(self) -> LadderServerLimits:
        """Get the ladder points limit for the players allowed on this server. The struct returned contains
        two fields LadderServerLimitMin and LadderServerLimitMax."""
        return LadderServerLimits(*self.GetLadderServerLimits().values())

    def set_vehicle_net_quality(self, quality: int) -> bool:
        """Set the network vehicle quality to Fast (0) or High (1). Only available to Admin.
        Requires a challenge restart to be taken into account."""
        return self.SetVehicleNetQuality(quality)

    def get_vehicle_net_quality(self) -> StateValue:
        """Get the current and next network vehicle quality on server. The struct returned contains two fields
        CurrentValue and NextValue."""
        return StateValue(*self.GetVehicleNetQuality().values())

    def set_server_options(self, server_options: ServerOptions) -> bool:
        """Set new server options using the struct passed as parameters. This struct must contain the following fields:
        Name, Comment, Password, PasswordForSpectator, NextMaxPlayers, NextMaxSpectators, IsP2PUpload, IsP2PDownload,
        NextLadderMode, NextVehicleNetQuality, NextCallVoteTimeOut, CallVoteRatio, AllowChallengeDownload,
        AutoSaveReplays, and optionally for forever: RefereePassword, RefereeMode, AutoSaveValidationReplays,
        HideServer, UseChangingValidationSeed. Only available to Admin. A change of NextMaxPlayers, NextMaxSpectators,
        NextLadderMode, NextVehicleNetQuality, NextCallVoteTimeOut or UseChangingValidationSeed
        requires a challenge restart to be taken into account."""
        return self.SetServerOptions(server_options.as_dict())

    # TODO fix: raise an exception wen given tm_version is set to 1. We should use 1 as default (TM FOREVER)
    def get_server_options(self, tm_version: int = 1) -> ServerOptions:
        """Optional parameter for compatibility: struct version (0 = united, 1 = forever).
        Returns a struct containing the server options: Name, Comment, Password, PasswordForSpectator,
        CurrentMaxPlayers, NextMaxPlayers, CurrentMaxSpectators, NextMaxSpectators, IsP2PUpload, IsP2PDownload,
        CurrentLadderMode, NextLadderMode, CurrentVehicleNetQuality, NextVehicleNetQuality, CurrentCallVoteTimeOut,
        NextCallVoteTimeOut, CallVoteRatio, AllowChallengeDownload and AutoSaveReplays, and additionally for forever:
        RefereePassword, RefereeMode, AutoSaveValidationReplays, HideServer, CurrentUseChangingValidationSeed,
        NextUseChangingValidationSeed."""
        return ServerOptions(*self.GetServerOptions(tm_version).values())

    def set_server_pack_mask(self, pack_mask: str) -> bool:
        """Defines the packmask of the server. Can be United, Nations, Sunrise, Original, or any of the
        environment names. (Only challenges matching the packmask will be allowed on the server, so that player
        connecting to it know what to expect.) Only available when the server is stopped. Only available to Admin."""
        return self.SetServerPackMask(pack_mask)

    def get_server_pack_mask(self) -> str:
        """Get the packmask of the server."""
        return self.GetServerPackMask()

    def set_forced_mods(self, override: bool, mods: Mods) -> bool:
        """Set the mods to apply on the clients. Parameters: Override, if true even the challenges with a mod will
        be overridden by the server setting; and Mods, an array of structures [{EnvName, Url}, ...].
        Requires a challenge restart to be taken into account. Only available to Admin."""
        return self.SetForcedMods(override, mods)

    def get_forced_mods(self) -> ForcedMods:
        """Get the mods settings."""
        return ForcedMods(*self.GetForcedMods().values())

    def set_forced_music(self, override: bool, url: str) -> bool:
        """Set the music to play on the clients. Parameters: Override, if true even the challenges with a
        custom music will be overridden by the server setting, and a UrlOrFileName for the music. Requires a
        challenge restart to be taken into account. Only available to Admin."""
        return self.SetForcedMusic(override, url)

    def get_forced_music(self) -> ForcedMusic:
        """Get the music setting."""
        return ForcedMusic(*self.GetForcedMusic().values())

    def set_forced_skins(self, forced_skin: ForcedSkin) -> bool:
        """Defines a list of remappings for player skins. It expects a list of structs Orig, Name, Checksum, Url.
        Orig is the name of the skin to remap, or * for any other. Name, Checksum, Url define the skin to use.
        (They are optional, you may set value  for any of those. All 3 null means same as Orig). Will only affect
        players connecting after the value is set. Only available to Admin."""
        return self.SetForcedSkins(forced_skin)

    def get_forced_skins(self) -> List[ForcedSkin]:
        """Get the current forced skins."""
        return [ForcedSkin(*result.values()) for result in self.GetForcedSkins()]

    def get_last_connection_error_message(self) -> str:
        """Returns the last error message for an internet connection. Only available to Admin."""
        return self.GetLastConnectionErrorMessage()

    def set_referee_password(self, password: str) -> bool:
        """Set a new password for the referee mode. Only available to Admin."""
        return self.SetRefereePassword(password)

    def get_referee_password(self) -> str:
        """Get the password for referee mode if called as Admin or Super Admin, else returns if a password is
        needed or not."""
        return self.GetRefereePassword()

    def set_referee_mode(self, validation_mode: int) -> bool:
        """Set the referee validation mode. 0 = validate the top3 players, 1 = validate all players.
        Only available to Admin."""
        return self.SetRefereeMode(validation_mode)

    def get_referee_mode(self) -> int:
        """Get the referee validation mode."""
        return self.GetRefereeMode()

    def set_use_changing_validation_seed(self, validation: bool) -> bool:
        """Set whether the game should use a variable validation seed or not. Only available to Admin.
        Requires a challenge restart to be taken into account."""
        return self.SetUseChangingValidationSeed(validation)

    def get_use_changing_validation_seed(self) -> StateValue:
        """Get the current and next value of UseChangingValidationSeed. The struct returned contains two fields
        CurrentValue and NextValue."""
        return StateValue(*self.GetUseChangingValidationSeed().values())

    def set_warm_up(self, warm_up: bool) -> bool:
        """Sets whether the server is in warm-up phase or not. Only available to Admin."""
        return self.SetWarmUp(warm_up)

    def get_warm_up(self) -> bool:
        """Returns whether the server is in warm-up phase."""
        return self.GetWarmUp()

    def challenge_restart(self) -> bool:
        """Restarts the challenge, with an optional boolean parameter DontClearCupScores (only available in cup mode).
        Only available to Admin."""
        return self.ChallengeRestart()

    def restart_challenge(self) -> bool:
        """Restarts the challenge, with an optional boolean parameter DontClearCupScores (only available in cup mode).
        Only available to Admin."""
        return self.RestartChallenge()

    def next_challenge(self) -> bool:
        """Switch to next challenge, with an optional boolean parameter DontClearCupScores (only available in cup mode).
        Only available to Admin."""
        return self.NextChallenge()

    def stop_server(self) -> bool:
        """Stop the server. Only available to SuperAdmin."""
        return self.StopServer()

    def force_end_round(self) -> bool:
        """In Rounds or Laps mode, force the end of round without waiting for all players to giveup/finish.
        Only available to Admin."""
        return self.ForceEndRound()

    def set_game_infos(self, game_infos: GameInfo) -> bool:
        """Set new game settings using the struct passed as parameters. This struct must contain the following fields :
        GameMode, ChatTime, RoundsPointsLimit, RoundsUseNewRules, RoundsForcedLaps, TimeAttackLimit,
        TimeAttackSynchStartPeriod, TeamPointsLimit, TeamMaxPoints, TeamUseNewRules, LapsNbLaps, LapsTimeLimit,
        FinishTimeout, and optionally: AllWarmUpDuration, DisableRespawn, ForceShowAllOpponents,
        RoundsPointsLimitNewRules, TeamPointsLimitNewRules, CupPointsLimit, CupRoundsPerChallenge, CupNbWinners,
        CupWarmUpDuration. Only available to Admin. Requires a challenge restart to be taken into account."""
        return self.SetGameInfos(game_infos)

    # TODO fix: raise an exception wen given tm_version is set to 1. We should use 1 as default (TM FOREVER)
    def get_current_game_info(self, tm_version: int = 1) -> GameInfo:
        """Optional parameter for compatibility: struct version (0 = united, 1 = forever). Returns a struct containing
        the current game settings, ie: GameMode, ChatTime, NbChallenge, RoundsPointsLimit, RoundsUseNewRules,
        RoundsForcedLaps, TimeAttackLimit, TimeAttackSynchStartPeriod, TeamPointsLimit, TeamMaxPoints, TeamUseNewRules,
        LapsNbLaps, LapsTimeLimit, FinishTimeout, and additionally for version 1: AllWarmUpDuration, DisableRespawn,
        ForceShowAllOpponents, RoundsPointsLimitNewRules, TeamPointsLimitNewRules, CupPointsLimit,
        CupRoundsPerChallenge, CupNbWinners, CupWarmUpDuration."""
        return GameInfo(*self.GetCurrentGameInfo(tm_version).values())

    # TODO fix: raise an exception wen given tm_version is set to 1. We should use 1 as default (TM FOREVER)
    def get_next_game_info(self, tm_version: int = 1) -> GameInfo:
        """Optional parameter for compatibility: struct version (0 = united, 1 = forever).
        Returns a struct containing the game settings for the next challenge, ie: GameMode, ChatTime, NbChallenge,
        RoundsPointsLimit, RoundsUseNewRules, RoundsForcedLaps, TimeAttackLimit, TimeAttackSynchStartPeriod,
        TeamPointsLimit, TeamMaxPoints, TeamUseNewRules, LapsNbLaps, LapsTimeLimit, FinishTimeout,
        and additionally for version 1: AllWarmUpDuration, DisableRespawn, ForceShowAllOpponents,
        RoundsPointsLimitNewRules, TeamPointsLimitNewRules, CupPointsLimit, CupRoundsPerChallenge, CupNbWinners,
        CupWarmUpDuration."""
        return GameInfo(*self.GetNextGameInfo(tm_version).values())

    # TODO fix: raise an exception wen given tm_version is set to 1. We should use 1 as default (TM FOREVER)
    def get_game_infos(self, tm_version: int = 1) -> StateValue:
        """Optional parameter for compatibility: struct version (0 = united, 1 = forever).
        Returns a struct containing two other structures, the first containing the current game settings and
        the second the game settings for next challenge. The first structure is named CurrentGameInfos and the
        second NextGameInfos."""
        return StateValue(*self.GetGameInfos(tm_version).values())

    def set_game_mode(self, game_mode: int) -> bool:
        """Set a new game mode between Rounds (0), TimeAttack (1), Team (2), Laps (3), Stunts (4) and Cup (5).
        Only available to Admin. Requires a challenge restart to be taken into account."""
        return self.SetGameMode(game_mode)

    def get_game_mode(self) -> int:
        """Get the current game mode."""
        return self.GetGameMode()

    def set_chat_time(self, chat_time: int) -> bool:
        """Set a new chat time value in milliseconds (actually chat time is the duration of the end race podium,
        0 means no podium displayed.). Only available to Admin."""
        return self.SetChatTime(chat_time)

    def get_chat_time(self) -> StateValue:
        """Get the current and next chat time. The struct returned contains two fields CurrentValue and NextValue."""
        return StateValue(*self.GetChatTime().values())

    def set_finish_timeout(self, timeout: int) -> bool:
        """Set a new finish timeout (for rounds/laps mode) value in milliseconds. 0 means default.
        1 means adaptative to the duration of the challenge. Only available to Admin.
        Requires a challenge restart to be taken into account."""
        return self.SetFinishTimeout(timeout)

    def get_finish_timeout(self) -> StateValue:
        """Get the current and next FinishTimeout. The struct returned contains two fields CurrentValue and
        NextValue."""
        return StateValue(*self.GetFinishTimeout().values())

    def set_all_warm_up_duration(self, warm_up: int) -> bool:
        """Set whether to enable the automatic warm-up phase in all modes. 0 = no, otherwise its the duration
        of the phase, expressed in number of rounds (in rounds/team mode), or in number of times the gold medal
        time (other modes). Only available to Admin. Requires a challenge restart to be taken into account."""
        return self.SetAllWarmUpDuration(warm_up)

    def get_all_warm_up_duration(self) -> StateValue:
        """Get whether the automatic warm-up phase is enabled in all modes. The struct returned contains two
        fields CurrentValue and NextValue."""
        return StateValue(*self.GetAllWarmUpDuration().values())

    def set_disable_respawn(self, respawn: bool) -> bool:
        """Set whether to disallow players to respawn. Only available to Admin. Requires a challenge restart to
        be taken into account."""
        return self.SetDisableRespawn(respawn)

    def get_disable_respawn(self) -> StateValue:
        """Get whether players are disallowed to respawn. The struct returned contains two fields CurrentValue
        and NextValue."""
        return StateValue(*self.GetDisableRespawn().values())

    def set_force_show_all_opponents(self, opponents_display: int) -> bool:
        """Set whether to override the players preferences and always display all opponents (0=no override,
        1=show all, other value=minimum number of opponents). Only available to Admin. Requires a challenge restart
        to be taken into account."""
        return self.SetForceShowAllOpponents(opponents_display)

    def get_force_show_all_opponents(self) -> StateValue:
        """Get whether players are forced to show all opponents. The struct returned contains two fields CurrentValue
        and NextValue."""
        return StateValue(*self.GetForceShowAllOpponents().values())

    def set_time_attack_limit(self, time_limit: int) -> bool:
        """Set a new time limit for time attack mode. Only available to Admin. Requires a challenge restart to be
        taken into account."""
        return self.SetTimeAttackLimit(time_limit)

    def get_time_attack_limit(self) -> StateValue:
        """Get the current and next time limit for time attack mode. The struct returned contains two fields
        CurrentValue and NextValue."""
        return StateValue(*self.GetTimeAttackLimit().values())

    def set_time_attack_synch_start_period(self, start_period: int) -> bool:
        """Set a new synchronized start period for time attack mode. Only available to Admin. Requires a challenge
        restart to be taken into account."""
        return self.SetTimeAttackSynchStartPeriod(start_period)

    def get_time_attack_synch_start_period(self) -> StateValue:
        """Get the current and synchronized start period for time attack mode. The struct returned contains two
        fields CurrentValue and NextValue."""
        return StateValue(*self.GetTimeAttackSynchStartPeriod().values())

    def set_laps_time_limit(self, time_limit: int) -> bool:
        """Set a new time limit for laps mode. Only available to Admin. Requires a challenge restart to be taken
        into account."""
        return self.SetLapsTimeLimit(time_limit)

    def get_laps_time_limit(self) -> StateValue:
        """Get the current and next time limit for laps mode. The struct returned contains two fields CurrentValue
        and NextValue."""
        return StateValue(*self.GetLapsTimeLimit().values())

    def set_nb_laps(self, number_of_laps: int) -> bool:
        """Set a new number of laps for laps mode. Only available to Admin. Requires a challenge restart to be
        taken into account."""
        return self.SetNbLaps(number_of_laps)

    def get_nb_laps(self) -> StateValue:
        """Get the current and next number of laps for laps mode. The struct returned contains two fields
        CurrentValue and NextValue."""
        return StateValue(*self.GetNbLaps().values())

    def set_round_forced_laps(self, number_of_laps: int) -> bool:
        """Set a new number of laps for rounds mode (0 = default, use the number of laps from the challenges,
        otherwise forces the number of rounds for multilaps challenges). Only available to Admin. Requires a
        challenge restart to be taken into account."""
        return self.SetRoundForcedLaps(number_of_laps)

    def get_round_forced_laps(self) -> StateValue:
        """Get the current and next number of laps for rounds mode. The struct returned contains two fields
        CurrentValue and NextValue."""
        return StateValue(*self.GetRoundForcedLaps().values())

    def set_round_points_limit(self, points_limit: int) -> bool:
        """Set a new points limit for rounds mode (value set depends on UseNewRulesRound). Only available to Admin.
        Requires a challenge restart to be taken into account."""
        return self.SetRoundPointsLimit(points_limit)

    def get_round_points_limit(self) -> StateValue:
        """Get the current and next points limit for rounds mode (values returned depend on UseNewRulesRound).
        The struct returned contains two fields CurrentValue and NextValue."""
        return StateValue(*self.GetRoundPointsLimit().values())

    def set_round_custom_points(self, custom_points: List[int]) -> bool:
        """Set the points used for the scores in rounds mode. Points is an array of decreasing integers for the
        players from the first to last. And you can add an optional boolean to relax the constraint checking
        on the scores. Only available to Admin."""
        return self.SetRoundCustomPoints(custom_points)

    def get_round_custom_points(self) -> List[int]:
        """Gets the points used for the scores in rounds mode."""
        return self.GetRoundCustomPoints()

    def set_use_new_rules_round(self, new_rules: bool) -> bool:
        """Set if new rules are used for rounds mode. Only available to Admin. Requires a challenge restart to be
        taken into account."""
        return self.SetUseNewRulesRound(new_rules)

    def get_use_new_rules_round(self) -> StateValue:
        """Get if the new rules are used for rounds mode (Current and next values). The struct returned contains
        two fields CurrentValue and NextValue."""
        return StateValue(*self.GetUseNewRulesRound().values())

    def set_team_points_limit(self, points_limit: int) -> bool:
        """Set a new points limit for team mode (value set depends on UseNewRulesTeam). Only available to Admin.
        Requires a challenge restart to be taken into account."""
        return self.SetTeamPointsLimit(points_limit)

    def get_team_points_limit(self) -> StateValue:
        """Get the current and next points limit for team mode (values returned depend on UseNewRulesTeam).
        The struct returned contains two fields CurrentValue and NextValue."""
        return StateValue(*self.GetTeamPointsLimit().values())

    def set_max_points_team(self, max_points: int) -> bool:
        """Set a new number of maximum points per round for team mode. Only available to Admin. Requires a
        challenge restart to be taken into account."""
        return self.SetMaxPointsTeam(max_points)

    def get_max_points_team(self) -> StateValue:
        """Get the current and next number of maximum points per round for team mode. The struct returned contains
        two fields CurrentValue and NextValue."""
        return StateValue(*self.GetMaxPointsTeam().values())

    def set_use_new_rules_team(self, team_mode: bool) -> bool:
        """Set if new rules are used for team mode. Only available to Admin. Requires a challenge restart to be
        taken into account."""
        return self.SetUseNewRulesTeam(team_mode)

    def get_use_new_rules_team(self) -> StateValue:
        """Get if the new rules are used for team mode (Current and next values). The struct returned contains
        two fields CurrentValue and NextValue."""
        return StateValue(*self.GetUseNewRulesTeam().values())

    def set_cup_points_limit(self, points: int) -> bool:
        """Set the points needed for victory in Cup mode. Only available to Admin. Requires a challenge restart
        to be taken into account."""
        return self.SetCupPointsLimit(points)

    def get_cup_points_limit(self) -> StateValue:
        """Get the points needed for victory in Cup mode. The struct returned contains two fields CurrentValue
        and NextValue."""
        return StateValue(*self.GetCupPointsLimit().values())

    def set_cup_rounds_per_challenge(self, number_of_rounds: int) -> bool:
        """Sets the number of rounds before going to next challenge in Cup mode. Only available to Admin.
        Requires a challenge restart to be taken into account."""
        return self.SetCupRoundsPerChallenge(number_of_rounds)

    def get_cup_rounds_per_challenge(self) -> StateValue:
        """Get the number of rounds before going to next challenge in Cup mode. The struct returned contains
        two fields CurrentValue and NextValue."""
        return StateValue(*self.GetCupRoundsPerChallenge().values())

    def set_cup_warm_up_duration(self, number_of_rounds: int) -> bool:
        """Set whether to enable the automatic warm-up phase in Cup mode. 0 = no, otherwise its the duration of
        the phase, expressed in number of rounds. Only available to Admin. Requires a challenge restart to be
        taken into account."""
        return self.SetCupWarmUpDuration(number_of_rounds)

    def get_cup_warm_up_duration(self) -> StateValue:
        """Get whether the automatic warm-up phase is enabled in Cup mode. The struct returned contains two fields
        CurrentValue and NextValue."""
        return StateValue(*self.GetCupWarmUpDuration().values())

    def set_cup_nb_winners(self, number_of_winners: int) -> bool:
        """Set the number of winners to determine before the match is considered over. Only available to Admin.
        Requires a challenge restart to be taken into account."""
        return self.SetCupNbWinners(number_of_winners)

    def get_cup_nb_winners(self) -> StateValue:
        """Get the number of winners to determine before the match is considered over. The struct returned contains
        two fields CurrentValue and NextValue."""
        return StateValue(*self.GetCupNbWinners().values())

    def get_current_challenge_index(self) -> int:
        """Returns the current challenge index in the selection, or -1 if the challenge is no longer in the
        selection."""
        return self.GetCurrentChallengeIndex()

    def get_next_challenge_index(self) -> int:
        """Returns the challenge index in the selection that will be played next (unless the current one is
        restarted...)"""
        return self.GetNextChallengeIndex()

    def set_next_challenge_index(self, challenge_index: int) -> bool:
        """Sets the challenge index in the selection that will be played next (unless the current one is
        restarted...)"""
        return self.SetNextChallengeIndex(challenge_index)

    def get_current_challenge_info(self) -> ChallengeInfo:
        """Returns a struct containing the infos for the current challenge. The struct contains the following
        fields : Name, UId, FileName, Author, Environnement, Mood, BronzeTime, SilverTime, GoldTime, AuthorTime,
        CopperPrice, LapRace, NbLaps and NbCheckpoints."""
        return ChallengeInfo(*self.GetCurrentChallengeInfo().values())

    def get_next_challenge_info(self) -> ChallengeInfo:
        """Returns a struct containing the infos for the next challenge. The struct contains the following fields:
        Name, UId, FileName, Author, Environnement, Mood, BronzeTime, SilverTime, GoldTime, AuthorTime, CopperPrice
        and LapRace. (NbLaps and NbCheckpoints are also present but always set to -1)"""
        return ChallengeInfo(*self.GetNextChallengeInfo().values())

    def get_challenge_info(self, filename: str) -> ChallengeInfo:
        """Returns a struct containing the infos for the challenge with the specified filename. The struct contains
        the following fields : Name, UId, FileName, Author, Environnement, Mood, BronzeTime, SilverTime, GoldTime,
        AuthorTime, CopperPrice and LapRace. (NbLaps and NbCheckpoints are also present but always set to -1)"""
        return ChallengeInfo(*self.GetChallengeInfo(filename).values())

    def check_challenge_for_current_server_params(self, filename: str) -> bool:
        """Returns a boolean if the challenge with the specified filename matches the current server settings."""
        return self.CheckChallengeForCurrentServerParams(filename)

    def get_challenge_list(self, max_number_of_infos: int, starting_index: int) -> List[ChallengeInfo]:
        """Returns a list of challenges among the current selection of the server. This method take two parameters.
        The first parameter specifies the maximum number of infos to be returned, and the second one the starting
        index in the selection. The list is an array of structures. Each structure contains the following fields :
        Name, UId, FileName, Environnement, Author, GoldTime and CopperPrice."""
        return [ChallengeInfo(*result.values()) for result in
                self.GetList[ChallengeInfo](max_number_of_infos, starting_index)]

    def add_challenge(self, filename: str) -> bool:
        """Add the challenge with the specified filename at the end of the current selection.
        Only available to Admin."""
        return self.AddChallenge(filename)

    def add_challenge_list(self, filenames: List[str]) -> int:
        """Add the list of challenges with the specified filenames at the end of the current selection.
        The list of challenges to add is an array of strings. Only available to Admin."""
        return self.AddList[ChallengeInfo](filenames)

    def remove_challenge(self, filename: str) -> bool:
        """Remove the challenge with the specified filename from the current selection. Only available to Admin."""
        return self.RemoveChallenge(filename)

    def remove_challenge_list(self, filenames: List[str]) -> int:
        """Remove the list of challenges with the specified filenames from the current selection.
        The list of challenges to remove is an array of strings. Only available to Admin."""
        return self.RemoveList[ChallengeInfo](filenames)

    def insert_challenge(self, filename: str) -> bool:
        """Insert the challenge with the specified filename after the current challenge. Only available to Admin."""
        return self.InsertChallenge(filename)

    def insert_challenge_list(self, filenames: List[str]) -> int:
        """Insert the list of challenges with the specified filenames after the current challenge.
        The list of challenges to insert is an array of strings. Only available to Admin."""
        return self.InsertList[ChallengeInfo](filenames)

    def choose_next_challenge(self, filename: str) -> bool:
        """Set as next challenge the one with the specified filename, if it is present in the selection.
        Only available to Admin."""
        return self.ChooseNextChallenge(filename)

    def choose_next_challenge_list(self, filenames: List[str]) -> int:
        """Set as next challenges the list of challenges with the specified filenames,
        if they are present in the selection. The list of challenges to choose is an array of strings.
        Only available to Admin."""
        return self.ChooseNextList[ChallengeInfo](filenames)

    def load_match_settings(self, filename) -> int:
        """Set a list of challenges defined in the playlist with the specified filename as the current selection
        of the server, and load the gameinfos from the same file. Only available to Admin."""
        return self.LoadMatchSettings(filename)

    def append_playlist_from_match_settings(self, filename: str) -> int:
        """Add a list of challenges defined in the playlist with the specified filename at the end of the current
        selection. Only available to Admin."""
        return self.AppendPlaylistFromMatchSettings(filename)

    def save_match_settings(self, filename: str) -> int:
        """Save the current selection of challenge in the playlist with the specified filename,
        as well as the current gameinfos. Only available to Admin."""
        return self.SaveMatchSettings(filename)

    def insert_playlist_from_match_settings(self, filename: str) -> int:
        """Insert a list of challenges defined in the playlist with the specified filename after the current challenge.
        Only available to Admin."""
        return self.InsertPlaylistFromMatchSettings(filename)

    # TODO fix: raise an exception wen given tm_version is set to 1. We should use 1 as default (TM FOREVER)
    def get_player_info(self, login: str, tm_version: int = 1) -> PlayerInfo:
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
        return PlayerInfo(*self.GetPlayerInfo(login, tm_version).values())

    def get_detailed_player_info(self, login) -> DetailedPlayerInfo:
        """Returns a struct containing the infos on the player with the specified login.
        The structure contains the following fields : Login, NickName, PlayerId, TeamId, IPAddress,
        DownloadRate, UploadRate, Language, IsSpectator, IsInOfficialMode, a structure named Avatar,
        an array of structures named Skins, a structure named LadderStats, HoursSinceZoneInscription
        and OnlineRights (0: nations account, 3: united account). Each structure of the array Skins contains
        two fields Environnement and a struct PackDesc. Each structure PackDesc, as well as the struct Avatar,
        contains two fields FileName and Checksum."""
        return DetailedPlayerInfo(*self.GetDetailedPlayerInfo(login).values())

    def get_player_list(self,
                        max_number_of_infos: int,
                        starting_index: int = 0,
                        compatibility: int = 1) -> List[PlayerInfo]:
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
        return [PlayerInfo(*result.values()) for result in
                self.GetPlayerList(max_number_of_infos, starting_index, compatibility)]

    def get_main_server_player_info(self, compatibility: int = 1) -> PlayerInfo:
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
        return PlayerInfo(*self.GetMainServerPlayerInfo(compatibility).values())

    def get_current_ranking(self, max_number_of_infos: int, starting_index: int) -> List[PlayerRanking]:
        """Returns the current rankings for the race in progress. (in team mode, the scores for the two
        teams are returned. In other modes, its the individual players scores) This method take two parameters.
        The first parameter specifies the maximum number of infos to be returned, and the second one the starting
        index in the ranking. The ranking returned is a list of structures. Each structure contains the following
        fields : Login, NickName, PlayerId, Rank, BestTime, Score, NbrLapsFinished and LadderScore.
        It also contains an array BestCheckpoints that contains the checkpoint times for the best race."""
        return [PlayerRanking(*result.values()) for result in
                self.GetCurrentRanking(max_number_of_infos, starting_index)]

    def get_current_ranking_for_login(self, logins) -> List[PlayerRanking]:
        """Returns the current ranking for the race in progressof the player with the specified login
        (or list of comma-separated logins). The ranking returned is a list of structures, that contains the
        following fields : Login, NickName, PlayerId, Rank, BestTime, Score, NbrLapsFinished and LadderScore.
        It also contains an array BestCheckpoints that contains the checkpoint times for the best race."""
        return [PlayerRanking(*result.values()) for result in self.GetCurrentRankingForLogin(logins)]

    def force_scores(self, player_score: PlayerScore, silent_mode: bool) -> bool:
        """Force the scores of the current game. Only available in rounds and team mode. You have to pass an
        array of structs {int PlayerId, int Score}. And a boolean SilentMode - if true, the scores are silently
        updated (only available for SuperAdmin), allowing an external controller to do its custom counting...
        Only available to Admin/SuperAdmin."""
        return self.ForceScores(player_score, silent_mode)

    def force_player_team(self, login: str, team_id: int) -> bool:
        """Force the team of the player. Only available in team mode. You have to pass the login and the
        team number (0 or 1). Only available to Admin."""
        return self.ForcePlayerTeam(login, team_id)

    def force_player_team_id(self, player_id: int, team_id: int) -> bool:
        """Force the team of the player. Only available in team mode. You have to pass the playerid and the
        team number (0 or 1). Only available to Admin."""
        return self.ForcePlayerTeamId(player_id, team_id)

    def force_spectator(self, login: str, spectator_mode: int) -> bool:
        """Force the spectating status of the player. You have to pass the login and the spectator mode
        (0: user selectable, 1: spectator, 2: player). Only available to Admin."""
        return self.ForceSpectator(login, spectator_mode)

    def force_spectator_id(self, player_id: int, spectator_mode: int) -> bool:
        """Force the spectating status of the player. You have to pass the playerid and the spectator mode
        (0: user selectable, 1: spectator, 2: player). Only available to Admin."""
        return self.ForceSpectatorId(player_id, spectator_mode)

    def force_spectator_target(self, login: str, target: str, camera_type: int) -> bool:
        """Force spectators to look at a specific player. You have to pass the login of the spectator
        (or  for all) and the login of the target (or  for automatic), and an integer for the camera type to use
        (-1 = leave unchanged, 0 = replay, 1 = follow, 2 = free). Only available to Admin."""
        return self.ForceSpectatorTarget(login, target, camera_type)

    def force_spectator_target_id(self, spectator_id: int, target_id: int, camera_type: int) -> bool:
        """Force spectators to look at a specific player. You have to pass the id of the spectator (or -1 for all)
        and the id of the target (or -1 for automatic), and an integer for the camera type to use
        (-1 = leave unchanged, 0 = replay, 1 = follow, 2 = free). Only available to Admin."""
        return self.ForceSpectatorTargetId(spectator_id, target_id, camera_type)

    def spectator_release_player_slot(self, login: str) -> bool:
        """Pass the login of the spectator. A spectator that once was a player keeps his player slot,
        so that he can go back to race mode. Calling this function frees this slot for another player to connect.
        Only available to Admin."""
        return self.SpectatorReleasePlayerSlot(login)

    def spectator_release_player_slot_id(self, player_id: int) -> bool:
        """Pass the playerid of the spectator. A spectator that once was a player keeps his player slot,
        so that he can go back to race mode. Calling this function frees this slot for another player to connect.
        Only available to Admin."""
        return self.SpectatorReleasePlayerSlotId(player_id)

    def manual_flow_control_enable(self, flow: bool) -> bool:
        """Enable control of the game flow: the game will wait for the caller to validate state transitions.
        Only available to Admin."""
        return self.ManualFlowControlEnable(flow)

    def manual_flow_control_proceed(self) -> bool:
        """Allows the game to proceed. Only available to Admin."""
        return self.ManualFlowControlProceed()

    def manual_flow_control_is_enabled(self) -> int:
        """Returns whether the manual control of the game flow is enabled. 0 = no, 1 = yes by the xml-rpc
        client making the call, 2 = yes, by some other xml-rpc client. Only available to Admin."""
        return self.ManualFlowControlIsEnabled()

    def manual_flow_control_get_cur_transition(self) -> str:
        """Returns the transition that is currently blocked, or  if none.
        (Thats exactly the value last received by the callback.) Only available to Admin."""
        return self.ManualFlowControlGetCurTransition()

    def check_end_match_condition(self) -> str:
        """Returns the current match ending condition. Return values are: Playing, ChangeMap or Finished."""
        return self.CheckEndMatchCondition()

    def get_network_stats(self) -> NetworkStats:
        """Returns a struct containing the networks stats of the server. The structure contains the following fields :
        Uptime, NbrConnection, MeanConnectionTime, MeanNbrPlayer, RecvNetRate, SendNetRate, TotalReceivingSize,
        TotalSendingSize and an array of structures named PlayerNetInfos. Each structure of the array PlayerNetInfos
        contains the following fields : Login, IPAddress, LastTransferTime, DeltaBetweenTwoLastNetState,
        PacketLossRate. Only available to SuperAdmin."""
        return NetworkStats(*self.GetNetworkStats().values())

    def start_server_lan(self) -> bool:
        """Start a server on lan, using the current configuration. Only available to SuperAdmin."""
        return self.StartServerLan()

    def start_server_internet(self, login: str, password: str) -> bool:
        """Start a server on internet using the Login and Password specified in the struct passed as parameters.
        Only available to SuperAdmin."""
        return self.StartServerInternet(login, password)

    def get_status(self) -> Status:
        """Returns the current status of the server."""
        return Status(*self.GetStatus().values())

    def quit_game(self) -> bool:
        """Quit the application. Only available to SuperAdmin."""
        return self.QuitGame()

    def game_data_directory(self) -> str:
        """Returns the path of the game datas directory. Only available to Admin."""
        return self.GameDataDirectory()

    def get_tracks_directory(self) -> str:
        """Returns the path of the tracks directory. Only available to Admin."""
        return self.GetTracksDirectory()

    def get_skins_directory(self) -> str:
        """Returns the path of the skins directory. Only available to Admin."""
        return self.GetSkinsDirectory()


class Method:
    def __init__(self, send, name):
        self._send = send
        self._name = name

    def __getattr__(self, name):
        return Method(self._send, f'{self._name}.{name}')

    def __call__(self, *args):
        if 'noresponse.' in self._name:
            self._name = self._name.replace('noresponse.', '')
        return self._send(self._name, args)

    def set_send(self, send):
        self._send = send
