from pymysql import *

conn = connect(host='localhost',user='root',password='root',database='redbook',port=3306,charset='utf8')
cursor = conn.cursor()

def query(sql,params,type='no_select'):
    params = tuple(params)
    conn.ping(reconnect=True)
    cursor.execute(sql,params)
    if type != 'no_select':
        data_list = cursor.fetchall()
        return data_list
    else:
        conn.commit()
        return '数据库语句执行成功'