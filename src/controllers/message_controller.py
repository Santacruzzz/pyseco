from src.controllers.controller import Controller
from src.pyseco import Player
from src.utils import strip_size

class MessageController(Controller):
    def show_welcome_message(self, player: Player):
        self.pyseco.server_message(f'{strip_size(player.info.nickname)}$z$s$888 has joined')
        self.pyseco.server_message_to_login(player.info.login, f'$z$s$888Witaj na serwerze {self.pyseco.server.get_name()}')
