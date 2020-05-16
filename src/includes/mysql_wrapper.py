import pymysql
from src.includes.config import Config


class MySqlWrapper:
    PLAYERS = 'players'
    CHALLENGES = 'challenges'
    RECORDS = 'records'
    RS_KARMA = 'rs_karma'
    RS_RANK = 'rs_rank'
    RS_TIMES = 'rs_times'

    def __init__(self, config: Config):
        self._connection = pymysql.connect(host=config.db_hostname,
                                           user=config.db_user,
                                           password=config.db_password,
                                           db=config.db_name,
                                           charset=config.db_charset,
                                           cursorclass=pymysql.cursors.DictCursor)

    def _get_all_from(self, table):
        with self._connection.cursor() as cursor:
            sql = f'SELECT * from {table}'
            cursor.execute(sql)
            return cursor.fetchall()

    def get_players(self):
        return self._get_all_from(self.PLAYERS)

    def get_challenges(self):
        return self._get_all_from(self.CHALLENGES)
