import pymysql 
import os
import conf

config = conf.getconfig()
dbinfo = config['db']
conn = pymysql.connect(dbinfo['host'], dbinfo['user'], dbinfo['password'], dbinfo['dbname'], charset='utf8')
cursor = conn.cursor()

def executemany(str, data, vtype):
    # cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        cursor.executemany(str, data)
        # data = cursor.fetchone()
        conn.commit()
    except Exception as e:
        print('Sql err: ',vtype ,e)
        conn.rollback()

def execute(str, data):
    try:
        cursor.execute(str, data)
        # 使用 fetchone() 方法获取单条数据.
        # data = cursor.fetchone()
        conn.commit()
    except Exception as e:
        print('Execute sql err: ', e)
        conn.rollback()

def select(str):
    try:
        cursor.execute(str)
    except Exception as e:
        print('Select sql err: ', e)
    return cursor

def closeconn():
    cursor.close()
     # close conn
    conn.close()
