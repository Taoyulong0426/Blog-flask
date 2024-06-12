from pymysql import connect
from pymysql.converters import escape_string
from pymysql.cursors import DictCursor

from config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE


class Comments:
    def __init__(self):
        self.conn = connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            max_allowed_packet=256*((2**10)**2) #256MB
        )
        self.cursor = self.conn.cursor(DictCursor)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def delete_comment(self, commentid):
        select_user_sql = 'delete from comments where comment_id="%s";' % (commentid)
        # 执行mysql语句
        try:
            result = self.cursor.execute(select_user_sql)
            self.conn.commit()
            result = True
        except:
            result = False
            print('there is no comments where comment_id="%s"!!' % (commentid))
        return result
        # 如果返回了一条数据，则删除成功，否则删除失败

    def select_comment(self, commentid):
        # print('select user')
        # mysql语句
        select_user_sql = 'select * from comments where comment_id="%s";' % (commentid)
        # 执行mysql语句
        result = self.cursor.execute(select_user_sql)
        # 如果返回了一条数据，则登录成功，否则登录失败
        if 1 == result:
            result = True
        else:
            result = False
            print('there is no comments where comment_id="%s"!!' % (commentid))
        return result

    def insert_comment(self, data: dict) -> bool:
        keys = ''
        values = ''
        for k, v in data.items():
            keys += "`"+k+"`"
            keys += ','
            values += "'"
            values += escape_string(str(v))
            values += "'"
            values += ','
        keys = keys[:-1]
        values = values[:-1]
        insert_user_sql = "INSERT INTO comments({}) values({});".format(keys, values)
        print(insert_user_sql)
        # 执行mysql语句，如果插入成功，则注册成功，否则注册失败
        try:
            self.cursor.execute(insert_user_sql)
            self.conn.commit()
            print('success')
            result = True
        except Exception as e:
            print('failed, ', e)
            self.conn.rollback()
            result = False
        finally:
            return result

    def select_comment_with_conditions(self, data:dict):
        strs = []
        condition = ""
        isMultiCondWithHardcond = False

        if not 'hardcond' in data.keys():
            data['hardcond']=''
        for k, v in data.items():
            if (v != '') and (k !='op') and (k !='hardcond'):
                if(k == 'comment_id' or (k == data['hardcond'])):
                    thestr = "`"+k+"`" + "=" + "'" + str(v) + "'"
                else:
                    thestr = "`"+k+"`" + " like " + "'%" + str(v) + "%'"
                strs.append(thestr)

        for i in range(len(strs)):
            if strs[i].startswith("`"+data['hardcond']+"`") and len(strs)>1:
                isMultiCondWithHardcond = True
                del strs[i]

        for i in range(len(strs)):
            if i != len(strs) - 1:
                condition = condition + strs[i] + " "+data['op']+" "
            else:
                condition = condition + strs[i]

        if condition != '':
            select_user_conditionally_sql = "select * from user join comments on `user_id`=`cuser_id` where " + condition + ";"
            if(isMultiCondWithHardcond):
                select_user_conditionally_sql = "select * from ("+select_user_conditionally_sql[:-1]+") cq where `"+data['hardcond']+"`" + "=" + "'" + data[data['hardcond']] + "' order by comment_id;"
            print(select_user_conditionally_sql)
            self.cursor.execute(select_user_conditionally_sql)
        else:
            select_user_conditionally_sql = "select * from user join comments on `user_id`=`cuser_id` order by comment_id;"
            print(select_user_conditionally_sql)
            self.cursor.execute(select_user_conditionally_sql)

        result = self.cursor.fetchall()
        #print(result)
        return result