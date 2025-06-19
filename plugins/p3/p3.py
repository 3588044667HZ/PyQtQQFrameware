import tkinter
import requests

name = 'p3'

from Plugin import Bot

# from sdk import Bot

complain = '搜图'
qqbot: Bot
gp_id = 0


def init(p_id: int, Api: object):  # 插件第一次安装时调用
    global gp_id
    global qqbot
    gp_id = p_id
    qqbot = Api
    return {'name': name, 'complain': complain, 'author': 'None', 'ver': '0.1', 'p_id': p_id, 'respond_group_msg': True,
            'respond_private_msg': True, 'respond_notice': False, 'respond_request': False}


def enable():  # 插件被启用时被调用
    pass
    # global qqbot
    # qqbot = Api
    # return {'name': name, 'complain': complain, 'author': 'None', 'ver': '0.1', 'p_id': p_id}


def disable():
    pass


def close():
    pass


def on_group_msg(dic: dict):
    if '搜图' in dic['raw_message']:
        s = dic['raw_message']
        if s.index('搜图') == 0:
            s1 = s.replace('搜图', '')
            # print(s1)
            api = 'http://lkaa.top/API/sgst/api.php?msg=' + str(s1)
            re = requests.get(api).json()
            # print(re)
            re1 = re['data']['url']
            s = '[CQ:image,file={},cache=0]'.format(re1)
            qqbot.send_group_msg(group=dic['group_id'], msg=s)
            # qqbot.send_msg({'msg_type': 'group', 'number': dic['group_id'], 'msg': s})


def on_private_msg(dic: dict):
    s = dic['raw_message']
    if '搜图' in s and s.index('搜图') == 0:
        s1 = s.replace('搜图', '')
        # print(s1)
        api = 'http://lkaa.top/API/sgst/api.php?msg=' + str(s1)
        re = requests.get(api).json()
        # print(re)
        re1 = re['data']['url']
        s = '[CQ:image,file={},cache=0]'.format(re1)
        qqbot.send_private_msg(user_id=dic['user_id'], msg=s)
        # qqbot.send_msg({'msg_type': 'private', 'number': dic['user_id'], 'msg': s})


def on_notice(dic):
    pass


def setting():
    tk = tkinter.Tk()
    tk.geometry('300x200')
    tk.title('p3')
    tkinter.Label(tk, text='输入主人').pack()
    e = tkinter.Entry(tk)
    e.pack()
    b = tkinter.Button(text='确定')
    b.pack()
    tk.mainloop()
