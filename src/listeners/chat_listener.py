from inspect import signature
from src.includes.log import setup_logger

from src.pyseco import Listener
from src.includes.events_types import *
from src.controllers.admin_controller import AdminController
from src.utils import CommandParser
from src.errors import WrongNumberOfParams

logger = setup_logger(__name__)


class ChatListener(Listener):
    def __init__(self, name: str, pyseco_instance):
        super(ChatListener, self).__init__(name, pyseco_instance)
        self.pyseco.register(EventPlayerChat.name, self.on_player_chat)
        self.admin_controller = AdminController(self.pyseco)

    def on_player_chat(self, data: EventPlayerChat):
        login, text = data.login, data.text
        if text.startswith('*') and login in ['rafallo', 'santacruz7']:
            command, params = CommandParser.parser_regex(AdminController, text)
            params = (login, ) + params
            method = getattr(self.admin_controller, f'{command}')
            sig = signature(method)
            if len(sig.parameters) == len(params):
                method(*params)
            else:
                raise WrongNumberOfParams
