from pymysql import connect
from pymysql.cursors import DictCursor

from config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE


class User:
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

    def select_user(self, username, user_password):
        # print('select user')
        # mysql语句
        select_user_sql = 'select * from user where username="%s" and user_password="%s";' % (username, user_password)
        # 执行mysql语句
        result = self.cursor.execute(select_user_sql)
        # 如果返回了一条数据，则登录成功，否则登录失败
        if 1 == result:
            result = True
        else:
            result = False
            print('there is no user where username="%s" and password="%s"!!' % (username, user_password))
        return result

    def insert_user(self, data: dict) -> bool:
        keys = ''
        values = ''
        for k, v in data.items():
            keys += k
            keys += ','
            values += "'"
            values += v
            values += "'"
            values += ','
        keys = keys[:-1]
        values = values[:-1]
        insert_user_sql = "INSERT INTO user({}) values({});".format(keys, values)
        print(insert_user_sql)
        # 执行mysql语句，如果插入成功，则注册成功，否则注册失败
        try:
            self.cursor.execute(insert_user_sql)
            self.conn.commit()
            print('success')
            result = True
        except:
            print('failed')
            self.conn.rollback()
            result = False
        finally:
            return result

    def update_user_info(self, data: dict) -> bool:
        username = data['username']
        phone_number = data['phone_number']
        gender = data['gender']
        sql = "UPDATE user SET phone_number='{}', gender='{}' WHERE username='{}'".format(phone_number, gender,
                                                                                          username)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            print('success')
            result = True
        except:
            print('failed')
            self.conn.rollback()
            result = False
        finally:
            return result

    def update_user(self, data: dict, user_id) -> bool:
        for key, value in data.items():
            update_user_sql = "UPDATE user SET {}='{}' WHERE user_id={};".format(key, value, user_id)
            print(update_user_sql)
            self.cursor.execute(update_user_sql)

        # 执行mysql语句，如果插入成功，则注册成功，否则注册失败
        try:
            self.conn.commit()
            print('success')
            result = True
        except:
            print('failed')
            self.conn.rollback()
            result = False
        finally:
            return result

    def get_user_info_by_name(self, username, word='*') -> dict:
        get_user_info_sql = "SELECT {} from user WHERE username='{}'".format(word, username)
        self.cursor.execute(get_user_info_sql)
        return self.cursor.fetchone()

    def reset_password(self, email) -> bool:
        reset_password_sql = "UPDATE user SET user_password='123456' where email='{}'".format(email)
        self.cursor.execute(reset_password_sql)
        try:
            self.conn.commit()
            print('success')
            result = True
        except:
            self.conn.rollback()
            result = False
        return result

    def get_user_info_by_email(self, email, word='*') -> dict:
        get_user_info_sql = "SELECT {} from user WHERE email='{}'".format(word, email)
        print(get_user_info_sql)
        self.cursor.execute(get_user_info_sql)
        user_info = self.cursor.fetchone()
        print(user_info)
        return user_info

    def select_user_with_conditions(self, data: dict):
        strs = []
        condition = ""
        # print(data)
        for k, v in data.items():
            if v != '':
                str = k + "=" + "'" + v + "'"
                strs.append(str)
        # print(strs)
        for i in range(len(strs)):
            if i != len(strs) - 1:
                condition = condition + strs[i] + " and "
            else:
                condition = condition + strs[i]
        # print("condition:", condition)
        if condition != '':
            select_user_conditionally_sql = "select * from user where " + condition + ";"
            self.cursor.execute(select_user_conditionally_sql)
        else:
            select_sql = "select * from user;"
            self.cursor.execute(select_sql)

        result = self.cursor.fetchall()
        print(result)
        return result

    def fix_user_information(self, data: dict):
        u_id = data['user_id']
        strs = []
        set = ""
        for k, v in data.items():
            if v != '':
                if k != 'user_id':
                    str = k + "=" + "'" + v + "'"
                    strs.append(str)
        for i in range(len(strs)):
            if i != len(strs) - 1:
                set = set + strs[i] + ", "
            else:
                set = set + strs[i]
        try:
            if set != "":
                fix_user_sql = "update user set " + set + " where user_id=" + "'" + u_id + "';"
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

    def select_byname(self, uname):
        sql = 'select * from user where username = "%s";' % uname
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def getInfoByUsername(self, username) -> dict:
        sql = 'select * from user where username = "%s";' % username
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result

    def select_user_byname(self, username):
        # print('select user')
        # mysql语句
        select_user_sql = 'select * from user where username="%s" ;' % username
        # 执行mysql语句
        result = self.cursor.execute(select_user_sql)
        # 如果返回了一条数据，则说明已经存在该昵称
        if 1 == result:
            result = True
        else:
            result = False
        return result

    def changename_byname(self, newname, username):
        # print('select user')
        # mysql语句
        update_user_sql = 'update user set username = ' + "%s " + ' WHERE username = %s ;'
        # 执行mysql语句
        result = self.cursor.execute(update_user_sql, (newname, username))

        if 1 == result:
            try:
                self.conn.commit()
                result = True
            except:
                self.conn.rollback()
                result = False
        else:
            result = False
        return result

    def change_email_by_name(self, email, username):
        # print('select user')
        # mysql语句
        update_user_sql = 'update user set email = ' + "%s " + ' WHERE username = %s ;'
        # 执行mysql语句
        result = self.cursor.execute(update_user_sql, (email, username))
        if 1 == result:
            try:
                self.conn.commit()
                result = True
            except:
                self.conn.rollback()
                result = False
        else:
            result = False
        return result

    def changegender_byname(self, newgender, username):
        # print('select user')
        # mysql语句
        update_user_sql = 'update user set gender = ' + "%s " + ' WHERE username = %s ;'
        # 执行mysql语句
        result = self.cursor.execute(update_user_sql, (newgender, username))
        self.conn.commit()
        if 1 == result:
            result = True
        else:
            result = False
        return result

    def changenum_byname(self, newnum, username):
        # print('select user')
        # mysql语句
        update_user_sql = 'update user set phone_number = ' + "%s " + ' WHERE username = %s ;'
        # 执行mysql语句
        result = self.cursor.execute(update_user_sql, (newnum, username))
        print(result)
        self.conn.commit()
        if 1 == result:
            result = True
        else:
            result = False
        return result

    def changepsd_byname(self, newpsd, username):
        # print('select user')
        # mysql语句
        update_user_sql = 'update user set user_password = ' + "%s " + ' WHERE username = %s ;'
        # 执行mysql语句
        result = self.cursor.execute(update_user_sql, (newpsd, username))
        print(result)
        self.conn.commit()
        if 1 == result:
            result = True
        else:
            result = False
        return result

    def changephoto_byname(self, newphoto, username):
        # print('select user')
        # mysql语句
        update_user_sql = 'update user set profile_photo = ' + "%s " + ' WHERE username = %s ;'
        # 执行mysql语句
        try:
            self.cursor.execute(update_user_sql, (newphoto, username))
            self.conn.commit()
            print('success')
            result = True
        except:
            self.conn.rollback()
            result = False
        return result

    def delete_user_with_id(self, user_id):
        delete_sql = 'delete from user where user_id=' + "'" + user_id + "'" + ';'
        print(delete_sql)
        result = self.cursor.execute(delete_sql)
        try:
            self.conn.commit()
        except:
            print('delete failed!')
            result = 0
        finally:
            return result

    def select_user_by_user_id(self, user_id):
        user_info = ''
        sql = "select * from user where user_id = '{}'".format(user_id)
        result = self.cursor.execute(sql)
        if result == 1:
            user_info = self.cursor.fetchone()
        return user_info
