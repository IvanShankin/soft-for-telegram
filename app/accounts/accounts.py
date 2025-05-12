import os  # это для действия ниже перед запуском функции
import sys  # информация о системе
import sqlite3
import datetime as dt

import socks
import socket
import time
import asyncio
import aiohttp
from aiohttp_socks import ProxyConnector
import shutil # для удаления папки
import faulthandler # для просмотра стека вызовов
import subprocess # для запуска exe файлов
import sys
sys.path.append("..")  # Добавляет родительскую папку в путь поиска

from opentele.td import TDesktop
from opentele.api import UseCurrentSession
from opentele.exception import TFileNotFound

from app.accounts.add_accounts import Dialog_add_accounts
from app.accounts.info_add_accounts import Dialog_info_add_accounts
from app.accounts.flag import get_country_flag
from app.general.info import Dialog_info
from app.accounts.error_open_accounts import Dialog_error_open_accounts
from app.general.error_proxy import Dialog_error_proxy
from app.general.check_proxy import check_proxy
from app.general.error_handler import error_handler, get_description_and_solution
from app.accounts.more_info_account import Dialog_more_info_account
from app.general.yes_or_cancel import Dialog_yes_or_cancel

# Включаем faulthandler для получения информации об ошибках
faulthandler.enable()

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")# 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():# 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path# 3. Установка пути

# 4. Только после этого импортируем PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView, QFileDialog, QWidget, QPushButton, QGraphicsOpacityEffect
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QThread, pyqtSignal, QPropertyAnimation, Qt, QSize
from PyQt5.QtCore import QRect

class show_account(QThread):

    # если есть второй список, то значит не смогли войти в аккаунт
    task_done = pyqtSignal(list, bool)# Сигнал, который мы будем использовать для обновления интерфейса
    def __init__(self,folder_path_account: str, id_account: int, account_type: str, use_proxy: bool,id_proxy: str, port: int, login: str, password: str):
        super().__init__()
        self.folder_path_account = folder_path_account
        self.id_account = id_account
        self.account_type = account_type
        self.use_proxy = use_proxy
        self.id_proxy = id_proxy
        self.port = port
        self.login = login
        self.password = password

    def run(self):
        asyncio.run(self.get_info_account())

    async def get_info_account(self):
        if self.use_proxy:
            socks.set_default_proxy(socks.SOCKS5, self.id_proxy, self.port, True, self.login,self.password)  # Установка прокси-соединения
            socket.socket = socks.socksocket

        me = None
        try:
            tdesk = TDesktop(self.folder_path_account + '/tdata')
            client = await tdesk.ToTelethon(session=f"{self.folder_path_account}/session.session", flag=UseCurrentSession)
            await asyncio.wait_for( client.connect(),timeout=7 ) # вход в аккаунт
            me = await client.get_me()
            test_id = me.id
            await client.disconnect()
        except (Exception, TFileNotFound) as e:
            try:
                await client.disconnect()
            except UnboundLocalError:
                pass
            error_type = type(e)
            error_and_id_accounts_error = [str(error_type.__name__), self.id_account]
            self.task_done.emit(error_and_id_accounts_error, True) # возвращает id_tg, user_name, description,solution
            return

        geo = get_country_flag(me.phone)

        # последнее использование и примечание
        self.task_done.emit([str(self.id_account), str(me.id), me.username, me.first_name, geo, me.phone], False)
        return


