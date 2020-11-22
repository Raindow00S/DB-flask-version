#! /usr/bin/env python
# -*- coding:utf-8 -*-


# python内置标准模块，用于输出运行日志
import logging
logging.basicConfig(level=logging.INFO, format='127.0.0.1 - - [%(asctime)s - %(name)s - %(levelname)s - %(message)s]')
logger = logging.getLogger(__name__)

from flask import Flask, request, render_template
import json
import util
import db

# 【试图设置全局变量，以在整个登录过程中保存信息方便查找】
# userID = "0" # 账号（学生-学号；教师-职工号；仪器管理员-职工号）
# identity = "undefined"  # 身份（学生/教师/仪器管理员）
userID = "01"   # 学生测试
identity = "student"
# userID = "02"   # 老师测试
# identity = "faculty"
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
