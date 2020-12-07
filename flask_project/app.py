#! /usr/bin/env python
# -*- coding:utf-8 -*-

import glo  # 全局变量
from logging import NullHandler
import db
import wrap
import util
import json
from flask import Flask, request, render_template, jsonify

# 用于输出运行日志
import logging
logging.basicConfig(level=logging.INFO,
                    format='127.0.0.1 - - [%(asctime)s - %(name)s - %(levelname)s - %(message)s]')
logger = logging.getLogger(__name__)


app = Flask(__name__)  # 首先定义一个应用程序 Flask构造函数使用当前模块的名称作为参数

@app.route('/demo', methods=['GET', 'POST'])
def test():
    # 若是从服务器发送页面给客户端
    if request.method == 'GET':
        db_insts = db.get_insts(opt='all')  # 获得全部仪器的数据

        # return '没做完呢'
        return render_template('demo.html',insts=db_insts)
    
    # 若是从客户端发送数据给服务器
    else:
        inst_id = request.form.get('inst_id')   # 从ajax的data中又把数据取出来
        inst_name = request.form.get('inst_name')
        inst_type = request.form.get('inst_type')
        inst_desc = request.form.get('inst_desc')
        logger.info("<前端获取>仪器信息 "+str(inst_id)+" "+str(inst_name)
                    +" "+str(inst_type)+" "+str(inst_desc)) # 输出看一下
        db.update_inst(inst_id,inst_name,inst_type,inst_desc)   # 更新数据库

        return "updated"


# ================TODO留作参考注册页=====================
# @app.route('/signup', methods=['GET', 'POST'])
# def enroll():
#     if request.method == 'GET': # 客户端向服务端请求页面
#         return render_template('enroll.html'), 200
#     else:   # 若方法为POST，则是从客户端向服务端发送了信息
#         #接受数据
#         username = request.form.get('form-username', default='user')
#         password = request.form.get('form-password', default='pass')
#         logger.info("注册的用户是："+str(username))     # 用于测试
#         logger.info("用户的密码是："+str(password))
#         if db.get_pass(username):   # 应该是若数据库中找到了该数据
#             return 'existed'
#         else:   # 若找不到，则新存入该数据
#             db.save_user(username, password)
#             return 'ok'
# ================TODO留作参考用户页=====================
# @app.route('/user', methods=['POST'])   # 只有服务器接收到信息，才会跳转至/user
# def login_success():
#     username = request.form.get('username', default='user')
#     return render_template('user.html', username=username), 200     # 将用户名传入html进行渲染

# ================TODO首页=====================
@app.route('/', methods=['GET'])
# 定义处理函数
def form():
      # 引入模板
    return '首页'

# ================登录页=====================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html'), 200

    else:
        username = request.form.get('form-username', default='user')
        password = request.form.get('form-password', default='pass')
        logger.info("<前端获取> 账号："+str((username))+" 密码："+str(password))

        db_user = db.get_user(username)
        logger.info("<数据库传回> "+str(db_user))
        if not db_user:     # 用户账号不存在
            # logger.info("<返回前端> none")
            return 'none'
        elif db_user[1] != password:   # 密码错误
            # logger.info("<返回前端> wrong")
            return 'wrong'
        else:   # 密码正确
            # 设置全局变量
            glo.set_value('glo_userID', username)
            glo.set_value('glo_identity', db_user[2])
            # logger.info("<返回前端> right")
            return 'right'

# ================个人信息页(三个身份共用)=====================
@app.route('/myinfo', methods=['GET'])
def showInfo():
    # 取个人信息
    glo_userID = glo.get_value('glo_userID')
    glo_identity = glo.get_value('glo_identity')
    # logger.info("<全局变量> glo_userID:"+glo_userID+" glo_identity:"+glo_identity)
    db_info = db.get_info(glo_userID, glo_identity)
    logger.info("<数据库传回> "+str(db_info))

    return render_template('myinfo.html',
                           identity=glo_identity,
                           info=db_info)

