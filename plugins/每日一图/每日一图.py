import requests

name = '每日一图'
qqbot = None
gp_id = 0
# import re
import sys
import copy

user_list = list()
url = 'https://api.lolicon.app/setu/v2?size=original&size=regular'


def parseParm(s: str):
    ParmList = s.split(' ')
    # ParmDict = dict()
    for i in ParmList:
        try:
            url_ = copy.deepcopy(url)
            url_ = url_ + '&' + i
        except:
            return ''
    return url_


def init(p_id: int, Api):  # 框架启动调用
    # print('init', Api, p_id)
    global gp_id
    global qqbot
    gp_id = p_id
    qqbot = Api
    return {'name': name, 'complain': '发送每日一图即可', 'author': 'huazi', 'ver': '0.1', 'p_id': p_id,
            'respond_group_msg': True, 'respond_private_msg': True, 'respond_notice': False, 'respond_request': False}


def close():
    pass


def enable():  # 插件被启用时被调用
    pass


def disable():
    pass


def on_group_msg(dic: dict):
    try:
        if dic['post_type'] == 'message':
            if dic['raw_message'] == '一图':
                user_list.append(dic['user_id'])
                qqbot.send_group_msg(dic['group_id'], '请发送参数，或发送 跳过 来直接获得图片', delay=0.5)
                return
            else:
                if dic['user_id'] in user_list:
                    user_list.remove(dic['user_id'])
                    if dic['raw_message'] == '跳过':
                        res = requests.get(url).json()['data'][0]
                        qqbot.send_group_msg(dic['group_id'],
                                             f"已取得作品信息如下：\n 标题:{res['title']}\n 画师:{res['author']}\n tags:{res['tags']}\n 网址:{res['urls']['original']}",
                                             delay=0.5)
                        return
                    else:
                        url2 = parseParm(dic['raw_message'])
                        res = requests.get(url2).json()['data'][0]
                        qqbot.send_group_msg(dic['group_id'],
                                             f"已取得作品信息如下：\n 标题:{res['title']}\n 画师:{res['author']}\n tags:{res['tags']}\n 网址:{res['urls']['original']}",
                                             delay=0.5)
                        return
        else:
            return
    except:
        print(str(sys.exc_info()[1]))


def on_private_msg(dic: dict):
    try:
        if dic['post_type'] == 'raw_message':
            if dic['raw_message'] == '一图':
                user_list.append(dic['user_id'])
                qqbot.send_msg({'msg_type': 'private', 'number': dic['user_id'], 'msg': '请发送参数，或发送 跳过 来直接获得图片'})
                # qqbot.send_group_msg(dic['group_id'], '请发送参数，或发送 跳过 来直接获得图片')
                return
            else:
                if dic['user_id'] in user_list:
                    user_list.remove(dic['user_id'])
                    if dic['raw_message'] == '跳过':
                        # res = requests.get(url).json()['data'][0]
                        qqbot.send_msg({'msg_type': 'private', 'number': dic['user_id'], 'msg': '请发送参数，或发送 跳过 来直接获得图片'},
                                       delay=0.9)
                        # qqbot.send_group_msg(dic['group_id'],
                        #                      f"已取得作品信息如下：\n 标题:{res['title']}\n 画师:{res['author']}\n tags:{res['tags']}\n 网址:{res['urls']['original']}")
                        return
                    else:
                        url2 = parseParm(dic['raw_message'])
                        res = requests.get(url2).json()['data'][0]
                        qqbot.send_msg({'msg_type': 'private', 'number': dic['user_id'],
                                        'msg': f"已取得作品信息如下：\n 标题:{res['title']}\n 画师:{res['author']}\n tags:{res['tags']}\n 网址:{res['urls']['original']}"},
                                       delay=0.9)
                        return
        else:
            return
    except:
        print(str(sys.exc_info()[1]))


# def on_notice(dic):
#     return


def setting():
    return


if __name__ == '__main__':
    url1 = parseParm('r18=1')
    # res = requests.get(url).json()['data'][0]
    print(url1)
