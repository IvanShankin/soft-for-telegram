import re # для проверки txt файла на правильность записи
import os  # это для действия ниже перед запуском функции
import sys  # информация о системе
import sqlite3
import datetime as dt
import math
import socks
import socket
import asyncio
import shutil  # для удаления папки
import subprocess  # для запуска exe файлов

from opentele.td import TDesktop
from opentele.api import UseCurrentSession
from opentele.exception import TFileNotFound
from telethon import errors

from app.mailing_by_users.ui.window_mailing_by_users_ui import WindowMailingByUsersUi
from app.general.views.info import DialogInfo
from app.general.check_proxy import check_proxy
from app.general.views.error_proxy_for_work import DialogErrorProxyForWork
from app.general.error_handler import get_description_and_solution, error_handler
from app.general.check_html_parse import check_html_parse
from app.general.views.yes_or_cancel import DialogYesOrCancel

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")# 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():# 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path# 3. Установка пути

# 4. Только после этого импортируем PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIntValidator  # для разрешения ввода только цифр в LineEdit
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QLineEdit,  QSizePolicy, QFileDialog


class MailingWithStreams(QThread): # затухание progress_bar
    task_done = pyqtSignal(str, list, bool, list, list, str, list, bool)  # Сигнал, который мы будем использовать для обновления интерфейса
    # вывод в консоль(str), количество успешных и неудачных сообщений(list), ошибка прокси(bool), ошибка(str), конец работы(bool)

    def __init__(self,id_account: int,message: str,user_list: list,time_sleep: int, use_file_for_message: bool,
                 file_path: str, use_proxy: bool,ip: str, port: int, login: str, password: str):
        super().__init__()
        self.root_project_dir = '..'
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

        self.client = None
        self.account_id = None
        self.last_used = ''

        self.successful_messages = 0
        self.failed_messages = 0
        self.list_accounts_which_sent = []

        self.stop_thread = False

    def run(self):
        asyncio.run(self.run_2())

    async def run_2(self):
        me = None

        if self.use_proxy:
            socks.set_default_proxy(socks.SOCKS5, self.ip, self.port, True, self.login, self.password)
            socket.socket = socks.socksocket

        try:  # пытаемся войти в аккаунт
            folder_path_account = self.root_project_dir + f'/accounts/active_accounts/{self.id_account}'  # путь к tdata
            tdesk = TDesktop(folder_path_account + '/tdata')

            self.self.client = await tdesk.ToTelethon(session=f"{folder_path_account}/session.session",flag=UseCurrentSession,)

            await asyncio.wait_for(self.client.connect(), timeout=15)  # вход в аккаунт
            me = await self.client.get_me()
            self.account_id = me.id

            self.task_done.emit(f'Запущенна рассылка с аккаунта "{me.username}"',
                                [self.successful_messages, self.failed_messages],False,[],[], '', [], False)

            for user in self.user_list:

                connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
                cursor = connection.cursor()
                cursor.execute(f"SELECT stop_mailing_by_users FROM stop_process", )
                closure_test = cursor.fetchone()
                connection.close()

                if closure_test[0] == 1:  # если необходимо остановить рассылку
                    return

                try:
                    now = dt.datetime.now()  # Получаем время именно тут, т.к. может возникнут ошибка и это тоже считается как использование аккаунта
                    self.last_used = now.strftime('%H:%M %d-%m-%Y')  # Форматируем дату и время согласно формату

                    if self.use_file_for_message:
                        await self.client.send_file(user, self.file_path, parse_mode='HTML',caption=self.message)  # отсылка файла
                    else:
                        await self.client.send_message(user, self.message, parse_mode='HTML')  # отправка сообщения

                    self.successful_messages += 1
                    self.list_accounts_which_sent.append(user)

                    await asyncio.sleep(self.time_sleep)
                except FileNotFoundError:  # файл не найден
                    self.task_done.emit('',[self.successful_messages, self.failed_messages], False,self.list_accounts_which_sent, [],
                                        'Ошибка отсылки файла!\nДобавьте новый файл', [], False)
                    return
                except errors.MessageEmptyError:  # Было отправлено пустое или недопустимое сообщение в формате UTF-8.
                    self.task_done.emit('',[self.successful_messages, self.failed_messages], False, self.list_accounts_which_sent, [],
                                        'Ошибка отправки сообщения!\nСообщение в недопустимом формате UTF-8', [], False)
                    return
                except errors.MessageTooLongError:  # сообщение слишком длинное
                    self.task_done.emit('', [self.successful_messages, self.failed_messages], False, self.list_accounts_which_sent, [],
                                        'Ошибка отправки сообщения!\nСообщение слишком длинное.\nМаксимальная длинная = 4096 символов в UTF-8', [], False)
                    return
                except (errors.UserPrivacyRestrictedError, errors.ForbiddenError):  # кому хотим отослать стоит настройка приватности что нельзя отсылать или в чёрном списке
                    self.list_accounts_which_sent.append(user)
                    self.failed_messages += 1
                except (ValueError, errors.UsernameInvalidError, errors.InputUserDeactivatedError,
                        errors.YouBlockedUserError, errors.UserIsBlockedError):
                    self.list_accounts_which_sent.append(user)
                    self.failed_messages += 1
        except asyncio.exceptions.CancelledError:  # если экстренно остановили поток и в методе который вызывается с await может произойти такая ошибка
            return
        except (Exception, TFileNotFound) as e:  # здесь ошибки с аккаунтом откуда отсылаем
            try:
                await self.client.disconnect()
            except UnboundLocalError:
                pass

            error_name = str(type(e).__name__)
            if error_name == 'ConnectionError' and self.stop_thread: # если экстренно остановили поток, может возникнуть такая ошибка
                return

            connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
            cursor = connection.cursor()
            cursor.execute(f"SELECT user_name FROM accounts WHERE id = ? AND account_status = ?",(self.id_account, 'active'))
            user_name_from_db = cursor.fetchone()  # берём с БД т.к. мы можем даже не войти в аккаунт и тогда не получим его user_name для вывода
            connection.close()

            error_description_solution = get_description_and_solution(error_name)
            self.task_done.emit(f'На аккаунте "{user_name_from_db[0]}" произошла ошибка он будет убран из активных.\nОшибка: '
                                f'{error_description_solution[0]}\nОтосланных сообщений: {self.successful_messages} из {len(self.user_list)}',
                                [self.successful_messages, self.failed_messages], True, self.list_accounts_which_sent, [self.account_id, self.last_used],
                                '',[error_name, self.id_account], True)
            return

        self.task_done.emit(f'Аккаунт "{me.username}" закончил рассылку\nОтосланных сообщений: {self.successful_messages} из {len(self.user_list)}',
            [self.successful_messages, self.failed_messages], False, self.list_accounts_which_sent, [self.account_id, self.last_used], '',[], True)
        try:
            await self.client.disconnect()
        except UnboundLocalError:
            pass
        return

    async def quit_async(self):
        """Асинхронный метод для завершения потока"""
        self.stop_thread = True
        try:
            await self.client.disconnect()
        except Exception:
            pass

        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()
        cursor.execute(f"SELECT user_name FROM accounts WHERE id = ? AND account_status = ?",
                       (self.id_account, 'active'))
        user_name_from_db = cursor.fetchone()  # берём с БД т.к. мы можем даже не войти в аккаунт и тогда не получим его user_name для вывода
        connection.close()

        self.task_done.emit(
            f'Аккаунт "{user_name_from_db[0]}" Завершил рассылку.\n'
            f'Отосланных сообщений: {self.successful_messages} из {len(self.user_list)}',
            [self.successful_messages, self.failed_messages], True, self.list_accounts_which_sent, [self.account_id, self.last_used],
            '', [], True)

        self.terminate()  # Принудительное завершение

