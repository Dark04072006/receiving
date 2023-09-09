import logging
import pymysql.cursors
from os import getenv
from dotenv import load_dotenv
from pymysqlpool import ConnectionPool

load_dotenv('files/.env')

logger = logging.getLogger(__name__)


config = dict(
    host=getenv("HOST"),
    port=int(getenv("PORT")),
    user=getenv("USERDB"),
    password=getenv('PASSWORD'),
    db=getenv('DB'),
    cursorclass=pymysql.cursors.DictCursor
)


class Database:
    def __init__(self):
        self.pool = ConnectionPool(
            size=3,
            maxsize=5,
            pre_create_num=2,
            name='pool1',
            **config
        )

    def execute_query(self, query: str):
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            logger.error(e)
        finally:
            conn.close()
