import mysql.connector
conn = mysql.connector.connect(user='root', password='123456', database='test')


def search(conn,inputs):
    cursor = conn.cursor()
    cursor.execute('select * from user where id = {}'.format(inputs))
    values = cursor.fetchall()
    print(values)