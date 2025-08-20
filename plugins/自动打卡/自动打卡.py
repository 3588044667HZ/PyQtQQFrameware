import tkinter

import time
from Plugin import Bot
import random

name = '自动打卡'
qqbot: Bot
gp_id = 0
face_list = [
    '[CQ:image,summary=&#91;动画表情&#93;,file=9D122EC85DCE955D3E8091C7C985A623.jpg,sub_type=1,url=https://gchat.qpic.cn/gchatpic_new/0/0-0-9D122EC85DCE955D3E8091C7C985A623/0,file_size=2506]',
    '[CQ:image,summary=&#91;动画表情&#93;,file=207AADB3EBE596A262223A3300E9CE13.gif,sub_type=1,url=https://gchat.qpic.cn/gchatpic_new/0/0-0-207AADB3EBE596A262223A3300E9CE13/0,file_size=533007]',
    '[CQ:image,file=BFDC7052D7E6E22F57090B24F6B15309.jpg,sub_type=0,url=https://gchat.qpic.cn/gchatpic_new/0/0-0-BFDC7052D7E6E22F57090B24F6B15309/0,file_size=9804]',
    '[CQ:image,file=https://c-ssl.duitang.com/uploads/blog/202304/02/20230402050453_d7ce1.jpg]']


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
        msg = f"""活着
        {random.choice(face_list)}
        """
        qqbot.send_group_msg(dic['group_id'], msg, delay=3)
    else:
        pass


def setting():
    tk = tkinter.Tk()
    tk.mainloop()
