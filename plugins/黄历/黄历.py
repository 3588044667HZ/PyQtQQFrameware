name = '黄历'
import requests

# from sdk import Bot

api = 'http://xiaobai.klizi.cn/API/other/laohuangli.php'

gp_id = 0
complain = '老黄历'
qqbot = None


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


def on_private_msg(dic):
    if dic['message'] == '老黄历':
        s = requests.get(api).text
        qqbot.send_msg({'msg_type': 'private', 'number': dic['user_id'], 'msg': s}, delay=len(s) * 0.05)


def on_group_msg(dic):
    if dic['message'] == '老黄历':
        s = requests.get(api).text
        qqbot.send_group_msg(dic['group_id'], s, delay=len(s) * 0.05)


# def on_notice(dic):
#     pass


def setting():
    pass
# def disable
