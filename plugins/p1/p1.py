import tkinter

import json
import re
import requests
import configparser
from Plugin import Bot

name = 'p1'
conf = configparser.ConfigParser()
conf.read('./plugins/p1/conf.ini')

url = 'https://api.mlyai.com/reply'
mly_head = {'Api-Key': conf.get('main', 'Api-Key'), 'Api-Secret': conf.get('main', 'Api-Secret'),
            'Content-Type': 'application/json;charset=UTF-8'}
qqbot: Bot
gp_id = 0


def init(p_id: int, Api: Bot, ):  # 框架启动调用
    global gp_id
    global qqbot
    gp_id = p_id
    qqbot = Api
    return {'name': name, 'complain': '茉莉云AI对话', 'author': 'huazi', 'ver': '0.1', 'p_id': p_id,
            'respond_group_msg': True, 'respond_private_msg': True, 'respond_notice': True, 'respond_request': False}


def close():
    pass


def enable():  # 插件被启用时被调用
    pass
    # return {'name': name, 'complain': '茉莉云对话AI', 'author': 'None', 'ver': '0.1', 'p_id': p_id}


def disable():
    pass


def on_group_msg(dic: dict):
    try:
        msg = dic['message']
        qq = dic['user_id']
        if dic['post_type'] == 'message' and '[CQ:at,qq=3155789073]' in dic['raw_message']:
            data = {'content': msg.replace('[CQ:at,qq=3155789073]', ''), 'type': '2', 'from': qq,
                    'fromName': dic['sender']['nickname'], 'to': dic['group_id']}
            res = requests.post(url, data=json.dumps(data), headers=mly_head).json()
            qqbot.send_group_msg(dic['group_id'],
                                 "[CQ:reply,id={0}] [CQ:at,qq={1}]".format(str(dic['message_id']), dic['user_id']) +
                                 res['data'][0]['content'],
                                 delay=len(res['data'][0]['content']) * 0.5)
        if re.match('^/echo.(.*?)', msg):
            qqbot.send_group_msg(dic['group_id'], str(re.findall(r'^/echo.(.*?)$', msg)[0]), delay=0.7)

    except:
        pass


def on_private_msg(dic: dict):
    try:
        msg = dic['raw_message']
        qq = dic['user_id']
        if dic['raw_message'] == '一言':
            return
        elif dic['raw_message'] == '一图':
            return
        elif '搜图' in dic['raw_message'] and dic['raw_message'].index('搜图') == 0:
            return
        elif dic["raw_message"] == '老黄历':
            return
        elif dic['raw_message'] == '百度词条':
            return
        elif dic['raw_message'] == '查询天气':
            return
        elif dic['raw_message'] == '华子我要个性名片':
            return
        elif '禁言' in dic['raw_message'] and dic['raw_message'].index('禁言') == 0:
            return
        elif '解除禁言' in dic['raw_message'] and dic['raw_message'].index('解除禁言') == 0:
            return
        elif '加代管' in dic['raw_message'] and dic['raw_message'].index('加代管') == 0:
            return
        elif '删代管' in dic['raw_message'] and dic['raw_message'].index('删代管') == 0:
            return
        elif dic['raw_message'] == '查询所有代管':
            return
        elif '我要头衔' in dic['raw_message'] and dic['raw_message'].index('我要头衔') == 0:
            return
        elif '固定头衔' in dic['raw_message'] and dic['raw_message'].index('固定头衔') == 0:
            return
        elif '解除固定' in dic['raw_message'] and dic['raw_message'].index('解除固定') == 0:
            return
        elif '设置头衔' in dic['raw_message'] and dic['raw_message'].index('设置头衔') == 0:
            return
        elif dic['raw_message'] == '每日新闻':
            return
        if ('sender_id' in dic and 'group_id' not in dic) or dic['message_type'] == 'private':
            data = {'content': msg, 'type': '1', 'from': qq}
            res = requests.post(url, data=json.dumps(data), headers=mly_head).json()
            qqbot.send_private_msg(user_id=dic['user_id'], msg=res['data'][0]['content'],
                                   delay=len(res['data'][0]['content']) * 0.4)
    except ZeroDivisionError:

        pass


# {'msg_type': 'private', 'number': dic['user_id'], 'msg': res['data'][0]['content']},
# delay=len(res['data'][0]['content']) * 0.9)
def on_notice(dic):
    # print(dic)
    subtype: str = dic['sub_type']
    qq = dic['user_id']
    if dic['target_id'] == 3155789073:
        if 'group_id' in dic:  # 群聊戳
            data = {'content': subtype, 'type': '2', 'from': qq,
                    'to': dic['group_id']}
            res = requests.post(url, data=json.dumps(data), headers=mly_head).json()
            qqbot.send_group_msg(dic['group_id'], res['data'][0]['content'],
                                 delay=len(res['data'][0]['content']) * 0.4)
        else:
            data = {'content': subtype, 'type': '1', 'from': qq,
                    'to': dic['user_id']}
            res = requests.post(url, data=json.dumps(data), headers=mly_head).json()
            qqbot.send_private_msg(user_id=dic['user_id'], msg=res['data'][0]['content'],
                                   delay=len(res['data'][0]['content']) * 0.4)


def setting():
    tk = tkinter.Tk()
    tk.geometry('300x200')
    tk.title('p1')

    tkinter.Label(tk, text='输入Api-Key').pack()
    api_key = tkinter.Entry(tk)
    api_key.pack(fill=tkinter.X)
    api_key.insert(0, conf['main']['Api-Key'])

    tkinter.Label(tk, text='输入Api-Secret').pack()
    Api_Secret = tkinter.Entry(tk)
    Api_Secret.pack(fill=tkinter.X)
    Api_Secret.insert(0, conf['main']['Api-Secret'])

    def writing_config():
        conf['main']['Api-Key'] = api_key.get()
        conf['main']['Api-Secret'] = Api_Secret.get()
        with open('conf.ini', 'w') as f:
            conf.write(f)

    b = tkinter.Button(text='保存', command=writing_config)
    b.pack()
    # b.
    tk.mainloop()


if __name__ == '__main__':
    setting()
