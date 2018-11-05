import psycopg2
import logging
import os

logger = logging.getLogger("Gateway")
ema_tab = """CREATE TABLE IF NOT EXISTS ema_dict (
                    period integer PRIMARY KEY NOT NULL, 
                    ema_value float)"""


class DB:
    def __init__(self):
        self.is_connection = False
        #self.url = 'postgres://ecrmfkqqqcvvho:c94e935358c1d75bcd7076c398eefdd32533f4ade481ff9849b6e34d7ee2367a@ec2-54-225-200-15.compute-1.amazonaws.com:5432/d27og9ka9joj6f'
        self.url = os.environ['DATABASE_URL']
        self.conn = self.connect()
        self.create_tab()

    def connect(self):
        try:
            conn = psycopg2.connect(self.url, sslmode='require')
        except Exception as e:
            logger.error('db connection error: {}'.format(e))
        else:
            self.is_connection = True
            logger.info('Success DB connection')
            return conn

    def create_tab(self):
        self.cursor_execute(ema_tab)

    # -----------------ema_dict---------------------

    def get_ema(self):
        ls = self.cursor_execute("select * from ema_dict order by period")
        return {k: v for k, v in ls}

    def set_ema(self, ema_dict):
        query = "BEGIN;\n"
        ema = "insert into ema_dict (period, ema_value) values({}, {}) " \
              "ON CONFLICT (period) DO UPDATE SET ema_value = {};\n"
        for period, value in ema_dict.items():
            query += ema.format(period, value, value)
        query += 'COMMIT;'
        self.cursor_execute(query)

    # -------------------execute----------------------

    def cursor_execute(self, query):
        try:
            cur = self.conn.cursor()
            cur.execute(query)
        except Exception as e:
            logger.error('execute query error: {} in request: {}'.format(e, query))
        else:
            self.conn.commit()
            return cur.fetchall() if cur.description else None