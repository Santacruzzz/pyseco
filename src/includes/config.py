from dataclasses import dataclass

import yaml


@dataclass
class Config(object):
    prefix: str
    color: str
    tm_login: str
    rcp_login: str
    rcp_password: str
    rcp_ip: str
    rcp_port: int
    db_user: str
    db_password: str
    db_name: str
    db_charset: str
    db_hostname: str

    def __init__(self, config_file):
        self._config = yaml.safe_load(open(config_file))
        self.prefix = self._config['prefix']
        self.color = self._config['color']
        self.tm_login = self._config['tm_login']
        self.rcp_login = self._config['rcp_login']
        self.rcp_password = self._config['rcp_password']
        self.rcp_ip = self._config['rcp_ip']
        self.rcp_port = self._config['rcp_port']
        self.db_user = self._config['db_user']
        self.db_password = self._config['db_password']
        self.db_name = self._config['db_name']
        self.db_charset = self._config['db_charset']
        self.db_hostname = self._config['db_hostname']