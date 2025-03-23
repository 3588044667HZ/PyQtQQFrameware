import tkinter

name = '群管'
import configparser
import os
from threading import Thread
import msg_deliver

# import re

# from sdk import Bot

conf = configparser.ConfigParser()
try:
    conf.read('./data/群管插件/data.ini', encoding='UTF-8')
    daiguan = conf.get('system', 'admin').split(',')
    guding = conf.get('data', '固定头衔').split(r',')
except:
    print('群管数据不存在')
qqbot = None
gp_id = 0
complain = '群管'


def init(p_id: int, Api: object):
    global gp_id
    global qqbot
    gp_id = p_id
    qqbot = Api
    if os.path.exists('./data/群管插件/data.ini'):
        pass
    else:
        os.mkdir('./data/群管插件')
        os.chdir('./data/群管插件')
        conf.read('data.ini', encoding='UTF-8')
        conf.add_section('system')
        conf.add_section('data')
    return {'name': name, 'complain': complain, 'author': 'None', 'ver': '0.1', 'p_id': p_id, 'respond_group_msg': True,
            'respond_private_msg': False, 'respond_notice': False, 'respond_request': True}


def on_group_msg(rev):
    if rev['raw_message'] == 'com撤回消息' and str(rev['user_id']) in daiguan:
        qqbot.delete_msg(msg_deliver.last_message_id)
    if '禁言' in rev['raw_message'] and rev['raw_message'].index('禁言') == 0:
        t = Thread(target=group_ban, args=(rev,))
        t.start()

    elif '解除禁言' in rev['raw_message'] and rev['raw_message'].index('解除禁言') == 0:
        t = Thread(target=cancel_groupban, args=(rev,))
        t.start()
    elif '加代管' in rev['raw_message'] and rev['raw_message'].index('加代管') == 0:
        t = Thread(target=setadmin, args=(rev,))
        t.start()
    elif '删代管' in rev['raw_message'] and rev['raw_message'].index('删代管') == 0:
        t = Thread(target=deladmin, args=(rev,))
        t.start()
    elif rev['raw_message'] == '查询所有代管':
        t = Thread(target=count_admin, args=(rev,))
        t.start()
    elif '我要头衔' in rev['raw_message'] and rev['raw_message'].index('我要头衔') == 0:
        settitle(rev)
    elif '固定头衔' in rev['raw_message'] and rev['raw_message'].index('固定头衔') == 0:
        set_fix_title(rev['user_id'], rev['raw_message'].replace('固定头衔', ''), rev['group_id'])
    elif '解除固定' in rev['raw_message'] and rev['raw_message'].index('解除固定') == 0:
        cancel_fix(rev['user_id'], rev['raw_message'].replace('解除固定', ''), rev['group_id'])
    elif '设置头衔' in rev['raw_message'] and rev['raw_message'].index('设置头衔') == 0:
        admin_set_title(rev)


def on_request(dic: dict):
    if dic['request_type'] == 'friend':
        qqbot.send_msg({'msg_type': 'private', 'number': conf.getint('system', 'master'),
                        'msg': '收到好友请求，QQ号：{0}\nflag:{1}'.format(dic['user_id'], dic['flag'])})
    elif dic['request_type'] == 'group':
        qqbot.send_msg({'msg_type': 'private', 'number': conf.getint('system', 'master'),
                        'msg': '收到加群请求，群号：{0}\nflag:{1}\n发送请求的好友:{2}'.format(dic['group_id'], dic['flag'],
                                                                             dic['user_id'])})


# def on_private_msg(dic:dict):
#     if re.match(r'',dic['message'])

def group_ban(dic):  # 设置禁言
    uid, time = dic['message'].replace('禁言', '').split(' ')
    if str(dic['user_id']) in daiguan:
        if '秒' in time:
            tim1 = time.replace('秒', '')
        elif '分钟' in time:
            tim = time.replace('分钟', '')
            tim1 = int(tim) * 60
        elif '小时' in time:
            tim = time.replace('小时', '')
            tim1 = int(tim) * 3600
        elif '天' in time:
            tim = time.replace('天', '')
            tim1 = int(tim) * 86400
        elif '月' in time:
            tim = time.replace('天', '')
            tim1 = int(tim) * 2592000
    qqbot.ban(group_id=dic['group_id'], user_id=uid, time=tim1)


def cancel_groupban(dic):
    if dic['message_type'] == 'group' and str(dic['user_id']) in daiguan:
        uid = int(dic['message'].replace('解除禁言', ''))
        qqbot.ban(group_id=dic['group_id'], user_id=int(uid), time=0)
        qqbot.send_group_msg(dic['group_id'], '已执行')
    else:
        qqbot.send_group_msg(group=dic['group_id'], msg='操作失败')