# ================学生=====================
# ================我的课题组=====================
# 展示已加入的所有课题组
@app.route('/mygroup-student', methods=['GET'])
def myGroupStudent():
    glo_userID = glo.get_value('glo_userID')
    #db_groups = db.get_group_stu(glo_userID)
    db_groups = db.get_groups(opt='in', stuID=glo_userID)
    logger.info("<数据库传回> "+str(db_groups))

    return render_template('mygroup-student.html',
                           groups=db_groups)

# ================TODO加入课题组=====================
# 展示未加入的课题组,发送加入课题组请求
@app.route('/allgroup', methods=['GET', 'POST'])
def allGroup():
    if request.method == 'GET':
        # db_groups = db.get_all_groups()
        db_groups = db.get_groups(opt='out', stuID=glo.get_value(
            'glo_userID'))  # 我TM大无语……只是忘记传参，结果以为是什么bug改了几小时
        # db_groups = db.get_groups(opt='all')
        logger.info("<数据库传回> "+str(db_groups))

        return render_template('allgroup.html',
                               groups=db_groups)

    # TODO按钮交互
    else:
        # 按下加入按钮，传回选中数据
        leaderID = request.form.get('leaderID', default='000')    # 所属教师编号
        groupID = request.form.get('groupID', default='000')  # 课题组编号
        logger.info("<前端获取>所属教师编号："+leaderID+" 课题组编号："+groupID)

        stuID = glo.get_value('glo_userID')
        db.add_apply_for_group(stuID, leaderID)
        return 'applied'

# ================TODO操作资格申请=====================
@app.route('/applyqual', methods=['GET', 'POST'])
def applyQual():
    if request.method == 'GET':
        # 显示所有未获得操作资格的仪器
        stuID = glo.get_value('glo_userID')
        db_insts = db.get_insts(opt='unqual', stuID=stuID)

        return render_template('applyqual.html',
                               instruments=db_insts)
    else:
        # 选中某个仪器，显示可以审批的老师
        instID = request.form.get('form-instID', default='10001')    # 选中的仪器编号
        logger.info("<前端获取> 仪器编号："+instID)
        db_teachers = db.get_qual(opt='faculty', instID=instID)
        logger.info("<数据库传回>teachers "+str(db_teachers))
        # TODO 将老师数据返回前端

        # TODO 发送申请
        # 要插入的新仪器申请记录的参数
        recordNum = glo.get_value('glo_record_num')
        glo.set_value('glo_record_num', recordNum+1)
        recordID = recordNum+1  # 编号
        state = 's1'    # 状态
        stuID = glo.get_value('glo_userID')  # 申请人学号
        groupName = None
        timeID = None
        instName = request.form.get(
            'form-instname', default='default name')    # 仪器名称
        approvalID = request.form.get(
            'form-approvalID', default='0000')    # 审批人编号

        db.add_inst_record(recordID, state, stuID, groupName,
                           timeID, instName, approvalID)
        return 'applied'

# ================TODO预约申请=====================
@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    if request.method == 'GET':
        # 显示所有已获得操作资格的仪器
        stuID = glo.get_value('glo_userID')
        db_insts = db.get_insts(opt='qual', stuID=stuID)

        return render_template('applyqual.html',
                               instruments=db_insts)
    else:
        # 选中某个仪器，显示可以审批的仪器管理员、可用时间段和可选课题组
        instID = request.form.get('form-instID', default='10001')    # 选中的仪器编号
        logger.info("<前端获取> 仪器编号："+instID)

        db_admins = db.get_qual(opt='admin', instID=instID)
        logger.info("<数据库传回>db_admins "+str(db_admins))
        db_times = db.get_spare_time(instID)
        logger.info("<数据库传回>db_admins "+str(db_times))
        stuID = glo.get_value('glo_userID')
        db_groups = db.get_groups(opt='in', stuID=stuID)
        logger.info("<数据库传回>db_groups "+str(db_groups))

        # TODO 将所有数据返回前端

        # TODO 发送申请
        # 要插入的新仪器申请记录的参数
        recordNum = glo.get_value('glo_record_num')
        glo.set_value('glo_record_num', recordNum+1)
        recordID = recordNum+1  # 编号
        state = 's1'    # 状态
        stuID = glo.get_value('glo_userID')  # 申请人学号
        groupName = request.form.get(
            'form-groupname', default='default g name')    # 课题组名称
        timeID = request.form.get(
            'form-timeID', default='default timeID')  # 时间段编号
        instName = request.form.get(
            'form-instname', default='default i name')    # 仪器名称
        approvalID = request.form.get(
            'form-approvalID', default='0000')    # 审批人编号

        db.add_inst_record(recordID, state, stuID, groupName,
                           timeID, instName, approvalID)
        return 'applied'

