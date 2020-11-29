#! /usr/bin/env python
# -*- coding:utf-8 -*-


# python内置标准模块，用于输出运行日志
import logging
logging.basicConfig(level=logging.INFO, format='127.0.0.1 - - [%(asctime)s - %(name)s - %(levelname)s - %(message)s]')
logger = logging.getLogger(__name__)

from flask import Flask, request, render_template, jsonify
import json
import util
import db

# 【试图设置全局变量，以在整个登录过程中保存信息方便查找】
# userID = "0" # 账号（学生-学号；教师-职工号；仪器管理员-职工号）
# identity = "undefined"  # 身份（学生/教师/仪器管理员）
# userID = "01"   # 学生测试
# identity = "student"
userID = "02"   # 老师测试
identity = "faculty"
# userID = "03"   # 仪器管理员测试
# identity = "equipment_manager"

app = Flask(__name__) #首先定义一个应用程序 Flask构造函数使用当前模块的名称作为参数
# 路由配置
# @app.route('/')
# # 定义处理函数
# def test():
#     #处理逻辑
#     # List = [1,2,3,4,5]
#     return 'hello,world!'     #响应
#     # return render_template('test.html',Lst = List), 200

@app.route('/', methods=['GET'])
#定义处理函数
def form():
      # 引入模板
    return render_template('index.html'), 200

@app.route('/signup', methods=['GET', 'POST'])
def enroll():
    if request.method == 'GET': # 客户端向服务端请求页面
        return render_template('enroll.html'), 200
    else:   # 若方法为POST，则是从客户端向服务端发送了信息
        #接受数据
        username = request.form.get('form-username', default='user')
        password = request.form.get('form-password', default='pass')
        logger.info("注册的用户是："+str(username))     # 用于测试
        logger.info("用户的密码是："+str(password))
        if db.get_pass(username):   # 应该是若数据库中找到了该数据
            return 'existed'
        else:   # 若找不到，则新存入该数据
            db.save_user(username, password)
            return 'ok'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':     # 客户端向服务器请求页面
        return render_template('login.html'), 200
    else:   # 客户端向服务器发送表单信息
        username = request.form.get('form-username', default='user')
        password = request.form.get('form-password', default='pass')
        logger.info("登录的用户是："+str((username)))
        logger.info("用户的密码是："+str(password))
        db_pass = db.get_pass(username)
        if not db_pass:     # 若数据库中查询到的密码结果为空
            return 'none'
        elif db_pass != password:   # 若密码不对应
            return 'wrong'
        else:   # 密码存在且符合
            return 'right'

@app.route('/user', methods=['POST'])   # 只有服务器接收到信息，才会跳转至/user
def login_success():
    username = request.form.get('username', default='user')
    return render_template('user.html', username=username), 200     # 将用户名传入html进行渲染

@app.route('/myinfo', methods=['GET','POST'])
def showInfo():
    if request.method == 'GET':
        logger.info("全局变量userID："+userID)
        logger.info("全局变量identity："+identity)
        # 根据身份和账号(全局变量)，从数据库取出和身份对应的个人信息，传给前端
        # 若数据库正常，不会出现找不着的情况
        db_info = db.get_info(userID, identity) # 返回的是个字典
        logger.info("获得的信息："+str(db_info))
        
        # 传送数据给前端
        # 【老冯，拆字典的任务就交给你了！】
        return render_template('myinfo.html',
                                identity=identity,
                                info=db_info)

@app.route('/allgroup', methods=['GET','POST'])
def allGroup():
    if request.method == 'GET':
        db_groups = db.get_all_groups()
        logger.info("获得的所有课题组信息："+str(db_groups))

        return render_template('allgroup.html',
                                groups=db_groups)
    else:   # 当按下加入按钮时，发送过来申请对象课题组的老师ID
        leaderID = request.form.get('leaderID', default='undefined')    # 课题组所属教师ID
        groupID = request.form.get('groupID',default='undefined')
        logger.info("申请加入的课题组所属教师ID："+leaderID)
        logger.info("申请加入的课题组ID："+groupID)
        # 学生ID在全局变量里面
        # 【TO DO 查找学生是否已在该课题组中，不在则生成申请记录】
        # 【若已在，返回joined】
        # 【若不在，则生成申请记录存入数据库，返回applied】
        db_group = db.get_group_by_student(userID,groupID)
        if not db_group:    # 若不在
            logger.info("插入加入课题组申请："+userID+"-->"+leaderID)
            db.add_apply_for_group(userID, leaderID)
            return 'applied'
        else:
            logger.info("学生"+userID+"已经加入课题组"+groupID)
            return 'joined'

# 显示教师的课题组信息及人员信息
@app.route('/mygroup-teacher', methods=['GET','POST'])
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
            membersInfo=[]
        
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
        elif action=="edit":
            groupID = request.form.get("groupID",default="undefined")
            newName = request.form.get("newName",default="undefined")
            newType = request.form.get("newType",default="undefined")
            logger.info("groupID:"+str(groupID)+" newName:"+str(newName)+" newType:"+str(newType))
            db.update_group_info(groupID,newName,newType)
            return "updated"
        else:
            all_students = db.get_all_students()
            print(type(all_students))
            logger.info("all_students:"+str(all_students)) # 我晕了……这是个列表，没法return

            index = []
            for i in range(len(all_students)):
                index.append(i)
            logger.info("index:"+str(index))
            d = dict(zip(index,all_students))
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
    app.run(host=host, port=port, threaded=True, debug=debug)