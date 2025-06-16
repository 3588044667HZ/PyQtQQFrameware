import sys
import threading

from time import sleep

import pluginLaoder
import pybot
from msg_deliver import deliver_msg
from pluginLaoder import loadplugin, add_plugins_to_ui
import argparse
import configparser

config = configparser.ConfigParser()
config.read('./data/config.ini')
if 'main' in config and 'ws_addr' in config['main']:
    pass
else:
    config['main'] = {'ws_addr': 'ws://192.1.68.1.109:6700', }

parser = argparse.ArgumentParser(description='选择是否启动UI.')
parser.add_argument('If_window', metavar='If_window', type=bool, nargs='?',
                    help='y or n or 不填,y即为启动UI,不填默认启动。', default=True)
opt = parser.parse_args()
if not opt.If_window:
    pass
else:  # UI初始化
    from PyQt5 import QtWidgets
    from PyQt5.QtCore import Qt
    from pybot import qqbot
    from window import Ui_MainWindow, TrayIcon

    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()

    ui = Ui_MainWindow(config)
    ui.setupUi(win)
    ui.WebsocketAddressEdit.setText(config.get('main', 'ws_addr'))
    if 'log' in config and 'lowest_log_level' in config['log'] and 'debug' in config['log'] and 'info' in config[
        'log'] and 'warning' in config['log'] and 'error' in config['log'] and 'critical' in config[
        'log'] and 'send_message' in config[
        'log'] and 'send_group_message' in config['log'] and 'recv_private_message' in config[
        'log'] and 'recv_group_message' in config['log'] and 'action' in config['log']:
        ui.logdic = config
    else:
        config['log']['debug'] = 'aaaa7f'
        config['log']['info'] = '55aaff'
        config['log']['warning'] = 'fff01c'
        config['log']['error'] = 'aa00ff'
        config['log']['critical'] = '000000'
        config['log']['send_message'] = '55aa00'
        config['log']['send_group_message'] = 'ff5500'
        config['log']['recv_private_message'] = '00aa00'
        config['log']['recv_group_message'] = '005500'
        config['log']['action'] = '00aaff'
        config['log']['lowest_log_level'] = '0'
    ti = TrayIcon(win)
    ti.show()
    win.show()

if pybot.USE_WEBSOCKET:
    cli = qqbot()


    def connect_():
        try:
            cli.connect(config.get('main', 'ws_addr'))
        except ConnectionRefusedError:
            ui.s.sendmsg.emit({'type': 'error', 'sender': '框架', 'text': '未成功连接到gocq,下面进行重试'})
            for i in range(5):
                try:
                    cli.connect()
                    ui.s.sendmsg.emit({'type': 'info', 'sender': '框架', 'text': '连接成功'})
                    break
                except ConnectionRefusedError:
                    ui.s.sendmsg.emit({'type': 'error', 'sender': '框架', 'text': '重试第%i次' % i})
                    continue


    threading.Thread(target=connect_).start()

else:
    cli = pybot.HttpClient()
ui.s.sendmsg.emit({'type': 'info', 'sender': '框架', 'text': '框架启动，版本0.1'})


def delay_deco(func):  # 延时装饰器
    def inner_delay(delay, *args, **kwargs):
        # print('延时', delay)
        if delay:
            # print(delay)
            sleep(delay)
        func(*args, **kwargs)

    return inner_delay