def setadmin(dic):  # 设置代管
    if str(dic['user_id']) == conf.get('system', 'master'):
        admin = dic['message'].replace('加代管', '')
        daiguan.append(admin)
        conf.set('system', 'admin', ','.join(daiguan))
        conf.write(open('data.ini', 'w', encoding='utf-8'))
        del admin
        if dic['message_type'] == 'group':
            qqbot.send_group_msg(group=dic['group_id'], msg='成功')
        else:
            qqbot.send_msg({'msg_type': 'private', 'number': dic['user_id'], 'msg': '成功'})
    else:
        qqbot.send_group_msg(group=dic['group_id'], msg='失败')


def deladmin(dic):  # 删除代管
    if str(dic['user_id']) == conf.get('system', 'master'):
        admin = dic['message'].replace('删代管', '')
        daiguan.remove(admin)
        del admin
        conf.set('system', 'admin', ','.join(daiguan))
        conf.write(open('data.ini', 'w', encoding='utf-8'))
        if dic['message_type'] == 'group':
            qqbot.send_group_msg(group=dic['group_id'], msg='[CQ:reply,id=%s] 成功' % dic['message_id'])
        else:
            qqbot.send_msg(
                {'msg_type': 'private', 'number': dic['user_id'], 'msg': '[CQ:reply,id=%s] 成功' % dic['message_id']})
    else:
        if dic['message_type'] == 'group':
            qqbot.send_group_msg(group=dic['group_id'], msg='失败')
        else:
            qqbot.send_msg({'msg_type': 'private', 'number': dic['user_id'], 'msg': '失败'})


def count_admin(dic):  # 输出代管
    admins = '\n'.join(daiguan)
    if str(dic['user_id']) in daiguan:
        if dic['message_type'] == 'group':
            qqbot.send_group_msg(group=dic['group_id'], msg=admins)
        else:
            qqbot.send_msg({'msg_type': 'private', 'number': dic['user_id'], 'msg': admins})
    else:
        if dic['message_type'] == 'group':
            qqbot.send_group_msg(group=dic['group_id'], msg='只有代管才能查看呦～')
        else:
            qqbot.send_msg({'msg_type': 'private', 'number': dic['user_id'], 'msg': '只有代管才能查看呦～'})


def settitle(dic):
    if dic['message_type'] == 'group':
        m_str = dic['message'].replace('我要头衔', '')
        if len(m_str) <= 6:
            if str(hash(str(dic['user_id'])) + hash(str(dic['group_id']))) not in guding:
                qqbot.set_group_special_title(gid=dic['group_id'], uid=dic['user_id'], title=m_str)
            else:
                qqbot.send_group_msg(dic['group_id'], '头衔已被固定，无法更改哦')
        else:
            qqbot.send_group_msg(dic['group_id'], '头衔太长了啦', p_id=gp_id)
    else:
        qqbot.send_msg({'msg_type': 'private', 'number': dic['user_id'], 'msg': '只能群聊使用～'})


def admin_set_title(dic):
    if dic['message_type'] == 'group' and dic['message'].insex('我要头衔') == 0:
        if str(dic['user_id']) in daiguan:
            uid, title = dic['message'].replace('设置头衔', '').split(' ')
            qqbot.set_group_special_title(gid=dic['group_id'], uid=uid, title=title)
            qqbot.send_group_msg(dic['group_id'], '[CQ:reply,id=%s]  完成' % dic['message_id'])
        else:
            qqbot.send_group_msg(dic['group_id'], '[CQ:reply,id=%s] 此功能仅代管可用' % dic['message_id'])
    else:
        pass


def set_fix_title(sender_id, uid, gid):
    if str(sender_id) in daiguan:
        text = str(hash(str(uid)) + hash(str(gid)))
        guding.append(text)
        conf.set('data', '固定头衔', ','.join(guding))
        conf.write(open('data.ini', 'w', encoding='UTF-8'))
        print('fix', text)


def cancel_fix(sender_id, uid: int, gid: int):
    if str(sender_id) in daiguan:
        text = str(hash(str(uid)) + hash(str(gid)))
        guding.remove(text)
        conf.set('data', '固定头衔', ','.join(guding))
        conf.write(open('data.ini', 'w', encoding='UTF-8'))
        print('cancel_fix', text)


def enable():  # 插件被启用时被调用
    pass


def disable():
    pass


def set_ini(i):
    conf.set('system', 'master', i)
    conf.write(open('data.ini', 'w', encoding='utf-8'))


def setting():
    tk = tkinter.Tk()
    tk.geometry('300x200')
    tk.title('群管')
    tkinter.Label(tk, text='输入主人').pack()
    e = tkinter.Entry(tk)
    e.pack()
    e.insert(0, conf.get('system', 'master'))
    b = tkinter.Button(text='确定', command=lambda: set_ini(e.get()))
    b.pack()
    tk.mainloop()
