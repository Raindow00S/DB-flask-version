# -*- coding: utf-8 -*-

# 用于输出运行日志
import logging
logging.basicConfig(level=logging.INFO, format='127.0.0.1 - - [%(asctime)s - %(name)s - %(levelname)s - %(message)s]')
logger = logging.getLogger(__name__)

# 数据库连接信息
import mysql.connector
import util
config = util.get_config()
USER = config["user"]
PASSWORD = config["password"]
DATABASE = config["database"] 

# 连接mysql数据库
def get_connect():
    conn = mysql.connector.connect(user=USER, password=PASSWORD, database=DATABASE)    
    return conn

# ==============TODO留作参考注册函数=======================
# def save_user(username, password):
#     try:
#         conn = get_connect()    # 连接mysql数据库
#         cursor = conn.cursor()  # 新建游标
#         cursor.execute('insert into users(name, pass) values(%s, %s)', (username, password))    # 存入参数传来的用户名及密码
#         conn.commit()   # 数据表内容有更新，必须使用到该语句
#     except Exception as e:  # 若发生错误
#         print(e)    # 打印错误信息
#         if conn:    # 【嗯……若连接还在？】
#             conn.rollback()     # 回溯
#     finally:
#         cursor.close()  # 关闭游标
#         conn.close()    # 关闭mysql数据库连接

# 传入用户账号，确定登录是否成功，传回全局变量
def get_user(username):
    try:
        conn = get_connect();cursor = conn.cursor()
        cursor.execute('select * from 账号信息表 where 账号 = %s', (username,)) # 这里使用(username)会报错【可是为啥嘞】
        user = cursor.fetchall()
        logger.info("get_user查询结果："+str(user))
    except Exception as e:
        print(e)        
    finally:
        cursor.close();conn.close()

    if not user: # 若查询结果为空->账号不存在，登录失败，返回空列表
        return user
    else: # 若结果不为空->返回一行（元组）
        return user[0]

#  根据身份和账号(全局变量)，查询和身份对应的个人信息
def get_info(userID, identity):
    try:
        conn = get_connect();cursor = conn.cursor()

        if identity == 'student':
            cursor.execute('select * from 学生表 where 学号 = %s', (userID,))
        elif identity == 'faculty':
            cursor.execute('select * from 老师表 where 职工号 = %s', (userID,))
        else:
            cursor.execute('select * from 仪器管理员表 where 职工号 = %s', (userID,))
        info = cursor.fetchone()
        logger.info("get_info查询结果："+str(info))
    except Exception as e:
        print(e)
    finally:
        cursor.close();conn.close()
    
    # 将元组中的数据和属性名拼接成字典 属性名:属性值
    if identity == 'student':
        attr = ["学号", "姓名", "院系", "专业", "年级"]
    elif identity == 'faculty':
        attr = ["职工号", "姓名", "职称"]
    else:
        attr = ["职工号", "姓名"]
    info_dict = dict(zip(attr, info))
    return info_dict

# 传入学号,查询该学生所在的所有课题组
def get_group_stu(stuID):
    try:
        conn = get_connect();cursor = conn.cursor()
        cursor.execute('select * from 课题组表 where 编号 in (select 课题组编号 from 课题成员表 where 学号 = %s)', (stuID,))
        groups = cursor.fetchall()
        logger.info("get_group_stu查询结果："+str(groups))
    except Exception as e:
        print(e)        
    finally:
        cursor.close();conn.close()

    if not groups:  # 若还没有加入的课题组
        return groups
    else:   # 若有加入的课题组
        return groups

# 获得全部课题组的信息
def get_all_groups():
    try:
        conn = get_connect()    # 建立连接和游标
        cursor = conn.cursor()
        cursor.execute('select * from research_group')
        groups = cursor.fetchall()    # 元组列表
    except Exception as e:  # 报错
        print(e)
    finally:
        cursor.close()  # 关闭游标和连接
        conn.close()
    
    # 添加属性名
    attr = ["所属教师","编号","名称","类型"]
    groups.insert(0,attr)
    
    return groups