class MailingOneStream(QThread): # затухание progress_bar
    task_done = pyqtSignal(str, list,str, bool)  # Сигнал, который мы будем использовать для обновления интерфейса
    # вывод в консоль(str), количество успешных и неудачных сообщений, колличество забаненых аккаунтов(list),
    # ошибка прокси(bool), ошибка(str), конец работы(bool)

    original_socket = socket.socket  # запоминаем какой сокет был до
    error_and_id_errors_accounts = []  # хранит массивы в которых ошибка и id папки, где произошла эта ошибка
    def __init__(self,message: str,user_list: list,time_sleep: int, max_message: int,
                 max_message_per_account: int,use_file_for_message: bool, file_path: str, use_proxy: bool):
        super().__init__()
        self.root_project_dir = '..'
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

        self.client = None

    def run(self):
        try:
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
        except (asyncio.exceptions.CancelledError, ConnectionError): # если экстренно остановили поток и в методе который вызывается с await может произойти такая ошибка
            return

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
            self.client = await tdesk.ToTelethon(session = f"{folder_path_account}/session.session",flag = UseCurrentSession)
            await asyncio.wait_for(self.client.connect(), timeout = 7)  # вход в аккаунт

            me = await self.client.get_me()
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
                        await self.client.send_file(user, self.file_path, parse_mode = 'HTML',caption = self.message)  # отсылка файла
                    else:
                        await self.client.send_message(user, self.message, parse_mode = 'HTML')  # отправка сообщения

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

        except (asyncio.exceptions.CancelledError, ConnectionError):  # если экстренно остановили поток и в методе который вызывается с await может произойти такая ошибка
            return[list_accounts_which_sent, True]
        except (Exception, TFileNotFound) as e:  # здесь ошибки с аккаунтом откуда отсылаем
            socket.socket = self.original_socket
            self.banned_accounts += 1
            try:
                await self.client.disconnect()
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
            await self.client.disconnect()
        except UnboundLocalError:
            pass
        connection.close()
        socket.socket = self.original_socket
        return  [list_accounts_which_sent, True]

    async def quit_async(self):
        """Асинхронный метод для завершения потока"""
        try:
            await self.client.disconnect()
        except Exception:
            pass
        self.terminate()  # Принудительное завершение