class Window_accounts(QtWidgets.QMainWindow):
    open_account = True # True если аккаунты открываются
    program_launch = True # True если программа запускается (необходимо для отображения аккаунтов)
    selected_account_type = 'active' # отображает вкладка с какими аккаунтаами открыта

    original_socket = socket.socket  # запоминаем какой сокет был до

    accounts = [] # список данных об аккаунтах (хранит в себе массивы с инфой об аккаунте)
    error_accounts = [] # список аккаунтов с которыми произошла ошибка входа (первое значение значение ошибка второе id аккаунта )
    quantity_start_accounts = 0 # количество аккаунтов запущенных для дальнейшего вывода
    quantity_received_accounts = 0 # количество аккаунтов вернувшихся аккаунтов после получения информации о нём

    def __init__(self, switch_window = None):
        super().__init__()
        self.switch_window = switch_window

        self.active_threads = []  # ВАЖНО! хранит в себе запущенные потоки

        self.root_project_dir = '..'

        self.setObjectName("MainWindow")
        self.setWindowModality(QtCore.Qt.NonModal)
        self.resize(1500, 850)
        self.setMinimumSize(QtCore.QSize(1200, 750))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.setFont(font)
        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.setStyleSheet("background-color: rgb(236, 237, 240);")
        self.setIconSize(QtCore.QSize(24, 24))
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(0, 0, -1, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(25, 10, 20, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_5.addWidget(self.label_13)
        self.pushButton_info = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_info.setStyleSheet("border: none;\n")
        self.pushButton_info.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/icon/info.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_info.setIcon(icon)
        self.pushButton_info.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_info.setObjectName("pushButton_info")
        self.horizontalLayout_5.addWidget(self.pushButton_info)
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setText("")
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_5.addWidget(self.label_15)

        self.groupBox_progress = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_progress.sizePolicy().hasHeightForWidth())
        self.groupBox_progress.setSizePolicy(sizePolicy)
        self.groupBox_progress.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "border-radius: 13px;\n"
                                      "")
        self.groupBox_progress.setTitle("")
        self.groupBox_progress.setObjectName("groupBox_progress")
        self.groupBox_progress.setMinimumSize(0,0)
        self.groupBox_progress.setMaximumSize(20000, 40)
        self.horizontalLayout_5.addWidget(self.groupBox_progress)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox_progress)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(10, 0, 10, 0)  # Отступы в 10px со всех сторон

        self.label_gif_load = QtWidgets.QLabel(self.groupBox_progress)
        self.label_gif_load.setScaledContents(True)# Установка свойства для масштабирования содержимого
        self.label_gif_load.setMaximumSize(30,30)
        movie = QtGui.QMovie(self.root_project_dir + '/resources/icon/load.gif')# Загрузка GIF с использованием QMovie
        self.label_gif_load.setMovie(movie)
        movie.start() # Запуск анимации
        self.horizontalLayout_6.addWidget(self.label_gif_load)

        self.groupBox_progress.hide()

        self.button_info_open_account = QtWidgets.QPushButton(self.groupBox_progress)
        self.button_info_open_account.setText('')
        icon0 = QtGui.QIcon()
        icon0.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/icon/success.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_info_open_account.setIcon(icon0)
        size = QSize(20,20)
        self.button_info_open_account.setIconSize(size)
        self.horizontalLayout_6.addWidget(self.button_info_open_account)
        self.button_info_open_account.hide()

        self.label_result_open_account = QtWidgets.QLabel(self.groupBox_progress)
        self.label_result_open_account.setText('')
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_result_open_account.setFont(font)
        self.horizontalLayout_6.addWidget(self.label_result_open_account)
        self.label_result_open_account.hide()

        self.gridLayout_2.addLayout(self.horizontalLayout_5, 0, 1, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_2.setStyleSheet("border: none;\n"
                                        "")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 1205, 481))
        self.scrollAreaWidgetContents_2.setStyleSheet("/* Убираем вертикальную полосу прокрутки */\n"
                                                      "QScrollBar:vertical {\n"
                                                      "    width: 0px; /* Установка ширины на 1 пикселей */\n"
                                                      "    background: transparent; /* Делаем фон прозрачным */\n"
                                                      "    border: none; /* Убираем рамку */\n"
                                                      "\n"
                                                      "}\n"
                                                      "\n"
                                                      "/* Убираем ползунок вертикального скроллбара */\n"
                                                      "QScrollBar::handle:vertical {\n"
                                                      "    background: none; /* Делаем ползунок невидимым */\n"
                                                      "}\n"
                                                      "\n"
                                                      "/* Убираем кнопки сверху и снизу */\n"
                                                      "QScrollBar::sub-line:vertical,\n"
                                                      "QScrollBar::add-line:vertical {\n"
                                                      "    background: none; /* Убираем кнопки */\n"
                                                      "}\n"
                                                      "\n"
                                                      "/* Убираем стрелки */\n"
                                                      "QScrollBar::up-arrow:vertical,\n"
                                                      "QScrollBar::down-arrow:vertical {\n"
                                                      "    background: none; /* Убираем стрелки */\n"
                                                      "}\n"
                                                      "/* СТИЛЬ ГОРИЗОНТАЛЬНОГО СКРОЛЛБАРА */\n"
                                                      "QScrollBar:horizontal {\n"
                                                      "    border-radius: 8px;\n"
                                                      "    background: rgb(255, 255, 255); /* Стандартный цвет фона */\n"
                                                      "    height: 14px;\n"
                                                      "    margin: 1 15px 1 15px; /* Отступы по горизонтали */\n"
                                                      "}\n"
                                                      "\n"
                                                      "/* HANDLE BAR ГОРИЗОНТАЛЬНОГО СКРОЛЛБАРА */\n"
                                                      "QScrollBar::handle:horizontal {\n"
                                                      "    background-color: rgb(210, 210, 213); /* Стандартный цвет фона для ползунка */\n"
                                                      "    min-width: 30px; /* Минимальная ширина ползунка */\n"
                                                      "    border-radius: 7px;\n"
                                                      "    transition: background-color 1.2s ease, min-width 1.2s ease; /* Плавный переход цвета и ширины */\n"
                                                      "}\n"
                                                      "\n"
                                                      "QScrollBar::handle:horizontal:hover {\n"
                                                      "    background-color: rgb(180, 180, 184); /* Цвет ползунка при наведении */\n"
                                                      "}\n"
                                                      "\n"
                                                      "QScrollBar::handle:horizontal:pressed {\n"
                                                      "    background-color: rgb(150, 150, 153); /* Цвет ползунка при нажатии */\n"
                                                      "}\n"
                                                      "\n"
                                                      "/* КНОПКА СЛЕВА - ГОРИЗОНТАЛЬНЫЙ СКРОЛЛБАР */\n"
                                                      "QScrollBar::sub-line:horizontal {\n"
                                                      "    border: none;\n"
                                                      "    background-color: rgb(210, 210, 213); /* Стандартный цвет фона для кнопки влево */\n"
                                                      "    width: 15px;\n"
                                                      "    border-top-left-radius: 7px;\n"
                                                      "    border-bottom-left-radius: 7px;\n"
                                                      "    subcontrol-position: left;\n"
                                                      "    subcontrol-origin: margin;\n"
                                                      "    transition: background-color 1.2s ease; /* Плавный переход цвета */\n"
                                                      "}\n"
                                                      "\n"
                                                      "QScrollBar::sub-line:horizontal:hover {\n"
                                                      "    background-color: rgb(180, 180, 184); /* Цвет кнопки влево при наведении */\n"
                                                      "}\n"
                                                      "\n"
                                                      "QScrollBar::sub-line:horizontal:pressed {\n"
                                                      "    background-color: rgb(150, 150, 153); /* Цвет кнопки влево при нажатии */\n"
                                                      "}\n"
                                                      "\n"
                                                      "/* КНОПКА СПРАВА - ГОРИЗОНТАЛЬНЫЙ СКРОЛЛБАР */\n"
                                                      "QScrollBar::add-line:horizontal {\n"
                                                      "    border: none;\n"
                                                      "    background-color: rgb(210, 210, 213); /* Стандартный цвет фона для кнопки вправо */\n"
                                                      "    width: 15px;\n"
                                                      "    border-top-right-radius: 7px;\n"
                                                      "    border-bottom-right-radius: 7px;\n"
                                                      "    subcontrol-position: right;\n"
                                                      "    subcontrol-origin: margin;\n"
                                                      "    transition: background-color 1.2s ease; /* Плавный переход цвета */\n"
                                                      "}\n"
                                                      "\n"
                                                      "QScrollBar::add-line:horizontal:hover {\n"
                                                      "    background-color: rgb(180, 180, 184); /* Цвет кнопки вправо при наведении */\n"
                                                      "}\n"
                                                      "\n"
                                                      "QScrollBar::add-line:horizontal:pressed {\n"
                                                      "    background-color: rgb(150, 150, 153); /* Цвет кнопки вправо при нажатии */\n"
                                                      "}\n"
                                                      "\n"
                                                      "/* УБРАТЬ СТРЕЛКИ */\n"
                                                      "QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {\n"
                                                      "    background: none; /* Убираем стрелки */\n"
                                                      "}\n"
                                                      "\n"
                                                      "QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {\n"
                                                      "    background: none; /* Убираем фоновую страницу */\n"
                                                      "}")
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tableWidget_account = QtWidgets.QTableWidget(self.scrollAreaWidgetContents_2)
        self.tableWidget_account.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tableWidget_account.setFont(font)
        self.tableWidget_account.setStyleSheet("\n"
                                               "QTableWidget {\n"
                                               "background-color: rgb(255, 255, 255);\n"
                                               "outline: 1;\n"
                                               "}\n"
                                               "\n"
                                               "QTableWidget::item {\n"
                                               "    border: none;/*  Убираем границу у ячеек */\n"
                                               "    padding: 5px; /* Устанавливаем отступы (по желанию) */\n"
                                               "    border-bottom: 1px solid rgb(210, 210, 213); /* Добавляем нижнюю границу */\n"
                                               "}\n"
                                               "\n"
                                               "QHeaderView::section {\n"
                                               "    border: none; /* Убираем границу у заголовков */\n"
                                               "     background-color: rgb(230, 230, 230); /* цвет фона заголовка  ячейки */\n"
                                               "}\n"
                                               "\n"
                                               "QTableWidget::item:selected {\n"
                                               "	color: rgb(1,1,1);\n"
                                               "    background-color:  rgb(210, 210, 213); /* цвет фона для выделенной ячейки */\n"
                                               "}")
        self.tableWidget_account.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableWidget_account.setAlternatingRowColors(False)
        self.tableWidget_account.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tableWidget_account.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_account.setShowGrid(False)
        self.tableWidget_account.setGridStyle(QtCore.Qt.NoPen)
        self.tableWidget_account.setRowCount(0)
        self.tableWidget_account.setObjectName("tableWidget_account")
        self.tableWidget_account.setColumnCount(9)

        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_account.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setBackground(QtGui.QColor(255, 255, 255))
        self.tableWidget_account.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_account.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_account.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        item.setTextAlignment(0)
        self.tableWidget_account.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_account.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_account.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)

        self.tableWidget_account.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)

        self.tableWidget_account.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)



        self.tableWidget_account.setHorizontalHeaderItem(7, item)
        self.tableWidget_account.horizontalHeader().setVisible(True)
        self.tableWidget_account.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_account.horizontalHeader().setDefaultSectionSize(120)
        self.tableWidget_account.horizontalHeader().setHighlightSections(True)
        self.tableWidget_account.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget_account.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_account.verticalHeader().setVisible(False)
        self.tableWidget_account.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget_account.verticalHeader().setHighlightSections(True)
        self.tableWidget_account.verticalHeader().setSortIndicatorShown(False)
        self.tableWidget_account.verticalHeader().setStretchLastSection(False)
        self.tableWidget_account.setIconSize(QSize(25,15))

        self.tableWidget_account.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed) # запрет на изменения ширины колонки

        # задаём ширину колонок
        self.tableWidget_account.setColumnWidth(0, 60)
        self.tableWidget_account.setColumnWidth(1, 110)
        self.tableWidget_account.setColumnWidth(2, 170)
        self.tableWidget_account.setColumnWidth(3, 150)
        self.tableWidget_account.setColumnWidth(4, 60)
        self.tableWidget_account.setColumnWidth(5, 150)
        self.tableWidget_account.setColumnWidth(6, 100)
        self.tableWidget_account.setColumnWidth(7, 160)

        self.gridLayout_3.addWidget(self.tableWidget_account, 0, 0, 1, 1)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout.addWidget(self.scrollArea_2, 1, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                    "border-radius: 8px;")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_account = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_account.setFont(font)
        self.label_account.setStyleSheet("")
        self.label_account.setObjectName("label_account")
        self.horizontalLayout_3.addWidget(self.label_account)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("")
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)

        self.pushButton_move_active = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_move_active.sizePolicy().hasHeightForWidth())
        self.pushButton_move_active.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_move_active.setFont(font)
        self.pushButton_move_active.setStyleSheet("QPushButton {\n"
                                                  "  background: rgb(210, 210, 213);\n"
                                                  "text-align: center;\n"
                                                  "border-radius: 10px;\n"
                                                  "   }\n"
                                                  "   QPushButton:hover {\n"
                                                  "          background-color: rgb(180, 180, 184); /* Цвет при наведении */\n"
                                                  "   }\n"
                                                  "\n"
                                                  "QPushButton:pressed {\n"
                                                  "                   background-color: rgb(150, 150, 153); /* Цвет фона при нажатии */\n"
                                                  "            }")
        self.pushButton_move_active.setObjectName("pushButton_move_active")
        self.horizontalLayout_3.addWidget(self.pushButton_move_active)

        self.pushButton_move_archive = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_move_archive.sizePolicy().hasHeightForWidth())
        self.pushButton_move_archive.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_move_archive.setFont(font)
        self.pushButton_move_archive.setStyleSheet("QPushButton {\n"
                                                   "  background: rgb(210, 210, 213);\n"
                                                   "text-align: center;\n"
                                                   "border-radius: 10px;\n"
                                                   "   }\n"
                                                   "   QPushButton:hover {\n"
                                                   "          background-color: rgb(180, 180, 184); /* Цвет при наведении */\n"
                                                   "   }\n"
                                                   "\n"
                                                   "QPushButton:pressed {\n"
                                                   "                   background-color: rgb(150, 150, 153); /* Цвет фона при нажатии */\n"
                                                   "            }")
        self.pushButton_move_archive.setObjectName("pushButton_move_archive")
        self.horizontalLayout_3.addWidget(self.pushButton_move_archive)

        self.pushButton_move_main_account = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_move_main_account.sizePolicy().hasHeightForWidth())

        self.pushButton_move_main_account.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_move_main_account.setFont(font)
        self.pushButton_move_main_account.setStyleSheet("QPushButton {\n"
                                                        "  background: rgb(210, 210, 213);\n"
                                                        "text-align: center;\n"
                                                        "border-radius: 10px;\n"
                                                        "   }\n"
                                                        "   QPushButton:hover {\n"
                                                        "          background-color: rgb(180, 180, 184); /* Цвет при наведении */\n"
                                                        "   }\n"
                                                        "\n"
                                                        "QPushButton:pressed {\n"
                                                        "                   background-color: rgb(150, 150, 153); /* Цвет фона при нажатии */\n"
                                                        "            }")
        self.pushButton_move_main_account.setObjectName("pushButton_move_main_account")
        self.horizontalLayout_3.addWidget(self.pushButton_move_main_account)

        self.pushButton_update = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_update.setSizePolicy(sizePolicy)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_update.sizePolicy().hasHeightForWidth())
        self.pushButton_update.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_update.setFont(font)
        self.pushButton_update.setStyleSheet("QPushButton {\n"
                                                        "  background: rgb(210, 210, 213);\n"
                                                        "text-align: center;\n"
                                                        "border-radius: 10px;\n"
                                                        "   }\n"
                                                        "   QPushButton:hover {\n"
                                                        "          background-color: rgb(180, 180, 184); /* Цвет при наведении */\n"
                                                        "   }\n"
                                                        "\n"
                                                        "QPushButton:pressed {\n"
                                                        "                   background-color: rgb(150, 150, 153); /* Цвет фона при нажатии */\n"
                                                        "            }")
        self.pushButton_update.setObjectName("pushButton_update")
        self.pushButton_update.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/icon/update.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_update.setIcon(icon1)
        self.pushButton_update.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_update.setCheckable(False)
        self.pushButton_update.setMinimumSize(QtCore.QSize(42, 42))
        self.horizontalLayout_3.addWidget(self.pushButton_update)

        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_7 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_7.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "border-radius: 8px;")
        self.groupBox_7.setTitle("")
        self.groupBox_7.setObjectName("groupBox_7")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_7)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_open_active_accounts = QtWidgets.QPushButton(self.groupBox_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_open_active_accounts.sizePolicy().hasHeightForWidth())
        self.pushButton_open_active_accounts.setSizePolicy(sizePolicy)
        self.pushButton_open_active_accounts.setMinimumSize(QtCore.QSize(0, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_open_active_accounts.setFont(font)
        self.pushButton_open_active_accounts.setStyleSheet("QPushButton {\n"
                                                                    "  background: rgb(150, 150, 153);\n"
                                                                    "text-align: center;\n"
                                                                    "border-radius: 10px;\n"
                                                                    "   }")
        self.pushButton_open_active_accounts.setObjectName("pushButton_open_active_accounts")
        self.horizontalLayout_4.addWidget(self.pushButton_open_active_accounts)
        self.pushButton_open_arxive_accounts = QtWidgets.QPushButton(self.groupBox_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_open_arxive_accounts.sizePolicy().hasHeightForWidth())
        self.pushButton_open_arxive_accounts.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_open_arxive_accounts.setFont(font)
        self.pushButton_open_arxive_accounts.setStyleSheet("QPushButton {\n"
                                                           "  background: rgb(210, 210, 213);\n"
                                                           "text-align: center;\n"
                                                           "border-radius: 10px;\n"
                                                           "   }\n"
                                                           "   QPushButton:hover {\n"
                                                           "          background-color: rgb(180, 180, 184); /* Цвет при наведении */\n"
                                                           "   }\n"
                                                           "\n"
                                                           "QPushButton:pressed {\n"
                                                           "                   background-color: rgb(150, 150, 153); /* Цвет фона при нажатии */\n"
                                                           "            }")
        self.pushButton_open_arxive_accounts.setObjectName("pushButton_open_arxive_accounts")
        self.horizontalLayout_4.addWidget(self.pushButton_open_arxive_accounts)
        self.pushButton_open_main_account = QtWidgets.QPushButton(self.groupBox_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_open_main_account.sizePolicy().hasHeightForWidth())
        self.pushButton_open_main_account.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_open_main_account.setFont(font)
        self.pushButton_open_main_account.setStyleSheet("QPushButton {\n"
                                                        "  background: rgb(210, 210, 213);\n"
                                                        "text-align: center;\n"
                                                        "border-radius: 10px;\n"
                                                        "   }\n"
                                                        "   QPushButton:hover {\n"
                                                        "          background-color: rgb(180, 180, 184); /* Цвет при наведении */\n"
                                                        "   }\n"
                                                        "\n"
                                                        "QPushButton:pressed {\n"
                                                        "                   background-color: rgb(150, 150, 153); /* Цвет фона при нажатии */\n"
                                                        "            }")
        self.pushButton_open_main_account.setObjectName("pushButton_open_main_account")
        self.horizontalLayout_4.addWidget(self.pushButton_open_main_account)
        self.pushButton_open_temporary_ban_accounts = QtWidgets.QPushButton(self.groupBox_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_open_temporary_ban_accounts.sizePolicy().hasHeightForWidth())
        self.pushButton_open_temporary_ban_accounts.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_open_temporary_ban_accounts.setFont(font)
        self.pushButton_open_temporary_ban_accounts.setStyleSheet("QPushButton {\n"
                                                                  "  background: rgb(210, 210, 213);\n"
                                                                  "text-align: center;\n"
                                                                  "border-radius: 10px;\n"
                                                                  "   }\n"
                                                                  "   QPushButton:hover {\n"
                                                                  "          background-color: rgb(180, 180, 184); /* Цвет при наведении */\n"
                                                                  "   }\n"
                                                                  "\n"
                                                                  "QPushButton:pressed {\n"
                                                                  "                   background-color: rgb(150, 150, 153); /* Цвет фона при нажатии */\n"
                                                                  "            }")
        self.pushButton_open_temporary_ban_accounts.setObjectName("pushButton_open_temporary_ban_accounts")
        self.horizontalLayout_4.addWidget(self.pushButton_open_temporary_ban_accounts)
        self.pushButton_open_login_error = QtWidgets.QPushButton(self.groupBox_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_open_login_error.sizePolicy().hasHeightForWidth())
        self.pushButton_open_login_error.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_open_login_error.setFont(font)
        self.pushButton_open_login_error.setStyleSheet("QPushButton {\n"
                                                       "  background: rgb(210, 210, 213);\n"
                                                       "text-align: center;\n"
                                                       "border-radius: 10px;\n"
                                                       "   }\n"
                                                       "   QPushButton:hover {\n"
                                                       "          background-color: rgb(180, 180, 184); /* Цвет при наведении */\n"
                                                       "   }\n"
                                                       "\n"
                                                       "QPushButton:pressed {\n"
                                                       "                   background-color: rgb(150, 150, 153); /* Цвет фона при нажатии */\n"
                                                       "            }")
        self.pushButton_open_login_error.setObjectName("pushButton_open_login_error")
        self.horizontalLayout_4.addWidget(self.pushButton_open_login_error)
        self.gridLayout.addWidget(self.groupBox_7, 2, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 2, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(20, 0, 20, 10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_add = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_add.sizePolicy().hasHeightForWidth())
        self.pushButton_add.setSizePolicy(sizePolicy)
        self.pushButton_add.setMinimumSize(QtCore.QSize(185, 55))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_add.setFont(font)
        self.pushButton_add.setStyleSheet("\n"
                                          "QPushButton {\n"
                                          "    background-color: rgb(255, 255, 255);\n"
                                          "    text-align: center;\n"
                                          "    border-radius: 17px;\n"
                                          "   }\n"
                                          "QPushButton:hover {\n"
                                          "    background-color: rgb(230, 230, 230); /* Цвет фона при наведении (немного серый) */\n"
                                          "}\n"
                                          "\n"
                                          "QPushButton:pressed {\n"
                                          "     background: rgb(210, 210, 213); /* Цвет фона при нажатии (еще серее) */\n"
                                          "}")
        self.pushButton_add.setIconSize(QtCore.QSize(120, 120))
        self.pushButton_add.setObjectName("pushButton_add")
        self.horizontalLayout.addWidget(self.pushButton_add)
        self.pushButton_show_data_account = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_show_data_account.sizePolicy().hasHeightForWidth())
        self.pushButton_show_data_account.setSizePolicy(sizePolicy)
        self.pushButton_show_data_account.setMinimumSize(QtCore.QSize(185, 55))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_show_data_account.setFont(font)
        self.pushButton_show_data_account.setStyleSheet("\n"
                                                     "QPushButton {\n"
                                                     "    background-color: rgb(255, 255, 255);\n"
                                                     "    text-align: center;\n"
                                                     "    border-radius: 17px;\n"
                                                     "   }\n"
                                                     "QPushButton:hover {\n"
                                                     "    background-color: rgb(230, 230, 230); /* Цвет фона при наведении (немного серый) */\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:pressed {\n"
                                                     "     background: rgb(210, 210, 213); /* Цвет фона при нажатии (еще серее) */\n"
                                                     "}")
        self.pushButton_show_data_account.setIconSize(QtCore.QSize(120, 120))
        self.pushButton_show_data_account.setObjectName("pushButton_show_data_account")
        self.horizontalLayout.addWidget(self.pushButton_show_data_account)
        self.pushButton_enter = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_enter.sizePolicy().hasHeightForWidth())
        self.pushButton_enter.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_enter.setFont(font)
        self.pushButton_enter.setStyleSheet("\n"
                                            "QPushButton {\n"
                                            "    background-color: rgb(255, 255, 255);\n"
                                            "    text-align: center;\n"
                                            "    border-radius: 17px;\n"
                                            "   }\n"
                                            "QPushButton:hover {\n"
                                            "    background-color: rgb(230, 230, 230); /* Цвет фона при наведении (немного серый) */\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:pressed {\n"
                                            "     background: rgb(210, 210, 213); /* Цвет фона при нажатии (еще серее) */\n"
                                            "}")
        self.pushButton_enter.setObjectName("pushButton_enter")
        self.horizontalLayout.addWidget(self.pushButton_enter)
        self.pushButton_upload_tdata = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_upload_tdata.sizePolicy().hasHeightForWidth())
        self.pushButton_upload_tdata.setSizePolicy(sizePolicy)
        self.pushButton_upload_tdata.setMinimumSize(QtCore.QSize(185, 55))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_upload_tdata.setFont(font)
        self.pushButton_upload_tdata.setStyleSheet("\n"
                                                   "QPushButton {\n"
                                                   "    background-color: rgb(255, 255, 255);\n"
                                                   "    text-align: center;\n"
                                                   "    border-radius: 17px;\n"
                                                   "    padding-left: 5px;\n"
                                                   "    padding-right: 5px;\n"
                                                   "   }\n"
                                                   "QPushButton:hover {\n"
                                                   "    background-color: rgb(230, 230, 230); /* Цвет фона при наведении (немного серый) */\n"
                                                   "}\n"
                                                   "\n"
                                                   "QPushButton:pressed {\n"
                                                   "     background: rgb(210, 210, 213); /* Цвет фона при нажатии (еще серее) */\n"
                                                   "}")
        self.pushButton_upload_tdata.setObjectName("pushButton_upload_tdata")
        self.horizontalLayout.addWidget(self.pushButton_upload_tdata)
        self.pushButton_delete = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_delete.sizePolicy().hasHeightForWidth())
        self.pushButton_delete.setSizePolicy(sizePolicy)
        self.pushButton_delete.setMinimumSize(QtCore.QSize(185, 55))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_delete.setFont(font)
        self.pushButton_delete.setStyleSheet("\n"
                                             "QPushButton {\n"
                                             "    background-color: rgb(255, 255, 255);\n"
                                             "    text-align: center;\n"
                                             "    border-radius: 17px;\n"
                                             "   }\n"
                                             "QPushButton:hover {\n"
                                             "    background-color: rgb(230, 230, 230); /* Цвет фона при наведении (немного серый) */\n"
                                             "}\n"
                                             "\n"
                                             "QPushButton:pressed {\n"
                                             "     background: rgb(210, 210, 213); /* Цвет фона при нажатии (еще серее) */\n"
                                             "}")
        self.pushButton_delete.setIconSize(QtCore.QSize(120, 120))
        self.pushButton_delete.setObjectName("pushButton_delete")
        self.horizontalLayout.addWidget(self.pushButton_delete)
        self.gridLayout_2.addLayout(self.horizontalLayout, 3, 1, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(20, 0, 20, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "border-radius: 13px;")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_count_all_account = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_count_all_account.sizePolicy().hasHeightForWidth())
        self.label_count_all_account.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_count_all_account.setFont(font)
        self.label_count_all_account.setStyleSheet("")
        self.label_count_all_account.setObjectName("label_count_all_account")
        self.verticalLayout_2.addWidget(self.label_count_all_account)
        self.label = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setStyleSheet("")
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout_2.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "border-radius: 13px;")
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_count_active_account = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_count_active_account.sizePolicy().hasHeightForWidth())
        self.label_count_active_account.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_count_active_account.setFont(font)
        self.label_count_active_account.setStyleSheet("")
        self.label_count_active_account.setObjectName("label_count_active_account")
        self.verticalLayout_3.addWidget(self.label_count_active_account)
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.horizontalLayout_2.addWidget(self.groupBox_3)

        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "border-radius: 13px;")
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_count_archive_account = QtWidgets.QLabel(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_count_archive_account.sizePolicy().hasHeightForWidth())
        self.label_count_archive_account.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_count_archive_account.setFont(font)
        self.label_count_archive_account.setStyleSheet("")
        self.label_count_archive_account.setObjectName("label_count_archive_account")
        self.verticalLayout_4.addWidget(self.label_count_archive_account)
        self.label_3 = QtWidgets.QLabel(self.groupBox_4)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("")
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.horizontalLayout_2.addWidget(self.groupBox_4)



        self.groupBox_8 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_8.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "border-radius: 13px;")
        self.groupBox_8.setTitle("")
        self.groupBox_8.setObjectName("groupBox_8")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.groupBox_8)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_count_main_account = QtWidgets.QLabel(self.groupBox_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_count_main_account.sizePolicy().hasHeightForWidth())
        self.label_count_main_account.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_count_main_account.setFont(font)
        self.label_count_main_account.setStyleSheet("")
        self.label_count_main_account.setObjectName("label_count_main_account")
        self.verticalLayout_8.addWidget(self.label_count_main_account)
        self.label_10 = QtWidgets.QLabel(self.groupBox_8)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("")
        self.label_10.setObjectName("label_10")
        self.verticalLayout_8.addWidget(self.label_10)
        self.horizontalLayout_2.addWidget(self.groupBox_8)



        self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_5.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "border-radius: 13px;\n"
                                      "")
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_count_temporary_banned_account = QtWidgets.QLabel(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_count_temporary_banned_account.sizePolicy().hasHeightForWidth())
        self.label_count_temporary_banned_account.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_count_temporary_banned_account.setFont(font)
        self.label_count_temporary_banned_account.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_count_temporary_banned_account.setStyleSheet("")
        self.label_count_temporary_banned_account.setObjectName("label_count_temporary_banned_account")
        self.verticalLayout_5.addWidget(self.label_count_temporary_banned_account)
        self.label_6 = QtWidgets.QLabel(self.groupBox_5)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("")
        self.label_6.setObjectName("label_6")
        self.verticalLayout_5.addWidget(self.label_6)
        self.horizontalLayout_2.addWidget(self.groupBox_5)
        self.groupBox_6 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_6.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "border-radius: 13px;\n"
                                      "")
        self.groupBox_6.setTitle("")
        self.groupBox_6.setObjectName("groupBox_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_6)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_count_login_error = QtWidgets.QLabel(self.groupBox_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_count_login_error.sizePolicy().hasHeightForWidth())
        self.label_count_login_error.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_count_login_error.setFont(font)
        self.label_count_login_error.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_count_login_error.setStyleSheet("border: 0px ;\n"
                                                   "border-radius: 1;\n"
                                                   "")
        self.label_count_login_error.setObjectName("label_count_login_error")
        self.verticalLayout_6.addWidget(self.label_count_login_error)
        self.label_7 = QtWidgets.QLabel(self.groupBox_6)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("border: 0px ;\n"
                                   "border-radius: 1;\n"
                                   "")
        self.label_7.setObjectName("label_7")
        self.verticalLayout_6.addWidget(self.label_7)
        self.horizontalLayout_2.addWidget(self.groupBox_6)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(270, 0))
        self.scrollArea.setMaximumSize(QtCore.QSize(270, 16777215))
        self.scrollArea.setStyleSheet("background-color: rgb(14, 22, 33);\n"
                                      "border: none;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 238, 848))
        self.scrollAreaWidgetContents.setStyleSheet("")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_account_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
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
                                                "border: 1;\n"
                                                "text-align: center;\n"
                                                "padding: 10px;")
        self.pushButton_account_2.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/logo.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_account_2.setIcon(icon1)
        self.pushButton_account_2.setIconSize(QtCore.QSize(300, 60))
        self.pushButton_account_2.setCheckable(False)
        self.pushButton_account_2.setObjectName("pushButton_account_2")
        self.verticalLayout.addWidget(self.pushButton_account_2)
        self.label_9 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QtCore.QSize(0, 0))
        self.label_9.setText("")
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9)
        self.pushButton_account = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
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
                                              "color: rgb(255, 255, 255);\n"
                                              "border: 1;\n"
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
        icon2.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/account.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_account.setIcon(icon2)
        self.pushButton_account.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_account.setCheckable(False)
        self.pushButton_account.setObjectName("pushButton_account")
        self.verticalLayout.addWidget(self.pushButton_account)
        self.pushButton_mailing = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
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
                                              "border: 1;\n"
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
        icon3.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/mailing.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_mailing.setIcon(icon3)
        self.pushButton_mailing.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_mailing.setObjectName("pushButton_mailing")
        self.verticalLayout.addWidget(self.pushButton_mailing)
        self.pushButton_mailing_chat = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_mailing_chat.setFont(font)
        self.pushButton_mailing_chat.setStyleSheet("QPushButton {\n"
                                                   "color: rgb(143, 145, 165);\n"
                                                   "border: 1;\n"
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
        self.pushButton_mailing_chat.setIcon(icon3)
        self.pushButton_mailing_chat.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_mailing_chat.setObjectName("pushButton_mailing_chat")
        self.verticalLayout.addWidget(self.pushButton_mailing_chat)
        self.pushButton_invite = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
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
                                             "border: 1;\n"
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
        icon4.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/invaite.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_invite.setIcon(icon4)
        self.pushButton_invite.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_invite.setObjectName("pushButton_invite")
        self.verticalLayout.addWidget(self.pushButton_invite)
        self.pushButton_parser = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
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
                                             "border: 1;\n"
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
        icon5.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/parser.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_parser.setIcon(icon5)
        self.pushButton_parser.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_parser.setObjectName("pushButton_parser")
        self.verticalLayout.addWidget(self.pushButton_parser)
        self.pushButton_proxy = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
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
                                            "border: 1;\n"
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
        icon6.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/proxy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_proxy.setIcon(icon6)
        self.pushButton_proxy.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_proxy.setObjectName("pushButton_proxy")
        self.verticalLayout.addWidget(self.pushButton_proxy)
        self.pushButton_bomber = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_bomber.setMinimumSize(QtCore.QSize(185, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_bomber.setFont(font)
        self.pushButton_bomber.setStyleSheet("QPushButton {\n"
                                             "color: rgb(143, 145, 165);\n"
                                             "border: 1;\n"
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
        icon7.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/bomber.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_bomber.setIcon(icon7)
        self.pushButton_bomber.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_bomber.setObjectName("pushButton_bomber")
        self.verticalLayout.addWidget(self.pushButton_bomber)
        self.pushButton_enter_group = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_enter_group.setFont(font)
        self.pushButton_enter_group.setStyleSheet("QPushButton {\n"
                                                  "color: rgb(143, 145, 165);\n"
                                                  "border: 1;\n"
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
        icon8.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/enter_the_group.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_enter_group.setIcon(icon8)
        self.pushButton_enter_group.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_enter_group.setObjectName("pushButton_enter_group")
        self.verticalLayout.addWidget(self.pushButton_enter_group)
        self.pushButton_reactions = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_reactions.setFont(font)
        self.pushButton_reactions.setStyleSheet("QPushButton {\n"
                                                "color: rgb(143, 145, 165);\n"
                                                "border: 1;\n"
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
        icon9.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/like.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_reactions.setIcon(icon9)
        self.pushButton_reactions.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_reactions.setObjectName("pushButton_reactions")
        self.verticalLayout.addWidget(self.pushButton_reactions)
        self.pushButton_comment = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_comment.setFont(font)
        self.pushButton_comment.setStyleSheet("QPushButton {\n"
                                              "color: rgb(143, 145, 165);\n"
                                              "border: 1;\n"
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
        icon10.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/coment.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_comment.setIcon(icon10)
        self.pushButton_comment.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_comment.setObjectName("pushButton_comment")
        self.verticalLayout.addWidget(self.pushButton_comment)
        self.pushButton_convert = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
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
                                              "color: rgb(143, 145, 165);\n"
                                              "border: 1;\n"
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
        icon11.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/convert.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_convert.setIcon(icon11)
        self.pushButton_convert.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_convert.setObjectName("pushButton_convert")
        self.verticalLayout.addWidget(self.pushButton_convert)

        self.pushButton_clone = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_clone.sizePolicy().hasHeightForWidth())
        self.pushButton_clone.setSizePolicy(sizePolicy)
        self.pushButton_clone.setMinimumSize(QtCore.QSize(185, 0))
        self.pushButton_clone.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_clone.setFont(font)
        self.pushButton_clone.setStyleSheet("QPushButton {\n"
                                          "color: rgb(143, 145, 165);\n"
                                          "border: 1;\n"
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
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/clone.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_clone.setIcon(icon12)
        self.pushButton_clone.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_clone.setObjectName("pushButton_clone")
        self.verticalLayout.addWidget(self.pushButton_clone)

        self.pushButton_doc = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
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
                                          "border: 1;\n"
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
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/doc.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_doc.setIcon(icon12)
        self.pushButton_doc.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_doc.setObjectName("pushButton_doc")
        self.verticalLayout.addWidget(self.pushButton_doc)

        self.pushButton_settings = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_settings.sizePolicy().hasHeightForWidth())
        self.pushButton_settings.setSizePolicy(sizePolicy)
        self.pushButton_settings.setMinimumSize(QtCore.QSize(185, 0))
        self.pushButton_settings.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_settings.setFont(font)
        self.pushButton_settings.setStyleSheet("QPushButton {\n"
                                          "color: rgb(143, 145, 165);\n"
                                          "border: 1;\n"
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
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_settings.setIcon(icon12)
        self.pushButton_settings.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_settings.setObjectName("pushButton_settings")
        self.verticalLayout.addWidget(self.pushButton_settings)

        self.label_8 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QtCore.QSize(0, 0))
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 4, 1)
        self.setCentralWidget(self.centralwidget)
        self.action = QtWidgets.QAction(self)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(self)
        self.action_2.setObjectName("action_2")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)



        # события
        self.pushButton_mailing.clicked.connect(lambda: self._transition('mailing_by_users'))
        self.pushButton_mailing_chat.clicked.connect(lambda: self._transition('mailing_by_chats'))
        self.pushButton_invite.clicked.connect(lambda: self._transition('invite'))
        self.pushButton_parser.clicked.connect(lambda: self._transition('parser'))
        self.pushButton_proxy.clicked.connect(lambda: self._transition('proxy'))
        self.pushButton_bomber.clicked.connect(lambda: self._transition('bomber'))
        self.pushButton_enter_group.clicked.connect(lambda: self._transition('enter_group'))
        self.pushButton_reactions.clicked.connect(lambda: self._transition('reactions'))
        self.pushButton_comment.clicked.connect(lambda: self._transition('comment'))
        self.pushButton_convert.clicked.connect(lambda: self._transition('convert'))
        self.pushButton_doc.clicked.connect(lambda: self._transition('doc'))

        self.pushButton_open_active_accounts.clicked.connect(lambda: self._show_tab_account(self.pushButton_open_active_accounts))
        self.pushButton_open_arxive_accounts.clicked.connect(lambda: self._show_tab_account(self.pushButton_open_arxive_accounts))
        self.pushButton_open_main_account.clicked.connect(lambda: self._show_tab_account(self.pushButton_open_main_account))
        self.pushButton_open_temporary_ban_accounts.clicked.connect(lambda: self._show_tab_account(self.pushButton_open_temporary_ban_accounts))
        self.pushButton_open_login_error.clicked.connect(lambda: self._show_tab_account(self.pushButton_open_login_error))

        self.pushButton_add.clicked.connect(lambda: self._add_accounts())

        self.pushButton_move_active.clicked.connect(lambda: self._move_accounts(self.pushButton_move_active))
        self.pushButton_move_main_account.clicked.connect(lambda: self._move_accounts(self.pushButton_move_main_account))
        self.pushButton_move_archive.clicked.connect(lambda: self._move_accounts(self.pushButton_move_archive))

        self.pushButton_update.clicked.connect(lambda: self.start_show_account(self.selected_account_type))

        self.pushButton_show_data_account.clicked.connect(lambda: self._show_more_info_account())
        self.pushButton_enter.clicked.connect(lambda: self._enter_account())
        self.pushButton_upload_tdata.clicked.connect(lambda: self._upload_tdata())
        self.pushButton_delete.clicked.connect(lambda: self._delete_accounts())

        self.tableWidget_account.itemChanged.connect(lambda: self._on_item_changed())
        # события

    def _transition(self, target_window: str):
        if self.open_account:
            error_info = Dialog_info('Внимание!', 'Дождитесь загрузки аккаунтов!\nЭто необходимо для предотвращения возможных ошибок.',
                                     'notification.mp3')  # Создаем экземпляр
            error_info.exec_()  # Открываем
        else:
            self.switch_window(target_window)

    def start_show_account(self,type_accounts: str):
        self._update_count_accounts()
        self.open_account = True

        # Проверка на существующую анимацию и остановка
        if hasattr(self, 'animation_fading_progress_bar'):
            self.animation_fading_progress_bar.stop()

        self.opacity_effect = QGraphicsOpacityEffect(self.groupBox_progress)
        self.groupBox_progress.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1)  # Полностью не прозрачен

        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()
        cursor.execute(f"SELECT ip,port,login,password,use_proxy_to_enter FROM proxy")
        proxy_from_db = cursor.fetchone()
        connection.close()
        proxy = False
        if proxy_from_db[4] == 1 and self.selected_account_type != 'login_error':  # если необходимо использовать прокси
            efficiency = check_proxy(proxy_from_db[0], int(proxy_from_db[1]), proxy_from_db[2], proxy_from_db[3])
            if efficiency:
                proxy = True
            else:  # если получили ошибку прокси
                icon = QIcon()
                icon.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/icon/warning.png"), QtGui.QIcon.Normal,
                               QtGui.QIcon.Off)
                self.label_result_open_account.setText('Ошибка прокси!        ')
                self.button_info_open_account.setIcon(icon)
                self.label_gif_load.hide()
                self.button_info_open_account.show()
                self.label_result_open_account.show()
                self._fading_progress_bar()  # вызываем затухание

                connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
                cursor = connection.cursor()
                cursor.execute(f"SELECT ip,port,login,password FROM proxy")
                proxy_from_db = cursor.fetchone()
                connection.close()
                self._show_error_proxy(proxy_from_db[0], proxy_from_db[1], proxy_from_db[2], proxy_from_db[3])

                self.open_account = False
                return

        self.label_gif_load.show()
        self.button_info_open_account.hide()
        self.label_result_open_account.hide()
        self.groupBox_progress.show()
        self.tableWidget_account.setRowCount(0)

        # обнуляем всё
        self.active_threads = []
        self.accounts = []
        self.error_accounts = []
        self.quantity_start_accounts = 0
        self.quantity_received_accounts = 0

        # запуск показа аккаунтов

        if type_accounts == 'login_error': # если необходимо показать аккаунты из БД
            self.show_accounts_from_db()
            self.open_account = False
            return
        else:
            id_account = 0
            while True:
                if os.path.isdir(self.root_project_dir + f'/accounts/{type_accounts}_accounts/{id_account}'):  # если аккаунт есть
                    show_account_stream = show_account(self.root_project_dir + f'/accounts/{type_accounts}_accounts/{id_account}',
                                                       id_account, type_accounts,proxy,proxy_from_db[0],
                                                       proxy_from_db[1],proxy_from_db[2],proxy_from_db[3])  # Инициализируем рабочий поток
                    show_account_stream.task_done.connect(self._show_account_done)  # Подключаем сигнал к слоту
                    show_account_stream.start()  # Запускаем поток

                    self.active_threads.append(show_account_stream) # Добавляем в массив с потоками (что бы не очистились эти потоки)
                    id_account += 1
                    self.quantity_start_accounts += 1
                else:
                    if id_account == 0:
                        if not self.program_launch: # если программа уже запущенна
                            error_info = Dialog_info('Внимание!', 'В данной вкладке нет аккаунтов', 'notification.mp3')
                            error_info.exec_()
                        self.groupBox_progress.hide()
                        self.open_account = False
                        self.program_launch = False  # устанавливаем, что программа больше не загружается
                        break
                    else:
                        break

    def _show_account_done(self, account_data: list, account_error: bool):
        if account_error: # если произошла ошибка входа в аккаунт
            self.error_accounts.append(account_data)
        else:
            self.accounts.append(account_data)

        self.quantity_received_accounts += 1 # т.к. у нас вернулся один аккаунт-

        if self.quantity_received_accounts >= self.quantity_start_accounts: # если число запущенных аккаунтов совпало с числом вернувшихся
            self.active_threads.clear()
            socket.socket = self.original_socket  # убираем прокси

            if self.accounts:
                sorted_accounts = sorted( self.accounts, key=lambda x: x[0]) # фильтруем (в порядке возрастания по первому элементу вложенного списка)

                row = 0
                for account_info in sorted_accounts:
                    self._update_account_data(account_info) # обновление данных в БД (если не сходятся с имеющимися)

                    for information in self._get_additional_information(account_info): # получение доп информации об аккаунте через БД
                        account_info.append(information)

                    col = 0
                    self.tableWidget_account.insertRow(row)
                    for info in account_info:
                        item = None
                        if col == 4:  # если это колонка с гео
                            flag_pixmap = QPixmap(self.root_project_dir + f'/resources/pictures_flag/{info}.png')  # Путь к изображению флага
                            if not flag_pixmap.isNull():  # Проверяем, что изображение загружено успешно
                                item = QTableWidgetItem()
                                item.setIcon(QIcon(flag_pixmap))  # Устанавливаем изображение в ячейку
                            else:
                                flag_pixmap = QPixmap(self.root_project_dir + f'/resources/pictures_flag/default_flag.png')  # Путь к изображению флага
                                item = QTableWidgetItem()
                                item.setIcon(QIcon(flag_pixmap))  # Устанавливаем изображение в ячейку
                        elif col == 0: # если это строка с id
                            item = QTableWidgetItem(str(row))
                        else:
                            item = QTableWidgetItem(info)

                        item.setTextAlignment(Qt.AlignCenter)  # Центрируем текст в ячейке
                        font = QtGui.QFont()
                        font.setPointSize(9)
                        item.setFont(font)

                        if col == self.tableWidget_account.columnCount() - 1:  # Если это последняя строка
                            item.setFlags(item.flags() | Qt.ItemIsEditable)  # Разрешаем редактирование
                        else:
                            item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Запрещаем редактирование
                        self.tableWidget_account.setItem(row, col, item)
                        col += 1
                    row += 1

            if self.error_accounts: # если есть ошибки при показе аккаунтов
                icon = QIcon()
                icon.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/icon/warning.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.label_result_open_account.setText('При загрузке произошла ошибка!')

                full_list_error_account = []
                connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
                cursor = connection.cursor()
                for account in self.error_accounts:
                    cursor.execute(f"SELECT id_tg,user_name FROM accounts WHERE id = ? AND account_status = ?",
                                   (account[1],self.selected_account_type))
                    id_and_user_name = cursor.fetchone()
                    error_and_solution_error = get_description_and_solution(account[0])
                    full_list_error_account.append([id_and_user_name[0], id_and_user_name[1],error_and_solution_error[0], error_and_solution_error[1]])

                connection.close()

                sorted_list = sorted(self.error_accounts, key=lambda x: x[1], reverse=True)
                for error_and_id in sorted_list:  # работаем с аккаунтами в которые не смогли войти
                    error_handler(error_and_id[0], error_and_id[1], self.selected_account_type)

                error_info = Dialog_error_open_accounts(full_list_error_account)
                error_info.exec_()
            else:
                icon = QIcon()
                icon.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/icon/success.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.label_result_open_account.setText('Загрузка прошла успешно!')

            self._update_count_accounts()
            self.button_info_open_account.setIcon(icon)
            self.label_gif_load.hide()
            self.button_info_open_account.show()
            self.label_result_open_account.show()
            self._fading_progress_bar() # вызываем затухание

            if not self.accounts and self.program_launch == False: #
                error_info = Dialog_info('Внимание!', 'В данной вкладке нет аккаунтов','notification.mp3')
                error_info.exec_()

            self._update_count_accounts()
            self.open_account = False # устанавливаем что аккаунты загружены
            self.program_launch = False # устанавливаем, что программа больше не загружается

    def _show_tab_account(self, button: QPushButton):
        if self.open_account == True:
            error_info = Dialog_info('Внимание!', 'Уже происходит открытие аккаунтов!','notification.mp3')  # Создаем экземпляр
            error_info.exec_()  # Открываем
            return


        # если кнопка не нажата
        if not button.styleSheet() == "QPushButton {\n  background: rgb(150, 150, 153);\ntext-align: center;\nborder-radius: 10px;\n   }":

            style_sheet = ("QPushButton {\n"
                           "  background: rgb(210, 210, 213);\n"
                           "text-align: center;\n"
                           "border-radius: 10px;\n"
                           "   }\n"
                           "   QPushButton:hover {\n"
                           "          background-color: rgb(180, 180, 184); /* Цвет при наведении */\n"
                           "   }\n"
                           "\n"
                           "QPushButton:pressed {\n"
                           "                   background-color: rgb(150, 150, 153); /* Цвет фона при нажатии */\n"
                           "            }")

            self.pushButton_open_active_accounts.setStyleSheet(style_sheet)
            self.pushButton_open_arxive_accounts.setStyleSheet(style_sheet)
            self.pushButton_open_main_account.setStyleSheet(style_sheet)
            self.pushButton_open_temporary_ban_accounts.setStyleSheet(style_sheet)
            self.pushButton_open_login_error.setStyleSheet(style_sheet)

            button.setStyleSheet("QPushButton {\n"
                                "  background: rgb(150, 150, 153);\n"
                                "text-align: center;\n"
                                "border-radius: 10px;\n"
                                "   }") # устанавливаем определённый стиль для кнопки которую нажали

            label_name = 'Активные:'
            if button.objectName() == 'pushButton_open_active_accounts':
                self.selected_account_type = 'active'
                label_name = 'Активные:'
            elif button.objectName() == 'pushButton_open_arxive_accounts':
                self.selected_account_type = 'archive'
                label_name = 'Архив:'
            elif button.objectName() == 'pushButton_open_main_account':
                self.selected_account_type = 'main'
                label_name = 'Главные:'
            elif button.objectName() == 'pushButton_open_temporary_ban_accounts':
                self.selected_account_type = 'temporary_ban'
                label_name = 'Во временном бане:'
            elif button.objectName() == 'pushButton_open_login_error':
                self.selected_account_type = 'login_error'
                label_name = 'С ошибкой входа:'

            self.label_account.setText(label_name)
            self.start_show_account(self.selected_account_type)
            # вызвать показ аккаунтов (в показе аккаунтов добавить поменять лейбл который отображает на каких мы сейчас аккаунтах)

    def _add_accounts(self):
        if self.open_account == True:
            error_info = Dialog_info('Внимание!', 'Дождитесь загрузки аккаунтов!','notification.mp3')  # Создаем экземпляр
            error_info.exec_()  # Открываем
            return

        info_add_accounts = Dialog_info_add_accounts()  # Создаем экземпляр
        info_add_accounts.data_returned.connect(self._start_add_accounts)  # Подключаем сигнал
        info_add_accounts.exec_()  # Открываем модальное окно

    def _start_add_accounts(self,path: str):
        add_accounts = Dialog_add_accounts(path)  # Создаем экземпляр
        add_accounts.start()
        add_accounts.exec_()  # Открываем модальное окно

        if self.label_account.text() == 'Активные:': # если открыты активные аккауты, то необходимо добавить в список новые добавленные аккаунты
            self.show_accounts_from_db() # добавление новых строк из добавленных аккаунтов

        self._update_count_accounts()

    def show_accounts_from_db(self): # покажет аккаунты на вкладке которая открыта сейчас
        self.tableWidget_account.setRowCount(0)

        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()

        counter = 0
        while True:
            cursor.execute(f"SELECT id,id_tg,user_name,name,phone,data_time_add,last_used,notes FROM accounts WHERE id = ? AND account_status = ?",
                (counter, self.selected_account_type))
            account_from_db = cursor.fetchone()
            counter += 1
            if account_from_db:

                dt_from_db = dt.datetime.strptime(account_from_db[5],'%H:%M %d-%m-%Y')  # первый принимаемый параметр это входная строка с датой, второй это формат даты
                time_difference = dt.datetime.now() - dt_from_db  # Вычисляем разницу во времени
                days_difference = time_difference.days
                resting_place = f"{days_difference} {'день' if days_difference == 1 else 'дня' if 2 <= days_difference <= 4 else 'дней'}"

                geo = get_country_flag(account_from_db[4])

                # информация об аккаунте
                info_account = [str(account_from_db[0]), str(account_from_db[1]), account_from_db[2], account_from_db[3],
                                geo, account_from_db[4], resting_place, account_from_db[6], account_from_db[7]]

                self.tableWidget_account.insertRow(int(info_account[0]))
                col = 0

                for info in info_account:
                    item = None
                    if col == 4:  # если это колонка с гео
                        flag_pixmap = QPixmap(self.root_project_dir + f'/resources/pictures_flag/{info}.png')  # Путь к изображению флага
                        if not flag_pixmap.isNull():  # Проверяем, что изображение загружено успешно
                            item = QTableWidgetItem()
                            item.setIcon(QIcon(flag_pixmap))  # Устанавливаем изображение в ячейку
                        else:
                            flag_pixmap = QPixmap(self.root_project_dir + f'/resources/pictures_flag/default_flag.png')  # Путь к изображению флага
                            item = QTableWidgetItem()
                            item.setIcon(QIcon(flag_pixmap))  # Устанавливаем изображение в ячейку
                    else:
                        item = QTableWidgetItem(info)

                    item.setTextAlignment(Qt.AlignCenter)  # Центрируем текст в ячейке
                    font = QtGui.QFont()
                    font.setPointSize(9)
                    item.setFont(font)

                    if col == self.tableWidget_account.columnCount() - 1:  # Если это последняя строка
                        item.setFlags(item.flags() | Qt.ItemIsEditable)  # Разрешаем редактирование
                    else:
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Запрещаем редактирование
                    self.tableWidget_account.setItem(int(info_account[0]), col, item)
                    col += 1
            else:
                break

        connection.close()

        icon = QIcon()
        icon.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/icon/success.png"), QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.label_result_open_account.setText('Загрузка прошла успешно!')
        self._update_count_accounts()
        self.button_info_open_account.setIcon(icon)
        self.label_gif_load.hide()
        self.button_info_open_account.show()
        self.label_result_open_account.show()
        self._fading_progress_bar()  # вызываем затухание

    def _move_accounts(self,button: QPushButton):
        if self.selected_account_type == 'login_error':
            error_info = Dialog_info('Внимание!', 'С данного раздела нельзя\nперемещать аккаунты!', 'notification.mp3')
            error_info.exec_()  # Открываем
            return

        selected_rows = set()
        for item in self.tableWidget_account.selectedItems():
            selected_rows.add(item.row())  # добавляем номер строки и добавляем в множество

        if not selected_rows: # если пользователь не выбрал строки
            error_info = Dialog_info('Внимание!', 'Для данного действия выберите аккаунты!','notification.mp3')
            error_info.exec_()  # Открываем
            return

        target_type_account = 'active'
        if button.objectName() == 'pushButton_move_active':
            target_type_account = 'active'
        elif button.objectName() == 'pushButton_move_archive':
            target_type_account = 'archive'
        elif button.objectName() == 'pushButton_move_main_account':
            target_type_account = 'main'

        if target_type_account == self.selected_account_type: # если пользователь захотел переместить аккаунты в папку что уже открыта
            error_info = Dialog_info('Внимание!', 'Выбранные аккаунты уже\nнаходятся в этом разделе!', 'notification.mp3')
            error_info.exec_()  # Открываем
            return

        selected_rows = sorted(selected_rows, reverse=True)  # Превращаем множество в отсортированный список по убыванию
        where_from_copy_path = self.root_project_dir + f'/accounts/{self.selected_account_type}_accounts' # откуда копировать
        where_copy_path = self.root_project_dir + f'/accounts/{target_type_account}_accounts' # куда копировать

        # узнать id с которого будет необходимо вставлять папки
        items = os.listdir(where_copy_path)  # Получаем список файлов и папок в указанной директории
        last_id_in_target_copy = sum(1 for item in items if os.path.isdir(os.path.join(where_copy_path, item)))  # Фильтруем только папки

        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()
        cursor.execute(f"SELECT ip,port,login,password FROM proxy")

        for id_folder in selected_rows: # добавление и удаление ненужных папок
            try:  # копирование (принимает папку в которой хранится tdata, то есть мы копируем содержимое указанной папки)
                shutil.copytree(where_from_copy_path + f'/{id_folder}',where_copy_path + f'/{last_id_in_target_copy}') # копирование
                cursor.execute(f"UPDATE accounts SET id = ?, account_status = ?  WHERE id = ? AND account_status = ?",
                               (last_id_in_target_copy, target_type_account, id_folder, self.selected_account_type))
                connection.commit()  # меняем в БД значения
                shutil.rmtree(where_from_copy_path + f'/{id_folder}') # удаление что только что скопировали
                last_id_in_target_copy += 1
            except FileNotFoundError:
                pass


        for id_from_folder_copy in selected_rows:# меняем последовательность id из папки откуда копировали
            while True:
                id_result = id_from_folder_copy
                id_from_folder_copy += 1
                try:
                    if os.path.isdir(where_from_copy_path + f'/{id_from_folder_copy}'):  # если такая папка есть
                        os.rename(where_from_copy_path + f'/{id_from_folder_copy}',where_from_copy_path + f'/{id_result}')  # переименование
                        cursor.execute(f"UPDATE accounts SET id = ?, account_status = ?  WHERE id = ? AND account_status = ?",
                                       (id_result, self.selected_account_type, id_from_folder_copy, self.selected_account_type))
                        connection.commit()  # меняем в БД значения
                    else:
                        break
                except Exception:
                    pass

        connection.close()

        self.show_accounts_from_db()
        self._update_count_accounts()

        if len(selected_rows) > 1:
            message = f'Аккаунты успешно перемещены\nВ количестве {len(selected_rows)}'
        else:
            message = 'Аккаунт успешно перемещён'
        error_info = Dialog_info('Готово!', message, 'notification.mp3')
        error_info.exec_()  # Открываем

    def _show_more_info_account(self):
        selected_rows = set()
        for item in self.tableWidget_account.selectedItems():
            selected_rows.add(item.row())  # Получаем номер строки и добавляем в множество

        if len(selected_rows) != 1:
            error_info = Dialog_info('Внимание!', 'Выберите только один аккаунт!', 'notification.mp3')
            error_info.exec_()  # Открываем
            return

        element = next(iter(selected_rows)) # хранит первый элемент из множества

        more_info = Dialog_more_info_account(int(element),self.selected_account_type)
        asyncio.run(more_info.show_info_account()) # выводим данные об аккаунте
        more_info.exec_()  # Открываем

        self.show_accounts_from_db()
        self._update_count_accounts()

    def _enter_account(self):
        if self.selected_account_type == 'login_error':
            error_info = Dialog_info('Внимание!', 'В данные аккаунты невозможно войти!', 'notification.mp3')
            error_info.exec_()  # Открываем
            return

        selected_rows = set()
        for item in self.tableWidget_account.selectedItems():
            selected_rows.add(item.row())  # Получаем номер строки и добавляем в множество

        if len(selected_rows) != 1:
            error_info = Dialog_info('Внимание!', 'Выберите только один аккаунт!', 'notification.mp3')
            error_info.exec_()  # Открываем
            return
        if os.path.exists(self.root_project_dir + '/Telegram Desktop/tdata') and os.path.isdir(self.root_project_dir + '/Telegram Desktop/tdata'): # проверяем есть ли такой путь и есть ли по такому пути папка
            try:
                shutil.rmtree(self.root_project_dir + '/Telegram Desktop/tdata')
            except PermissionError:
                error_info = Dialog_info('Внимание!', 'Невозможно войти в аккаунт!\nФайлы для входа заняты другим процессом\nЗакройте телеграмм который открывали через программу!', 'notification.mp3')
                error_info.exec_()  # Открываем
                return
            except Exception as e:
                error_info = Dialog_info('Внимание!', 'Не удалось войти в аккаунт!', 'notification.mp3')
                error_info.exec_()  # Открываем
                return

        id_folder = next(iter(selected_rows))  # хранит первый элемент из множества

        try:
            # Проверяем, существует ли директория-исходник
            if not os.path.exists(self.root_project_dir + f'/accounts/{self.selected_account_type}_accounts/{id_folder}'): # если нету по указанному пути папки
                error_info = Dialog_info('Внимание!', f'Произошла ошибка!\nПапки с выбранным id = {id_folder} нет.\nУдалите аккаунт под таким id!', 'notification.mp3')
                error_info.exec_()  # Открываем
                return
            else:
                shutil.copytree(self.root_project_dir + f'/accounts/{self.selected_account_type}_accounts/{id_folder}/tdata', self.root_project_dir + '/Telegram Desktop/tdata')# Копируем директорию
        except Exception as e:
            error_info = Dialog_info('Внимание!',f'Произошла ошибка!\nУдалите аккаунт под id = {id_folder}!','notification.mp3')
            error_info.exec_()  # Открываем
            return

        try:
            subprocess.Popen(self.root_project_dir + '/Telegram Desktop/Telegram.exe')# Запускаем исполняемый файл
        except (subprocess.CalledProcessError,Exception )as e:
            error_info = Dialog_info('Внимание!', f'Ошибка при запуске exe файла\n{e}!','notification.mp3')
            error_info.exec_()  # Открываем
            return

    def _upload_tdata(self):
        selected_rows = set()
        for item in self.tableWidget_account.selectedItems():
            selected_rows.add(item.row())  # Получаем номер строки и добавляем в множество

        if len(selected_rows) < 1:
            error_info = Dialog_info('Внимание!', 'Выберите как минимум один аккаунт!', 'notification.mp3')
            error_info.exec_()  # Открываем
            return

        required_ids = [] # хранит необходимые id
        for id in selected_rows:
            required_ids.append(id)

        required_ids = sorted(required_ids)

        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")  # Получаем путь к рабочему столу
        # Открываем диалог выбора папки, начнем с рабочего стола
        # если пользователь выбрал папку, то вернётся путь иначе None
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку", desktop_path)
        name_copy_folder = "folder_with_tdata" # имя папки где будет хранится tdata
        if folder_path:  # если пользователь выбрал путь
            count_folder_copy = 1
            counts = 0
            for id in required_ids:
                try:
                    shutil.copytree(self.root_project_dir + f'/accounts/{self.selected_account_type}_accounts/{id}/tdata', f'{folder_path}/{name_copy_folder}/{counts}/tdata')
                    counts += 1
                except FileExistsError:
                    name_copy_folder = f'folder_with_tdata ({count_folder_copy})'
                    count_folder_copy += 1
                    required_ids.append(id) # добавляем id который не смогли добавить
                except OSError as e:
                    error_info = Dialog_info('Внимание!', f"Ошибка при копировании:\n{e}", 'notification.mp3')
                    error_info.exec_()  # Открываем
                    return

            error_info = Dialog_info('Готово!', f'Выгрузка произошла успешно в:\n{folder_path}/{name_copy_folder}', 'notification.mp3')
            error_info.exec_()  # Открываем

    def _delete_accounts(self):
        selected_rows = set()
        for item in self.tableWidget_account.selectedItems():
            selected_rows.add(item.row())  # Получаем номер строки и добавляем в множество

        if len(selected_rows) < 1:
            error_info = Dialog_info('Внимание!', 'Выберите хотя бы один аккаунт!', 'notification.mp3')
            error_info.exec_()  # Открываем
            return

        Dialog1 = Dialog_yes_or_cancel('Внимание!',
                                          'Вы действительно хотите удалить выбранные аккаунты?',
                                          'notification.mp3')  # Создаем экземпляр
        Dialog1.data_returned.connect(self._start_delete_accounts)  # Подключаем сигнал
        Dialog1.exec_()  # Открываем модальное окно

    def _start_delete_accounts(self, answer: bool):
        if not answer:
            return

        selected_rows = set()
        for item in self.tableWidget_account.selectedItems():
            selected_rows.add(item.row())  # Получаем номер строки и добавляем в множество

        if len(selected_rows) < 1:
            error_info = Dialog_info('Внимание!', 'Выберите хотя бы один аккаунт!', 'notification.mp3')
            error_info.exec_()  # Открываем
            return

        list_id = []
        for row in selected_rows:
            list_id.append(row)

        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')  # в предоваемых параметрах имя БД
        # подключение к бд
        cursor = connection.cursor()
        for id in list_id:
            # удаление по папкам и БД
            try:
                cursor.execute(f'DELETE FROM accounts WHERE id = ? AND account_status = ?',
                               (id, self.selected_account_type))
                connection.commit()  # сохранение
                shutil.rmtree(self.root_project_dir + f'/accounts/{self.selected_account_type}_accounts/{id}')  # Удаляем папку и её содержимое
            except FileNotFoundError:
                list_id.remove(id)
            except Exception:
                pass

        list_id = sorted(list_id, reverse = True)

        for id in list_id:# меняем последовательность id из папки откуда удаляли и из БД
            while True:
                id_result = id
                id += 1
                try:
                    if os.path.isdir( self.root_project_dir + f'/accounts/{self.selected_account_type}_accounts/{id}'):  # если такая папка есть
                        os.rename(self.root_project_dir + f'/accounts/{self.selected_account_type}_accounts/{id}', self.root_project_dir + f'/accounts/{self.selected_account_type}_accounts/{id_result}')  # переименование
                        cursor.execute(f"UPDATE accounts SET id = ?, account_status = ?  WHERE id = ? AND account_status = ?",
                                       (id_result, self.selected_account_type, id, self.selected_account_type))
                        connection.commit()  # меняем в БД значения
                    else:
                        break
                except Exception:
                    pass

        connection.close()
        self.show_accounts_from_db()
        self._update_count_accounts()

    def _on_item_changed(self):
        selected_rows = set()
        for item in self.tableWidget_account.selectedItems():
            selected_rows.add(item.row())
        if len(selected_rows) == 1:
            id_account = next(iter(selected_rows))  # хранит первый элемент из множества
            item = self.tableWidget_account.item(id_account, self.tableWidget_account.columnCount() - 1)

            connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')  # в предоваемых параметрах имя БД
            cursor = connection.cursor()
            cursor.execute(f"UPDATE accounts SET notes = ? WHERE id = ? AND account_status = ?",
                           (item.text(),id_account, self.selected_account_type))
            connection.commit()
            connection.close()

    def _show_error_proxy(self,ip: str,port: str,login: str,password: str):
        error_proxy = Dialog_error_proxy(ip,port,login,password)  # Создаем экземпляр
        error_proxy.show_info()
        error_proxy.exec_()  # Открываем

    def _update_count_accounts(self):
        all_quantity = 0

        folder_path = self.root_project_dir + f'/accounts/active_accounts'
        quantity = self._get_quantity_accounts(folder_path)
        self.label_count_active_account.setText(str(quantity))
        all_quantity += quantity

        folder_path = self.root_project_dir + f'/accounts/archive_accounts'
        quantity = self._get_quantity_accounts(folder_path)
        self.label_count_archive_account.setText(str(quantity))
        all_quantity += quantity

        folder_path = self.root_project_dir + f'/accounts/main_accounts'
        quantity = self._get_quantity_accounts(folder_path)
        self.label_count_main_account.setText(str(quantity))
        all_quantity += quantity

        folder_path = self.root_project_dir + f'/accounts/temporary_ban_accounts'
        quantity = self._get_quantity_accounts(folder_path)
        self.label_count_temporary_banned_account.setText(str(quantity))
        all_quantity += quantity

        folder_path = self.root_project_dir + f'/accounts/login_error_accounts'
        quantity = self._get_quantity_accounts(folder_path)
        self.label_count_login_error.setText(str(quantity))
        all_quantity += quantity
        self.label_count_all_account.setText(str(all_quantity))

    def _get_quantity_accounts(self,folder_path: str) -> int:
        items = os.listdir(folder_path)  # Получаем список файлов и папок в указанной директории
        folder_count = sum(1 for item in items if os.path.isdir(os.path.join(folder_path, item)))  # Фильтруем только папки
        return folder_count

    def _fading_progress_bar(self):
        self.opacity_effect_for_progress_bar = QGraphicsOpacityEffect(self.groupBox_progress)
        self.groupBox_progress.setGraphicsEffect(self.opacity_effect_for_progress_bar)
        self.opacity_effect_for_progress_bar.setOpacity(1.0)  # Устанавливаем начальное значение прозрачности
        self.animation_fading_progress_bar = QPropertyAnimation(self.opacity_effect_for_progress_bar,b"opacity")  # Создаем анимацию прозрачности
        self.animation_fading_progress_bar.setDuration(6000)  # 6 секунды для затухания
        self.animation_fading_progress_bar.setStartValue(1.0)  # Начальное значение (полная видимость)
        self.animation_fading_progress_bar.setEndValue(0.0)  # Конечное значение (полная прозрачность)
        self.animation_fading_progress_bar.finished.connect(self._hide_info_progress_bar)  # Устанавливаем, что по завершении анимации группа будет скрыта
        self.animation_fading_progress_bar.start()  # Запускаем анимацию

    def _hide_info_progress_bar(self):
        self.groupBox_progress.hide()
        self.button_info_open_account.hide()
        self.label_result_open_account.hide()

    def _update_account_data(self, account_data: list):
        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()
        cursor.execute(f"SELECT id_tg,user_name,name,phone,data_time_add,notes,last_used FROM accounts WHERE id = ? AND account_status = ? ",
                       (account_data[0], self.selected_account_type))
        account_from_db = cursor.fetchone()

        if account_from_db[0] != account_data[1]:
            cursor.execute(f"UPDATE accounts SET id_tg = ?  WHERE id = ? AND account_status = ?",
                           (account_data[1], account_data[0], self.selected_account_type))
            connection.commit()  # сохранение
        if account_from_db[1] != account_data[2]:
            cursor.execute(f"UPDATE accounts SET user_name = ?  WHERE id = ? AND account_status = ? ",
                           (account_data[2], account_data[0],self.selected_account_type))
            connection.commit()
        if account_from_db[2] != account_data[3]:
            cursor.execute(f"UPDATE accounts SET name = ?  WHERE id = ? AND account_status = ? ",
                           (account_data[3], account_data[0],self.selected_account_type))
            connection.commit()
        if account_from_db[3] != account_data[5]:
            cursor.execute(f"UPDATE accounts SET phone = ?  WHERE id = ? AND account_status = ? ",
                           (account_data[5], account_data[0], self.selected_account_type))
            connection.commit()
        connection.close()

    def _get_additional_information(self, account_data: list)-> list:
        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT data_time_add,last_used ,notes FROM accounts WHERE id = ? AND account_status = ? ",
            (account_data[0], self.selected_account_type))
        account_from_db = cursor.fetchone()
        connection.close()

        dt_from_db = dt.datetime.strptime(account_from_db[0],'%H:%M %d-%m-%Y')  # первый принимаемый параметр это входная строка с датой, второй это формат даты
        time_difference = dt.datetime.now() - dt_from_db  # Вычисляем разницу во времени
        days_difference = time_difference.days
        resting_place = f"{days_difference} {'день' if days_difference == 1 else 'дня' if 2 <= days_difference <= 4 else 'дней'}"

        return [resting_place, account_from_db[1],account_from_db[2]]


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_13.setText(_translate("MainWindow", "Аккаунты"))
        self.tableWidget_account.setSortingEnabled(True)

        item = self.tableWidget_account.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "#"))
        item = self.tableWidget_account.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "ID"))
        item = self.tableWidget_account.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Юзернейм"))
        item = self.tableWidget_account.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Имя"))
        item = self.tableWidget_account.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", " Гео"))
        item = self.tableWidget_account.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Телефон"))
        item = self.tableWidget_account.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Отлёжка"))
        item = self.tableWidget_account.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Использован"))
        item = self.tableWidget_account.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "Примечания"))
        self.label_account.setText(_translate("MainWindow", "Активные:"))

        self.pushButton_move_active.setText(_translate("MainWindow", "Переместить к \nактивным"))
        self.pushButton_move_main_account.setText(_translate("MainWindow", "Переместить в \nглавные аккаунты"))
        self.pushButton_move_archive.setText(_translate("MainWindow", "Переместить в \nархив"))

        self.pushButton_open_active_accounts.setText(_translate("MainWindow", "Активные аккаунты"))
        self.pushButton_open_arxive_accounts.setText(_translate("MainWindow", "Аккаунты в архиве"))
        self.pushButton_open_main_account.setText(_translate("MainWindow", "Главные аккаунты"))
        self.pushButton_open_temporary_ban_accounts.setText(_translate("MainWindow", "Аккаунты во \nвременном бане"))
        self.pushButton_open_login_error.setText(_translate("MainWindow", "Аккаунты с\nошибкой входа"))
        self.pushButton_add.setText(_translate("MainWindow", "Добавить"))
        self.pushButton_show_data_account.setText(_translate("MainWindow", "Просмотр данных"))
        self.pushButton_enter.setText(_translate("MainWindow", "Войти"))
        self.pushButton_upload_tdata.setText(_translate("MainWindow", "Выгрузить Tdata"))
        self.pushButton_delete.setText(_translate("MainWindow", "Удалить"))
        self.label_count_all_account.setToolTip(
            _translate("MainWindow", "<html><head/><body><p align=\"justify\"><br/></p></body></html>"))
        self.label_count_all_account.setText(_translate("MainWindow", "<html><head/><body><p>1</p></body></html>"))
        self.label.setText(_translate("MainWindow", "Аккаунтов всего"))
        self.label_count_active_account.setText(_translate("MainWindow", "<html><head/><body><p>0</p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "Активных"))
        self.label_count_archive_account.setText(_translate("MainWindow", "<html><head/><body><p>0</p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "В архиве"))
        self.label_count_temporary_banned_account.setText(
            _translate("MainWindow", "<html><head/><body><p>0</p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "Во временном бане"))
        self.label_count_login_error.setText(_translate("MainWindow", "<html><head/><body><p>0</p></body></html>"))
        self.label_7.setText(_translate("MainWindow", "С ошибкой входа"))
        self.label_count_main_account.setText(_translate("MainWindow", "<html><head/><body><p>0</p></body></html>"))
        self.label_10.setText(_translate("MainWindow", "Главные аккаунты"))

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
        self.pushButton_clone.setText(_translate("MainWindow", "   Клонер каналов"))
        self.pushButton_doc.setText(_translate("MainWindow", "   Документация"))
        self.pushButton_settings.setText(_translate("MainWindow", "   Настройки"))
        self.action.setText(_translate("MainWindow", "сохранить"))
        self.action_2.setText(_translate("MainWindow", "добавить"))

def application():
    try:
        app =  QtWidgets.QApplication(sys.argv)
        account = Window_accounts()
        account.show()
        account.start_show_account('active')
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Произошла ошибка при запуске приложения: {e}")

if __name__ == "__main__":
    application()