# ================TODO记录与反馈=====================
@app.route('/record-student', methods=['GET', 'POST'])
def recordStudent():
    if request.method == 'GET':
        stuID = glo.get_value('glo_userID')
        db_records = db.get_records(opt='applier', userID=stuID)
        logger.info("<数据库传回>db_records "+str(db_records))

        # TODO 这里所有类型和状态的记录都混在一起……交给前端分开吗？
        return "unfinished"
    else:
        # TODO 填写反馈
        return "unfinished"


# ================老师=====================
# 显示教师的课题组信息及人员信息
@app.route('/mygroup-teacher', methods=['GET', 'POST'])
def teacherGroup():
    if request.method == 'GET':
        # 显示教师的课题组信息
        # db_group = db.get_group_by_teacher(userID)
        db_group = db.get_groups(
            opt='teacher', teaID=glo.get_value('glo_userID'))
        # logger.info("<数据库传回db_group> "+str(db_group))
        db_group = wrap.wrap_one_group(db_group[1])
        logger.info("<数据库传回（转变格式后）db_group> "+str(db_group))

        if db_group:
            group_id = db_group["编号"]
            # 学生人员信息
            membersInfo = db.get_students_by_group(group_id)
            logger.info("<数据库传回membersInfo> "+str(membersInfo))
        else:
            membersInfo = []

        return render_template('mygroup-teacher.html',
                               group=db_group,
                               membersInfo=membersInfo)

    # TODO按钮交互
    else:   # 添加/删除了学生 或 修改了课题组信息
        # 判断操作
        action = request.form.get('action', default='undefined')
        # 若按下删除学生按钮
        if action == "delete":
            memberID = request.form.get(
                'memberID', default='undefined')    # 选中学生学号
            groupID = request.form.get('groupID', default='undefined')  # 课题组编号
            logger.info("<前端获取> memberID:"+str(memberID) +
                        " groupID:"+str(groupID))

            db.remove_student_from_group(memberID, groupID)
            return "deleted"

        # 若按下保存编辑后的课题组信息按钮
        elif action == "edit":
            groupID = request.form.get("groupID", default="undefined")  # 课题组编号
            newName = request.form.get(
                "newName", default="undefined")  # 编辑后的课题组名称
            newType = request.form.get(
                "newType", default="undefined")  # 编辑后的课题组类型
            logger.info("<前端获取> groupID:"+str(groupID)+" newName:" +
                        str(newName)+" newType:"+str(newType))
            db.update_group_info(groupID, newName, newType)
            return "updated"
        # 若新增成员
        else:
            # 显示可以加入的成员
            # 若按下确定按钮后
            # 若删除课题组
            # 若创建课题组

            # all_students = db.get_all_students()
            # print(type(all_students))
            # # 我晕了……这是个列表，没法return
            # logger.info("all_students:"+str(all_students))

            # index = []
            # for i in range(len(all_students)):
            #     index.append(i)
            # logger.info("index:"+str(index))
            # d = dict(zip(index, all_students))
            # logger.info("d:"+str(d))

            return "unfinished"

