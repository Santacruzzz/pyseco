from src.controllers.controller import Controller


class AdminController(Controller):
    def kick(self, login, message):
        if self.pyseco.is_player_on_server(login):
            self.pyseco.rpc.kick(login, message)
            self.pyseco.server_message(f'{login} was kicked')
        else:
            self.pyseco.server_message(f'{login} not found')


    def restart_challenge(self):
        self.pyseco.rpc.restart_challenge()
        self.pyseco.server_message(f'Challenge was restarted')

    def skip(self):
        self.pyseco.rpc.next_challenge()
        self.pyseco.server_message(f'Challenge was skipped')

