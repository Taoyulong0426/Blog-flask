from pymysql import connect
from pymysql.cursors import DictCursor

from config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE


class Admin:
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

    def select_admin(self, adminid, password):
        # print('select admin')
        # mysql语句
        select_admin_sql = 'select * from admin where admin_id="%s" and admin_password="%s";' % (adminid, password)
        # 执行mysql语句
        result = self.cursor.execute(select_admin_sql)
        # 如果返回了一条数据，则登录成功，否则登录失败
        if 1 == result:
            result = True
        else:
            result = False
            print('there is no administrator where adminid="%s" and password="%s"!!' % (adminid, password))
        return result

    def select_admin_without_password(self, adminid):
        select_sql = 'select * from admin where admin_id="%s";' % adminid
        self.cursor.execute(select_sql)
        result = self.cursor.fetchall()
        return result

    def fix_admin_information(self, data: dict):
        admin_id = data['admin_id']
        strs = []
        set = ""
        for k, v in data.items():
            if v != '':
                if k != 'admin_id':
                    str = k + "=" + "'" + v + "'"
                    strs.append(str)
        for i in range(len(strs)):
            if i != len(strs) - 1:
                set = set + strs[i] + ", "
            else:
                set = set + strs[i]
        try:
            if set != "":
                fix_user_sql = "update admin set " + set + " where admin_id=" + "'" + admin_id + "';"
                print(fix_user_sql)
                result = self.cursor.execute(fix_user_sql)
                self.conn.commit()
                print("number changed: ", result)
            else:
                return 0
            print('success')
        except:
            print('failed')
            result = 0
        finally:
            return result
