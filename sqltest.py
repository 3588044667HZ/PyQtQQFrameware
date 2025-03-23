import sqlite

#
# cur.execute(
#     'create table if not exists plugin_set(pid int PRIMARY Key not null,name text,author text,ver number,is_enable bool);')
# cur.execute('select * from plugin_set')
# cur.execute('insert into plugin_set (pid name author ver is_enable)')
# name = cur.fetchall()
# print(name)
sql = sqlite.SqliteSDB('./data/data.db')
sql.create_table('plugin_setting', 'pid int PRIMARY Key not null', 'name text', 'author text', 'ver int', 'is_enable bool')
sql.insert('plugin_setting', '123456', 'p1', 'hua', 0.1, 'true')
res = sql.selectAll('plugin_setting')
print(res)
