import re # для проверки txt файла на правильность записи
import os  # это для действия ниже перед запуском функции
import sys  # информация о системе
import sqlite3
import datetime as dt
import math
import socks
import socket
import time
import asyncio
import aiohttp
from aiohttp_socks import ProxyConnector
import shutil  # для удаления папки
import faulthandler  # для просмотра стека вызовов
import subprocess  # для запуска exe файлов

from opentele.td import TDesktop
from opentele.api import UseCurrentSession
from opentele.exception import TFileNotFound
from telethon import errors

from app.general.info import Dialog_info
from app.general.yes_or_cancel import Dialog_yes_or_cancel
from app.general.check_proxy import check_proxy
from app.general.error_proxy_for_work import Dialog_error_proxy
from app.general.error_handler import get_description_and_solution, error_handler
from app.general.check_html_parse import check_html_parse

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")# 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():# 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path# 3. Установка пути

# 4. Только после этого импортируем PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIntValidator  # для разрешения ввода только цифр в LineEdit
from PyQt5.QtCore import QThread, pyqtSignal, QPropertyAnimation, Qt, QSize
from PyQt5.QtWidgets import QLineEdit,  QSizePolicy, QFileDialog
from PyQt5.QtCore import QTimer

class MailingWithStreams(QThread): # затухание progress_bar
    task_done = pyqtSignal(str, list, bool, list, list, str, list, bool)  # Сигнал, который мы будем использовать для обновления интерфейса
    # вывод в консоль(str), количество успешных и неудачных сообщений(list), ошибка прокси(bool), ошибка(str), конец работы(bool)
    root_project_dir = '..'

    def __init__(self,id_account: int,message: str,user_list: list,time_sleep: int, use_file_for_message: bool,
                 file_path: str, use_proxy: bool,ip: str, port: int, login: str, password: str):
        super().__init__()
        self.id_account = id_account
        self.message = message
        self.user_list = user_list
        self.time_sleep = time_sleep
        self.use_file_for_message = use_file_for_message
        self.file_path = file_path

        self.use_proxy = use_proxy
        self.ip = ip
        self.port = port
        self.login = login
        self.password = password

    def run(self):
        asyncio.run(self.run_2())

    async def run_2(self):
        successful_messages = 0
        failed_messages = 0
        list_accounts_which_sent = []
        me = None
        account_id = None
        last_used = ''

        if self.use_proxy:
            socks.set_default_proxy(socks.SOCKS5, self.ip, self.port, True, self.login, self.password)
            socket.socket = socks.socksocket

        try:  # пытаемся войти в аккаунт
            folder_path_account = self.root_project_dir + f'/accounts/active_accounts/{self.id_account}'  # путь к tdata
            tdesk = TDesktop(folder_path_account + '/tdata')

            client = await tdesk.ToTelethon(session=f"{folder_path_account}/session.session",flag=UseCurrentSession,)

            await asyncio.wait_for(client.connect(), timeout=7)  # вход в аккаунт
            me = await client.get_me()
            account_id = me.id

            self.task_done.emit(f'Запущенна рассылка с аккаунта "{me.username}"',[successful_messages, failed_messages],False,[],[], '', [], False)

            for user in self.user_list:
                while True:# необходимо для предотвращения ошибки если БД была открыта ранее (другим асинхронным потоком)
                    try:
                        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
                        cursor = connection.cursor()
                        cursor.execute(f"SELECT stop_mailing_by_users FROM stop_process", )
                        closure_test = cursor.fetchone()
                        connection.close()
                        break
                    except sqlite3.OperationalError:
                        pass

                if closure_test[0] == 1:  # если необходимо остановить рассылку
                    return

                try:
                    now = dt.datetime.now()  # Получаем время именно тут, т.к. может возникнут ошибка и это тоже считается как использование аккаунта
                    last_used = now.strftime('%H:%M %d-%m-%Y')  # Форматируем дату и время согласно формату

                    if self.use_file_for_message:
                        await client.send_file(user, self.file_path, parse_mode='HTML',caption=self.message)  # отсылка файла
                    else:
                        await client.send_message(user, self.message, parse_mode='HTML')  # отправка сообщения

                    successful_messages += 1
                    list_accounts_which_sent.append(user)

                    await asyncio.sleep(self.time_sleep)
                except FileNotFoundError:  # файл не найден
                    self.task_done.emit('',[successful_messages, failed_messages], False,list_accounts_which_sent, [],
                                        'Ошибка отсылки файла!\nДобавьте новый файл', [], False)
                    return
                except errors.MessageEmptyError:  # Было отправлено пустое или недопустимое сообщение в формате UTF-8.
                    self.task_done.emit('',[successful_messages, failed_messages], False, list_accounts_which_sent, [],
                                        'Ошибка отправки сообщения!\nСообщение в недопустимом формате UTF-8', [], False)
                    return
                except errors.MessageTooLongError:  # сообщение слишком длинное
                    self.task_done.emit('', [successful_messages, failed_messages], False, list_accounts_which_sent, [],
                                        'Ошибка отправки сообщения!\nСообщение слишком длинное.\nМаксимальная длинная = 4096 символов в UTF-8', [], False)
                    return
                except (errors.UserPrivacyRestrictedError, errors.ForbiddenError):  # кому хотим отослать стоит настройка приватности что нельзя отсылать или в чёрном списке
                    list_accounts_which_sent.append(user)
                    failed_messages += 1
                except (ValueError, errors.UsernameInvalidError, errors.InputUserDeactivatedError,
                        errors.YouBlockedUserError, errors.UserIsBlockedError):
                    list_accounts_which_sent.append(user)
                    failed_messages += 1

        except (Exception, TFileNotFound) as e:  # здесь ошибки с аккаунтом откуда отсылаем
            try:
                await client.disconnect()
            except UnboundLocalError:
                pass

            while True:# необходимо для предотвращения ошибки если БД была открыта ранее (другим асинхронным потоком)
                try:
                    connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
                    cursor = connection.cursor()
                    cursor.execute(f"SELECT user_name FROM accounts WHERE id = ? AND account_status = ?",(self.id_account, 'active'))
                    user_name_from_db = cursor.fetchone()  # берём с БД т.к. мы можем даже не войти в аккаунт и тогда не получим его user_name для вывода
                    connection.close()
                    break
                except sqlite3.OperationalError:
                    pass

            error_type = type(e)
            error_description_solution = get_description_and_solution(str(error_type.__name__))
            self.task_done.emit(f'На аккаунте "{user_name_from_db[0]}" произошла ошибка он будет убран из активных.\nОшибка: '
                                f'{error_description_solution[0]}\nОтосланных сообщений: {successful_messages} из {len(self.user_list)}',
                                [successful_messages, failed_messages], True, list_accounts_which_sent, [account_id, last_used],
                                '',[str(error_type.__name__), self.id_account], True)
            return

        self.task_done.emit(f'Аккаунт "{me.username}" закончил рассылку\nОтосланных сообщений: {successful_messages} из {len(self.user_list)}',
            [successful_messages, failed_messages], False, list_accounts_which_sent, [account_id, last_used], '',[], True)
        try:
            await client.disconnect()
        except UnboundLocalError:
            pass
        return

