import requests


# from sdk import Bot
from Plugin import Bot
name = '随机诗句'
qqbot: Bot
api = 'https://v1.jinrishici.com/all.json'
gp_id = 0


def enable():  # 插件被启用时被调用
    # qqbot.info({'type': 'debug', 'sender': '随机诗句', 'text': 'enable被执行，qqbot='+str(qqbot)})
    pass
    # global qqbot
    # qqbot = Api
    # return {'name': name, 'complain': '关键词：一言', 'author': 'None', 'ver': '0.1', 'p_id': p_id}


def init(p_id: int, Api: Bot):  # 插件第一次安装时调用
    global gp_id
    global qqbot
    gp_id = p_id
    qqbot = Api
    # qqbot.info({'type': 'debug', 'sender': '随机诗句', 'text': 'init被执行，pid='+str(p_id)})
    return {'name': name, 'complain': '关键词：一言', 'author': 'huazi', 'ver': '0.1', 'p_id': p_id,
            'respond_group_msg': True,
            'respond_private_msg': True, 'respond_notice': False, 'respond_request': False}


def close():
    pass


def on_group_msg(dic: dict):
    # qqbot.info({'type': 'debug', 'sender': '随机诗句', 'text': 'on_group_msg被执行，msg='+dic['message']})
    if dic['raw_message'] == '一言':
        response = requests.post(api).json()
        r1 = response['content'] + '\n' + '出处：' + response['origin'] + '\n' + '作者：' + response[
            'author'] + '\n' + '标签:' + response['category']
        qqbot.send_msg({'msg_type': 'group', 'number': dic['group_id'],
                        'msg': '[CQ:at,qq={}]'.format(str(dic['user_id'])) + r1}, delay=len(r1) ** 0.2)


def on_private_msg(dic: dict):
    if dic['raw_message'] == '一言':
        response = requests.post(api).json()
        r1 = response['content'] + '\n' + '出处：' + response['origin'] + '\n' + '作者：' + response[
            'author'] + '\n' + '标签:' + response['category']
        # print(r1)
        qqbot.send_msg({'msg_type': 'private', 'number': dic['user_id'], 'msg': r1}, delay=len(r1) ** 0.2)


# def on_notice(dic):
#     pass


def setting():
    pass


def disable():
    pass
