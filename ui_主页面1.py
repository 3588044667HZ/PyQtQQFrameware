# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '��ҳ��InNqgr.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(686, 393)
        icon = QIcon()
        icon.addFile(u"C:/Users/Administrator/.designer/backup/icons/qmiao.png", QSize(), QIcon.Normal, QIcon.Off)
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
        self.treeWidget_2.setObjectName(u"treeWidget_2")
        self.treeWidget_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.treeWidget_2.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.verticalLayout.addWidget(self.treeWidget_2)

        icon1 = QIcon()
        icon1.addFile(u"C:/Users/Administrator/.designer/backup/icons/pyd.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.main.addTab(self.plugin_managment_tree_widget, icon1, "")
        self.log_tab = QWidget()
        self.log_tab.setObjectName(u"log_tab")
        self.logging_treeWidget = QTreeWidget(self.log_tab)
        self.logging_treeWidget.setObjectName(u"logging_treeWidget")
        self.logging_treeWidget.setGeometry(QRect(-5, 1, 1061, 361))
        self.logging_treeWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.logging_treeWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.main.addTab(self.log_tab, "")
        self.setting_tab = QWidget()
        self.setting_tab.setObjectName(u"setting_tab")
        self.horizontalLayout_3 = QHBoxLayout(self.setting_tab)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.scrollArea = QScrollArea(self.setting_tab)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 660, 302))
        self.horizontalLayout_2 = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.AboatLogging = QGroupBox(self.scrollAreaWidgetContents)
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
        QListWidgetItem(self.degrees_list_widget)
        QListWidgetItem(self.degrees_list_widget)
        QListWidgetItem(self.degrees_list_widget)
        QListWidgetItem(self.degrees_list_widget)
        QListWidgetItem(self.degrees_list_widget)
        QListWidgetItem(self.degrees_list_widget)
        QListWidgetItem(self.degrees_list_widget)
        QListWidgetItem(self.degrees_list_widget)
        QListWidgetItem(self.degrees_list_widget)
        QListWidgetItem(self.degrees_list_widget)
        self.degrees_list_widget.setObjectName(u"degrees_list_widget")
        self.degrees_list_widget.setGeometry(QRect(10, 20, 151, 131))
        self.change_button = QPushButton(self.chaget_log_color)
        self.change_button.setObjectName(u"change_button")
        self.change_button.setGeometry(QRect(30, 170, 111, 21))

        self.horizontalLayout_2.addWidget(self.AboatLogging)

        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
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

        self.horizontalLayout_2.addWidget(self.groupBox)

        self.save_chager_button = QPushButton(self.scrollAreaWidgetContents)
        self.save_chager_button.setObjectName(u"save_chager_button")

        self.horizontalLayout_2.addWidget(self.save_chager_button)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_3.addWidget(self.scrollArea)

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

        self.main.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        ___qtreewidgetitem = self.treeWidget_2.headerItem()
        ___qtreewidgetitem.setText(5, QCoreApplication.translate("MainWindow", u"\u8bf4\u660e", None));
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("MainWindow", u"\u7248\u672c", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("MainWindow", u"\u4f5c\u8005", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MainWindow", u"\u63d2\u4ef6", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"\u72b6\u6001", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"\u5e8f\u53f7", None));
        self.main.setTabText(self.main.indexOf(self.plugin_managment_tree_widget), QCoreApplication.translate("MainWindow", u"\u63d2\u4ef6\u7ba1\u7406", None))
        ___qtreewidgetitem1 = self.logging_treeWidget.headerItem()
        ___qtreewidgetitem1.setText(4, QCoreApplication.translate("MainWindow", u"\u5185\u5bb9", None));
        ___qtreewidgetitem1.setText(3, QCoreApplication.translate("MainWindow", u"\u53d1\u9001\u8005", None));
        ___qtreewidgetitem1.setText(2, QCoreApplication.translate("MainWindow", u"\u79cd\u7c7b", None));
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("MainWindow", u"\u65f6\u95f4", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"\u5e8f\u53f7", None));
        self.main.setTabText(self.main.indexOf(self.log_tab), QCoreApplication.translate("MainWindow", u"\u65e5\u5fd7", None))
        self.AboatLogging.setTitle(QCoreApplication.translate("MainWindow", u"\u65e5\u5fd7\u76f8\u5173", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u4e0a\u62a5\u7684\u6700\u4f4e\u7b49\u7ea7", None))
        self.heigest_log_level.setItemText(0, QCoreApplication.translate("MainWindow", u"debug", None))
        self.heigest_log_level.setItemText(1, QCoreApplication.translate("MainWindow", u"info", None))
        self.heigest_log_level.setItemText(2, QCoreApplication.translate("MainWindow", u"warning", None))
        self.heigest_log_level.setItemText(3, QCoreApplication.translate("MainWindow", u"error", None))
        self.heigest_log_level.setItemText(4, QCoreApplication.translate("MainWindow", u"critical", None))

        self.chaget_log_color.setTitle(QCoreApplication.translate("MainWindow", u"\u66f4\u6539\u65e5\u5fd7\u989c\u8272", None))

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
        self.main.setTabText(self.main.indexOf(self.setting_tab), QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
    # retranslateUi