class Mailing_one_stream(QThread): # затухание progress_bar
    task_done = pyqtSignal(str, list,str, bool)  # Сигнал, который мы будем использовать для обновления интерфейса
    # вывод в консоль(str), количество успешных и неудачных сообщений, колличество забаненых аккаунтов(list),
    # ошибка прокси(bool), ошибка(str), конец работы(bool)
    root_project_dir = '..'

    original_socket = socket.socket  # запоминаем какой сокет был до
    error_and_id_errors_accounts = []  # хранит массивы в которых ошибка и id папки, где произошла эта ошибка
    def __init__(self,message: str,user_list: list,time_sleep: int, max_message: int,
                 max_message_per_account: int,use_file_for_message: bool, file_path: str, use_proxy: bool):
        super().__init__()
        self.message = message
        self.user_list = user_list
        self.time_sleep = time_sleep
        self.max_message = max_message
        self.max_message_per_account = max_message_per_account
        self.use_file_for_message = use_file_for_message
        self.file_path = file_path
        self.use_proxy = use_proxy

        self.account_counter = 0 # отображает на каком аккаунте находится программа (это будет id папки)
        self.successful_messages = 0
        self.failed_messages = 0
        self.banned_accounts = 0

    def run(self):
        while True:
            if os.path.isdir(self.root_project_dir + f'/accounts/active_accounts/{self.account_counter}'):  # если аккаунт есть
                result = asyncio.run(self.mailing(self.use_proxy,self.user_list))
                if result[0]:
                    self.user_list = [item for item in self.user_list if item not in result[0]]
                    # удаление элементов которые есть в вернувшемся списке из списка с аккаунтами

                if result[1]:
                    try:
                        # Открываем файл в режиме записи (режим 'w' очищает файл перед записью)
                        with open(self.root_project_dir + '/working_files/user_names_for_mailing.txt', 'w', encoding='utf-8') as file:
                            # Записываем данные из списка, разделяя их переводом на новую строку
                            file.write('\n'.join(self.user_list))  # объединяем все строки из списка в одну строку
                    except Exception:
                        pass

                    if self.error_and_id_errors_accounts:  # работаем с аккаунтами в которые не смогли войти
                        sorted_list = sorted(self.error_and_id_errors_accounts, key=lambda x: x[1], reverse=True)
                        for error_and_id in sorted_list:
                            error_handler(error_and_id[0], error_and_id[1], 'active')

                    return
            else:
                self.task_done.emit('',[self.successful_messages, self.failed_messages, self.banned_accounts], 'Рассылка остановлена\nАккаунты закончились!', False)
                try:
                    # Открываем файл в режиме записи (режим 'w' очищает файл перед записью)
                    with open(self.root_project_dir + '/working_files/user_names_for_mailing.txt', 'w', encoding='utf-8') as file:
                        # Записываем данные из списка, разделяя их переводом на новую строку
                        file.write('\n'.join(self.user_list))  # объединяем все строки из списка в одну строку
                except Exception:
                    pass
                if self.error_and_id_errors_accounts:  # работаем с аккаунтами в которые не смогли войти
                    sorted_list = sorted(self.error_and_id_errors_accounts, key=lambda x: x[1], reverse=True)
                    for error_and_id in sorted_list:
                        error_handler(error_and_id[0], error_and_id[1], 'active')
                return
            self.account_counter += 1

    async def mailing(self, proxy: bool, users_list: list) -> list: # 1 параметр это список юзеров по которым отработали,
                                                                    # второй это bool переменная если True, то надо завершить рассылку
        list_accounts_which_sent = []
        me = None
        messages_from_this_account = 0

        if proxy: # подключение к прокси если необходимо
            connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
            cursor = connection.cursor()
            cursor.execute(f"SELECT ip,port,login,password FROM proxy")
            proxy_from_db = cursor.fetchone()
            connection.close()
            socks.set_default_proxy(socks.SOCKS5, proxy_from_db[0], proxy_from_db[1], True, proxy_from_db[2],proxy_from_db[3])  # Установка прокси-соединения
            socket.socket = socks.socksocket

        try:  # пытаемся войти в аккаунт
            folder_path_account = self.root_project_dir + f'/accounts/active_accounts/{self.account_counter}'  # путь к tdata
            tdesk = TDesktop(folder_path_account + '/tdata')
            client = await tdesk.ToTelethon(session = f"{folder_path_account}/session.session",flag = UseCurrentSession)
            await asyncio.wait_for(client.connect(), timeout = 7)  # вход в аккаунт

            me = await client.get_me()
            test_id = me.id # Здесь может возникнуть ошибка, это будет означать, что аккаунт недействителен

            self.task_done.emit(f'Успешно вошли в аккаунт "{me.username}"',[self.successful_messages, self.failed_messages, self.banned_accounts], '', False)

            for user in users_list:
                connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
                cursor = connection.cursor()
                cursor.execute(f"SELECT stop_mailing_by_users FROM stop_process",)
                closure_test = cursor.fetchone()
                connection.close()
                if closure_test[0] == 1:  # если необходимо остановить рассылку
                    connection.close()
                    socket.socket = self.original_socket
                    return [list_accounts_which_sent, True]

                try:
                    if self.use_file_for_message:
                        await client.send_file(user, self.file_path, parse_mode = 'HTML',caption = self.message)  # отсылка файла
                    else:
                        await client.send_message(user, self.message, parse_mode = 'HTML')  # отправка сообщения

                    self.successful_messages += 1
                    messages_from_this_account += 1
                    list_accounts_which_sent.append(user)
                    self.task_done.emit(f'Успешно отослано сообщение для "{user}"',
                                        [self.successful_messages, self.failed_messages, self.banned_accounts],'',False)

                    now = dt.datetime.now()  # Получаем время именно тут, т.к. может возникнут ошибка и это тоже
                                            # считается как использование аккаунта
                    last_used = now.strftime('%H:%M %d-%m-%Y')  # Форматируем дату и время согласно формату

                    connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
                    cursor = connection.cursor()
                    cursor.execute(f"UPDATE accounts SET last_used = ? WHERE id_tg = ?", (last_used, me.id))
                    connection.commit()
                    connection.close()

                    if self.successful_messages >= self.max_message:
                        socket.socket = self.original_socket
                        self.task_done.emit(f'Достигнут лимит сообщений',
                                            [self.successful_messages, self.failed_messages, self.banned_accounts], '', True)
                        return [list_accounts_which_sent, True]

                    if messages_from_this_account >= self.max_message_per_account: # если превысили количество сообщений с одного аккаунта
                        socket.socket = self.original_socket
                        self.task_done.emit(f'Достигнут лимит сообщений с одного аккаунта. Аккаунт: {me.username}',
                                            [self.successful_messages, self.failed_messages, self.banned_accounts], '', False)
                        return [list_accounts_which_sent, False]

                    await asyncio.sleep(self.time_sleep)
                except FileNotFoundError: # файл не найден
                    socket.socket = self.original_socket
                    self.task_done.emit('', [], False,'Рассылка не начата!\nОшибка отсылки файла!\nДобавьте новый файл')
                    return [list_accounts_which_sent,True]
                except errors.MessageEmptyError:# Было отправлено пустое или недопустимое сообщение в формате UTF-8.
                    socket.socket = self.original_socket
                    self.task_done.emit('', [], False,'Рассылка не начата!\nОшибка отправки сообщения!\nСообщение в недопустимом формате UTF-8')
                    return [list_accounts_which_sent, True]
                except errors.MessageTooLongError:# сообщение слишком длинное
                    socket.socket = self.original_socket
                    self.task_done.emit('', [], 'Рассылка не начата!\nОшибка отправки сообщения!\nСообщение слишком длинное.'
                                                '\nМаксимальная длинная = 4096 символов в UTF-8', False)
                    return [list_accounts_which_sent, True]
                except (errors.UserPrivacyRestrictedError, errors.ForbiddenError): # кому хотим отослать стоит настройка приватности что нельзя отсылать
                    list_accounts_which_sent.append(user)
                    self.failed_messages += 1
                    self.task_done.emit(f'аккаунту "{user}" нельзя отослать сообщение из-за настроек приватности',
                                        [self.successful_messages, self.failed_messages, self.banned_accounts],'',False)
                except (ValueError, errors.UsernameInvalidError,errors.InputUserDeactivatedError, errors.PeerIdInvalidError,
                        errors.YouBlockedUserError, errors.UserIsBlockedError):
                    list_accounts_which_sent.append(user)
                    self.failed_messages += 1
                    self.task_done.emit(f'пользователь с таким юзернеймом "{user}" не найден',
                                        [self.successful_messages, self.failed_messages, self.banned_accounts], '', False)


        except (Exception, TFileNotFound) as e:  # здесь ошибки с аккаунтом откуда отсылаем
            socket.socket = self.original_socket
            self.banned_accounts += 1
            try:
                await client.disconnect()
            except UnboundLocalError:
                pass
            connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
            cursor = connection.cursor()
            cursor.execute(f"SELECT user_name FROM accounts WHERE id = ? AND account_status = ?",(self.account_counter,'active'))
            user_name_from_db = cursor.fetchone() # берём с БД т.к. мы можем даже не войти в аккаунт и тогда не получим его user_name для вывода
            connection.close()

            error_type = type(e)
            error_description_solution = get_description_and_solution(str(error_type.__name__))
            self.task_done.emit(f'На аккаунте "{user_name_from_db[0]}" произошла ошибка он будет сменён.\nОшибка: {error_description_solution[0]}',
                                [self.successful_messages, self.failed_messages, self.banned_accounts], '', False)
            self.error_and_id_errors_accounts.append([str(error_type.__name__), self.account_counter])
            return [list_accounts_which_sent, False]

        self.task_done.emit(f'',[self.successful_messages, self.failed_messages, self.banned_accounts],
                            'Рассылка остановлена!\nСписок пользователей для рассылки закончился', False)
        try:
            await client.disconnect()
        except UnboundLocalError:
            pass
        connection.close()
        socket.socket = self.original_socket
        return  [list_accounts_which_sent, True]

