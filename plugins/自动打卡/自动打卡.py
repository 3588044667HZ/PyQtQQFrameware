import tkinter

import time
from Plugin import Bot

name = '自动打卡'
qqbot: Bot
gp_id = 0


def init(p_id: int, Api: Bot, ):  # 框架启动调用
    # print('init')
    global gp_id
    global qqbot
    gp_id = p_id
    qqbot = Api
    return {'name': name, 'complain': '自动打卡', 'author': 'huazi', 'ver': '0.1', 'p_id': p_id,
            'respond_group_msg': True, 'respond_private_msg': False, 'respond_notice': False, 'respond_request': False}


def close():
    pass


def enable():  # 插件被启用时被调用
    pass
    # return {'name': name, 'complain': '茉莉云对话AI', 'author': 'None', 'ver': '0.1', 'p_id': p_id}


def disable():
    pass


def on_group_msg(dic: dict):
    # print(dic)
    msg = dic['message']
    qq = dic['user_id']
    if msg == '打卡' and qq == 3588044667:
        # print(1)
        time.sleep(3)
        qqbot.send_group_sign(dic['group_id'])
        qqbot.send_group_msg(dic['group_id'], '活着', delay=3)
    else:
        pass


def setting():
    tk = tkinter.Tk()
    tk.mainloop()
