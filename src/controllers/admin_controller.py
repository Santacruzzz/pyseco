from src.controllers.controller import Controller


class AdminController(Controller):
    def kick(self, who, whom, message):
        if self.pyseco.is_player_on_server(whom):
            self.pyseco.msg.show_player_kicked(
                self.pyseco.get_player(who), self.pyseco.get_player(whom))
            self.pyseco.rpc.kick(whom, message)

    def restart(self, who):
        self.pyseco.msg.show_map_restarted(self.pyseco.get_player(who))
        self.pyseco.rpc.restart_challenge()

    def skip(self, who):
        self.pyseco.msg.show_map_skipped(self.pyseco.get_player(who))
        self.pyseco.rpc.next_challenge()

