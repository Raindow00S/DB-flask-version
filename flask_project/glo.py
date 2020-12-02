# -*- coding: utf-8 -*-
 
def _init():#初始化
    global _global_dict
    _global_dict = {}
    print("全局变量已初始化")
 
 
def set_value(key,value):
    """ 定义一个全局变量 """
    _global_dict[key] = value
    print("设置全局变量的值 "+key+":"+str(value))
 
 
def get_value(key,defValue=None):
    """ 获得一个全局变量,不存在则返回默认值 """
    try:
        return _global_dict[key]
    except KeyError:
        print("不存在该全局变量")