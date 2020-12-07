# -*- coding: utf-8 -*-

import wrap

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
        # logger.info("get_user查询结果："+str(user))
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
        # logger.info("get_info查询结果："+str(info))
    except Exception as e:
        print(e)
    finally:
        cursor.close();conn.close()
    
    return wrap.wrap_info(info,identity)

# 一个总的获取课题组信息的函数
# opt:查询方式 all-查询全部课题组 in-使用stuID,查找学生在的课题组 out-查找学生不在的课题组 teacher-使用teaID,查找老师的课题组
# stuID:学号
# teaID:老师职工号
def get_groups(opt = 'all', stuID = 'undefined', teaID = 'undefined'):
    try:
        conn = get_connect();cursor = conn.cursor()
        
        if opt == 'all':
            cursor.execute('select * from 课题组表')
        elif opt == 'in':
            cursor.execute('select * from 课题组表 where 编号 in (select 课题组编号 from 课题成员表 where 学号 = %s)', (stuID,))
        elif opt == 'out':
            # 这里查询not in没有效果 # 对不起，是我忘了传参数
            cursor.execute('select * from 课题组表 where 编号 not in (select 课题组编号 from 课题成员表 where 学号 = %s)', (stuID,))
        elif opt == 'teacher':
            cursor.execute('select * from 课题组表 where 所属教师 = %s', (teaID,))
        else:
            print("不合法参数")
        groups = cursor.fetchall()
        # logger.info("get_groups查询结果："+str(groups))
    except Exception as e:
        print(e)
    finally:
        cursor.close();conn.close()
    
    return wrap.wrap_groups(groups)

# 插入申请加入课题组的记录
def add_apply_for_group(stuID, leaderID):
    try:
        conn = get_connect();cursor = conn.cursor()
        cursor.execute('insert into 课题申请记录表(学号, 职工号) values(%s, %s)', (stuID, leaderID))
        conn.commit()
        logger.info("插入课题组申请："+stuID+" --> "+leaderID)
    except Exception as e:
        print(e)
        if conn: conn.rollback()
    finally:
        cursor.close();conn.close()

# 一个总的获取仪器信息的函数
# opt:查询方式 all-全部 qual-使用stuID,查找学生有操作资格的仪器 unqual-查找学生没有操作资格的仪器
# stuID:学号
def get_insts(opt,stuID='0'):
    try:
        conn = get_connect();cursor = conn.cursor()
        if opt == 'all':
            cursor.execute('select * from 仪器表')
        elif opt == 'qual':
            cursor.execute('select * from 仪器表 where 仪器名称 in (select 仪器名称 from 仪器申请记录表 where 申请人学号 = %s and 状态 = "s2" and 时间段编号 is NULL)',(stuID,))
        elif opt == 'unqual':
            cursor.execute('select * from 仪器表 where 仪器名称 not in (select 仪器名称 from 仪器申请记录表 where 申请人学号 = %s and 状态 = "s2" and 时间段编号 is NULL)',(stuID,))
        else:
            print("参数不合法")

        insts = cursor.fetchall()
        logger.info("get_insts查询结果："+str(insts))
    except Exception as e:
        print(e)
    finally:
        cursor.close();conn.close()
    return insts

# 一个总的获取拥有仪器审批资格人员的函数
# opt:查询方式 faculty-查找老师审批资格 admin-查找管理员审批资格
# instID:仪器编号
def get_qual(opt,instID):
    try:
        conn = get_connect();cursor = conn.cursor()
        if opt == 'faculty':
            cursor.execute('select 姓名 from 老师表 where 职工号 in (select 职工号 from 老师资格表 where 仪器编号 = %s)',(instID,))
        elif opt == 'admin':
            cursor.execute('select 姓名 from 仪器管理员表 where 职工号 in (select 职工号 from 管理员资格表 where 仪器编号 = %s)',(instID,))
        else:
            print("参数不合法")

        approvals = cursor.fetchall()
        logger.info("get_inst查询结果："+str(approvals))
    except Exception as e:
        print(e)
    finally:
        cursor.close();conn.close()

# 插入新的仪器申请记录
# 参数：编号，状态，申请人学号，课题组名称，时间段编号，仪器名称，审批人职工号
def add_inst_record(ID,state,sID,gName,timeID,instName,appID):
    try:
        conn = get_connect();cursor = conn.cursor()
        cursor.execute('insert into 课题申请记录表(编号，状态，申请人学号，课题组名称，时间段编号，仪器名称，审批人职工号) values(%s,%s,%s,%s,%s,%s,%s)',
                         (ID,state,sID,gName,timeID,instName,appID))
        conn.commit()
        logger.info("插入仪器申请："+"编号"+ID+" "+sID+" --> "+appID)
    except Exception as e:
        print(e)
        if conn: conn.rollback()
    finally:
        cursor.close();conn.close()