class WindowMailingByUsers(WindowMailingByUsersUi):
    def __init__(self,switch_window):
        super().__init__()
        self.root_project_dir = '..'
        self.mailing_start = False # отображает запущенна ли рассылка
        self.file_path_for_mailing = '' # путь к файлу для рассылки
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

        # события
        self.pushButton_account.clicked.connect(lambda: self._transition('accounts'))
        self.pushButton_mailing_chat.clicked.connect(lambda: self._transition('mailing_by_chats'))
        self.pushButton_invite.clicked.connect(lambda: self._transition('invite'))
        self.pushButton_parser.clicked.connect(lambda: self._transition('parser'))
        self.pushButton_proxy.clicked.connect(lambda: self._transition('proxy'))
        self.pushButton_bomber.clicked.connect(lambda: self._transition('bomber'))
        self.pushButton_create_channel.clicked.connect(lambda: self._transition('create_channel'))
        self.pushButton_create_bot.clicked.connect(lambda: self._transition('create_bot'))
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
        info = DialogInfo(title, message,'notification.mp3')  # Создаем экземпляр
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
                    title_dialog = 'Внимание!'
                    message_dialog = 'Файл не сохранён!\n\nПроизошла ошибка при сохранении файла\nПопробуйте ещё раз.'

                self.show_info(title_dialog,message_dialog)

    def stop_mailing(self): # останавливает рассылку
        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()
        cursor.execute(f"UPDATE stop_process SET stop_mailing_by_users = ?",(1,))
        connection.commit()
        connection.close()

        for thread in self.active_threads:
            asyncio.run(thread.quit_async())
        self.active_threads.clear()

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

            if not check_html_parse(self.textEdit_message.toPlainText()): # если неверный HTML синтаксис
                self.textEdit_message.setStyleSheet()
                self.show_info('Внимание!', 'В сообщении для рассылки \nвведён некорректный HTML синтаксис!')
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
                    error_proxy = DialogErrorProxyForWork(proxy_from_db[0], str(proxy_from_db[1]), proxy_from_db[2],proxy_from_db[3])  # Создаем экземпляр
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

                list_users.reverse() # сортируем список в обратном порядке для быстродействия кода (теперь элементы в начале встали в конец)

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
                mailing = MailingOneStream(self.textEdit_message.toPlainText(),list_users,int(self.lineEdit_delay.text()),int(self.lineEdit_max_message.text()),
                                                  int(self.lineEdit_max_message_from_one_account.text()),self.checkBox_use_file_for_message.isChecked(),
                                                  self.file_path_for_mailing, self.checkBox_use_proxy.isChecked())  # Инициализируем рабочий поток
                mailing.task_done.connect(self.handler_signal)  # Подключаем сигнал к слоту
                mailing.start()  # Запускаем поток

                self.active_threads.append(mailing)

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
            Dialog1 = DialogYesOrCancel('Внимание!',
                                           'Вы действительно хотите остановить рассылку?',
                                           'notification.mp3')  # Создаем экземпляр
            Dialog1.data_returned.connect(self.stop_mailing)  # Подключаем сигнал
            Dialog1.exec_()  # Открываем модальное окно

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = WindowMailingByUsers('fbdgf')
    ui.show()
    sys.exit(app.exec_())
