# -*- coding: utf-8 -*-
'''
建表语句
create table users(
    id int not null auto_increment, 
    name varchar(100) not null,
    pass varchar(100) not null,
    primary key(id)
);
'''
import mysql.connector      # pip install mysql-connector
import util
config = util.get_config()  # mysql数据库的连接信息
USER = config["user"]
PASSWORD = config["password"]
DATABASE = config["database"] 

def get_connect():  # 连接mysql数据库
    conn = mysql.connector.connect(user=USER, password=PASSWORD, database=DATABASE)    
    return conn

def save_user(username, password):
    try:
        conn = get_connect()    # 连接mysql数据库
        cursor = conn.cursor()  # 【新建mysql游标？】可以理解为，命令行中，执行sql语句之前，先要有一个光标行，在光标行中进行操作
        cursor.execute('insert into users(name, pass) values(%s, %s)', (username, password))    # 存入参数传来的用户名及密码
        conn.commit()   # 数据表内容有更新，必须使用到该语句
    except Exception as e:  # 若发生错误
        print(e)    # 打印错误信息
        if conn:    # 【嗯……若连接还在？】
            conn.rollback()     # 回溯
    finally:
        cursor.close()  # 关闭游标
        conn.close()    # 关闭mysql数据库连接

def get_pass(username):
    try:
        conn = get_connect()    # 建立连接和游标
        cursor = conn.cursor()
        # 这里使用(username)会报错【可是为啥嘞】
        cursor.execute('select pass from users where name = %s', (username,))   # 通过用户名查询密码
        password = cursor.fetchall()    # 存储所有查询出来的密码
    except Exception as e:  # 报错
        print(e)        
    finally:
        cursor.close()  # 关闭游标和连接
        conn.close()
    if not password:    # 若查询结果为空？
        return password
    else:   # 若结果不为空，返回第一条
        return password[0][0]

if __name__ == '__main__':
    save_user("xhh", "123")
    print(get_pass("xhh"))
