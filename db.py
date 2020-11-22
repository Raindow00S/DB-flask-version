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

# 【TO DO 根据身份和账号(全局变量)，从数据库取出和身份对应的个人信息，传给前端】
def get_info(userID, identity):
    try:
        conn = get_connect()    # 建立连接和游标
        cursor = conn.cursor()
        # 通过身份判断查询哪个关系表
        if identity == 'student':
            print("身份校对：student")
            cursor.execute('select * from student where 学号 = %s', (userID,))
        elif identity == 'faculty':
            print("身份校对：faculty")
            cursor.execute('select * from faculty where 职工号 = %s', (userID,))
        else:
            print("身份校对：equipment_manager")
            cursor.execute('select * from equipment_manager where 职工号 = %s', (userID,))
        info = cursor.fetchone()    # 正常情况下，会查询出一条数据，只取这一条即可（数据类型为元组）
    except Exception as e:  # 报错
        print(e)
    finally:
        cursor.close()  # 关闭游标和连接
        conn.close()
    
    # 将元组中的数据和属性名拼接成字典 属性名:属性值
    if identity == 'student':
        attr = ["学号", "姓名", "院系", "专业", "年级"]
    elif identity == 'faculty':
        attr = ["职工号", "姓名", "职称"]
    else:
        attr = ["职工号", "姓名"]

    info_dict = dict(zip(attr, info))
    # 返回字典
    return info_dict

if __name__ == '__main__':
    save_user("xhh", "123")
    print(get_pass("xhh"))