class Window_mailing_by_users(QtWidgets.QMainWindow):
    root_project_dir = '..'

    mailing_start = False # отображает запущенна ли рассылка
    file_path_for_mailing = '' # путь к файлу для рассылки
    def __init__(self,switch_window):
        super().__init__()
        self.switch_window = switch_window

        self.active_threads = []  # ВАЖНО! хранит в себе запущенные потоки

        # для многопоточной рассылки
        self.original_socket = socket.socket
        self.id_and_last_use = [] # хранит массивы в которых tg_id аккаунта и его последнее использование
        self.user_name_list_to = [] # список user_names для рассылки до того как проводили с ним махинации
        self.quantity_accounts_for_mailing = 0 # количество аккаунтов для рассылки
        self.quantity_accounts_ending_mailing = 0 # количество аккаунтов закончивших рассылку
        self.error_and_id_errors_accounts = []  # хранит массивы в которых ошибка и id папки, где произошла эта ошибка
        # для многопоточной рассылки

        self.quantity_remaining_message = 0 # количество всех аккаунтов которые остались для рассылки
        self.count_attempts = 0 # количество попыток отправить сообщение

        # удаление ненужных файлов
        items = os.listdir(self.root_project_dir + '/working_files/file_from_user')# Получаем список всех файлов и папок в указанной директории
        for item in items:
            file_path = os.path.join(self.root_project_dir + '/working_files/file_from_user', item)
            if os.path.isfile(file_path):  # Проверяем, является ли элемент файлом
                os.remove(file_path)  # Удаляем файл

        if not os.path.isfile(self.root_project_dir + '/working_files/user_names_for_mailing.txt'): # если файл с user_names_for_mailing.txt не существует
            with open(self.root_project_dir + '/working_files/user_names_for_mailing.txt', 'w') as file:# Создаем файл в режиме записи (если файл существует, он будет перезаписан)
                file.write("")  # Записываем пустую строку, чтобы создать файл

        self.setObjectName("MainWindow")
        self.resize(1500, 850)
        self.setMinimumSize(QtCore.QSize(1200, 750))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.setFont(font)
        self.setStyleSheet("background-color: rgb(236, 237, 240);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_12.setContentsMargins(0, 0, 20, 0)
        self.gridLayout_12.setObjectName("gridLayout_12")
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
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 268, 848))
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
        icon.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/logo.PNG"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
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
        icon1.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/account.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
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
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/mailing.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
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
        icon3.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/invaite.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
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
        icon4.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/parser.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
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
        icon5.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/proxy.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
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
        icon6.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/bomber.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
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
        icon7.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/enter_the_group.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
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
        icon8.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/like.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
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
        icon9.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/coment.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
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
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/convert.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        self.pushButton_convert.setIcon(icon10)
        self.pushButton_convert.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_convert.setObjectName("pushButton_convert")
        self.verticalLayout.addWidget(self.pushButton_convert)

        self.pushButton_clone = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
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
        icon11.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/clone.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        self.pushButton_clone.setIcon(icon11)
        self.pushButton_clone.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_clone.setObjectName("pushButton_clone")
        self.verticalLayout.addWidget(self.pushButton_clone)

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
        icon11.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/doc.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        self.pushButton_doc.setIcon(icon11)
        self.pushButton_doc.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_doc.setObjectName("pushButton_doc")
        self.verticalLayout.addWidget(self.pushButton_doc)

        self.pushButton_setting = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_setting.sizePolicy().hasHeightForWidth())
        self.pushButton_setting.setSizePolicy(sizePolicy)
        self.pushButton_setting.setMinimumSize(QtCore.QSize(185, 0))
        self.pushButton_setting.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_setting.setFont(font)
        self.pushButton_setting.setStyleSheet("QPushButton {\n"
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
        icon11.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/settings.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        self.pushButton_setting.setIcon(icon11)
        self.pushButton_setting.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_setting.setObjectName("pushButton_setting")
        self.verticalLayout.addWidget(self.pushButton_setting)

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
        self.gridLayout_12.addWidget(self.scrollArea_3, 0, 0, 4, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(27, 10, -1, 10)
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
        icon12.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/icon/info.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
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
        self.gridLayout_12.addLayout(self.horizontalLayout, 0, 1, 1, 3)
        self.scrollArea_2 = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_2.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea_2.setStyleSheet("border: 0;")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 572, 385))
        self.scrollAreaWidgetContents_2.setStyleSheet("/* СТИЛЬ ВЕРТИКАЛЬНОГО СКРОЛЛБАРА */"
                                                        "QScrollBar:vertical {"
                                                        "    border-radius: 8px;"
                                                        "    background: rgb(210, 210, 213);"
                                                        "    width: 14px;"
                                                        "    margin: 0px 0 0px 0;"
                                                        "}"
                                                        ""
                                                        "/* HANDLE BAR ВЕРТИКАЛЬНОГО СКРОЛЛБАРА */"
                                                        "QScrollBar::handle:vertical {"
                                                        "    background-color: rgb(210, 210, 213);"
                                                        "    min-height: 30px;"
                                                        "    border-radius: 0px;"
                                                        "    transition: background-color 0.2s ease;"
                                                        "}"
                                                        ""
                                                        "QScrollBar::handle:vertical:hover {"
                                                        "    background-color: rgb(180, 180, 184);"
                                                        "}"
                                                        ""
                                                        "QScrollBar::handle:vertical:pressed {"
                                                        "    background-color: rgb(150, 150, 153);"
                                                        "}"
                                                        ""
                                                        "/* КНОПКА ВВЕРХУ - ВЕРТИКАЛЬНЫЙ СКРОЛЛБАР */"
                                                        "QScrollBar::sub-line:vertical {"
                                                        "    border: none;"
                                                        "    background-color: rgb(190, 190, 193);"
                                                        "    height: 15px;"
                                                        "    border-top-left-radius: 7px;"
                                                        "    border-top-right-radius: 7px;"
                                                        "    subcontrol-position: top;"
                                                        "    subcontrol-origin: margin;"
                                                        "}"
                                                        ""
                                                        "QScrollBar::sub-line:vertical:hover {"
                                                        "    background-color: rgb(170, 170, 174);"
                                                        "}"
                                                        ""
                                                        "QScrollBar::sub-line:vertical:pressed {"
                                                        "    background-color: rgb(140, 140, 143);"
                                                        "}"
                                                        ""
                                                        "/* КНОПКА ВНИЗУ - ВЕРТИКАЛЬНЫЙ СКРОЛЛБАР */"
                                                        "QScrollBar::add-line:vertical {"
                                                        "    border: none;"
                                                        "    background-color: rgb(190, 190, 193);"
                                                        "    height: 15px;"
                                                        "    border-bottom-left-radius: 7px;"
                                                        "    border-bottom-right-radius: 7px;"
                                                        "    subcontrol-position: bottom;"
                                                        "    subcontrol-origin: margin;"
                                                        "}"
                                                        ""
                                                        "QScrollBar::add-line:vertical:hover {"
                                                        "    background-color: rgb(170, 170, 174);"
                                                        "}"
                                                        ""
                                                        "QScrollBar::add-line:vertical:pressed {"
                                                        "    background-color: rgb(140, 140, 143);"
                                                        "}"
                                                        ""
                                                        "/* УБРАТЬ СТРЕЛКИ */"
                                                        "QScrollBar::up-arrow:vertical,"
                                                        "QScrollBar::down-arrow:vertical {"
                                                        "    background: none;"
                                                        "}"
                                                        ""
                                                        "/* УБРАТЬ ФОН */"
                                                        "QScrollBar::add-page:vertical,"
                                                        "QScrollBar::sub-page:vertical {"
                                                        "    background: none;"
                                                        "}")
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setContentsMargins(20, -1, 40, -1)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_6 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("")
        self.label_6.setObjectName("label_6")
        self.gridLayout_7.addWidget(self.label_6, 0, 0, 1, 1)
        self.scrollArea_4 = QtWidgets.QScrollArea(self.scrollAreaWidgetContents_2)
        self.scrollArea_4.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea_4.setStyleSheet("border: 0;")
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollArea_4.setObjectName("scrollArea_4")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 532, 343))
        self.scrollAreaWidgetContents_4.setStyleSheet("/* СТИЛЬ ВЕРТИКАЛЬНОГО СКРОЛЛБАРА */"
                                                        "QScrollBar:vertical {"
                                                        "    border-radius: 8px;"
                                                        "    background: rgb(210, 210, 213);"
                                                        "    width: 14px;"
                                                        "    margin: 0px 0 0px 0;"
                                                        "}"
                                                        ""
                                                        "/* HANDLE BAR ВЕРТИКАЛЬНОГО СКРОЛЛБАРА */"
                                                        "QScrollBar::handle:vertical {"
                                                        "    background-color: rgb(210, 210, 213);"
                                                        "    min-height: 30px;"
                                                        "    border-radius: 0px;"
                                                        "    transition: background-color 0.2s ease;"
                                                        "}"
                                                        ""
                                                        "QScrollBar::handle:vertical:hover {"
                                                        "    background-color: rgb(180, 180, 184);"
                                                        "}"
                                                        ""
                                                        "QScrollBar::handle:vertical:pressed {"
                                                        "    background-color: rgb(150, 150, 153);"
                                                        "}"
                                                        ""
                                                        "/* КНОПКА ВВЕРХУ - ВЕРТИКАЛЬНЫЙ СКРОЛЛБАР */"
                                                        "QScrollBar::sub-line:vertical {"
                                                        "    border: none;"
                                                        "    background-color: rgb(190, 190, 193);"
                                                        "    height: 15px;"
                                                        "    border-top-left-radius: 7px;"
                                                        "    border-top-right-radius: 7px;"
                                                        "    subcontrol-position: top;"
                                                        "    subcontrol-origin: margin;"
                                                        "}"
                                                        ""
                                                        "QScrollBar::sub-line:vertical:hover {"
                                                        "    background-color: rgb(170, 170, 174);"
                                                        "}"
                                                        ""
                                                        "QScrollBar::sub-line:vertical:pressed {"
                                                        "    background-color: rgb(140, 140, 143);"
                                                        "}"
                                                        ""
                                                        "/* КНОПКА ВНИЗУ - ВЕРТИКАЛЬНЫЙ СКРОЛЛБАР */"
                                                        "QScrollBar::add-line:vertical {"
                                                        "    border: none;"
                                                        "    background-color: rgb(190, 190, 193);"
                                                        "    height: 15px;"
                                                        "    border-bottom-left-radius: 7px;"
                                                        "    border-bottom-right-radius: 7px;"
                                                        "    subcontrol-position: bottom;"
                                                        "    subcontrol-origin: margin;"
                                                        "}"
                                                        ""
                                                        "QScrollBar::add-line:vertical:hover {"
                                                        "    background-color: rgb(170, 170, 174);"
                                                        "}"
                                                        ""
                                                        "QScrollBar::add-line:vertical:pressed {"
                                                        "    background-color: rgb(140, 140, 143);"
                                                        "}"
                                                        ""
                                                        "/* УБРАТЬ СТРЕЛКИ */"
                                                        "QScrollBar::up-arrow:vertical,"
                                                        "QScrollBar::down-arrow:vertical {"
                                                        "    background: none;"
                                                        "}"
                                                        ""
                                                        "/* УБРАТЬ ФОН */"
                                                        "QScrollBar::add-page:vertical,"
                                                        "QScrollBar::sub-page:vertical {"
                                                        "    background: none;"
                                                        "}")
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_4)
        self.gridLayout_5.setContentsMargins(-1, -1, -1, 10)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_10 = QtWidgets.QGridLayout()
        self.gridLayout_10.setContentsMargins(0, -1, -1, -1)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.textEdit_message = QtWidgets.QTextEdit(self.scrollAreaWidgetContents_4)
        self.textEdit_message.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.textEdit_message.setFont(font)
        self.textEdit_message.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                            "border-radius: 20px;\n"
                                            "padding-top: 15px; /* Отступ только слева */   \n"
                                            " padding-bottom: 15px; /* Отступ только снизу */\n"
                                            "")
        self.textEdit_message.setReadOnly(False)
        self.textEdit_message.setObjectName("textEdit_message")
        self.gridLayout_10.addWidget(self.textEdit_message, 0, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_10, 1, 0, 1, 1)
        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)
        self.gridLayout_7.addWidget(self.scrollArea_4, 1, 0, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_7, 2, 0, 1, 1)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout_12.addWidget(self.scrollArea_2, 1, 1, 1, 1)
        self.gridLayout_11 = QtWidgets.QGridLayout()
        self.gridLayout_11.setContentsMargins(-1, 40, -1, 10)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "border-radius: 20px;")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout.setContentsMargins(25, 10, -1, 20)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_choose_file_for_mailing = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_choose_file_for_mailing.setMaximumSize(QtCore.QSize(70, 35))
        self.pushButton_choose_file_for_mailing.setMinimumSize(QtCore.QSize(0, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        font.setPointSize(10)
        self.pushButton_choose_file_for_mailing.setFont(font)
        self.pushButton_choose_file_for_mailing.setStyleSheet("QPushButton {\n"
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
        self.pushButton_choose_file_for_mailing.setObjectName("pushButton_choose_file_for_mailing")
        self.gridLayout.addWidget(self.pushButton_choose_file_for_mailing, 5, 1, 1, 1)
        self.checkBox_use_file_for_message = QtWidgets.QCheckBox(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.checkBox_use_file_for_message.setFont(font)
        self.checkBox_use_file_for_message.setStyleSheet("\n"
                                                         "QCheckBox {\n"
                                                         "color: rgb(0, 0, 0);\n"
                                                         "    spacing: 5px; /* Отступ между иконкой и текстом */\n"
                                                         "\n"
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
                                                         "QCheckBox::indicator:checked:hover {\n"
                                                         "    background-color: rgb(180, 230, 180); \n"
                                                         "}")
        self.checkBox_use_file_for_message.setObjectName("checkBox_use_file_for_message")
        self.gridLayout.addWidget(self.checkBox_use_file_for_message, 5, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("")
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.lineEdit_delay = QtWidgets.QLineEdit(self.groupBox_2)
        validator = QIntValidator(0, 99999)  # Минимум 0, максимум большое число
        self.lineEdit_delay.setValidator(validator)
        self.lineEdit_delay.setMaximumSize(QtCore.QSize(70, 16777215))
        self.lineEdit_delay.setMaxLength(5)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lineEdit_delay.setFont(font)
        self.lineEdit_delay.setStyleSheet("QLineEdit {\n"
                                          "    background-color: rgb(255, 255, 255);      /* Цвет фона текстового поля */\n"
                                          "    border: 2px solid rgb(150, 150, 150); /* Рамка текстового поля */\n"
                                          "    border-radius: 10px; /* Закругление углов */\n"
                                          "    padding: 2px; /* Отступы внутри текстового поля */\n"
                                          "    color: rgb(50, 50, 50); /* Цвет текста */\n"
                                          "}\n"
                                          "\n"
                                          "/* Состояние при наведении */\n"
                                          "QLineEdit:hover {\n"
                                          "    border: 2px solid rgb(160, 160, 160); /* Цвет рамки при наведении */\n"
                                          "}\n"
                                          "\n"
                                          "/* Состояние при фокусировке */\n"
                                          "QLineEdit:focus {\n"
                                          "    border: 2px solid rgb(0, 0, 0); /* Цвет рамки при фокусировке */\n"
                                          "    background-color: rgb(255, 255, 255); /* Цвет фона при фокусировке */\n"
                                          "}\n"
                                          "/* Состояние для отключенного текстового поля */\n"
                                          "QLineEdit:disabled {\n"
                                          "    background-color: rgb(220, 220, 220); /* Цвет фона для отключенного */\n"
                                          "    color: rgb(170, 170, 170); /* Цвет текста для отключенного */\n"
                                          "    border: 2px solid rgb(200, 200, 200); /* Цвет рамки для отключенного */\n"
                                          "}")
        self.lineEdit_delay.setObjectName("lineEdit_delay")
        self.gridLayout.addWidget(self.lineEdit_delay, 2, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_7.setFont(font)
        self.label_7.setMouseTracking(True)
        self.label_7.setStyleSheet("")
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 2, 0, 1, 1)
        self.lineEdit_max_message = QtWidgets.QLineEdit(self.groupBox_2)
        validator = QIntValidator(1, 99999)  # Минимум 0, максимум большое число
        self.lineEdit_max_message.setValidator(validator)
        self.lineEdit_max_message.setMaximumSize(QtCore.QSize(70, 16777215))
        self.lineEdit_max_message.setMaxLength(5)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lineEdit_max_message.setFont(font)
        self.lineEdit_max_message.setStyleSheet("QLineEdit {\n"
                                                "    background-color: rgb(255, 255, 255);      /* Цвет фона текстового поля */\n"
                                                "    border: 2px solid rgb(150, 150, 150); /* Рамка текстового поля */\n"
                                                "    border-radius: 10px; /* Закругление углов */\n"
                                                "    padding: 2px; /* Отступы внутри текстового поля */\n"
                                                "    color: rgb(50, 50, 50); /* Цвет текста */\n"
                                                "}\n"
                                                "\n"
                                                "/* Состояние при наведении */\n"
                                                "QLineEdit:hover {\n"
                                                "    border: 2px solid rgb(160, 160, 160); /* Цвет рамки при наведении */\n"
                                                "}\n"
                                                "/* Состояние при фокусировке */\n"
                                                "QLineEdit:focus {\n"
                                                "    border: 2px solid rgb(0, 0, 0); /* Цвет рамки при фокусировке */\n"
                                                "    background-color: rgb(255, 255, 255); /* Цвет фона при фокусировке */\n"
                                                "}\n"
                                                "/* Состояние для отключенного текстового поля */\n"
                                                "QLineEdit:disabled {\n"
                                                "    background-color: rgb(220, 220, 220); /* Цвет фона для отключенного */\n"
                                                "    color: rgb(170, 170, 170); /* Цвет текста для отключенного */\n"
                                                "    border: 2px solid rgb(200, 200, 200); /* Цвет рамки для отключенного */\n"
                                                "}")
        self.lineEdit_max_message.setObjectName("lineEdit_max_message")
        self.gridLayout.addWidget(self.lineEdit_max_message, 3, 1, 1, 1)
        self.checkBox_use_proxy = QtWidgets.QCheckBox(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.checkBox_use_proxy.setFont(font)
        self.checkBox_use_proxy.setStyleSheet("\n"
                                              "QCheckBox {\n"
                                              "color: rgb(0, 0, 0);\n"
                                              "    spacing: 5px; /* Отступ между иконкой и текстом */\n"
                                              "\n"
                                              "}\n"
                                              "QCheckBox::indicator {\n"
                                              "    width: 15px; /* Ширина индикатора (чекбокса) */\n"
                                              "    height: 15px; /* Высота индикатора (чекбокса) */\n"
                                              "    border: 2px solid rgb(150, 150, 150); /* Обводка чекбокса */\n"
                                              "    border-radius: 4px; /* Закругление углов */\n"
                                              "    background-color: white; /* Цвет фона чекбокса */\n"
                                              "}\n"
                                              "QCheckBox::indicator:checked {\n"
                                              "    background-color: rgb(150, 200, 150); \n"
                                              "    border: 2px solid rgb(150, 150, 150); \n"
                                              "}\n"
                                              "\n"
                                              "\n"
                                              "QCheckBox::indicator:checked:hover {\n"
                                              "    background-color: rgb(180, 230, 180); \n"
                                              "}")
        self.checkBox_use_proxy.setObjectName("checkBox_use_proxy")
        self.gridLayout.addWidget(self.checkBox_use_proxy, 7, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_12.setFont(font)
        self.label_12.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_12.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 4, 0, 1, 1)
        self.lineEdit_max_message_from_one_account = QtWidgets.QLineEdit(self.groupBox_2)
        validator = QIntValidator(1, 99999)  # Минимум 0, максимум большое число
        self.lineEdit_max_message_from_one_account.setValidator(validator)
        self.lineEdit_max_message_from_one_account.setMaximumSize(QtCore.QSize(70, 16777215))
        self.lineEdit_max_message_from_one_account.setMaxLength(5)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lineEdit_max_message_from_one_account.setFont(font)
        self.lineEdit_max_message_from_one_account.setStyleSheet("QLineEdit {\n"
                                                                 "    background-color: rgb(255, 255, 255);      /* Цвет фона текстового поля */\n"
                                                                 "    border: 2px solid rgb(150, 150, 150); /* Рамка текстового поля */\n"
                                                                 "    border-radius: 10px; /* Закругление углов */\n"
                                                                 "    padding: 2px; /* Отступы внутри текстового поля */\n"
                                                                 "    color: rgb(50, 50, 50); /* Цвет текста */\n"
                                                                 "}\n"
                                                                 "\n"
                                                                 "/* Состояние при наведении */\n"
                                                                 "QLineEdit:hover {\n"
                                                                 "    border: 2px solid rgb(160, 160, 160); /* Цвет рамки при наведении */\n"
                                                                 "}\n"
                                                                 "\n"
                                                                 "/* Состояние при фокусировке */\n"
                                                                 "QLineEdit:focus {\n"
                                                                 "    border: 2px solid rgb(0, 0, 0); /* Цвет рамки при фокусировке */\n"
                                                                 "    background-color: rgb(255, 255, 255); /* Цвет фона при фокусировке */\n"
                                                                 "}\n"
                                                                 "\n"
                                                                 "/* Состояние для отключенного текстового поля */\n"
                                                                 "QLineEdit:disabled {\n"
                                                                 "    background-color: rgb(220, 220, 220); /* Цвет фона для отключенного */\n"
                                                                 "    color: rgb(170, 170, 170); /* Цвет текста для отключенного */\n"
                                                                 "    border: 2px solid rgb(200, 200, 200); /* Цвет рамки для отключенного */\n"
                                                                 "}")
        self.lineEdit_max_message_from_one_account.setObjectName("lineEdit_max_message_from_one_account")
        self.gridLayout.addWidget(self.lineEdit_max_message_from_one_account, 4, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setStyleSheet("")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.pushButton_check_user_name = QtWidgets.QPushButton(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_check_user_name.sizePolicy().hasHeightForWidth())
        self.pushButton_check_user_name.setSizePolicy(sizePolicy)
        self.pushButton_check_user_name.setMinimumSize(QtCore.QSize(0, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_check_user_name.setFont(font)
        self.pushButton_check_user_name.setStyleSheet("QPushButton {\n"
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
                                                     "            }\n"
                                                     "")
        self.pushButton_check_user_name.setObjectName("pushButton_check_user_name")
        self.gridLayout.addWidget(self.pushButton_check_user_name, 1, 1, 1, 1)
        self.gridLayout_11.addWidget(self.groupBox_2, 0, 0, 1, 1)
        self.gridLayout_12.addLayout(self.gridLayout_11, 1, 2, 1, 2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(20, 10, 10, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setStyleSheet("border: 0;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 818, 384))
        self.scrollAreaWidgetContents.setStyleSheet("/* СТИЛЬ ВЕРТИКАЛЬНОГО СКРОЛЛБАРА */\n"
                                                    "QScrollBar:vertical {\n"
                                                    "    border-radius: 8px; /* Закругление углов */\n"
                                                    "    background: rgb(210, 210, 213); /* Стандартный цвет фона */\n"
                                                    "    width: 14px; /* Ширина скроллбара */\n"
                                                    "    margin: 0px 0 0px 0;\n"
                                                    "}\n"
                                                    "\n"
                                                    "/* HANDLE BAR ВЕРТИКАЛЬНОГО СКРОЛЛБАРА */\n"
                                                    "QScrollBar::handle:vertical {  \n"
                                                    "    background-color: rgb(210, 210, 213); /* Стандартный цвет фона для ползунка */\n"
                                                    "    min-height: 30px; /* Минимальная высота ползунка */\n"
                                                    "    border-radius: 7px; /* Закругление углов ползунка */\n"
                                                    "    transition: background-color 0.2s ease; /* Плавный переход цвета */\n"
                                                    "}\n"
                                                    "\n"
                                                    "QScrollBar::handle:vertical:hover {  \n"
                                                    "    background-color: rgb(180, 180, 184); /* Цвет ползунка при наведении */\n"
                                                    "}\n"
                                                    "\n"
                                                    "QScrollBar::handle:vertical:pressed {  \n"
                                                    "    background-color: rgb(150, 150, 153); /* Цвет ползунка при нажатии */\n"
                                                    "}\n"
                                                    "\n"
                                                    "/* КНОПКА ВВЕРХУ - ВЕРТИКАЛЬНЫЙ СКРОЛЛБАР */\n"
                                                    "QScrollBar::sub-line:vertical {\n"
                                                    "    border: none;  \n"
                                                    "    background-color: rgb(210, 210, 213); /* Стандартный цвет фона для кнопки вверх */\n"
                                                    "    height: 15px; /* Высота кнопки */\n"
                                                    "    border-top-left-radius: 7px; /* Закругление верхних углов */\n"
                                                    "    border-top-right-radius: 7px; /* Закругление верхних углов */\n"
                                                    "    subcontrol-position: top; /* Позиция кнопки */\n"
                                                    "    subcontrol-origin: margin; /* Происхождение позиции кнопки */\n"
                                                    "}\n"
                                                    "\n"
                                                    "QScrollBar::sub-line:vertical:hover {  \n"
                                                    "    background-color: rgb(180, 180, 184); /* Цвет кнопки вверх при наведении */\n"
                                                    "}\n"
                                                    "\n"
                                                    "QScrollBar::sub-line:vertical:pressed {  \n"
                                                    "    background-color: rgb(150, 150, 153); /* Цвет кнопки вверх при нажатии */\n"
                                                    "}\n"
                                                    "\n"
                                                    "/* КНОПКА ВНИЗУ - ВЕРТИКАЛЬНЫЙ СКРОЛЛБАР */\n"
                                                    "QScrollBar::add-line:vertical {\n"
                                                    "    border: none;  \n"
                                                    "    background-color: rgb(210, 210, 213); /* Стандартный цвет фона для кнопки вниз */\n"
                                                    "    height: 15px; /* Высота кнопки */\n"
                                                    "    border-bottom-left-radius: 7px; /* Закругление нижних углов */\n"
                                                    "    border-bottom-right-radius: 7px; /* Закругление нижних углов */\n"
                                                    "    subcontrol-position: bottom; /* Позиция кнопки */\n"
                                                    "    subcontrol-origin: margin; /* Происхождение позиции кнопки */\n"
                                                    "}\n"
                                                    "\n"
                                                    "QScrollBar::add-line:vertical:hover {  \n"
                                                    "    background-color: rgb(180, 180, 184); /* Цвет кнопки вниз при наведении */\n"
                                                    "}\n"
                                                    "\n"
                                                    "QScrollBar::add-line:vertical:pressed {  \n"
                                                    "    background-color: rgb(150, 150, 153); /* Цвет кнопки вниз при нажатии */\n"
                                                    "}\n"
                                                    "\n"
                                                    "/* УБРАТЬ СТРЕЛКИ */\n"
                                                    "QScrollBar::up-arrow:vertical, \n"
                                                    "QScrollBar::down-arrow:vertical {\n"
                                                    "    background: none; /* Убираем стрелки */\n"
                                                    "}\n"
                                                    "\n"
                                                    "/* УБРАТЬ ФОН */\n"
                                                    "QScrollBar::add-page:vertical, \n"
                                                    "QScrollBar::sub-page:vertical {\n"
                                                    "    background: none; /* Убираем фоновую страницу */\n"
                                                    "}")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_4.setContentsMargins(-1, -1, -1, 10)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_4 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("")
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 1, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.textEdit_conclusion = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
        self.textEdit_conclusion.setMinimumSize(QtCore.QSize(350, 320))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.textEdit_conclusion.setFont(font)
        self.textEdit_conclusion.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                               "border-radius: 20px;\n"
                                               "padding-top: 15px; /* Отступ только слева */   \n"
                                               " padding-bottom: 15px; /* Отступ только снизу */\n"
                                               "")
        self.textEdit_conclusion.setReadOnly(True)
        self.textEdit_conclusion.setObjectName("textEdit_conclusion")
        self.gridLayout_3.addWidget(self.textEdit_conclusion, 1, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 2, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.gridLayout_12.addLayout(self.verticalLayout_2, 2, 1, 2, 2)
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setContentsMargins(-1, 50, -1, 15)
        self.gridLayout_9.setVerticalSpacing(25)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                    "border-radius: 20px;")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setMinimumSize(310,160)
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_count_attempts = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_count_attempts.setFont(font)
        self.label_count_attempts.setStyleSheet("")
        self.label_count_attempts.setObjectName("label_count_attempts")
        self.gridLayout_2.addWidget(self.label_count_attempts, 3, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_13.setFont(font)
        self.label_13.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_13.setStyleSheet("")
        self.label_13.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_13.setObjectName("label_13")
        self.gridLayout_2.addWidget(self.label_13, 3, 0, 1, 1)
        self.label_banned_account = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_banned_account.setFont(font)
        self.label_banned_account.setStyleSheet("")
        self.label_banned_account.setObjectName("label_banned_account")
        self.gridLayout_2.addWidget(self.label_banned_account, 4, 1, 1, 1)
        self.label_sent_message = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_sent_message.setFont(font)
        self.label_sent_message.setStyleSheet("")
        self.label_sent_message.setObjectName("label_sent_message")
        self.gridLayout_2.addWidget(self.label_sent_message, 0, 1, 1, 1)
        self.label_unsuccessful = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_unsuccessful.setFont(font)
        self.label_unsuccessful.setStyleSheet("")
        self.label_unsuccessful.setObjectName("label_unsuccessful")
        self.gridLayout_2.addWidget(self.label_unsuccessful, 2, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_14.setFont(font)
        self.label_14.setStyleSheet("")
        self.label_14.setObjectName("label_14")
        self.gridLayout_2.addWidget(self.label_14, 4, 0, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_15.setFont(font)
        self.label_15.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_15.setStyleSheet("")
        self.label_15.setObjectName("label_15")
        self.gridLayout_2.addWidget(self.label_15, 0, 0, 1, 1)

        self.label_remaining_message = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_remaining_message.setFont(font)
        self.label_remaining_message.setStyleSheet("")
        self.label_remaining_message.setObjectName("label_remaining_message")
        self.gridLayout_2.addWidget(self.label_remaining_message, 1, 1, 1, 1)

        self.label_10 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_10.setFont(font)
        self.label_10.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_10.setStyleSheet("")
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 1, 0, 1, 1)

        self.label_16 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_16.setFont(font)
        self.label_16.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_16.setStyleSheet("")
        self.label_16.setObjectName("label_16")
        self.gridLayout_2.addWidget(self.label_16, 2, 0, 1, 1)
        self.gridLayout_9.addWidget(self.groupBox, 1, 1, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                    "border-radius: 20px;")
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox")
        self.groupBox_3.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.groupBox_3.setMinimumSize(319, 108)
        self.gridLayout_10 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.checkBox_use_streams = QtWidgets.QCheckBox(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_use_streams.setFont(font)
        self.checkBox_use_streams.setStyleSheet("\n"
                                              "QCheckBox {\n"
                                              "color: rgb(0, 0, 0);\n"
                                              "    spacing: 5px; /* Отступ между иконкой и текстом */\n"
                                              "\n"
                                              "}\n"
                                              "QCheckBox::indicator {\n"
                                              "    width: 15px; /* Ширина индикатора (чекбокса) */\n"
                                              "    height: 15px; /* Высота индикатора (чекбокса) */\n"
                                              "    border: 2px solid rgb(150, 150, 150); /* Обводка чекбокса */\n"
                                              "    border-radius: 4px; /* Закругление углов */\n"
                                              "    background-color: white; /* Цвет фона чекбокса */\n"
                                              "}\n"
                                              "QCheckBox::indicator:checked {\n"
                                              "    background-color: rgb(150, 200, 150); \n"
                                              "    border: 2px solid rgb(150, 150, 150); \n"
                                              "}\n"
                                              "\n"
                                              "\n"
                                              "QCheckBox::indicator:checked:hover {\n"
                                              "    background-color: rgb(180, 230, 180); \n"
                                              "}")
        self.checkBox_use_streams.setObjectName("checkBox_use_streams")
        self.gridLayout_10.addWidget(self.checkBox_use_streams, 0, 0, 1, 4)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_2.setStyleSheet("")
        self.label_2.setObjectName("label_2")
        self.gridLayout_10.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_quantity_streams = QtWidgets.QLineEdit(self.groupBox_2)
        validator = QIntValidator(1, 99999)  # Минимум 0, максимум большое число
        self.lineEdit_quantity_streams.setValidator(validator)
        self.lineEdit_quantity_streams.setMaximumSize(QtCore.QSize(60, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_quantity_streams.setFont(font)
        self.lineEdit_quantity_streams.setMaxLength(5)
        self.lineEdit_quantity_streams.setStyleSheet("QLineEdit {\n"
                                                                 "    background-color: rgb(255, 255, 255);      /* Цвет фона текстового поля */\n"
                                                                 "    border: 2px solid rgb(150, 150, 150); /* Рамка текстового поля */\n"
                                                                 "    border-radius: 10px; /* Закругление углов */\n"
                                                                 "    padding: 2px; /* Отступы внутри текстового поля */\n"
                                                                 "    color: rgb(50, 50, 50); /* Цвет текста */\n"
                                                                 "}\n"
                                                                 "\n"
                                                                 "/* Состояние при наведении */\n"
                                                                 "QLineEdit:hover {\n"
                                                                 "    border: 2px solid rgb(160, 160, 160); /* Цвет рамки при наведении */\n"
                                                                 "}\n"
                                                                 "\n"
                                                                 "/* Состояние при фокусировке */\n"
                                                                 "QLineEdit:focus {\n"
                                                                 "    border: 2px solid rgb(0, 0, 0); /* Цвет рамки при фокусировке */\n"
                                                                 "    background-color: rgb(255, 255, 255); /* Цвет фона при фокусировке */\n"
                                                                 "}\n"
                                                                 "\n"
                                                                 "/* Состояние для отключенного текстового поля */\n"
                                                                 "QLineEdit:disabled {\n"
                                                                 "    background-color: rgb(220, 220, 220); /* Цвет фона для отключенного */\n"
                                                                 "    color: rgb(170, 170, 170); /* Цвет текста для отключенного */\n"
                                                                 "    border: 2px solid rgb(200, 200, 200); /* Цвет рамки для отключенного */\n"
                                                                 "}")
        self.lineEdit_quantity_streams.setObjectName("lineEdit_quantity_streams")
        self.gridLayout_10.addWidget(self.lineEdit_quantity_streams, 1, 1, 1, 1)
        self.pushButton_info_streams = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_info_streams.setStyleSheet("border: none;\n")
        self.pushButton_info_streams.setText("")
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/icon/question.png"), QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.pushButton_info_streams.setIcon(icon13)
        self.pushButton_info_streams.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_info_streams.setObjectName("pushButton_info_streams")
        self.gridLayout_10.addWidget(self.pushButton_info_streams, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_3.setStyleSheet("")
        self.label_3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.label_3.setObjectName("label_3")
        self.gridLayout_10.addWidget(self.label_3, 1, 3, 1, 1)
        self.gridLayout_9.addWidget(self.groupBox_3, 0, 1, 1, 1)
        self.gridLayout_12.addLayout(self.gridLayout_9, 2, 3, 1, 1)
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setContentsMargins(-1, -1, -1, 10)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setMinimumSize(QtCore.QSize(185, 80))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_start.setFont(font)
        self.pushButton_start.setStyleSheet("\n"
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
        self.pushButton_start.setIconSize(QtCore.QSize(120, 120))
        self.pushButton_start.setObjectName("pushButton_start")
        self.gridLayout_8.addWidget(self.pushButton_start, 0, 0, 2, 1)
        self.pushButton_clear_conclusion = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_clear_conclusion.setMinimumSize(QtCore.QSize(100, 50))
        self.pushButton_clear_conclusion.setMaximumSize(QtCore.QSize(200, 76))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_clear_conclusion.setFont(font)
        self.pushButton_clear_conclusion.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.pushButton_clear_conclusion.setStyleSheet("\n"
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
        self.pushButton_clear_conclusion.setIconSize(QtCore.QSize(60, 60))
        self.pushButton_clear_conclusion.setObjectName("pushButton_clear_conclusion")
        self.gridLayout_8.addWidget(self.pushButton_clear_conclusion, 1, 1, 1, 1)
        self.gridLayout_12.addLayout(self.gridLayout_8, 3, 3, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.action = QtWidgets.QAction(self)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(self)
        self.action_2.setObjectName("action_2")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        # события
        self.pushButton_account.clicked.connect(lambda: self._transition('accounts'))
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

        self.lineEdit_max_message_from_one_account.focusInEvent = lambda event: self.set_default_style(self.lineEdit_max_message_from_one_account)
        self.lineEdit_delay.focusInEvent = lambda event:  self.set_default_style(self.lineEdit_delay)
        self.lineEdit_max_message.focusInEvent = lambda event:  self.set_default_style(self.lineEdit_max_message)

        self.pushButton_start.clicked.connect(lambda: self.start())
        self.pushButton_clear_conclusion.clicked.connect(lambda: self.clear_conclusion())
        self.pushButton_choose_file_for_mailing.clicked.connect(lambda: self.choose_file_for_mailing())
        self.pushButton_check_user_name.clicked.connect(lambda: self.check_user_name_file())

        self.lineEdit_quantity_streams.textChanged.connect(lambda: self.line_edit_quantity_editing_finished())
        self.pushButton_info_streams.clicked.connect(lambda: self.get_info_about_thread())
        # события

    def _transition(self, window: str):
        if self.mailing_start:
            self.show_info('Внимание!', f'Для перехода на другую вкладку необходимо отключить рассылку')
        else:
            self.switch_window(window)

    def line_edit_quantity_editing_finished(self):
        if self.lineEdit_quantity_streams.text() == '0':
            self.lineEdit_quantity_streams.setText('')

        thread_limit = 0
        while True:  # переименовываем папки откуда скопировали
            directory_name = self.root_project_dir + "/accounts/active_accounts/" + str(thread_limit)
            if os.path.isdir(directory_name):
                thread_limit += 1
            else:
                break

        try:
            if int(self.lineEdit_quantity_streams.text()) > thread_limit:
                self.lineEdit_quantity_streams.setText(str(thread_limit))
        except ValueError:
            pass

    def get_info_about_thread(self):
        thread_limit = 0
        while True:  # переименовываем папки откуда скопировали
            directory_name = self.root_project_dir + "/accounts/active_accounts/" + str(thread_limit)
            if os.path.isdir(directory_name):
                thread_limit += 1
            else:
               break

        if thread_limit == 1:
            message = '1 поток'
        elif thread_limit == 2 or thread_limit == 3 or thread_limit == 4:
            message = str(thread_limit) + ' потока'
        else:
            message = str(thread_limit) + ' потоков'

        self.show_info('Информация',f'Количество потоков - это сколько аккаунтов\nбудут одновременно выполнять рассылку.'
                                    f'\n\nВнимание!\nКоличество потоков не может превышать количество аккаунтов.\n'
                                    f'Ваш лимит {message}')

    def set_default_style(self,line_edit: QLineEdit):
        style = ("QLineEdit {\n"
                 "    background-color: rgb(255, 255, 255);      /* Цвет фона текстового поля */\n"
                 "    border: 2px solid rgb(150, 150, 150); /* Рамка текстового поля */\n"
                 "    border-radius: 10px; /* Закругление углов */\n"
                 "    padding: 2px; /* Отступы внутри текстового поля */\n"
                 "    color: rgb(50, 50, 50); /* Цвет текста */\n"
                 "}\n"
                 "\n"
                 "/* Состояние при наведении */\n"
                 "QLineEdit:hover {\n"
                 "    border: 2px solid rgb(160, 160, 160); /* Цвет рамки при наведении */\n"
                 "}\n"
                 "\n"
                 "/* Состояние при фокусировке */\n"
                 "QLineEdit:focus {\n"
                 "    border: 2px solid rgb(0, 0, 0); /* Цвет рамки при фокусировке */\n"
                 "    background-color: rgb(255, 255, 255); /* Цвет фона при фокусировке */\n"
                 "}\n"
                 "\n"
                 "/* Состояние для отключенного текстового поля */\n"
                 "QLineEdit:disabled {\n"
                 "    background-color: rgb(220, 220, 220); /* Цвет фона для отключенного */\n"
                 "    color: rgb(170, 170, 170); /* Цвет текста для отключенного */\n"
                 "    border: 2px solid rgb(200, 200, 200); /* Цвет рамки для отключенного */\n"
                 "}")
        line_edit.setStyleSheet(style)

    def clear_conclusion(self):
        self.textEdit_conclusion.setText('')
        self.label_sent_message.setText('0')
        self.label_unsuccessful.setText('0')
        self.label_count_attempts.setText('0')
        self.label_banned_account.setText('0')
        self.label_remaining_message.setText('0')

    def show_info(self,title: str, message: str):
        info = Dialog_info(title, message,'notification.mp3')  # Создаем экземпляр
        info.exec_()  # Открываем

    def check_user_name_file(self):
        if not os.path.isfile(self.root_project_dir + '/working_files/user_names_for_mailing.txt'): # если файл с user_names_for_mailing.txt не существует
            with open(self.root_project_dir + '/working_files/user_names_for_mailing.txt', 'w') as file:# Создаем файл в режиме записи (если файл существует, он будет перезаписан)
                file.write("")  # Записываем пустую строку, чтобы создать файл

        if shutil.which('notepad.exe') is not None: # если блокнот есть на пк
            subprocess.Popen(['notepad.exe', self.root_project_dir + '/working_files/user_names_for_mailing.txt'])
        else:
            self.show_info('Внимание!', f'На вашем ПК не установлен блокнот!\n'
                                        f'Установите его или откройте файл самостоятельно\nПуть к файлу: {self.root_project_dir + '\\working_files\\user_names_for_mailing.txt'}')

    def choose_file_for_mailing(self):
        desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
        # Открываем диалог выбора файла
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", desktop_path, "Все файлы (*);", options=options)
        if file_path:
            size = os.path.getsize(file_path) # возвращает размер файла в байтах
            file_name = os.path.basename(file_path) # получаем имя файла
            if size > 2 * 1024 * 1024 * 1024:  # 2 ГБ = 2 * 1024^3 байт
                self.show_info('Внимание!','Файл не сохранён!\nРазмер файла не должен превышать 2гб.')
                return
            else:
                title_dialog = 'Готово!'
                message_dialog = 'Файл успешно сохранён!'
                try:
                    shutil.copy(file_path, self.root_project_dir + f'/working_files/file_from_user/{file_name}')
                    self.file_path_for_mailing = self.root_project_dir + f'/working_files/file_from_user/{file_name}'
                except PermissionError:
                    title_dialog = 'Внимание!'
                    message_dialog = 'Файл не сохранён!\n\nДанный файл занят другим процессом\nЗакройте все процессы связанные с этим файлом.'
                except Exception:
                    title_dialog = 'Готово!'
                    message_dialog = 'Файл не сохранён!\n\nПроизошла ошибка при сохранении файла\nПопробуйте ещё раз.'

                self.show_info(title_dialog,message_dialog)

    def stop_mailing(self): # останавливает рассылку
        while True:
            try:
                connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
                cursor = connection.cursor()
                cursor.execute(f"UPDATE stop_process SET stop_mailing_by_users = ?",(1,))
                connection.commit()
                connection.close()
                break
            except Exception:
                pass
        socket.socket = self.original_socket # востанавливаем сокет
        self.mailing_start = False
        self.pushButton_choose_file_for_mailing.setEnabled(True)
        self.pushButton_check_user_name.setEnabled(True)
        self.lineEdit_max_message_from_one_account.setEnabled(True)
        self.lineEdit_delay.setEnabled(True)
        self.lineEdit_max_message.setEnabled(True)
        self.textEdit_message.setEnabled(True)
        self.checkBox_use_proxy.setEnabled(True)
        self.checkBox_use_file_for_message.setEnabled(True)

        self.lineEdit_quantity_streams.setText('') # убираем колличество запущенных потоков

        current_time = dt.datetime.now()
        formatted_time = current_time.strftime("%H:%M:%S")  # Форматируем время сейчас
        self.textEdit_conclusion.append(f'\n[{formatted_time}] РАССЫЛКА ОСТАНОВЛЕННА')
        self.pushButton_start.setText('ЗАПУСТИТЬ')

    def handler_signal(self, console_output: str, counter_sent_and_unsuccessful_message: list, error: str, end_work: bool):
        if console_output:
            current_time = dt.datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S")  # Форматируем время сейчас
            self.textEdit_conclusion.append(f'[{formatted_time}] {console_output}')

        if counter_sent_and_unsuccessful_message:
            self.label_sent_message.setText(str(counter_sent_and_unsuccessful_message[0]))
            self.label_unsuccessful.setText(str(counter_sent_and_unsuccessful_message[1]))
            self.label_banned_account.setText(str(counter_sent_and_unsuccessful_message[2]))
            self.label_count_attempts.setText(str(counter_sent_and_unsuccessful_message[0] + counter_sent_and_unsuccessful_message[1]))
            self.label_remaining_message.setText(str(self.quantity_remaining_message - (counter_sent_and_unsuccessful_message[0] + counter_sent_and_unsuccessful_message[1])))

        if error:
            self.stop_mailing()
            self.show_info('Внимание!', error)

        if end_work:
            self.stop_mailing()
            self.show_info('Готово!', 'Рассылка успешно завершена')

    def handler_signal_with_streams(self, console_output: str, counter_sent_and_unsuccessful_message: list,
                                    account_banned: bool, list_processed_accounts: list, id_and_last_use: list,
                                    error: str, error_and_id_account: list, end_mailing_from_this_account: bool):
        if console_output:
            current_time = dt.datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S")  # Форматируем время сейчас
            self.textEdit_conclusion.append(f'[{formatted_time}] {console_output}')

        if counter_sent_and_unsuccessful_message:
            self.count_attempts += counter_sent_and_unsuccessful_message[0] + counter_sent_and_unsuccessful_message[1]
            self.label_sent_message.setText(str(counter_sent_and_unsuccessful_message[0] + int(self.label_sent_message.text())))
            self.label_unsuccessful.setText(str(counter_sent_and_unsuccessful_message[1] + int(self.label_unsuccessful.text())))
            self.label_count_attempts.setText(str(counter_sent_and_unsuccessful_message[0] + counter_sent_and_unsuccessful_message[1] + int(self.label_count_attempts.text())))
            self.label_remaining_message.setText(str( self.quantity_remaining_message - self.count_attempts))

        if account_banned:
            self.label_banned_account.setText( str(int(self.label_banned_account.text()) + 1))

        if list_processed_accounts: # это аккаунты по которым отработали
            self.user_name_list_to = [item for item in self.user_name_list_to if item not in list_processed_accounts]

        if id_and_last_use: # добавление для учёта времени последнего использования аккаунта (такое возращается только один раз с одного аккаунта)
            if id_and_last_use[1]:# будем работать если есть время последнего использования
                self.id_and_last_use.append(id_and_last_use)

        if error:
            if self.mailing_start: # если рассылка запущенна, то мы её остановим (это необходимо для того что бы несколько раз не заканчивали рассылку)
                self.stop_mailing()
                self.show_info('Внимание!', error)

        if error_and_id_account:
            self.error_and_id_errors_accounts.append(error_and_id_account)

        if end_mailing_from_this_account:
            self.quantity_accounts_ending_mailing += 1

            # если кол-во закончивших рассылку аккаунтов больше или равно запущенных аккаунтов
            if self.quantity_accounts_ending_mailing >= self.quantity_accounts_for_mailing:
                self.active_threads.clear()

                connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
                cursor = connection.cursor()
                for id_and_last_use in self.id_and_last_use: # установления последнего использования аккаунта
                    cursor.execute(f"UPDATE accounts SET last_used = ? WHERE id_tg = ?", (id_and_last_use[1],id_and_last_use[0]))
                    connection.commit()

                connection.close()

                if self.error_and_id_errors_accounts:  # работаем с аккаунтами в которые не смогли войти
                    sorted_list = sorted(self.error_and_id_errors_accounts, key=lambda x: x[1], reverse=True)
                    # обязательно сортируем список по убыванию для того что бы корректно работать с error_handler
                    for error_and_id in sorted_list:
                        error_handler(error_and_id[0], error_and_id[1], 'active')

                with open(self.root_project_dir + '/working_files/user_names_for_mailing.txt', 'w',encoding='utf-8') as file:  # Открываем файл в режиме записи (режим 'w' очищает файл перед записью)
                    # формируем новый список из юзернеймов (убирая юзернеймы которые использовали)
                    file.write('\n'.join(self.user_name_list_to))  # объединяем все строки из списка в одну строку

                self.stop_mailing()
                self.show_info('Готово!', 'Рассылка успешно завершена')


    def start(self):
        if not self.mailing_start: # если рассылка не запущена
            style = ("QLineEdit {\n"
                     "    background-color: rgb(252, 224, 228);      /* Цвет фона текстового поля */\n"
                     "    border: 2px solid rgb(150, 150, 150); /* Рамка текстового поля */\n"
                     "    border-radius: 10px; /* Закругление углов */\n"
                     "    padding: 2px; /* Отступы внутри текстового поля */\n"
                     "    color: rgb(50, 50, 50); /* Цвет текста */\n"
                     "}\n")

            if not self.textEdit_message.toPlainText(): # если пользователь не ввёл сообщение для рассылки
                self.show_info('Внимание!', 'Введите сообщение для рассылки!')
                return

            if not self.lineEdit_delay.text():
                self.lineEdit_delay.setStyleSheet(style)
                self.show_info('Внимание!', 'Введите задержку между сообщениями !')
                return

            if not self.lineEdit_max_message.text():
                self.lineEdit_max_message.setStyleSheet(style)
                self.show_info('Внимание!', 'Введите максимальное количество сообщений!')
                return

            if not self.lineEdit_max_message_from_one_account.text():
                self.lineEdit_max_message_from_one_account.setStyleSheet(style)
                self.show_info('Внимание!', 'Введите максимум сообщений с одного аккаунта!')
                return

            if not check_html_parse(self.textEdit_message.toPlainText()): # если неверный HTML синтаксис
                self.lineEdit_max_message_from_one_account.setStyleSheet(style)
                self.show_info('Внимание!', 'В сообщении для рассылки \nвведён некорректный HTML синтаксис!')
                return

            try:
                # Открываем файл в режиме чтения
                with open(self.root_project_dir + '/working_files/user_names_for_mailing.txt', 'r') as file:
                    lines = file.readlines()  # Читаем все строки файла в список
                    list_users = [ # Фильтруем строки, оставляя только те, что соответствуют критериям
                        line.strip() for line in lines
                        if re.fullmatch(r'^(?=.*[A-Za-z])[\w@]+$', line.strip())# Поиск строк с буквами и разрешёнными символами
                    ]
                    list_users = list(set(list_users))# Удаляем повторяющиеся элементы
                    self.quantity_remaining_message = len(list_users)# Сохраняем количество всех строк которые остались

                if len(lines) != len(list_users):
                    self.show_info('Внимание!', 'Некоторые строки не были добавлены в программу,\nт.к. не соответствуют критерию возможных юзернеймов')
                if not list_users: # если в файле user_names_for_mailing.txt нет записи
                    self.show_info('Внимание!', 'В файле c юзернеймами нет ни одной корректной записи!\n'
                                                'Юзернейм может быть написан только на английскими буквами.\n'
                                                'Так же строка может содержат только "@" в самом начале юзернейма,\n'
                                                'строка может содержать спец символов "_"')
                    return
            except FileNotFoundError: # если файл не найден
                with open(self.root_project_dir + '/working_files/user_names_for_mailing.txt','w') as file:  # Создаем файл в режиме записи
                    file.write("")  # Записываем пустую строку, чтобы создать файл
                self.show_info('Внимание!', 'В файле c юзернеймами нет ни одной записи!')
                return
            except PermissionError:
                self.show_info('Внимание!', 'Закройте файл c юзернеймами!')
                return
            except UnicodeDecodeError:
                self.show_info('Внимание!', 'В файле с юзернеймами введены некорректные данные!\nСимволы должны быть в формате UTF-8')
                return
            except Exception:
                self.show_info('Внимание!', 'Произошла неизвестная ошибка!\nПерезапустите программу.')
                return

            zero_account = self.root_project_dir + f'/accounts/active_accounts/0'
            if not os.path.isdir(zero_account): # проверяем есть ли аккаунты для рассылки (это если нету)
                self.show_info('Внимание!', 'У вас нет активных аккаунтов для рассылки!')
                return

            if self.checkBox_use_file_for_message.isChecked():
                if not os.path.isfile(self.file_path_for_mailing):
                    self.show_info('Внимание!', 'Укажите файл для сообщения!')
                    return

            proxy_from_db = ['', 0, '', '']

            if self.checkBox_use_proxy.isChecked(): # проверка прокси
                connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
                cursor = connection.cursor()
                cursor.execute(f"SELECT ip,port,login,password,use_proxy_to_enter FROM proxy")
                proxy_from_db = cursor.fetchone()
                connection.close()

                efficiency = check_proxy(proxy_from_db[0], int(proxy_from_db[1]), proxy_from_db[2],proxy_from_db[3])
                if not efficiency: # если прокси не действительно
                    error_proxy = Dialog_error_proxy(proxy_from_db[0], str(proxy_from_db[1]), proxy_from_db[2],proxy_from_db[3])  # Создаем экземпляр
                    error_proxy.show_info()
                    error_proxy.exec_()  # Открываем
                    return

            self.count_attempts = 0

            connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
            cursor = connection.cursor()
            cursor.execute(f"UPDATE stop_process SET stop_mailing_by_users = ?", (0,))
            connection.commit()
            connection.close()

            if self.checkBox_use_streams.isChecked(): # если надо запускать несколько потоков
                if not self.lineEdit_quantity_streams.text(): # если не ввели кол-во потоков
                    self.show_info('Внимание!', 'Введите количество потоков!')
                    return

                self.label_remaining_message.setText('0')
                self.mailing_start = True

                self.active_threads = []
                self.id_and_last_use = []
                self.user_name_list_to = list_users.copy()
                self.quantity_accounts_for_mailing = 0
                self.quantity_accounts_ending_mailing = 0
                self.error_and_id_errors_accounts = []
                quantity_streams = int(self.lineEdit_quantity_streams.text()) # необходимое кол-во потоков

                if len(list_users) > int(self.lineEdit_max_message.text()): # если список аккаунтов для рассылки больше чем необходимое кол-во аккаунтов для рассылки
                    difference = len(list_users) - int(self.lineEdit_max_message.text()) # узнаём разницу
                    for _ in range(difference):
                        list_users.pop() # удаление последнего элемента из списка

                quantity_user_for_one_account = math.floor(len(list_users) / quantity_streams) # округляем в меньшую сторону
                if quantity_user_for_one_account > int(self.lineEdit_max_message_from_one_account.text()):
                    # если количество аккаунтов для рассылки с одного аккаунта больше чем максимум с одного аккаунта
                    quantity_user_for_one_account = int(self.lineEdit_max_message_from_one_account.text())

                list_users.reverse() # сортируем списк в обратном порядке для быстродйствия кода (теперь элементы в начале встали в конец)

                current_time = dt.datetime.now()
                formatted_time = current_time.strftime("%H:%M:%S")  # Форматируем время сейчас
                self.textEdit_conclusion.append(f'[{formatted_time}] РАССЫЛКА ЗАПУЩЕННА\n')

                self.quantity_remaining_message = 0 # по количеству оставшихся аккаунтов тут будет другая логика нежели без использования потоков
                for id_account in range(int(self.lineEdit_quantity_streams.text())): # проходимся по кол-ву потоков
                    user_list_for_one_account = []
                    for _ in range(quantity_user_for_one_account):
                        user_list_for_one_account.append(list_users[-1]) # добавление последнего элемента из списка
                        list_users.pop() # удаление последнего элемента из списка

                    if os.path.isdir(self.root_project_dir + f'/accounts/active_accounts/{id_account}'):  # если аккаунт есть
                        mailing = MailingWithStreams(id_account,self.textEdit_message.toPlainText(),user_list_for_one_account,int(self.lineEdit_delay.text()),
                                                     self.checkBox_use_file_for_message.isChecked(),self.file_path_for_mailing, self.checkBox_use_proxy.isChecked(),
                                                     proxy_from_db[0], proxy_from_db[1], proxy_from_db[2],proxy_from_db[3])
                        mailing.task_done.connect(self.handler_signal_with_streams)  # Подключаем сигнал к слоту
                        mailing.start() # Запускаем поток

                        self.active_threads.append(mailing)

                        self.quantity_remaining_message += quantity_user_for_one_account
                        self.quantity_accounts_for_mailing += 1
            else:
                self.label_remaining_message.setText('0')
                self.mailing_start = True
                self.mailing = Mailing_one_stream(self.textEdit_message.toPlainText(),list_users,int(self.lineEdit_delay.text()),int(self.lineEdit_max_message.text()),
                                                  int(self.lineEdit_max_message_from_one_account.text()),self.checkBox_use_file_for_message.isChecked(),
                                                  self.file_path_for_mailing, self.checkBox_use_proxy.isChecked())  # Инициализируем рабочий поток
                self.mailing.task_done.connect(self.handler_signal)  # Подключаем сигнал к слоту
                self.mailing.start()  # Запускаем поток

                current_time = dt.datetime.now()
                formatted_time = current_time.strftime("%H:%M:%S")  # Форматируем время сейчас
                self.textEdit_conclusion.append(f'[{formatted_time}] РАССЫЛКА ЗАПУЩЕННА\n')


            self.pushButton_start.setText('ОСТАНОВИТЬ')
            self.pushButton_choose_file_for_mailing.setEnabled(False)
            self.pushButton_check_user_name.setEnabled(False)
            self.lineEdit_max_message_from_one_account.setEnabled(False)
            self.lineEdit_delay.setEnabled(False)
            self.lineEdit_max_message.setEnabled(False)
            self.textEdit_message.setEnabled(False)
            self.checkBox_use_proxy.setEnabled(False)
            self.checkBox_use_file_for_message.setEnabled(False)
        else:
            Dialog1 = Dialog_yes_or_cancel('Внимание!',
                                           'Вы действительно хотите остановить рассылку?',
                                           'notification.mp3')  # Создаем экземпляр
            Dialog1.data_returned.connect(self.stop_mailing)  # Подключаем сигнал
            Dialog1.exec_()  # Открываем модальное окно

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
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
        self.pushButton_setting.setText(_translate("MainWindow", "   Настройки"))
        self.label_18.setText(_translate("MainWindow", "Рассылка"))
        self.label_6.setText(_translate("MainWindow", " Сообщение для отправки:"))
        self.textEdit_message.setHtml(_translate("MainWindow",
                                                 "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                 "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                 "p, li { white-space: pre-wrap; }\n"
                                                 "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                                                 "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; -qt-user-state:65536;\"><br /></p></body></html>"))
        self.pushButton_choose_file_for_mailing.setText(_translate("MainWindow", "Выбрать"))
        self.checkBox_use_file_for_message.setText(_translate("MainWindow", "Использоват файл для сообщения "))
        self.label_5.setText(
            _translate("MainWindow", "<html><head/><body><p>Необходимое колличество сообщений:</p></body></html>"))
        self.label_7.setText(
            _translate("MainWindow", "<html><head/><body><p>Задержка между отправкой в секундах:</p></body></html>"))
        self.checkBox_use_proxy.setText(_translate("MainWindow", "Использоват прокси"))
        self.checkBox_use_streams.setText(_translate("MainWindow", "Использовать несколько потоков"))
        self.label_12.setText(_translate("MainWindow", "Максимум сообщений с одного аккаунта: "))
        self.label.setText(_translate("MainWindow", "Файл с @user_name для рассылки:"))
        self.pushButton_check_user_name.setText(_translate("MainWindow", "Просмотр"))
        self.label_4.setText(_translate("MainWindow", "Консоль вывода:"))
        self.textEdit_conclusion.setHtml(_translate("MainWindow",
                                                    "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                    "p, li { white-space: pre-wrap; }\n"
                                                    "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                                                    "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label_count_attempts.setText(_translate("MainWindow", "0"))
        self.label_13.setText(_translate("MainWindow", "количество попыток: "))
        self.label_banned_account.setText(_translate("MainWindow", "0"))
        self.label_sent_message.setText(_translate("MainWindow", "0"))
        self.label_unsuccessful.setText(_translate("MainWindow", "0"))
        self.label_remaining_message.setText(_translate("MainWindow", "0"))
        self.label_14.setText(_translate("MainWindow", "Забаненных аккаунтов:"))
        self.label_15.setText(_translate("MainWindow", "Отправленных сообщений: "))
        self.label_10.setText(_translate("MainWindow", "Осталось пользователей: "))
        self.label_16.setText(_translate("MainWindow", "Неудачных попыток: "))
        self.pushButton_start.setText(_translate("MainWindow", "ЗАПУСТИТЬ"))
        self.pushButton_clear_conclusion.setText(_translate("MainWindow", "Очистить\nконсоль"))
        self.action.setText(_translate("MainWindow", "сохранить"))
        self.action_2.setText(_translate("MainWindow", "добавить"))
        self.label_2.setText(_translate("MainWindow", "Количество:"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Window_mailing_by_users('fbdgf')
    ui.show()
    sys.exit(app.exec_())