# 插入申请加入课题组的记录
def add_apply_for_group(studentID, leaderID):
    try:
        conn = get_connect()    # 建立连接和游标
        cursor = conn.cursor()
        cursor.execute('insert into apply_for_group(学号, 课题组所属教师职工号) values(%s, %s)', (studentID, leaderID))
        conn.commit()
    except Exception as e:  # 报错
        print(e)
        if conn:
            conn.rollback()     # 回溯
    finally:
        cursor.close()  # 关闭游标和连接
        conn.close()

# 查找该学生是否已经加入指定课题组
def get_group_by_student(studentID,groupID):
    try:
        conn = get_connect()    # 建立连接和游标
        cursor = conn.cursor()
        cursor.execute('select * from student_group where 学号 = %s and 课题组编号 = %s', (studentID,groupID))
        group = cursor.fetchall()
    except Exception as e:  # 报错
        print(e)
    finally:
        cursor.close()  # 关闭游标和连接
        conn.close()
    if not group:   # 若该学生没有加入该课题组
        print("该学生没有加入该课题组")
        return group
    else:   # 若加入
        return groupID

# 查找老师的课题组
def get_group_by_teacher(teacherID):
    try:
        conn = get_connect()
        cursor = conn.cursor()
        cursor.execute('select * from research_group where 所属教师 = %s', (teacherID,))
        group = cursor.fetchone()   # 若数据库正常，则查询结果为空或只有一条数据
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    if not group:   # 若所有课题组表中没有属于该教师的课题组的记录，则返回空列表
        print("该教师不属于任何课题组！")
        return group
    else:   # 若该教师有课题组，则返回属性（字典）
        attr = ("所属教师","编号","名称","类型")
        group_dict = dict(zip(attr, group))
        return group_dict

# 查课题组中的所有学生的个人信息
def get_students_by_group(groupID):
    try:
        conn = get_connect()
        cursor = conn.cursor()
        cursor.execute('select 学号 from student_group where 课题组编号 = %s', (groupID,))
        membersID = cursor.fetchall()   # 数据的条数对应该课题组中学生的人数
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

    membersInfo = []
    # 通过学号取出每一个学生的个人信息
    # print("membersID是元组？") # YES是元组列表：[('01',), ('05',)]
    # print(membersID)
    for ID in membersID:
        membersInfo.append(get_info(ID[0],"student"))
    # print(membersInfo)
    return membersInfo

# 删除学生与课题组的联系
def remove_student_from_group(studentID, groupID):
    try:
        conn = get_connect()
        cursor = conn.cursor()
        cursor.execute('delete from student_group where 学号 = %s and 课题组编号 = %s', (studentID,groupID))
        print("学生"+studentID+"和课题组"+groupID+"的记录已删除")
        conn.commit()
    except Exception as e:
        print(e)
        if conn:
            conn.rollback()     # 回溯
    finally:
        cursor.close()
        conn.close()

# 传入新的名字和类型，更新课题组信息
def update_group_info(groupID,newName,newType):
    try:
        conn = get_connect()
        cursor = conn.cursor()
        cursor.execute('update research_group set 名称 = %s and 类型 = %s where 编号 = %s', (newName,newType,groupID))
        print("课题组"+groupID+"的信息已更新: "+newName+" "+newType)
        conn.commit()
    except Exception as e:
        print(e)
        if conn:
            conn.rollback()     # 回溯
    finally:
        cursor.close()
        conn.close()

# 查所有学生的个人信息
def get_all_students():
    try:
        conn = get_connect()
        cursor = conn.cursor()
        cursor.execute('select * from student')
        students = cursor.fetchall()   # 数据的条数对应该课题组中学生的人数
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

    # print("students:"+str(students))
    return students


# if __name__ == '__main__':
#     save_user("xhh", "123")
#     print(get_pass("xhh"))
