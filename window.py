import shutil
import sqlite3
import threading
from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRect, QCoreApplication, QSize, QMetaObject
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTreeWidgetItem, QHBoxLayout, QMenu, QColorDialog, QFileDialog
from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QTreeWidget, QAbstractScrollArea, QComboBox, \
    QListWidgetItem, QPushButton, QGroupBox, QCheckBox, QLabel, QListWidget, QMenuBar, QStatusBar, \
    QLineEdit

from Plugin import Plugin
from msg_deliver import del_plugin
from pluginLaoder import sql, add_plugin_with_win


class MyTypeSignal(QObject):
    # 定义一个信号
    sendmsg = pyqtSignal(dict)
    add_plugin = pyqtSignal(Plugin)


class ImportPluginThread(QThread):
    open_files = pyqtSignal()

    def __init__(self, parent=None):
        super(ImportPluginThread, self).__init__(parent=parent)

        # self.working = True

    def run(self):
        self.open_files.emit()

    def __del__(self):
        self.wait()


class Message_detail(object):  # 定义消息详情界面
    def __init__(self):
        self.Form = QtWidgets.QWidget()
        # Form.show()
        self.Form.setFixedSize(self.Form.width(), self.Form.height())
        self.Form.setObjectName("Message detail")
        self.Form.setWindowIcon(QIcon('./icons/message.png'))
        self.Form.resize(552, 299)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.Form)
        self.plainTextEdit.setGeometry(QtCore.QRect(3, 3, self.Form.width() - 10, self.Form.height() - 10))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.Form)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.Form.setWindowTitle(_translate("Message detail", "消息详情"))

    def show_ui(self):
        self.Form.show()

    def set_text(self, s: str):
        self.plainTextEdit.setPlainText(s)


