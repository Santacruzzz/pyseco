import pymysql

from src.api.tm_types import ChallengeInfo
from src.includes.config import Config
from src.includes.log import setup_logger

logger = setup_logger(__name__)


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

    def get_records(self, challenge: ChallengeInfo):
        with self._connection.cursor() as cursor:
            sql = 'SELECT c.Id AS ChallengeId, r.Score, p.NickName, p.Login, r.Date, r.Checkpoints '\
                'FROM challenges c '\
                'LEFT JOIN records r ON (r.ChallengeId=c.Id) '\
                'LEFT JOIN players p ON (r.PlayerId=p.Id) '\
                f'WHERE c.Uid="{challenge.uid}" '\
                'GROUP BY r.Id '\
                'ORDER BY r.Score ASC, r.Date ASC '\
                'LIMIT 20'
            logger.info(sql)

            cursor.execute(sql)
            return cursor.fetchall()
