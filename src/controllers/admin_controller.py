from src.controllers.controller import Controller


class AdminController(Controller):
    def kick(self, login, message):
        self.pyseco.kick(login, message)
        self.pyseco.server_message(f'{login} was kicked')

    def restart_challenge(self):
        self.pyseco.restart_challenge()
        self.pyseco.server_message(f'Challenge was restarted')

    def skip(self):
        self.pyseco.next_challenge()
        self.pyseco.server_message(f'Challenge was skipped')

