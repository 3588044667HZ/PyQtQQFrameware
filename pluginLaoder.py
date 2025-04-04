import json
import os
# import tkinter.filedialog as di
import shutil
import zipfile

import PyQt5
from PyQt5.QtWidgets import QMessageBox, QFileDialog

import sqlite
from Plugin import Plugin, Bot

Api = object
p_list = list()

ui: PyQt5.QtWidgets.QWidget
# respond_group_plugin = list()
# respond_private_plugin = list()
# respond_notice = list()
sql = sqlite.SqliteSDB('./data/data.db', check_same_thread=False)
sql.create_table('plugin_setting', 'pid int PRIMARY Key not null', 'name text', 'author text', 'ver int',
                 'is_enable int',
                 'complain text')


def loadplugin(_ui: object, BotApi):
    global Api
    Api = BotApi
    global ui
    ui = _ui
    name = sql.selectAll('plugin_setting')
    if name:  # 有插件
        for i in name:
            try:
                p = __import__('plugins' + '.' + i[1] + '.' + i[1],
                               fromlist=i[1])  # todo
                res = p.init(hash(p), Bot(Api, hash(p), can_group=True, name=p.name))
                tmp = Plugin(name=res['name'],
                             version=res.get('ver'),
                             author=res.get('author'), setting=p.setting, pid=res['p_id'],
                             enable_func=p.enable, disable_func=p.disable, complain=res.get('complain'),
                             if_groupMsg=True,
                             if_notice=True,
                             if_privateMsg=True, respond_group_msg=res.get('respond_group_msg', False),
                             respond_private_msg=res.get('respond_private_msg', False),
                             respond_notice=res.get('respond_notice', False),
                             respond_request=res.get('respond_request'))
                if tmp.respond_group_msg:
                    tmp.on_group_msg = p.on_group_msg
                if tmp.respond_private_msg:
                    tmp.on_private_msg = p.on_private_msg
                if tmp.respond_notice:
                    tmp.on_notice = p.on_notice
                if tmp.respond_request:
                    tmp.on_request = p.on_request
                if i[4] == 1:
                    tmp.enable = True
                else:
                    tmp.enable = False
                p_list.append(tmp)
                ui.s.sendmsg.emit({'type': 'info', 'sender': '框架', 'text': '加载插件%s' % i[1]})
            except ModuleNotFoundError:
                ui.s.sendmsg.emit({'type': 'error', 'sender': '框架', 'text': '加载插件%s时出错，未找到插件本体。' % i[1]})
                sql.delete('plugin_setting', name=i[1])
                sql.commit()
        return
    else:
        return 0


def add_plugins_to_ui() -> None:
    if p_list == 0:
        return 0
    else:
        for i in p_list:
            if i.enable:
                i.enable_func()
                ui.s.add_plugin.emit(i)
            else:
                ui.s.add_plugin.emit(i)


def add_plugin_with_win():  # 添加插件
    path, _ = QFileDialog.getOpenFileName()
    print(path)
    # path = filedialog.askopenfilename()  # todo
    if path:
        with zipfile.ZipFile(path, 'r') as f:
            info = json.loads(f.read('info.json'))
            print(info)
            ui.s.sendmsg.emit({'type': 'info', 'sender': '框架', 'text': '添加插件' + info['name']})
            print(1)
            if os.path.exists('./plugins/' + info['name']):
                QMessageBox.information(ui, '插件重名', info['name'] + '插件已存在或插件名冲突', QMessageBox.Yes)
                # messagebox.showinfo('插件重名', info['name'] + '插件已存在或插件名冲突')
            else:
                os.mkdir('./plugins/' + info['name'])
                f.extractall(path='./plugins/' + info['name'])
                if set(os.listdir('./plugins/' + info['name'])) == set(info['dist']):
                    module = __import__('plugins' + '.' + info['name'] + '.' + info['name'],
                                        fromlist=info['name'])  # todo
                    print(module)
                    res: dict = module.init(p_id=hash(module), Api=Api)
                    print('res', res)
                    pg = Plugin(name=res['name'],
                                version=res.get('ver', 0.0),
                                author=res.get('author', 'NNN'), setting=module.setting, pid=res['p_id'],
                                enable_func=module.enable, disable_func=module.disable, complain=res.get('complain'),
                                if_groupMsg=True,
                                if_notice=True,
                                if_privateMsg=True, respond_group_msg=res.get('respond_group_msg', False),
                                respond_private_msg=res.get('respond_private_msg', False),
                                respond_notice=res.get('respond_notice', False),
                                respond_request=res.get('respond_request', False))
                    print('pg', pg)
                    if pg.respond_group_msg:
                        pg.on_group_msg = module.on_group_msg
                    if pg.respond_private_msg:
                        pg.on_private_msg = module.on_private_msg
                    if pg.respond_notice:
                        pg.on_notice = module.on_notice
                    if pg.respond_request:
                        pg.on_request = module.on_request
                    p_list.append(pg)
                    print(p_list)
                    ui.s.add_plugin.emit(pg)
                    sql.insert('plugin_setting', hash(module), res['name'], res['author'], res['ver'], False,
                               res['complain'])
                else:
                    QMessageBox.warning(ui, '安装错误', info['name'] + '安装包不完整', QMessageBox.Yes)
                    # messagebox.showwarning('安装错误', info['name'] + '安装包不完整')  # todo
                    shutil.rmtree('./plugins/' + info['name'])
    else:
        ui.s.sendmsg.emit({'type': 'info', 'sender': '框架', 'text': '用户取消添加插件'})
