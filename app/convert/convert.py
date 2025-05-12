import os  # это для действия ниже перед запуском функции
import sys  # информация о системе
import sqlite3
import datetime as dt
import socks
import socket
import asyncio
import shutil  # для удаления папки
import pytz # для временной зоны

from opentele.td import TDesktop
from opentele.api import UseCurrentSession
from opentele.exception import TFileNotFound
from opentele.tl import TelegramClient

from telethon import errors
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

from app.general.info import Dialog_info
from app.general.yes_or_cancel import Dialog_yes_or_cancel
from app.general.check_proxy import check_proxy
from app.general.error_proxy_for_work import Dialog_error_proxy
from app.general.error_handler import error_handler

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")# 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():# 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path# 3. Установка пути

# Только после этого импортируем PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtGui import QIntValidator  # для разрешения ввода только цифр в LineEdit
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QLineEdit, QFileDialog


class Window_convert(QtWidgets.QMainWindow):
    root_project_dir = '..'

    def __init__(self,switch_window):
        super().__init__()
        self.switch_window = switch_window

        if os.path.isfile(f'{self.root_project_dir}/working_files/convert_file/account.session'):
            os.remove(f'{self.root_project_dir}/working_files/convert_file/account.session')  # удаляем остатки прошлой сессии

        if os.path.isdir(f'{self.root_project_dir}/working_files/convert_file/tdata'):
            shutil.rmtree(f'{self.root_project_dir}/working_files/convert_file/tdata')  # удаляем остатки прошлой сессии

        self.setObjectName("MainWindow")
        self.resize(1500, 850)
        self.setMinimumSize(QtCore.QSize(1200, 750))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.setFont(font)
        self.setStyleSheet("background-color: rgb(236, 237, 240);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(0, 0, -1, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.scrollArea_3 = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_3.sizePolicy().hasHeightForWidth())
        self.scrollArea_3.setSizePolicy(sizePolicy)
        self.scrollArea_3.setMinimumSize(QtCore.QSize(270, 0))
        self.scrollArea_3.setMaximumSize(QtCore.QSize(270, 16777215))
        self.scrollArea_3.setStyleSheet("background-color: rgb(14, 22, 33);\n"
                                        "border: none;")
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setObjectName("scrollArea_3")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 270, 850))
        self.scrollAreaWidgetContents_3.setStyleSheet("")
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_account_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        self.pushButton_account_2.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_account_2.sizePolicy().hasHeightForWidth())
        self.pushButton_account_2.setSizePolicy(sizePolicy)
        self.pushButton_account_2.setMinimumSize(QtCore.QSize(185, 0))
        self.pushButton_account_2.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_account_2.setFont(font)
        self.pushButton_account_2.setStyleSheet("color: rgb(255, 255, 255);\n"
                                                "border: 0;\n"
                                                "text-align: center;\n"
                                                "padding: 10px;")
        self.pushButton_account_2.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/logo.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_account_2.setIcon(icon)
        self.pushButton_account_2.setIconSize(QtCore.QSize(300, 60))
        self.pushButton_account_2.setCheckable(False)
        self.pushButton_account_2.setObjectName("pushButton_account_2")
        self.verticalLayout.addWidget(self.pushButton_account_2)
        self.label_9 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QtCore.QSize(0, 0))
        self.label_9.setText("")
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9)
        self.pushButton_account = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        self.pushButton_account.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_account.sizePolicy().hasHeightForWidth())
        self.pushButton_account.setSizePolicy(sizePolicy)
        self.pushButton_account.setMinimumSize(QtCore.QSize(185, 0))
        self.pushButton_account.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_account.setFont(font)
        self.pushButton_account.setStyleSheet("QPushButton {\n"
"color: rgb(143, 145, 165);\n"
"border: 0;\n"
"text-align: left;\n"
"padding: 10px;\n"
"   }\n"
"   QPushButton:hover {\n"
"       background-color: rgb(35, 54, 74); /* Цвет при наведении */\n"
"   }\n"
"\n"
"QPushButton:pressed {\n"
"                background-color:rgb(3, 11, 22); /* Цвет фона при нажатии */\n"
"            }")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/account.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_account.setIcon(icon1)
        self.pushButton_account.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_account.setCheckable(False)
        self.pushButton_account.setObjectName("pushButton_account")
        self.verticalLayout.addWidget(self.pushButton_account)
        self.pushButton_mailing = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_mailing.sizePolicy().hasHeightForWidth())
        self.pushButton_mailing.setSizePolicy(sizePolicy)
        self.pushButton_mailing.setMinimumSize(QtCore.QSize(185, 0))
        self.pushButton_mailing.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_mailing.setFont(font)
        self.pushButton_mailing.setStyleSheet("QPushButton {\n"
"color: rgb(143, 145, 165);\n"
"border: 0;\n"
"text-align: left;\n"
"padding: 10px;\n"
"   }\n"
"   QPushButton:hover {\n"
"       background-color: rgb(35, 54, 74); /* Цвет при наведении */\n"
"   }\n"
"\n"
"QPushButton:pressed {\n"
"                background-color:rgb(3, 11, 22); /* Цвет фона при нажатии */\n"
"            }")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/mailing.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_mailing.setIcon(icon2)
        self.pushButton_mailing.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_mailing.setObjectName("pushButton_mailing")
        self.verticalLayout.addWidget(self.pushButton_mailing)
        self.pushButton_mailing_chat = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_mailing_chat.setFont(font)
        self.pushButton_mailing_chat.setStyleSheet("QPushButton {\n"
"color: rgb(143, 145, 165);\n"
"border: 0;\n"
"text-align: left;\n"
"padding: 10px;\n"
"   }\n"
"   QPushButton:hover {\n"
"       background-color: rgb(35, 54, 74); /* Цвет при наведении */\n"
"   }\n"
"\n"
"QPushButton:pressed {\n"
"                background-color:rgb(3, 11, 22); /* Цвет фона при нажатии */\n"
"            }")
        self.pushButton_mailing_chat.setIcon(icon2)
        self.pushButton_mailing_chat.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_mailing_chat.setObjectName("pushButton_mailing_chat")
        self.verticalLayout.addWidget(self.pushButton_mailing_chat)
        self.pushButton_invite = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_invite.sizePolicy().hasHeightForWidth())
        self.pushButton_invite.setSizePolicy(sizePolicy)
        self.pushButton_invite.setMinimumSize(QtCore.QSize(185, 0))
        self.pushButton_invite.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_invite.setFont(font)
        self.pushButton_invite.setStyleSheet("QPushButton {\n"
"color: rgb(143, 145, 165);\n"
"border: 0;\n"
"text-align: left;\n"
"padding: 10px;\n"
"   }\n"
"   QPushButton:hover {\n"
"       background-color: rgb(35, 54, 74); /* Цвет при наведении */\n"
"   }\n"
"\n"
"QPushButton:pressed {\n"
"                background-color:rgb(3, 11, 22); /* Цвет фона при нажатии */\n"
"            }")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/invaite.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_invite.setIcon(icon3)
        self.pushButton_invite.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_invite.setObjectName("pushButton_invite")
        self.verticalLayout.addWidget(self.pushButton_invite)
        self.pushButton_parser = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_parser.sizePolicy().hasHeightForWidth())
        self.pushButton_parser.setSizePolicy(sizePolicy)
        self.pushButton_parser.setMinimumSize(QtCore.QSize(185, 0))
        self.pushButton_parser.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_parser.setFont(font)
        self.pushButton_parser.setStyleSheet("QPushButton {\n"
"color: rgb(143, 145, 165);\n"
"border: 0;\n"
"text-align: left;\n"
"padding: 10px;\n"
"   }\n"
"   QPushButton:hover {\n"
"       background-color: rgb(35, 54, 74); /* Цвет при наведении */\n"
"   }\n"
"\n"
"QPushButton:pressed {\n"
"                background-color:rgb(3, 11, 22); /* Цвет фона при нажатии */\n"
"            }")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/parser.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_parser.setIcon(icon4)
        self.pushButton_parser.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_parser.setObjectName("pushButton_parser")
        self.verticalLayout.addWidget(self.pushButton_parser)
        self.pushButton_proxy = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_proxy.sizePolicy().hasHeightForWidth())
        self.pushButton_proxy.setSizePolicy(sizePolicy)
        self.pushButton_proxy.setMinimumSize(QtCore.QSize(185, 0))
        self.pushButton_proxy.setMaximumSize(QtCore.QSize(16777215, 57))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_proxy.setFont(font)
        self.pushButton_proxy.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_proxy.setStyleSheet("QPushButton {\n"
"color: rgb(143, 145, 165);\n"
"border: 0;\n"
"text-align: left;\n"
"padding: 10px;\n"
"   }\n"
"   QPushButton:hover {\n"
"       background-color: rgb(35, 54, 74); /* Цвет при наведении */\n"
"   }\n"
"\n"
"QPushButton:pressed {\n"
"                background-color:rgb(3, 11, 22); /* Цвет фона при нажатии */\n"
"            }")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/proxy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_proxy.setIcon(icon5)
        self.pushButton_proxy.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_proxy.setObjectName("pushButton_proxy")
        self.verticalLayout.addWidget(self.pushButton_proxy)
        self.pushButton_bomber = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        self.pushButton_bomber.setMinimumSize(QtCore.QSize(185, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_bomber.setFont(font)
        self.pushButton_bomber.setStyleSheet("QPushButton {\n"
"color: rgb(143, 145, 165);\n"
"border: 0;\n"
"text-align: left;\n"
"padding: 10px;\n"
"   }\n"
"   QPushButton:hover {\n"
"       background-color: rgb(35, 54, 74); /* Цвет при наведении */\n"
"   }\n"
"\n"
"QPushButton:pressed {\n"
"                background-color:rgb(3, 11, 22); /* Цвет фона при нажатии */\n"
"            }")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/bomber.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_bomber.setIcon(icon6)
        self.pushButton_bomber.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_bomber.setObjectName("pushButton_bomber")
        self.verticalLayout.addWidget(self.pushButton_bomber)
        self.pushButton_enter_group = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_enter_group.setFont(font)
        self.pushButton_enter_group.setStyleSheet("QPushButton {\n"
"color: rgb(143, 145, 165);\n"
"border: 0;\n"
"text-align: left;\n"
"padding: 10px;\n"
"   }\n"
"   QPushButton:hover {\n"
"       background-color: rgb(35, 54, 74); /* Цвет при наведении */\n"
"   }\n"
"\n"
"QPushButton:pressed {\n"
"                background-color:rgb(3, 11, 22); /* Цвет фона при нажатии */\n"
"            }")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/enter_the_group.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_enter_group.setIcon(icon7)
        self.pushButton_enter_group.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_enter_group.setObjectName("pushButton_enter_group")
        self.verticalLayout.addWidget(self.pushButton_enter_group)
        self.pushButton_reactions = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_reactions.setFont(font)
        self.pushButton_reactions.setStyleSheet("QPushButton {\n"
"color: rgb(143, 145, 165);\n"
"border: 0;\n"
"text-align: left;\n"
"padding: 10px;\n"
"   }\n"
"   QPushButton:hover {\n"
"       background-color: rgb(35, 54, 74); /* Цвет при наведении */\n"
"   }\n"
"\n"
"QPushButton:pressed {\n"
"                background-color:rgb(3, 11, 22); /* Цвет фона при нажатии */\n"
"            }")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/like.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_reactions.setIcon(icon8)
        self.pushButton_reactions.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_reactions.setObjectName("pushButton_reactions")
        self.verticalLayout.addWidget(self.pushButton_reactions)
        self.pushButton_comment = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_comment.setFont(font)
        self.pushButton_comment.setStyleSheet("QPushButton {\n"
"color: rgb(143, 145, 165);\n"
"border: 0;\n"
"text-align: left;\n"
"padding: 10px;\n"
"   }\n"
"   QPushButton:hover {\n"
"       background-color: rgb(35, 54, 74); /* Цвет при наведении */\n"
"   }\n"
"\n"
"QPushButton:pressed {\n"
"                background-color:rgb(3, 11, 22); /* Цвет фона при нажатии */\n"
"            }")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/coment.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_comment.setIcon(icon9)
        self.pushButton_comment.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_comment.setObjectName("pushButton_comment")
        self.verticalLayout.addWidget(self.pushButton_comment)
        self.pushButton_convert = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_convert.sizePolicy().hasHeightForWidth())
        self.pushButton_convert.setSizePolicy(sizePolicy)
        self.pushButton_convert.setMinimumSize(QtCore.QSize(185, 0))
        self.pushButton_convert.setMaximumSize(QtCore.QSize(16777215, 57))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_convert.setFont(font)
        self.pushButton_convert.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_convert.setStyleSheet("QPushButton {\n"
"color: rgb(255, 255, 255);\n"
"border: 0;\n"
"text-align: left;\n"
"padding: 10px;\n"
"   }\n"
"   QPushButton:hover {\n"
"       background-color: rgb(35, 54, 74); /* Цвет при наведении */\n"
"   }\n"
"\n"
"QPushButton:pressed {\n"
"                background-color:rgb(3, 11, 22); /* Цвет фона при нажатии */\n"
"            }")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/convert.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_convert.setIcon(icon10)
        self.pushButton_convert.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_convert.setObjectName("pushButton_convert")
        self.verticalLayout.addWidget(self.pushButton_convert)
        self.pushButton_doc = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_doc.sizePolicy().hasHeightForWidth())
        self.pushButton_doc.setSizePolicy(sizePolicy)
        self.pushButton_doc.setMinimumSize(QtCore.QSize(185, 0))
        self.pushButton_doc.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_doc.setFont(font)
        self.pushButton_doc.setStyleSheet("QPushButton {\n"
"color: rgb(143, 145, 165);\n"
"border: 0;\n"
"text-align: left;\n"
"padding: 10px;\n"
"   }\n"
"   QPushButton:hover {\n"
"       background-color: rgb(35, 54, 74); /* Цвет при наведении */\n"
"   }\n"
"\n"
"QPushButton:pressed {\n"
"                background-color:rgb(3, 11, 22); /* Цвет фона при нажатии */\n"
"            }")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/doc.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_doc.setIcon(icon11)
        self.pushButton_doc.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_doc.setObjectName("pushButton_doc")
        self.verticalLayout.addWidget(self.pushButton_doc)
        self.label_8 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QtCore.QSize(0, 0))
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)
        self.gridLayout_2.addWidget(self.scrollArea_3, 0, 0, 3, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(24, -1, -1, 10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout.addWidget(self.label_18)
        self.pushButton_info = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_info.setStyleSheet("border: none;\n"
"")
        self.pushButton_info.setText("")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/icon/info.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_info.setIcon(icon12)
        self.pushButton_info.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_info.setObjectName("pushButton_info")
        self.horizontalLayout.addWidget(self.pushButton_info)
        self.label_19 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setText("")
        self.label_19.setObjectName("label_19")
        self.horizontalLayout.addWidget(self.label_19)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(20, 20, 700, -1)
        self.gridLayout.setVerticalSpacing(30)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 65))
        self.groupBox_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 20px;")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.pushButton_choose_file = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_choose_file.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_choose_file.setFont(font)
        self.pushButton_choose_file.setStyleSheet("QPushButton {\n"
"  background: rgb(210, 210, 213);\n"
"    text-align: center;\n"
"    border-radius: 10px;\n"
"    padding: 5 px;\n"
"    padding-left: 10 px;\n"
"    padding-right: 10 px;\n"
"   }\n"
"   QPushButton:hover {\n"
"          background-color: rgb(180, 180, 184); /* Цвет при наведении */\n"
"   }\n"
"\n"
"QPushButton:pressed {\n"
"                   background-color: rgb(150, 150, 153); /* Цвет фона при нажатии */\n"
"            }")
        self.pushButton_choose_file.setObjectName("pushButton_choose_file")
        self.horizontalLayout_3.addWidget(self.pushButton_choose_file)
        self.pushButton_info_convert_in_tdata = QtWidgets.QPushButton(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_info_convert_in_tdata.sizePolicy().hasHeightForWidth())
        self.pushButton_info_convert_in_tdata.setSizePolicy(sizePolicy)
        self.pushButton_info_convert_in_tdata.setText("")
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/icon/question.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_info_convert_in_tdata.setIcon(icon13)
        self.pushButton_info_convert_in_tdata.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_info_convert_in_tdata.setObjectName("pushButton_info_convert_in_tdata")
        self.horizontalLayout_3.addWidget(self.pushButton_info_convert_in_tdata)
        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setMinimumSize(QtCore.QSize(441, 65))
        self.groupBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 20px;")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.pushButton_choose_folder = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_choose_folder.setMinimumSize(QtCore.QSize(40, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_choose_folder.setFont(font)
        self.pushButton_choose_folder.setStyleSheet("QPushButton {\n"
"     background: rgb(210, 210, 213);\n"
"    text-align: center;\n"
"    border-radius: 10px;\n"
"    padding: 5 px;\n"
"    padding-left: 10 px;\n"
"    padding-right: 10 px;\n"
"   }\n"
"   QPushButton:hover {\n"
"          background-color: rgb(180, 180, 184); /* Цвет при наведении */\n"
"   }\n"
"\n"
"QPushButton:pressed {\n"
"                   background-color: rgb(150, 150, 153); /* Цвет фона при нажатии */\n"
"            }")
        self.pushButton_choose_folder.setObjectName("pushButton_choose_folder")
        self.horizontalLayout_2.addWidget(self.pushButton_choose_folder)
        self.pushButton_info_convert_in_session = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_info_convert_in_session.sizePolicy().hasHeightForWidth())
        self.pushButton_info_convert_in_session.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.pushButton_info_convert_in_session.setFont(font)
        self.pushButton_info_convert_in_session.setStyleSheet("")
        self.pushButton_info_convert_in_session.setText("")
        self.pushButton_info_convert_in_session.setIcon(icon13)
        self.pushButton_info_convert_in_session.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_info_convert_in_session.setObjectName("pushButton_info_convert_in_session")
        self.horizontalLayout_2.addWidget(self.pushButton_info_convert_in_session)

        self.checkBox_use_proxy = QtWidgets.QCheckBox(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_use_proxy.setFont(font)
        self.checkBox_use_proxy.setStyleSheet("QCheckBox {\n"
                                              "color: rgb(0, 0, 0);\n"
                                              "    spacing: 5px; /* Отступ между иконкой и текстом */\n"
                                              "    border: none;\n"
                                              "    margin-left: 5px;"
                                              "}\n"
                                              "\n"
                                              "QCheckBox::indicator {\n"
                                              "    width: 15px; /* Ширина индикатора (чекбокса) */\n"
                                              "    height: 15px; /* Высота индикатора (чекбокса) */\n"
                                              "    border: 2px solid rgb(150, 150, 150); /* Обводка чекбокса */\n"
                                              "    border-radius: 4px; /* Закругление углов */\n"
                                              "    background-color: white; /* Цвет фона чекбокса */\n"
                                              "}\n"
                                              "\n"
                                              "\n"
                                              "QCheckBox::indicator:checked {\n"
                                              "    background-color: rgb(150, 200, 150); \n"
                                              "    border: 2px solid rgb(150, 150, 150); \n"
                                              "}\n"
                                              "\n"
                                              "QCheckBox::indicator:unchecked:hover {\n"
                                              "    border: 2px solid rgb(150, 150, 150);\n"
                                              "}\n"
                                              "\n"
                                              "QCheckBox::indicator:checked:hover {\n"
                                              "    background-color: rgb(180, 230, 180); \n"
                                              "}")
        self.checkBox_use_proxy.setObjectName("checkBox_user_name")

        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.checkBox_use_proxy, 2, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setText("")
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 2, 1, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.action = QtWidgets.QAction(self)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(self)
        self.action_2.setObjectName("action_2")

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        # события
        self.pushButton_account.clicked.connect(lambda: self.switch_window('accounts'))
        self.pushButton_mailing.clicked.connect(lambda: self.switch_window('mailing_by_users'))
        self.pushButton_mailing_chat.clicked.connect(lambda: self.switch_window('mailing_by_chats'))
        self.pushButton_invite.clicked.connect(lambda: self.switch_window('invite'))
        self.pushButton_parser.clicked.connect(lambda: self.switch_window('parser'))
        self.pushButton_proxy.clicked.connect(lambda: self.switch_window('proxy'))
        self.pushButton_bomber.clicked.connect(lambda: self.switch_window('bomber'))
        self.pushButton_enter_group.clicked.connect(lambda: self.switch_window('enter_group'))
        self.pushButton_reactions.clicked.connect(lambda: self.switch_window('reactions'))
        self.pushButton_comment.clicked.connect(lambda: self.switch_window('comment'))
        self.pushButton_doc.clicked.connect(lambda: self.switch_window('doc'))

        self.pushButton_info_convert_in_session.clicked.connect(lambda: self._info_convert_in_session())
        self.pushButton_info_convert_in_tdata.clicked.connect(lambda: self._info_convert_in_tdata())

        self.pushButton_choose_folder.clicked.connect(lambda: asyncio.run(self._convert_in_session()))
        self.pushButton_choose_file.clicked.connect(lambda: asyncio.run(self._convert_in_tdata()))
        # события

    def _info_convert_in_session(self):
        info = Dialog_info('Информация', 'Укажите путь к папке Tdata\n\nВ ней хранятся данные для входа в аккаунт и настройки аккаунта\n'
                                'Будет произведена попытка входа и в случае успеха сформируется файл .session',
                                'notification.mp3')  # Создаем экземпляр
        info.exec_()  # Открываем

    def _info_convert_in_tdata(self):
        info = Dialog_info('Информация', 'Укажите путь к файлу с расширением .session\n\nЭто файл с данными для входа в аккаунт\n'
                                         'Будет произведена попытка входа и в случае успеха сформируется папка Tdata',
                           'notification.mp3')  # Создаем экземпляр
        info.exec_()  # Открываем

    def _check_proxy(self):
        """Если успешно подключились к прокси, то вернёт данные для входа
           возвращаемые значения:
            proxy_from_db[0] = ip прокси
            proxy_from_db[1] = port прокси
            proxy_from_db[2] = login прокси
            proxy_from_db[3] = password прокси

            если не смогли подключиться, то ничего не вернёт"""

        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()
        cursor.execute(f"SELECT ip,port,login,password FROM proxy")
        proxy_from_db = cursor.fetchone()
        connection.close()

        efficiency = check_proxy(proxy_from_db[0], proxy_from_db[1], proxy_from_db[2], proxy_from_db[3])
        if efficiency:
            return [proxy_from_db[0], str(proxy_from_db[1]), proxy_from_db[2],proxy_from_db[3]]
        else:
            # если проблема с прокси, то вызываем спец окно и в независимо от результата выбора,
            # запускаем ещё раз добавление аккаунтов
            error_proxy = Dialog_error_proxy(proxy_from_db[0], str(proxy_from_db[1]), proxy_from_db[2],proxy_from_db[3])  # Создаем экземпляр
            error_proxy.show_info()
            error_proxy.exec_()  # Открываем
            return

    async def _convert_in_session(self):
        data_proxy = []
        original_socket = socket.socket  # запоминаем какой сокет был до
        if self.checkBox_use_proxy.isChecked():
            data_proxy = self._check_proxy()
            if not data_proxy: # если прокси не действительно
                return

        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")  # Получаем путь к рабочему столу
        # Открываем диалог выбора папки, начнем с рабочего стола
        # если пользователь выбрал папку, то вернётся путь иначе None
        tdata_path = QFileDialog.getExistingDirectory(self, "Выберите папку", desktop_path)

        if tdata_path:  # если пользователь выбрал папку (хранит выбранный путь)
            if os.path.isfile(f'{self.root_project_dir}/working_files/convert_file/account.session'):
                os.remove(f'{self.root_project_dir}/working_files/convert_file/account.session') # удаляем остатки прошлой сессии

            if data_proxy:
                socks.set_default_proxy(socks.SOCKS5, data_proxy[0], data_proxy[1], True, data_proxy[2],data_proxy[3])  # Установка прокси-соединения
                socket.socket = socks.socksocket

            try:
                tdesk = TDesktop(tdata_path)
                client = await tdesk.ToTelethon(session=f"{self.root_project_dir}/working_files/convert_file/account.session",
                                                flag=UseCurrentSession)
                await asyncio.wait_for(client.connect(), timeout=10)  # вход в аккаунт
                me = await client.get_me()
                test_id = me.id
                await client.disconnect()
            except (Exception, TFileNotFound) as e:
                try:
                    await client.disconnect()
                except UnboundLocalError:
                    pass
                info = Dialog_info('Внимание!',
                                   'Не удалось создать файл .session\n\nДанные для входа не корректны!\n'
                                   'С помощь данной папки вход в аккаунт невозможен!',
                                   'notification.mp3')  # Создаем экземпляр
                info.exec_()  # Открываем
                return

            socket.socket = original_socket
            info = Dialog_info('Успешно!',
                               'Файл .session успешно сформирован\nВыберите путь его сохранения',
                               'notification.mp3','Выбрать')  # Создаем экземпляр
            info.exec_()  # Открываем

            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")  # Получаем путь к рабочему столу
            # Открываем диалог выбора папки, начнем с рабочего стола
            # если пользователь выбрал папку, то вернётся путь иначе None
            save_path = QFileDialog.getExistingDirectory(self, "Выберите папку", desktop_path)

            if save_path:
                counts = 1
                folder_name = '/account.session'

                while True:
                    try:
                        shutil.copy(f"{self.root_project_dir}/working_files/convert_file/account.session",
                                        save_path + folder_name)  # копирование

                        error_info = Dialog_info('Успешно!',
                                                 f'Файл успешно сохранена по пути:\n{save_path}{folder_name}',
                                                 'notification.mp3')  # Создаем экземпляр
                        error_info.exec_()  # Открываем
                        if os.path.isfile(f'{self.root_project_dir}/working_files/convert_file/account.session'):
                            os.remove(f'{self.root_project_dir}/working_files/convert_file/account.session')  # удаляем остатки прошлой сессии
                        break
                    except FileExistsError:
                        folder_name = f'/account({counts}).session'
                        counts += 1
                    except FileNotFoundError:
                        error_info = Dialog_info('Ошибка!', 'Указанный путь не найден!',
                                                 'notification.mp3')  # Создаем экземпляр
                        error_info.exec_()  # Открываем
                        break

    async def _convert_in_tdata(self):
        data_proxy = []
        original_socket = socket.socket  # запоминаем какой сокет был до
        if self.checkBox_use_proxy.isChecked():
            data_proxy = self._check_proxy()
            if not data_proxy:  # если прокси не действительно
                return

        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")  # Получаем путь к рабочему столу
        # Открываем диалог выбора папки, начнем с рабочего стола
        # если пользователь выбрал папку, то вернётся путь иначе None
        session_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", desktop_path, "Файл для входа (*.session)")

        if session_path:  # если пользователь выбрал папку (хранит выбранный путь)
            if os.path.isdir(f'{self.root_project_dir}/working_files/convert_file/tdata'):
                shutil.rmtree(f'{self.root_project_dir}/working_files/convert_file/tdata')  # удаляем остатки прошлой сессии

            if data_proxy:
                socks.set_default_proxy(socks.SOCKS5, data_proxy[0], data_proxy[1], True, data_proxy[2],data_proxy[3])  # Установка прокси-соединения
                socket.socket = socks.socksocket

            try:
                client = TelegramClient(session_path)
                tdesk = await client.ToTDesktop(flag=UseCurrentSession)
                await asyncio.wait_for(client.connect(), timeout=7)  # вход в аккаунт
                me = await client.get_me()
                test_id = me.id
                await client.disconnect()
                tdesk.SaveTData(f'{self.root_project_dir}/working_files/convert_file/tdata')
            except Exception:
                info = Dialog_info('Ошибка!','Данный файл не удалось конвертировать в папку Tdata',
                                   'notification.mp3', )
                info.exec_()  # Открываем
                return

            socket.socket = original_socket
            info = Dialog_info('Успешно!',
                               'Папка Tdata успешно сформирована\nВыберите путь её сохранения',
                               'notification.mp3', 'Выбрать')  # Создаем экземпляр
            info.exec_()  # Открываем

            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")  # Получаем путь к рабочему столу
            save_path = QFileDialog.getExistingDirectory(self, "Выберите папку", desktop_path)

            if save_path:
                counts = 1
                folder_name = '/tdata'

                while True:
                    try:
                        shutil.copytree(f"{self.root_project_dir}/working_files/convert_file/tdata",
                                    save_path + folder_name)  # копирование

                        error_info = Dialog_info('Успешно!',
                                                 f'Файл успешно сохранена по пути:\n{save_path}{folder_name}',
                                                 'notification.mp3')  # Создаем экземпляр
                        error_info.exec_()  # Открываем
                        if os.path.isdir(f'{self.root_project_dir}/working_files/convert_file/tdata'):
                            shutil.rmtree(f'{self.root_project_dir}/working_files/convert_file/tdata')  # удаляем остатки прошлой сессии
                        break
                    except FileExistsError:
                        folder_name = f'/tdata({counts})'
                        counts += 1
                    except FileNotFoundError:
                        error_info = Dialog_info('Ошибка!', 'Указанный путь не найден!',
                                                 'notification.mp3')  # Создаем экземпляр
                        error_info.exec_()  # Открываем
                        break


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_account.setText(_translate("MainWindow", "   Аккаунты"))
        self.pushButton_mailing.setText(_translate("MainWindow", "   Рассылка по юзерам"))
        self.pushButton_mailing_chat.setText(_translate("MainWindow", "   Рассылка по чатам"))
        self.pushButton_invite.setText(_translate("MainWindow", "   Инвайт"))
        self.pushButton_parser.setText(_translate("MainWindow", "   Парсер"))
        self.pushButton_proxy.setText(_translate("MainWindow", "   Прокси"))
        self.pushButton_bomber.setText(_translate("MainWindow", "   Бомбер на аккаунт"))
        self.pushButton_enter_group.setText(_translate("MainWindow", "   Массовый заход в группу"))
        self.pushButton_reactions.setText(_translate("MainWindow", "   Накрутка реакций"))
        self.pushButton_comment.setText(_translate("MainWindow", "   Накрутка комментариев"))
        self.pushButton_convert.setText(_translate("MainWindow", "   Конвертер tdata и session"))
        self.pushButton_doc.setText(_translate("MainWindow", "   Документация"))
        self.label_18.setText(_translate("MainWindow", "Конвертер"))
        self.label_3.setText(_translate("MainWindow", "session -> Tdata"))
        self.pushButton_choose_file.setText(_translate("MainWindow", "Выбрать файл"))
        self.label_2.setText(_translate("MainWindow", "Tdata -> session"))
        self.pushButton_choose_folder.setText(_translate("MainWindow", "Выбрать папку"))
        self.action.setText(_translate("MainWindow", "сохранить"))
        self.action_2.setText(_translate("MainWindow", "добавить"))
        self.checkBox_use_proxy.setText(_translate("MainWindow", "Использовать прокси"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Window_convert('fbdgf')
    ui.show()
    sys.exit(app.exec_())