class My_tree_item(QTreeWidgetItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin: Plugin


class Ui_MainWindow(object):
    s = MyTypeSignal()

    def __init__(self, config):
        self.logging_degrees = None
        self.logdic = None
        self.scrollAreaWidgetContents = None
        self.plugins = []
        self.plu_list = None
        self.mainwindow = None
        self.layout = QHBoxLayout()
        self.logs = []
        self.s.sendmsg.connect(self.addlog)
        self.s.add_plugin.connect(self.addplugin)  # 添加函数
        self.heighest_log_level = int(config['log']['lowest_log_level'])
        # self.logdic = config
        self.config = config

    def setupUi(self, MainWindow):
        self.mainwindow = MainWindow
        MainWindow.setWindowTitle(u"QC框架")
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(686, 393)
        icon = QIcon()
        icon.addFile(u"./icons/qmiao.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.main = QTabWidget(self.centralwidget)
        self.main.setObjectName(u"main")
        self.plugin_managment_tree_widget = QWidget()
        self.plugin_managment_tree_widget.setObjectName(u"plugin_managment_tree_widget")
        self.verticalLayout = QVBoxLayout(self.plugin_managment_tree_widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.treeWidget_2 = QTreeWidget(self.plugin_managment_tree_widget)
        # self.treeWidget_2.setWidgetResizable(False)
        self.treeWidget_2.setObjectName(u"treeWidget_2")
        self.treeWidget_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.treeWidget_2.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.verticalLayout.addWidget(self.treeWidget_2)

        icon1 = QIcon()
        icon1.addFile(u"./icons/pyd.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.main.addTab(self.plugin_managment_tree_widget, icon1, "")
        self.log_tab = QWidget()
        self.log_tab.setObjectName(u"log_tab")
        self.verticalLayout1 = QVBoxLayout(self.log_tab)
        self.verticalLayout1.setObjectName(u"verticalLayout1")
        self.logging_treeWidget = QTreeWidget(self.log_tab)
        self.logging_treeWidget.setObjectName(u"logging_treeWidget")
        self.logging_treeWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.logging_treeWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.verticalLayout1.addWidget(self.logging_treeWidget)
        self.main.addTab(self.log_tab, "")
        # self.logging_treeWidget.raise_()
        self.setting_tab = QWidget()
        self.setting_tab.setObjectName(u"setting_tab")
        self.horizontalLayout_3 = QHBoxLayout(self.setting_tab)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")

        self.AboatLogging = QGroupBox(self.setting_tab)
        self.AboatLogging.setObjectName(u"AboatLogging")
        self.label_2 = QLabel(self.AboatLogging)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 30, 91, 16))
        self.heigest_log_level = QComboBox(self.AboatLogging)
        self.heigest_log_level.addItem("")
        self.heigest_log_level.addItem("")
        self.heigest_log_level.addItem("")
        self.heigest_log_level.addItem("")
        self.heigest_log_level.addItem("")
        self.heigest_log_level.setObjectName(u"heigest_log_level")
        self.heigest_log_level.setGeometry(QRect(10, 60, 161, 22))
        self.chaget_log_color = QGroupBox(self.AboatLogging)
        self.chaget_log_color.setObjectName(u"chaget_log_color")
        self.chaget_log_color.setGeometry(QRect(10, 90, 181, 191))
        self.degrees_list_widget = QListWidget(self.chaget_log_color)

        q1 = QListWidgetItem(self.degrees_list_widget)
        color1 = QtGui.QColor()
        color1.setNamedColor('#' + self.config['log']['debug'])
        q1.setForeground(color1)

        q2 = QListWidgetItem(self.degrees_list_widget)
        color2 = QtGui.QColor()
        color2.setNamedColor('#' + self.config['log']['info'])
        q2.setForeground(color2)

        q3 = QListWidgetItem(self.degrees_list_widget)
        color3 = QtGui.QColor()
        color3.setNamedColor('#' + self.config['log']['warning'])
        q3.setForeground(color3)

        q4 = QListWidgetItem(self.degrees_list_widget)
        color4 = QtGui.QColor()
        color4.setNamedColor('#' + self.config['log']['error'])
        q4.setForeground(color4)

        q5 = QListWidgetItem(self.degrees_list_widget)
        color5 = QtGui.QColor()
        color5.setNamedColor('#' + self.config['log']['critical'])
        q5.setForeground(color5)

        q6 = QListWidgetItem(self.degrees_list_widget)
        color6 = QtGui.QColor()
        color6.setNamedColor('#' + self.config['log']['send_message'])
        q6.setForeground(color6)

        q7 = QListWidgetItem(self.degrees_list_widget)
        color7 = QtGui.QColor()
        color7.setNamedColor('#' + self.config['log']['send_group_message'])
        q7.setForeground(color7)

        q8 = QListWidgetItem(self.degrees_list_widget)
        color8 = QtGui.QColor()
        color8.setNamedColor('#' + self.config['log']['recv_private_message'])
        q8.setForeground(color8)

        q9 = QListWidgetItem(self.degrees_list_widget)
        color9 = QtGui.QColor()
        color9.setNamedColor('#' + self.config['log']['recv_group_message'])
        q9.setForeground(color9)

        q10 = QListWidgetItem(self.degrees_list_widget)
        color10 = QtGui.QColor()
        color10.setNamedColor('#' + self.config['log']['action'])
        q10.setForeground(color10)
        self.logging_degrees = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
        self.degrees_list_widget.setObjectName(u"degrees_list_widget")
        self.degrees_list_widget.setGeometry(QRect(10, 20, 151, 131))
        self.change_button = QPushButton(self.chaget_log_color)
        self.change_button.setObjectName(u"change_button")
        self.change_button.setGeometry(QRect(30, 170, 111, 21))

        self.horizontalLayout_3.addWidget(self.AboatLogging)

        self.groupBox = QGroupBox(self.setting_tab)
        self.groupBox.setObjectName(u"groupBox")
        self.restart_after_boom = QCheckBox(self.groupBox)
        self.restart_after_boom.setObjectName(u"restart_after_boom")
        self.restart_after_boom.setGeometry(QRect(10, 20, 68, 16))
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 50, 121, 21))
        self.WebsocketAddressEdit = QLineEdit(self.groupBox)
        self.WebsocketAddressEdit.setObjectName(u"WebsocketAddressEdit")
        self.WebsocketAddressEdit.setGeometry(QRect(10, 80, 131, 20))

        self.horizontalLayout_3.addWidget(self.groupBox)

        self.save_chager_button = QPushButton(self.setting_tab)
        self.save_chager_button.setObjectName(u"save_chager_button")

        self.horizontalLayout_3.addWidget(self.save_chager_button)

        icon2 = QIcon()
        icon2.addFile(u"C:/Users/Administrator/.designer/backup/icons/setting.png", QSize(), QIcon.Normal, QIcon.Off)
        self.main.addTab(self.setting_tab, icon2, "")

        self.horizontalLayout.addWidget(self.main)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 686, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")

        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.main.setCurrentIndex(1)
        self.connect_slots()
        QMetaObject.connectSlotsByName(MainWindow)

    def addplugin_(self, plu):
        self.plu_list = plu

    def connect_slots(self):
        self.treeWidget_2.customContextMenuRequested.connect(self.pluginMenu)  # 插件列表
        self.treeWidget_2.setContextMenuPolicy(Qt.CustomContextMenu)
        self.logging_treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.logging_treeWidget.customContextMenuRequested.connect(self.logMenu)
        self.change_button.clicked.connect(self.select_log_color)

    def logMenu(self, pos):

        menu = QMenu()
        item1 = menu.addAction("删除本条")
        item2 = menu.addAction("复制此条消息")
        item3 = menu.addAction("查看消息详情")
        screenPos = self.logging_treeWidget.mapToGlobal(pos)
        action = menu.exec(screenPos)
        if action == item1:
            if len(self.logging_treeWidget.selectedIndexes()) == 0:
                pass
            else:
                self.logging_treeWidget.takeTopLevelItem(self.logging_treeWidget.selectedIndexes()[0].row())
                return
        elif action == item2:
            if len(self.logging_treeWidget.selectedIndexes()) == 0:
                pass
            else:
                row = self.logging_treeWidget.selectedIndexes()[0].row()  # 列
                # print(row)
                # col = self.treeWidget.selectedIndexes()[0].column()
                # setText(self.logs[row].text(4))
            # print(self.logs[row].text(4))
        elif action == item3:
            if len(self.logging_treeWidget.selectedIndexes()) == 0:
                pass
            else:
                row = self.logging_treeWidget.selectedIndexes()[0].row()  # 列
                self.show_message(self.logging_treeWidget.selectedItems()[0].text(4))
                # print(self.logs[row].text(4))
                # (self.logs[row].text(4))

    def addlog(self, dic: dict):
        n = self.logging_treeWidget.topLevelItemCount()
        time_ = datetime.now().strftime("%H:%M:%S")
        root = QTreeWidgetItem(self.logging_treeWidget)
        color = QtGui.QColor()
        color.setNamedColor('#' + self.config['log'][dic['type']])
        root.setText(0, str(n + 1))
        root.setForeground(0, color)
        root.setText(1, time_)
        root.setForeground(1, color)
        root.setText(2, dic['type'])
        root.setForeground(2, color)
        root.setText(3, dic['sender'])
        root.setForeground(3, color)
        root.setText(4, dic['text'])
        root.setForeground(4, color)

        self.logging_treeWidget.setCurrentItem(root)

    def addplugin(self, plugin: Plugin):
        n = self.treeWidget_2.topLevelItemCount()
        root = My_tree_item(self.treeWidget_2)
        root.plugin = plugin
        root.setText(0, str(n + 1))
        root.setText(1, str(plugin.enable))
        root.setText(2, plugin.name)
        root.setText(3, plugin.author)
        root.setText(4, str(plugin.ver))
        root.setText(5, plugin.complain)
        self.plugins.append(root)

    def pluginMenu(self, pos):
        menu = QMenu()
        item1 = menu.addAction("启用插件")
        item2 = menu.addAction("禁用插件")
        item3 = menu.addAction("卸载插件")
        item4 = menu.addAction("设置")
        item5 = menu.addAction("添加插件")
        # item5 = menu.addAction("重载插件")
        screenPos = self.treeWidget_2.mapToGlobal(pos)
        action = menu.exec(screenPos)
        if action == item1:  # 启用插件
            if len(self.treeWidget_2.selectedIndexes()) == 0:
                pass
            else:
                row = self.treeWidget_2.selectedIndexes()[0].row()  # 列
                # print(row)
                plu_name = self.plugins[row]
                plu_name.plugin.enable_func()
                plu_name.plugin.enable = True
                self.plugins[row].setText(1, '启用')
                sql.execute("""update plugin_setting set enable=%s where name='%s'""" % (1, plu_name.plugin.name))
                sql.commit()

        elif action == item2:  # 禁用插件
            if len(self.treeWidget_2.selectedIndexes()) == 0:
                pass
            else:
                row = self.treeWidget_2.selectedIndexes()[0].row()  # 列
                # print(row)
                plu_name = self.plugins[row]
                plu_name.plugin.enable_func()
                plu_name.plugin.enable = False
                self.plugins[row].setText(1, '禁用')
                sql.execute("""update plugin_setting set enable=%s where name='%s'""" % (0, plu_name.plugin.name))
                sql.commit()

        elif action == item3:  # 卸载插件
            if len(self.treeWidget_2.selectedIndexes()) == 0:
                self.s.sendmsg.emit({'type': 'error', 'sender': '框架', 'text': '请选择一个要卸载的插件'})
            else:
                row = self.treeWidget_2.selectedIndexes()[0].row()  # 列
                # print(row)
                plu_name = self.plugins[row]
                plu_name.plugin.disable_func()
                self.plugins[row].setText(1, '已删除')
                try:
                    sql.execute('delete from plugin_setting where name=' + plu_name.plugin.name)
                except sqlite3.OperationalError:
                    sql.execute(r"delete from plugin_setting where name='%s'" % plu_name.plugin.name)
                    sql.commit()

                # sql.delete('plugin_setting', name=plu_name.plugin.name)
                shutil.rmtree('./plugins/' + plu_name.plugin.name)
                del_plugin(plu_name.plugin)
        elif action == item4:  # 设置
            # print('设置')
            if len(self.treeWidget_2.selectedIndexes()) == 0:
                print('pass')
                self.s.sendmsg.emit({'type': 'error', 'sender': '框架', 'text': '请选择一个要设置的插件'})
            else:
                row = self.treeWidget_2.selectedIndexes()[0].row()  # 列
                # print(row)
                plu_name = self.plugins[row]
                # plu_name.plugin.enable_func()
                threading.Thread(target=plu_name.plugin.setting).start()
        elif action == item5:
            t = ImportPluginThread(self.mainwindow)  # todo
            t.open_files.connect(self.open_file)
            # t = threading.Thread(target=add_plugin_with_win)
            t.start()

    def open_file(self):
        add_plugin_with_win()

    def show_message(self, s):
        self.ui = Message_detail()
        self.ui.set_text(s)
        self.ui.show_ui()

    def select_log_color(self):
        color = QColorDialog.getColor()  # 返回字符串。
        color_name = color.name()
        # print(color_name)
        names = self.degrees_list_widget.selectedItems()
        # print(names)
        if names and color_name:
            self.config['log'][names[0].text()] = color_name.replace('#', '')
            names[0].setForeground(color)  # 更改颜色
        else:
            pass

    def save_config(self):
        self.config['main']['ws_addr'](self.WebsocketAddressEdit.text())

    def export_logs(self):
        path, _ = QFileDialog.getSaveFileName(self.mainwindow, "导出日志", "", "Text Files (*.txt)")
        if path:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    for i in range(self.logging_treeWidget.topLevelItemCount()):
                        item = self.logging_treeWidget.topLevelItem(i)
                        f.write(f"{item.text(1)} [{item.text(2)}] {item.text(3)}: {item.text(4)}\n")
            except Exception as e:
                self.s.sendmsg.emit({'type': 'error', 'sender': '框架', 'text': f'导出日志失败: {str(e)}'})

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        ___qtreewidgetitem = self.treeWidget_2.headerItem()
        ___qtreewidgetitem.setText(5, QCoreApplication.translate("MainWindow", u"\u8bf4\u660e", None));
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("MainWindow", u"\u7248\u672c", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("MainWindow", u"\u4f5c\u8005", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MainWindow", u"\u63d2\u4ef6", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"\u72b6\u6001", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"\u5e8f\u53f7", None));
        self.main.setTabText(self.main.indexOf(self.plugin_managment_tree_widget),
                             QCoreApplication.translate("MainWindow", u"\u63d2\u4ef6\u7ba1\u7406", None))
        ___qtreewidgetitem1 = self.logging_treeWidget.headerItem()
        ___qtreewidgetitem1.setText(4, QCoreApplication.translate("MainWindow", u"\u5185\u5bb9", None));
        ___qtreewidgetitem1.setText(3, QCoreApplication.translate("MainWindow", u"\u53d1\u9001\u8005", None));
        ___qtreewidgetitem1.setText(2, QCoreApplication.translate("MainWindow", u"\u79cd\u7c7b", None));
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("MainWindow", u"\u65f6\u95f4", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"\u5e8f\u53f7", None));
        self.main.setTabText(self.main.indexOf(self.log_tab),
                             QCoreApplication.translate("MainWindow", u"\u65e5\u5fd7", None))
        self.AboatLogging.setTitle(QCoreApplication.translate("MainWindow", u"\u65e5\u5fd7\u76f8\u5173", None))
        self.label_2.setText(
            QCoreApplication.translate("MainWindow", u"\u4e0a\u62a5\u7684\u6700\u4f4e\u7b49\u7ea7", None))
        self.heigest_log_level.setItemText(0, QCoreApplication.translate("MainWindow", u"debug", None))
        self.heigest_log_level.setItemText(1, QCoreApplication.translate("MainWindow", u"info", None))
        self.heigest_log_level.setItemText(2, QCoreApplication.translate("MainWindow", u"warning", None))
        self.heigest_log_level.setItemText(3, QCoreApplication.translate("MainWindow", u"error", None))
        self.heigest_log_level.setItemText(4, QCoreApplication.translate("MainWindow", u"critical", None))

        self.chaget_log_color.setTitle(
            QCoreApplication.translate("MainWindow", u"\u66f4\u6539\u65e5\u5fd7\u989c\u8272", None))

        __sortingEnabled = self.degrees_list_widget.isSortingEnabled()
        self.degrees_list_widget.setSortingEnabled(False)
        ___qlistwidgetitem = self.degrees_list_widget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"debug", None));
        ___qlistwidgetitem1 = self.degrees_list_widget.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u"info", None));
        ___qlistwidgetitem2 = self.degrees_list_widget.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("MainWindow", u"warning", None));
        ___qlistwidgetitem3 = self.degrees_list_widget.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("MainWindow", u"error", None));
        ___qlistwidgetitem4 = self.degrees_list_widget.item(4)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("MainWindow", u"critical", None));
        ___qlistwidgetitem5 = self.degrees_list_widget.item(5)
        ___qlistwidgetitem5.setText(QCoreApplication.translate("MainWindow", u"send_message", None));
        ___qlistwidgetitem6 = self.degrees_list_widget.item(6)
        ___qlistwidgetitem6.setText(QCoreApplication.translate("MainWindow", u"send_group_message", None));
        ___qlistwidgetitem7 = self.degrees_list_widget.item(7)
        ___qlistwidgetitem7.setText(QCoreApplication.translate("MainWindow", u"recv_private_message", None));
        ___qlistwidgetitem8 = self.degrees_list_widget.item(8)
        ___qlistwidgetitem8.setText(QCoreApplication.translate("MainWindow", u"recv_group_message", None));
        ___qlistwidgetitem9 = self.degrees_list_widget.item(9)
        ___qlistwidgetitem9.setText(QCoreApplication.translate("MainWindow", u"action", None));
        self.degrees_list_widget.setSortingEnabled(__sortingEnabled)

        self.change_button.setText(QCoreApplication.translate("MainWindow", u"\u66f4\u6539", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u8fd0\u884c\u76f8\u5173", None))
        self.restart_after_boom.setText(QCoreApplication.translate("MainWindow", u"\u5d29\u6e83\u91cd\u542f", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u6b63\u5411Websocket\u5730\u5740", None))
        self.save_chager_button.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u8bbe\u7f6e", None))
        self.main.setTabText(self.main.indexOf(self.setting_tab),
                             QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))


class TrayIcon(QtWidgets.QSystemTrayIcon):  # 系统托盘类
    def __init__(self, MainWindow, parent=None):
        super(TrayIcon, self).__init__(parent)
        self.ui = MainWindow
        self.createMenu()

    def createMenu(self):
        self.menu = QtWidgets.QMenu()
        self.showAction1 = QtWidgets.QAction(text="启动", parent=self, triggered=self.show_window)
        self.showAction2 = QtWidgets.QAction("显示通知", self, triggered=self.showMsg)
        self.quitAction = QtWidgets.QAction("退出", self, triggered=self.quit)

        self.menu.addAction(self.showAction1)
        self.menu.addAction(self.showAction2)
        self.menu.addAction(self.quitAction)
        self.setContextMenu(self.menu)

        # 设置图标
        self.setIcon(QtGui.QIcon("./icons/qmiao.png"))
        self.icon = self.MessageIcon()

        # 把鼠标点击图标的信号和槽连接
        self.activated.connect(self.onIconClicked)

    def showMsg(self):
        self.showMessage("Message", "skr at here", self.icon)

    def show_window(self):
        # 若是最小化，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
        self.ui.showNormal()
        self.ui.activateWindow()

    def quit(self):
        QtWidgets.qApp.quit()

    # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
    def onIconClicked(self, reason):
        if reason == 2 or reason == 3:
            # self.showMessage("Message", "skr at here", self.icon)
            if self.ui.isMinimized() or not self.ui.isVisible():
                # 若是最小化，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
                self.ui.showNormal()
                self.ui.activateWindow()
                self.ui.setWindowFlags(QtCore.Qt.Window)
                self.ui.show()
            else:
                # 若不是最小化，则最小化
                self.ui.showMinimized()
                self.ui.setWindowFlags(QtCore.Qt.SplashScreen)
                self.ui.show()
                # self.ui.show()
