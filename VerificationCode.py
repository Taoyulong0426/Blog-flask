from pymysql import connect
from pymysql.cursors import DictCursor

from config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE


class Token(object):
    def __init__(self):
        self.conn = connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
        )

        self.cursor = self.conn.cursor(DictCursor)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def insert(self, email):
        sql = "insert into token(email, code, time) values ('{}', '0', 0)".format(email)
        self.cursor.execute(sql)
        try:
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def get_info_by_email(self, email) -> dict:
        token_info = ''
        sql = "select * from token where email='{}'".format(email)
        result = self.cursor.execute(sql)
        if result == 1:
            token_info = self.cursor.fetchone()
        return token_info

    def update_token(self, email, code, time) -> bool:
        sql = "update token set code='{}', time='{}'where email='{}'".format(code, time, email)
        self.cursor.execute(sql)
        try:
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def update_email_by_email(self, email_new, email):
        sql = "update token set email='{}' where email='{}'".format(email_new, email)
        self.cursor.execute(sql)
        try:
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def delete_by_email(self, email):
        sql = "delete from token where email='{}'".format(email)
        self.cursor.execute(sql)
        try:
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False
