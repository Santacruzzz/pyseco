from src.server_context import ServerCtx
from src.api.tm_types import ChallengeInfo
from src.api.tm_requests import XmlRpc
from src.pyseco import Player
from src.utils import strip_size
from src.includes.config import Config


class MessageManager():
    def __init__(self, rpc: XmlRpc, config: Config, to_login=None):
        self.rpc = rpc
        self.config = config
        self.text_reset = "$z$s$888"
        self.login = to_login

    def to_login(self, login):
        return MessageManager(self.rpc, self.config, login)

    def _send_message(self, msg):
        if self.login:
            self.rpc.chat_send_server_message_to_login(
                f'{self.config.color}{self.config.prefix}~ {self.text_reset}{msg}', self.login)
        else:
            self.rpc.chat_send_server_message(
                f'{self.config.color}{self.config.prefix}~ {self.text_reset}{msg}')

    def show_welcome_message(self, player: Player, server_name: str):
        self._send_message(f'{player}{self.text_reset} has joined')
        self.to_login(player.info.login)._send_message(f'{self.text_reset}Welcome on {server_name}')

    def show_current_map_info(self, challenge: ChallengeInfo):
        self._send_message(
            f'Current map is {strip_size(challenge.name)}{self.text_reset} author: {challenge.author}')

    def show_player_kicked(self, who: Player, whom: Player):
        self._send_message(f'{who}{self.text_reset} kicks {whom}')

    def show_map_restarted(self, who: Player):
        self._send_message(f'{who}{self.text_reset} restarts challenge')

    def show_map_skipped(self, who: Player):
        self._send_message(f'{who}{self.text_reset} skips challenge')

    def show_player_left(self, player: Player):
        self._send_message(f'{player}{self.text_reset} has left')