class BotApi:
    @staticmethod
    @delay_deco
    def send_msg(dic: dict, plugin_name: str):
        cli.send_msg(dic)
        ui.s.sendmsg.emit({'type': 'send_message', 'sender': '插件' + plugin_name, 'text': str(dic)})

    @staticmethod
    @delay_deco
    def send_group_msg(group: int, msg: str, plugin_name: str):
        cli.send_group_msg(group=group, msg=msg)
        ui.s.sendmsg.emit(
            {'type': 'send_group_message', 'sender': '插件' + plugin_name, 'text': '发送群' + str(group) + msg})

    @staticmethod
    @delay_deco
    def info(s: dict):
        ui.s.sendmsg.emit(s)

    @staticmethod
    @delay_deco
    def delete_friend(friend_id: int, plugin_name: str):
        # sleep(delay)
        cli.delete_friend(id=friend_id)
        ui.s.sendmsg.emit({'type': 'action', 'sender': '插件' + plugin_name, 'text': '删除好友' + str(friend_id)})

    @staticmethod
    @delay_deco
    def group_request(flag, type_, approve, reason, plugin_name: str):
        # sleep(delay)
        cli.group_request(flag=flag, type=type_, approve=approve, reason=reason, )
        ui.s.sendmsg.emit({'type': 'action', 'sender': '插件' + plugin_name, 'text': '回应群邀请' + str(flag)})

    @staticmethod
    @delay_deco
    def friend_request(flag, approve, remark):  # 加好友请求的 flag（需从上报的数据中获得）|是否同意请求|添加后的好友备注（仅在同意时有效）
        # sleep(delay)
        cli.friend_request(flag=flag, approve=approve, remark=remark)

    @staticmethod
    @delay_deco
    def kick(group_id: int, user_id, reject_add_request, plugin_name: str):
        # sleep(delay)
        cli.kick(group_id=group_id, user_id=user_id, reject_add_request=reject_add_request)
        ui.s.sendmsg.emit(
            {'type': 'action', 'sender': '插件' + plugin_name, 'text': str(group_id) + '踢' + str(user_id)})
        return 0

    @staticmethod
    @delay_deco
    def ban(group_id, user_id, time, plugin_name: str):  # 群中单人禁言
        # sleep(delay)
        cli.ban(group_id=group_id, user_id=user_id, time=time)
        ui.s.sendmsg.emit({'type': 'action', 'sender': '插件' + plugin_name,
                           'text': '群' + str(group_id) + '禁言' + str(user_id) + ' ' + str(time) + '秒'})
        return 0

    @staticmethod
    @delay_deco
    def set_title(group_id, user_id, special_title, plugin_name: str):
        # sleep(delay)
        cli.set_title(group_id=group_id, user_id=user_id, special_title=special_title)
        ui.s.sendmsg.emit({'type': 'action', 'sender': '插件' + plugin_name,
                           'text': '群%i 改昵称%s %s' % (group_id, user_id, special_title)})
        return

    @staticmethod
    @delay_deco
    def group_ban(group_id, enable, plugin_name: str):
        # sleep(delay)
        cli.group_ban(group_id=group_id, enable=enable)
        ui.s.sendmsg.emit(
            {'type': 'action', 'sender': '插件' + plugin_name, 'text': '%i全体群禁%s' % (group_id, enable)})

    @staticmethod
    @delay_deco
    def set_group_special_title(gid: int, uid: int, title: str, plugin_name: str):
        # sleep(delay)
        cli.set_group_special_title(gid=gid, uid=uid, title=title)
        ui.s.sendmsg.emit({'type': 'action', 'sender': '插件' + plugin_name,
                           'text': '群%i 改头衔%s %s' % (gid, uid, title)})

    @staticmethod
    @delay_deco
    def send_group_sign(group_id: int, plugin_name: str):
        # sleep(delay)
        cli.send_group_sign(group_id)
        ui.s.sendmsg.emit({'type': 'action', 'sender': '插件' + plugin_name,
                           'text': '群%d打卡' % group_id})

    @staticmethod
    @delay_deco
    def send_private_msg(user_id, msg: str, plugin_name: str):
        cli.send_private_msg(user_id, msg)
        ui.s.sendmsg.emit({'type': 'action', 'sender': '插件' + plugin_name,
                           'text': '向%d发送私聊消息%s' % (user_id, msg)})

    @staticmethod
    def delete_msg(msg_id):
        cli.del_msg(msg_id)


loadplugin(ui, BotApi)
add_plugins_to_ui()
if cli.connection is None and pybot.USE_WEBSOCKET:  # 使用websocket协议且未链接时
    ui.s.sendmsg.emit({'type': 'error', 'sender': '框架', 'text': '连接gocq失败，请重启框架'})
    deliver_msg(ui, pluginLaoder.p_list, None, BotApi)
else:
    deliver_msg(ui, pluginLaoder.p_list, cli, BotApi)
# except AttributeError:

if pybot.USE_WEBSOCKET:
    ui.s.sendmsg.emit({'type': 'info', 'sender': '框架', 'text': '使用websocket协议进行链接'})
else:
    ui.s.sendmsg.emit({'type': 'error', 'sender': '框架', 'text': '使用http协议'})
if opt.If_window:
    app.exec_()
    win.close()
    cli.connection.close()
else:
    pass
with open('./data/config.ini', 'w+') as configfile:
    config.write(configfile)
    # print('end')