# 显示等待教师审批的仪器操作资格申请
@app.route('/instapprove-teacher', methods=['GET', 'POST'])
def instApproveTeacher():
    if request.method == 'GET':
        facultyID = glo.get_value('glo_userID')
        db_records = db.get_records(opt='approval', userID=facultyID)   # 获得该教师负责审批的记录
        db_records = wrap.select_records_by_state(db_records, '待处理') # 获得该教师负责审批，且状态为待处理的记录
        logger.info("<数据库传回（转变格式后）db_records> "+str(db_records))
        return render_template('instapprove-teacher.html',records=db_records)
    else:
        recordID = request.form.get('record-id')    # 选中记录编号
        action = request.form.get('action')
        logger.info("<前端获取> recordID:"+str(recordID))

        # 按下审批通过按钮后，更新状态->s2（已通过）
        if action == "pass":
            # 更新状态
            db.update_record_state(recordID,"已通过")
            return "passed"
        # 驳回->s4（拒绝）
        else:
            db.update_record_state(recordID,"拒绝")
            return "rejected"

# 显示教师的记录与反馈
# 共三个表：1. 由自己审批的操作资格申请 2.由自己课题组的同学发起的预约申请 3.与表2对应的仪器使用反馈
@app.route('/record-teacher', methods=['GET', 'POST'])
def recordTeacher():
    if request.method == 'GET':
        # db_insts=db.get_insts(opt='all') #获得全部仪器数据（照着晓曦的思路写的...）
        teaID = glo.get_value('glo_userID')
        # 由自己审批的操作资格申请
        db_app_records = db.get_records(opt='approval', userID=teaID)
        logger.info("<数据库传回>db_app_records "+str(db_app_records))
        # 由自己课题组的同学发起的预约申请
        groupName = db.get_groups(opt='teacher',teaID=teaID)[1][2]
        # print("groupID:"+str(groupID))
        db_group_records = db.get_records_by_groupID(groupName)
        logger.info("<数据库传回>db_group_records "+str(db_group_records))

        # TODO 这里所有类型和状态的记录都混在一起……交给前端分开吗？
        return render_template('record-teacher.html',
                                a_records=db_app_records,
                                g_records=db_group_records)
    else:
        # TODO 在哪里通过课题组的申请？？
        return "unfinished"

# ================管理员=====================
# 显示等待管理员审批的仪器操作资格申请
@app.route('/instapprove-admin', methods=['GET', 'POST'])
def instApproveAdmin():
    if request.method == 'GET':
        adminID = glo.get_value('glo_userID')
        db_records = db.get_records(opt='approval', userID=adminID)
        db_records = wrap.select_records_by_state(db_records, 's1')
        logger.info("<数据库传回（转变格式后）db_records> "+str(db_records))
        return "unfinished"
    else:
        # 按下审批通过按钮后，更新仪器申请记录表的状态
        recordID = request.form.get(
            'recordID', default='undefined')    # 选中记录编号
        logger.info("<前端获取> recordID:"+str(recordID))
        db.update_record_state(recordID, 's2')

        return "unfinished"

# 显示管理员的记录与反馈
@app.route('/record-admin', methods=['GET'])
def recordAdmin():
    adminID = glo.get_value('glo_userID')
    db_records = db.get_records(opt='approval', userID=adminID)
    logger.info("<数据库传回>db_records "+str(db_records))

    # TODO 这里所有类型和状态的记录都混在一起……交给前端分开吗？
    return "unfinished"


if __name__ == '__main__':
    host = util.get_config()["host"]    # 获取配置信息
    port = int(util.get_config()["port"])
    debug = util.get_config()["debug"]
    if debug == "True":
        debug = True
    else:
        debug = False
    print(debug)
    glo._init()
    glo.set_value('glo_userID', '101')   # 登录的账号
    glo.set_value('glo_identity', 'faculty')  # 登录的身份
    record_num = db.get_records_num()
    glo.set_value('glo_record_num', record_num) # 仪器申请记录表行数（用于新插入记录时，确定记录编号属性）
    app.run(host=host, port=port, threaded=True, debug=debug)
