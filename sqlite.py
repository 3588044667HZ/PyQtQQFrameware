import sqlite3


class SqliteSDB(object):
    def __init__(self, path: str, check_same_thread=True) -> None:
        """path是数据库目录"""
        db = sqlite3.connect(path, check_same_thread=check_same_thread)
        self.cu = db.cursor()
        self.close = db.close
        self.commit = db.commit
        self.execute = self.cu.execute
        self.fetchone = self.cu.fetchone
        self.fetchall = self.cu.fetchall

    # 'create table if not exists book(id primary key,name,tel)'
    def create_table(self, table_name, *args):
        try:
            # self.execute('create table %s %s' % (table_name, str(args).replace(r"'", '')))
            self.execute('create table if not exists %s %s' % (table_name, str(args).replace(r"'", '')))
            self.commit()
            return True
        except BaseException as e:
            print('\033[31m数据库错误,{}\033[0m'.format(e))
            return False

    def insert(self, table_name, *args):
        """table_name:表名"""
        try:
            args = [f"'{arg}'" if isinstance(arg, str) else str(arg) for arg in args]
            self.execute("insert into %s values (%s)" % (
                table_name, ", ".join(args)
            ))
            self.commit()
            return True
        except BaseException as e:
            print('\033[31m数据库错误,{}\033[0m'.format(e))
            return False

    def insert_tuple(self, table_name: str, key: tuple, value: tuple):
        try:
            self.execute("insert into %s %s values %s" % (table_name, str(key), str(value)))
            self.commit()
            return True
        except BaseException as e:
            print('\033[31m数据库错误,{}\033[0m'.format(e))
            return False

    def insert_dic(self, table_name, dic: dict):
        key = list()
        value = list()
        for i in dic:
            key.append(i)
            value.append(dic[i])
        try:
            self.execute("insert into %s %s values %s" % (table_name, str(tuple(key)), str(tuple(value))))
            self.commit()
        except sqlite3.IntegrityError:
            print('数据库错误，主键重复')

    def select(self, table_name: str, **params) -> list:
        self.execute("select * from %s where %s" % (
            table_name, " and ".join(
                [f"{key}={params[key]}" for key in params])
        ))
        return self.fetchall()

    def selectAll(self, tableName: str):
        self.execute("select * from %s" % tableName)
        return self.fetchall()

    def exist(self, table_name: str, **params) -> bool:
        """返回是否存在"""
        return bool(self.select(table_name, **params))

    def update(self, table_name: str, *args, **params):
        args = " ".join(args)
        params = " ".join([f"{key}={params[key]}" for key in params])
        # print("update %s set %s where %s" % (
        #     table_name, args, params
        # ))
        self.execute("update %s set %s where '%s'" % (
            table_name, args, params
        ))
        self.commit()

    def delete(self, table_name: str, **params):
        # print("delete from %s where %s" % (
        #     table_name, "".join([f"{key}={params[key]}" for key in params])
        # ))
        """删除数据"""
        self.execute("delete from %s where '%s'" % (
            table_name, "".join([f"{key}={params[key]}" for key in params])
        ))
        self.commit()

    def count(self, table_name: str) -> int:
        try:
            self.execute("select count(*) from %s" % (table_name))
            return self.fetchone()[0]
        except sqlite3.OperationalError:
            return -1

    def close(self):
        self.cu.close()
        self.close()

if __name__ == '__main__':
    s = SqliteSDB('data.db')
    s.create_table('friends ', 'ID INT PRIMARY KEY NOT NULL', 'NAME TEXT NOT NULL')
    s.insert('friends', '2', '666')
    # s.insert_tuple('friends', ('id', 'name'), ('6', '888'))
    # s.insert_dic('friends', {'ID': '0', 'NAME': 'wang'})
    # print(s.select('friends', id=0))
    s.update('friends', ' name=1', ID=1)
# s.delete('friends', id=1)
# print(s.count('friends'))
