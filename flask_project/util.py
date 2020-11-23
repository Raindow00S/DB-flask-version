# -*- coding:utf-8 -*-
import json
def get_config():   # 将json文件内容转成python object后返回
    with open('config.json', 'r') as f:
        str_config = f.read()
    config = json.loads(str_config)
    return config

if __name__ == '__main__':  # 直接运行，则打印json内容
    print(get_config())
