#https://www.liaoxuefeng.com/wiki/1016959663602400/1017802264972000
import mysql.connector

conn = mysql.connector.connect(user='root', password='123456', database='test')
cursor = conn.cursor()
# 创建user表:
cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
# 插入一行记录，注意MySQL的占位符是%s:
cursor.execute('insert into user (id, name) values (%s, %s)', ['1', 'Michael'])
#该占位符现也可以用{}+format的组合表示。

print(cursor.rowcount)
# 1
# 提交事务:
conn.commit()
cursor.close()
# 运行查询:
cursor = conn.cursor()
cursor.execute('select * from user where id = %s', ('1',))
values = cursor.fetchall()
print(values)
# [('1', 'Michael')]
# 关闭Cursor和Connection:
cursor.close()
conn.close()