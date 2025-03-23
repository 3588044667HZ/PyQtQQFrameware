import tkinter

name = '每日新闻'
import requests

complain = '每日新闻'

api = 'http://dwz.2xb.cn/zaob'

# from sdk import Bot

qqbot = None
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
    # global gp_id
    # global qqbot
    # gp_id = p_id
    # qqbot = Api
    # return {'name': name, 'complain': complain, 'author': 'None', 'ver': '0.1', 'p_id': p_id}


def disable():  # 插件被禁用时被调用
    pass


def on_group_msg(dic):
    if dic['message'] == '每日新闻':
        res = requests.get(url=api).json()
        if res['code'] == 200:
            qqbot.send_group_msg(dic['group_id'],
                                 '[CQ:image,file={1},cache=0]'.format(res['datatime'], res['imageUrl']))
        else:
            qqbot.send_group_msg(dic['group_id'], '获取失败')


def on_private_msg(dic):
    if dic['message'] == '每日新闻':
        res = requests.get(url=api).json()
        if res['code'] == 200:
            qqbot.send_msg({'msg_type': 'private', 'number': dic['user_id'],
                            'msg': '[CQ:image,file={1},cache=0]'.format(res['datatime'], res['imageUrl'])}, delay=1)
        else:
            qqbot.send_msg({'msg_type': 'private', 'number': dic['user_id'], 'msg': '获取失败'})


def on_notice(dic):
    pass


def setting():
    tk = tkinter.Tk()
    tk.geometry('300x200')
    tk.title('每日新闻')
    tkinter.Label(tk, text='test').pack()
    e = tkinter.Entry(tk)
    e.pack()
    b = tkinter.Button(text='确定')
    b.pack()
    tk.mainloop()
# def disable()
