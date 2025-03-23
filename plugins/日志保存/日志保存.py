import os
import tkinter
import logging.handlers

name = '日志保存'
qqbot = None
gp_id = 0

# import time
try:
    os.mkdir('./日志')
except FileExistsError:
    pass
# logging初始化工作
logging.basicConfig()
logger = logging.getLogger('messager-bot')
logger.setLevel(logging.INFO)
# 添加TimedRotatingFileHandler
timefilehandler = logging.handlers.TimedRotatingFileHandler(
    "./日志/log.log",  # 日志路径
    when='D',  # S秒 M分 H时 D天 W周 按时间切割 测试选用S
    interval=1)  # 多少天切割一次
# backupCount=7  # 保留多少天
# )
# 设置后缀名称，跟strftime的格式一样
timefilehandler.suffix = "%Y-%m-%d_%H-%M-%S.log"
formatter = logging.Formatter('%(asctime)s|%(name)s | %(levelname)s | %(message)s')
timefilehandler.setFormatter(formatter)
logger.addHandler(timefilehandler)


# logger.info('test')


# import re
# import sys
# import copy

def init(p_id: int, Api):  # 框架启动调用
    # print('init', Api, p_id)
    global gp_id
    global qqbot
    gp_id = p_id
    qqbot = Api
    return {'name': name, 'complain': '自动保存日志', 'author': 'huazi', 'ver': '0.1', 'p_id': p_id}


def close():
    pass


def enable():  # 插件被启用时被调用
    pass


def disable():
    pass


def on_group_msg(dic: dict):
    logger.info(f'group->{dic["group_id"]}->{dic["user_id"]}->{dic["message"]}')
    return


def on_notice(dic):
    logger.info(f'notice->{dic["user_id"]}->{dic["sub_type"]}')
    return


def setting():
    root = tkinter.Tk()
    root.geometry('300x200')
    t = tkinter.Message(root, text='自动保存插件，保存在./data/日志/xxx-xxx-xxx.log\n')
    t.pack()
    root.mainloop()
    # root.geometry('')


def on_private_msg(dic: dict):
    logger.info(f'private->{dic["user_id"]}->{dic["message"]}')
    return

# def on_notice(dic):


# if __name__ == '__main__':
#     os.mkdir('./data/日志')
# setting()
