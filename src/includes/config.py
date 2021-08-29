import yaml

class Config():
    def __init__(self, config_file):
        self._config = yaml.safe_load(open(config_file))
        self.prefix = self._config['prefix']
        self.color = self._config['color']
        self.tm_login = self._config['tm_login']
        self.rpc_login = self._config['rpc_login']
        self.rpc_password = self._config['rpc_password']
        self.rpc_ip = self._config['rpc_ip']
        self.rpc_port = self._config['rpc_port']
        self.db_user = self._config['db_user']
        self.db_password = self._config['db_password']
        self.db_name = self._config['db_name']
        self.db_charset = self._config['db_charset']
        self.db_hostname = self._config['db_hostname']