# 查找某个仪器可以选择的预约时间
# 可以选择的预约时间：其编号不在仪器申请记录表中，或其编号存在，但是状态为“拒绝”
# 也就是说，只要某条仪器申请记录包含了该时间段，且没有被拒绝，则这个时间段都已经被占用，且不会被释放
def get_spare_time(instID):
    try:
        conn = get_connect();cursor = conn.cursor()
        cursor.execute('select 时间段编号,起始时间,结束时间 from 仪器可用时间段表 where 仪器编号 = %s', (instID),)
        times = cursor.fetchall()
    except Exception as e:
        print(e)        
    finally:
        cursor.close();conn.close()

    return times

# 根据不同身份查找记录
# opt:身份 applier-发起人 approval-审批人
# userID:学号或职工号
def get_records(opt,userID):
    try:
        conn = get_connect();cursor = conn.cursor()

        if opt == 'applier':
            cursor.execute('select * from 仪器申请记录表 where 申请人学号 = %s', (userID,))
        elif opt == 'approval':
            cursor.execute('select * from 仪器申请记录表 where 审批人职工号 = %s', (userID,))
        else:
            print("不合法参数")
        records = cursor.fetchall()
    except Exception as e:
        print(e)        
    finally:
        cursor.close();conn.close()
    
    return records

# 根据课题组名字，查找记录
def get_records_by_groupID(groupName):
    # print("进入get_records_by_groupID")
    try:
        conn = get_connect();cursor = conn.cursor()
        cursor.execute('select * from 仪器申请记录表 where 课题组名称 = %s', (groupName,))
        print("查询结果：",end='')
        print(str(cursor))
        records = cursor.fetchall()
    except Exception as e:
        print(e)        
    finally:
        cursor.close();conn.close()

    return records
    

def get_records_num():
    try:
        conn = get_connect();cursor = conn.cursor()
        cursor.execute('select count(*) from 仪器申请记录表')
        num = cursor.fetchone()
    except Exception as e:
        print(e)        
    finally:
        cursor.close();conn.close()
    
    return num[0]

# 更新仪器申请记录状态
def update_record_state(recordID,state):
    try:
        conn = get_connect();cursor = conn.cursor()
        cursor.execute('update 仪器申请记录表 set 状态 = %s where 编号 = %s', (state,recordID))
        conn.commit()
        logger.info("更新申请状态："+recordID+" --> "+state)
    except Exception as e:
        print(e)
        if conn: conn.rollback()
    finally:
        cursor.close();conn.close()

# 查课题组中的所有学生的个人信息
# TODO 这个可以和其他函数合并一下？
def get_students_by_group(groupID):
    try:
        conn = get_connect();cursor = conn.cursor()
        cursor.execute('select 学号 from 课题成员表 where 课题组编号 = %s', (groupID,))
        membersID = cursor.fetchall()   # 数据的条数对应该课题组中学生的人数
        logger.info("get_students_by_group查询结果："+str(membersID))
    except Exception as e:
        print(e)
    finally:
        cursor.close();conn.close()

    membersInfo = []
    # 通过学号取出每一个学生的个人信息
    for ID in membersID:
        membersInfo.append(get_info(ID[0],"student"))
    return membersInfo

# 删除学生与课题组的联系
def remove_student_from_group(studentID, groupID):
    try:
        conn = get_connect();cursor = conn.cursor()
        cursor.execute('delete from 课题成员表 where 学号 = %s and 课题组编号 = %s', (studentID,groupID))
        print("学生"+studentID+"和课题组"+groupID+"的记录已删除")
        conn.commit()
    except Exception as e:
        print(e)
        if conn:
            conn.rollback()     # 回溯
    finally:
        cursor.close();conn.close()

# 传入新的名字和类型，更新课题组信息
def update_group_info(groupID,newName,newType):
    try:
        conn = get_connect();cursor = conn.cursor()
        cursor.execute('update 课题组表 set 名称 = %s and 类型 = %s where 编号 = %s', (newName,newType,groupID))
        print("课题组"+groupID+"的信息已更新: "+newName+" "+newType)
        conn.commit()
    except Exception as e:
        print(e)
        if conn:
            conn.rollback()     # 回溯
    finally:
        cursor.close();conn.close()

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

# 更新仪器信息
def update_inst(id,name,type,desc):
    try:
        conn = get_connect();cursor = conn.cursor()
        cursor.execute('update 仪器表 set 仪器名称 = %s,型号规格 = %s,功能描述 = %s where 仪器编号 = %s', (name,type,desc,id))
        print("仪器"+id+"的信息已更新: "+name+" "+type+" "+desc)
        conn.commit()
    except Exception as e:
        print(e)
        if conn:
            conn.rollback()     # 回溯
    finally:
        cursor.close();conn.close()

# if __name__ == '__main__':
#     save_user("xhh", "123")
#     print(get_pass("xhh"))
