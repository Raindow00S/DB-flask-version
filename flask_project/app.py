#! /usr/bin/env python
# -*- coding:utf-8 -*-

import db
import util
import json
from flask import Flask, request, render_template, jsonify

# 用于输出运行日志
import logging
logging.basicConfig(level=logging.INFO,
                    format='127.0.0.1 - - [%(asctime)s - %(name)s - %(levelname)s - %(message)s]')
logger = logging.getLogger(__name__)

#用于控制全局变量
import glo


# =====================================
# 设置全局变量，以在整个登录过程中保存信息方便查找
# glo_userID = "0" # 账号（学生-学号；教师-职工号；仪器管理员-职工号）
# glo_identity = "undefined"  # 身份（学生/教师/仪器管理员）
#glo_userID = "001"   # 学生测试
#glo_identity = "student"
# userID = "101"   # 老师测试
# identity = "faculty"
# userID = "151"   # 仪器管理员测试
# identity = "equipment_manager"
# =====================================

app = Flask(__name__)  # 首先定义一个应用程序 Flask构造函数使用当前模块的名称作为参数

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
    return render_template('index.html'), 200

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
            logger.info("<返回前端>none")
            return 'none'
        elif db_user[1] != password:   # 密码错误
            logger.info("<返回前端>wrong")
            return 'wrong'
        else:   # 密码正确
            # 设置全局变量
            glo.set_value('glo_userID', username)
            glo.set_value('glo_identity', db_user[2])
            logger.info("<返回前端>right")
            return 'right'

# ================个人信息页(三个身份共用)=====================
@app.route('/myinfo', methods=['GET'])
def showInfo():
    # 取个人信息
    glo_userID = glo.get_value('glo_userID')
    glo_identity = glo.get_value('glo_identity')
    logger.info("<全局变量> glo_userID:"+glo_userID+" glo_identity:"+glo_identity)
    db_info = db.get_info(glo_userID, glo_identity)
    logger.info("<数据库传回> "+str(db_info))

    return render_template('myinfo.html',
                           identity=glo_identity,
                           info=db_info)

# ================学生=====================
# ================我的课题组=====================
@app.route('/mygroup-student', methods=['GET'])
def  mygroup_student():
    glo_userID = glo.get_value('glo_userID')
    db_groups = db.get_group_stu(glo_userID)
    logger.info("<数据库传回> "+str(db_groups))

    return render_template('mygroup-student.html',
                           groups = db_groups)



@app.route('/allgroup', methods=['GET', 'POST'])
def allGroup():
    if request.method == 'GET':
        db_groups = db.get_all_groups()
        logger.info("获得的所有课题组信息："+str(db_groups))

        return render_template('allgroup.html',
                               groups=db_groups)
    else:   # 当按下加入按钮时，发送过来申请对象课题组的老师ID
        leaderID = request.form.get(
            'leaderID', default='undefined')    # 课题组所属教师ID
        groupID = request.form.get('groupID', default='undefined')
        logger.info("申请加入的课题组所属教师ID："+leaderID)
        logger.info("申请加入的课题组ID："+groupID)
        # 学生ID在全局变量里面
        # 【TO DO 查找学生是否已在该课题组中，不在则生成申请记录】
        # 【若已在，返回joined】
        # 【若不在，则生成申请记录存入数据库，返回applied】
        db_group = db.get_group_by_student(userID, groupID)
        if not db_group:    # 若不在
            logger.info("插入加入课题组申请："+userID+"-->"+leaderID)
            db.add_apply_for_group(userID, leaderID)
            return 'applied'
        else:
            logger.info("学生"+userID+"已经加入课题组"+groupID)
            return 'joined'

# 显示教师的课题组信息及人员信息
@app.route('/mygroup-teacher', methods=['GET', 'POST'])
def teacherGroup():
    if request.method == 'GET':
        # 显示教师的课题组信息
        db_group = db.get_group_by_teacher(userID)
        # logger.info("db_group:"+str(db_group))
        if db_group:
            group_id = db_group["编号"]
            # logger.info("group_id:"+str(group_id))
            # 学生人员信息
            membersInfo = db.get_students_by_group(group_id)
            # logger.info("membersInfo:"+str(membersInfo))
        else:
            membersInfo = []

        return render_template('mygroup-teacher.html',
                               group=db_group,
                               membersInfo=membersInfo)

    else:   # 添加/删除了学生 或 修改了课题组信息
        # 总之先判断一下是什么操作啦
        action = request.form.get('action', default='undefined')
        # 若操作为删除学生
        if action == "delete":
            memberID = request.form.get('memberID', default='undefined')
            groupID = request.form.get('groupID', default='undefined')
            logger.info("memberID:"+str(memberID)+" groupID:"+str(groupID))

            db.remove_student_from_group(memberID, groupID)
            return "deleted"
        # 若操作为编辑课题组信息
        elif action == "edit":
            groupID = request.form.get("groupID", default="undefined")
            newName = request.form.get("newName", default="undefined")
            newType = request.form.get("newType", default="undefined")
            logger.info("groupID:"+str(groupID)+" newName:" +
                        str(newName)+" newType:"+str(newType))
            db.update_group_info(groupID, newName, newType)
            return "updated"
        else:
            all_students = db.get_all_students()
            print(type(all_students))
            # 我晕了……这是个列表，没法return
            logger.info("all_students:"+str(all_students))

            index = []
            for i in range(len(all_students)):
                index.append(i)
            logger.info("index:"+str(index))
            d = dict(zip(index, all_students))
            logger.info("d:"+str(d))

            return jsonify(d)


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
    glo.set_value('glo_userID','undefined')
    glo.set_value('glo_identity','undefined')
    app.run(host=host, port=port, threaded=True, debug=debug)
