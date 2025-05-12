import re  # для проверки txt файла на правильность записи
import os  # это для действия ниже перед запуском функции
import sys  # информация о системе
import sqlite3
import datetime as dt
import math
from sys import exception

import socks
import socket
import time
import asyncio
import aiohttp
from aiohttp.log import client_logger
from aiohttp_socks import ProxyConnector
import shutil  # для удаления папки
import faulthandler  # для просмотра стека вызовов
import subprocess  # для запуска exe файлов

from opentele.td import TDesktop
from opentele.api import UseCurrentSession
from opentele.exception import TFileNotFound
from telethon import errors

from telethon import TelegramClient, events
from telethon.tl.functions.channels import InviteToChannelRequest, InviteToChannelRequest, JoinChannelRequest, EditAdminRequest, JoinChannelRequest
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.types import InputPeerChannel ,InputPeerUser,InputUser, InputUserEmpty, InputPeerUser,InputChannel, ChatAdminRights
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact

from app.general.info import Dialog_info
from app.general.yes_or_cancel import Dialog_yes_or_cancel
from app.general.check_proxy import check_proxy
from app.general.error_proxy_for_work import Dialog_error_proxy
from app.general.error_handler import get_description_and_solution, error_handler
from app.general.check_html_parse import check_html_parse

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")  # 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():  # 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path  # 3. Установка пути

# 4. Только после этого импортируем PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIntValidator  # для разрешения ввода только цифр в LineEdit
from PyQt5.QtCore import QThread, pyqtSignal, QPropertyAnimation, Qt, QSize
from PyQt5.QtWidgets import QLineEdit, QSizePolicy, QFileDialog
from PyQt5.QtCore import QTimer

class Invait_one_stream(QThread): # затухание progress_bar
    task_done = pyqtSignal(str, list,bool, bool, bool, str, bool)  # Сигнал, который мы будем использовать для обновления интерфейса
    # вывод в консоль(str), количество успешных и неудачных сообщений(list), ошибка(str), конец работы(bool)
    root_project_dir = '..'

    original_socket = socket.socket  # запоминаем какой сокет был до
    def __init__(self,name_group: str, user_list: list,time_sleep: int,max_invite: int,max_invite_from_one_account: int,
                      use_proxy: bool,ip: str, port: int, login: str, password: str):
        super().__init__()
        self.name_group = name_group
        self.user_list = user_list
        self.time_sleep = time_sleep
        self.max_invite = max_invite
        self.max_invite_from_one_account = max_invite_from_one_account

        self.use_proxy = use_proxy
        self.ip = ip
        self.port = port
        self.login = login
        self.password = password

        self.active_account_counter = 0 # отображает на каком активном аккаунте находится программа (это будет id папки)
        self.main_account_counter = 0 # отображает на каком главном аккаунте находится программа (это будет id папки)
        self.counter_invites = 0 # счётчик успешных приглашений
        self.list_used_users = [] # список user_names которые учавствовали в инвайте

        self.error_and_id_errors_main_accounts = []  # хранит массивы в которых ошибка и id папки, где произошла эта ошибка (для главных аккаунтов)
        self.error_and_id_errors_active_accounts = []  # хранит массивы в которых ошибка и id папки, где произошла эта ошибка (для активных акаунтов)

    def run(self):
        asyncio.run(self.run_2())

    async def run_2(self):
        me_main_account = None
        me_active_account = None

        main_client = None
        client = None

        if self.use_proxy: # подключение к прокси если необходимо
            socks.set_default_proxy(socks.SOCKS5, self.ip, self.port, True, self.login,self.password)  # Установка прокси-соединения
            socket.socket = socks.socksocket

        while True:
            try:
                id_main_account = 0
                if os.path.isdir(f'{self.root_project_dir}/accounts/main_accounts/{self.main_account_counter}'):
                    folder_path_main_account = f'{self.root_project_dir}/accounts/main_accounts/{self.main_account_counter}'  # путь к tdata
                    tdesk = TDesktop(f'{folder_path_main_account}/tdata')

                    main_client = await tdesk.ToTelethon(session=f"{folder_path_main_account}/session.session",flag=UseCurrentSession,)

                    await asyncio.wait_for(main_client.connect(), timeout=10)  # вход в аккаунт
                    me_main_account = await main_client.get_me()
                    id_main_account = me_main_account.id # выйдет ошибка если не смогли получить данные с аккаунта

                    self.task_done.emit(f'Вошли в главный аккаунт "{me_main_account.username}"',
                                        self.list_used_users, False, False, False,'',False)

                    # необходим для добавления во взаимные контакты
                    main_contact = InputPhoneContact(client_id=0, phone=me_main_account.phone,
                                                     first_name="Основной ", last_name="аккаунт")
                    while True:
                        folder_path_active_account = None
                        active_contact = None
                        channel_temp = None
                        channel = None
                        id_active_account = 0

                        try:
                            if os.path.isdir(f'{self.root_project_dir}/accounts/active_accounts/{self.active_account_counter}'):
                                folder_path_active_account = f'{self.root_project_dir}/accounts/active_accounts/{self.active_account_counter}'  # путь к tdata
                                tdesk = TDesktop(f'{folder_path_active_account}/tdata')

                                client = await tdesk.ToTelethon(session=f"{folder_path_active_account}/session.session",flag=UseCurrentSession,)

                                await asyncio.wait_for(client.connect(), timeout=10)  # вход в аккаунт
                                me_active_account = await client.get_me()
                                id_active_account = me_active_account.id  # выйдет ошибка если не смогли получить данные с аккаунта

                                active_contact = InputPhoneContact(client_id=0, phone=me_active_account.phone,
                                                                    first_name=f"{me_active_account.id} ", last_name="аккаунт")
                                # Добавляем во взаимные контакты
                                await client(ImportContactsRequest(contacts=[main_contact])) # добавляем в контакт у активного аккаунта

                                try:
                                    channel_temp = await client.get_entity(self.name_group)
                                    channel = InputChannel(channel_temp.id, channel_temp.access_hash)
                                except (AttributeError, ValueError, TypeError, errors.PeerIdInvalidError):
                                    await client.disconnect()
                                    await main_client.disconnect()
                                    self.task_done.emit('Неверно указан user_name группы или группа не имеет открытый статус!',
                                                        self.list_used_users, False, False, False,
                                                        'Неверно указан user_name группы или группа не имеет открытый статус!',
                                                        True)
                                    socket.socket = self.original_socket
                                    self.working_witch_accounts_in_banned()
                                    return
                                except (errors.ChannelPrivateError, errors.ChatAdminRequiredError):
                                    await client.disconnect()
                                    await main_client.disconnect()
                                    self.task_done.emit('Невозможно пригласить в группу. Сделайте группу открытой!',
                                                        self.list_used_users, False, False, False,
                                                        'Невозможно пригласить в группу. Сделайте группу открытой!', True)
                                    socket.socket = self.original_socket
                                    self.working_witch_accounts_in_banned()
                                    return
                                except errors.RPCError as e:
                                    await client.disconnect()
                                    await main_client.disconnect()
                                    self.task_done.emit(f'Возникла ошибка: {e}!',
                                                        self.list_used_users, False, False, False, e, True)
                                    socket.socket = self.original_socket
                                    self.working_witch_accounts_in_banned()
                                    return

                                await client(JoinChannelRequest(channel))  # вхождение в канал

                                await client.disconnect()

                            else:
                                self.task_done.emit('Активные аккаунты закончились!', self.list_used_users,
                                                    False, False,False, '', True)
                                socket.socket = self.original_socket
                                self.working_witch_accounts_in_banned()
                                return

                        except Exception as e: # здесь обрабатываются ошибки связанные с активными аккаунтами
                            try:
                                await client.disconnect()
                            except UnboundLocalError:
                                pass

                            connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
                            cursor = connection.cursor()
                            cursor.execute(f"SELECT user_name FROM accounts WHERE id = ? AND account_status = ?",
                                           (self.active_account_counter, 'active'))
                            user_name_from_db = cursor.fetchone()  # берём с БД т.к. мы можем даже не войти в аккаунт и тогда не получим его user_name для вывода
                            connection.close()

                            error_type = type(e)
                            error_description_solution = get_description_and_solution(str(error_type.__name__))
                            self.error_and_id_errors_active_accounts.append(error_description_solution)

                            self.task_done.emit(f'На активном аккаунте "{user_name_from_db[0]}" произошла ошибка он будет сменён.'
                                f'\nОшибка: {error_description_solution[0]}', [], False, False, True, '', False)


                        # необходима именно такая очерёдность работы с аккаунтами для того что бы было возможно
                        # отследить ошибку у главного аккаунта

                        await main_client(ImportContactsRequest(contacts=[active_contact]))  # добавляем в контакт у главного аккаунта

                        try:
                            channel_temp_for_admin = await main_client.get_entity(self.name_group)  # для админа нужен свой канал
                            channel_for_admin = InputChannel(channel_temp_for_admin.id,channel_temp_for_admin.access_hash)  # для админа нужен свой канал
                        except (AttributeError, ValueError, TypeError, errors.PeerIdInvalidError):
                            await client.disconnect()
                            await main_client.disconnect()
                            self.task_done.emit('Неверно указан user_name группы или группа не имеет открытый статус!',
                                                self.list_used_users, False, False, False,
                                                'Неверно указан user_name группы или группа не имеет открытый статус!',
                                                True)
                            socket.socket = self.original_socket
                            self.working_witch_accounts_in_banned()
                            return
                        except (errors.ChannelPrivateError, errors.ChatAdminRequiredError):
                            await client.disconnect()
                            await main_client.disconnect()
                            self.task_done.emit('Невозможно пригласить в группу. Сделайте группу открытой!',
                                                self.list_used_users, False, False, False,
                                                'Невозможно пригласить в группу. Сделайте группу открытой!', True)
                            socket.socket = self.original_socket
                            self.working_witch_accounts_in_banned()
                            return
                        except errors.RPCError as e:
                            await client.disconnect()
                            await main_client.disconnect()
                            self.task_done.emit(f'Возникла ошибка: {e}!',
                                                self.list_used_users, False, False, False, e, True)
                            socket.socket = self.original_socket
                            self.working_witch_accounts_in_banned()
                            return

                        rights = ChatAdminRights(invite_users=True, )  # список предоставляемых разрешений

                        try:# назначение админом (в user_id необходимо передать user_name пользователя)
                            await main_client(EditAdminRequest(channel=channel_for_admin, user_id=me_active_account.id,
                                                 admin_rights=rights, rank='Админ'))

                        except errors.ChatAdminRequiredError:  # если главный аккаунт не назначен админом
                            await client.disconnect()
                            await main_client.disconnect()
                            self.main_account_counter += 1
                            self.task_done.emit(f'Главный аккаунт "{me_main_account.username}" не назначен админом '
                                                f'с возможностью добавлять других администраторов. Он будет пропущен!',
                                                [], False, False, False, '', False)
                            break

                        except errors.AdminsTooMuchError:  # если админов слишком много
                            await client.disconnect()
                            await main_client.disconnect()
                            self.task_done.emit(f'В вашей группе максимум админов, для работы скрипта необходимо '
                                                f'освободить как минимум одно место для админа!',
                                                self.list_used_users, False, False, False,
                                                'В вашей группе максимум админов, для работы скрипта необходимо '
                                                'освободить как минимум одно место для админа!',
                                                True)
                            socket.socket = self.original_socket
                            self.working_witch_accounts_in_banned()
                            return
                        except errors.RPCError as e:
                            await client.disconnect()
                            await main_client.disconnect()
                            self.task_done.emit(f'Возникла ошибка: {e}!', self.list_used_users, False, False, False, e,
                                                True)
                            socket.socket = self.original_socket
                            self.working_witch_accounts_in_banned()
                            return

                        socket.socket = self.original_socket # восстановление прокси

                        self.update_last_used(id_main_account) # установление последнего использования главного аккаунта

                        # инвайт происходит через этот метод
                        stop_invite = await self.invite(folder_path_active_account, channel)
                        self.active_account_counter += 1 # меняем id аккаунта на следующий

                        self.update_last_used(id_active_account) # установление последнего использования активного аккаунта

                        admin_rights = ChatAdminRights(
                            change_info=False,
                            post_messages=False,
                            edit_messages=False,
                            delete_messages=False,
                            ban_users=False,
                            invite_users=False,
                            pin_messages=False,
                            add_admins=False,
                            anonymous=False,
                            manage_call=False,
                            other=False
                        )

                        # Убираем права админа
                        await main_client(EditAdminRequest(
                            channel=channel_for_admin,
                            user_id=me_active_account.id,
                            admin_rights=admin_rights,
                            rank=''
                        ))

                        if stop_invite:  # если с метода вернулось True, то необходимо остановить инвайт
                            self.task_done.emit('', self.list_used_users, False, False, False, '', True)
                            try:
                                await main_client.disconnect()
                            except UnboundLocalError:
                                pass
                            socket.socket = self.original_socket
                            self.working_witch_accounts_in_banned()
                            return

                        if self.use_proxy:  # подключение к прокси если необходимо
                            socks.set_default_proxy(socks.SOCKS5, self.ip, self.port, True, self.login, self.password)
                            socket.socket = socks.socksocket  # Установка прокси-соединения


                else:
                    self.task_done.emit('Главные аккаунты закончились!', self.list_used_users, False, False, False, '',True)
                    socket.socket = self.original_socket
                    self.working_witch_accounts_in_banned()
                    return
            except Exception as e: #  здесь обрабатываются ошибки связанные с главными аккаунтами
                try:
                    await main_client.disconnect()
                    await client.disconnect()
                except UnboundLocalError:
                    pass
                self.main_account_counter += 1

                connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
                cursor = connection.cursor()
                cursor.execute(f"SELECT user_name FROM accounts WHERE id = ? AND account_status = ?",
                               (self.main_account_counter, 'main'))
                user_name_from_db = cursor.fetchone()  # берём с БД т.к. мы можем даже не войти в аккаунт и тогда не получим его user_name для вывода
                connection.close()

                error_type = type(e)
                error_description_solution = get_description_and_solution(str(error_type.__name__))
                self.error_and_id_errors_main_accounts.append(error_description_solution)

                self.task_done.emit(f'На главном аккаунте "{user_name_from_db[0]}" произошла ошибка он будет сменён.'
                                    f'\nОшибка: {error_description_solution[0]}', [], False, False, True, '', False)


    async def invite(self, path_in_account: str, channel: InputChannel)-> bool:
        """Принимает путь к аккаунту и объект канала\n
        пример: .../accounts/active_accounts/0  \n
        Возвращает bool это флаг, что необходимо остановить приглашение (bool)\n
        """

        count_invite_with_this_accounts = 0

        if self.use_proxy: # подключение к прокси если необходимо
            socks.set_default_proxy(socks.SOCKS5, self.ip, self.port, True, self.login,self.password)  # Установка прокси-соединения
            socket.socket = socks.socksocket

        try:
            tdesk = TDesktop(f'{path_in_account}/tdata')
            client = await tdesk.ToTelethon(session=f"{path_in_account}/session.session", flag=UseCurrentSession, )
            await asyncio.wait_for(client.connect(), timeout=10)  # вход в аккаунт
            me = await client.get_me()
            test_id = me.id  # выйдет ошибка если не смогли получить данные с аккаунта
        except Exception as e:
            connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
            cursor = connection.cursor()
            cursor.execute(f"SELECT user_name FROM accounts WHERE id = ? AND account_status = ?",
                           (self.active_account_counter, 'active'))
            user_name_from_db = cursor.fetchone()  # берём с БД т.к. мы можем даже не войти в аккаунт и тогда не получим его user_name для вывода
            connection.close()

            error_type = type(e)
            error_description_solution = get_description_and_solution(str(error_type.__name__))

            self.error_and_id_errors_active_accounts.append(error_description_solution)
            self.task_done.emit(f'На аккаунте "{user_name_from_db[0]}" произошла ошибка он будет сменён.'
                                f'\nОшибка: {error_description_solution[0]}', [], False, False, True, '',False)

            socket.socket = self.original_socket
            return False

        self.task_done.emit(f'Успешно вошли в аккаунт "{me.username}"', [], False, False, False, '', False)

        for user_name in self.user_list:
            # запрос в БД на остановку инвайта
            connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
            cursor = connection.cursor()
            cursor.execute(f"SELECT stop_invite FROM stop_process")
            stop_process = cursor.fetchone()
            connection.close()
            if stop_process[0] == 1:
                try:
                    await client.disconnect()
                except UnboundLocalError:
                    pass
                self.task_done.emit('', [], False, False, False, '', False)
                self.update_user_list()
                socket.socket = self.original_socket
                return True

            if count_invite_with_this_accounts >= self.max_invite_from_one_account:
                try:
                    await client.disconnect()
                except UnboundLocalError:
                    pass
                self.update_user_list()
                self.task_done.emit(f'на аккаунте "{me.username}" достигнуто максимально количество сообщений с одного аккаунта '
                                    f'\nОн будет сменён', [], False, False, False,'', False)
                socket.socket = self.original_socket
                return False

            if self.counter_invites >= self.max_invite:
                try:
                    await client.disconnect()
                except UnboundLocalError:
                    pass
                self.update_user_list()
                self.task_done.emit(f'Достигнут лимит приглашений. Инвайт будет остановлен!', [], False, False, False, '', False)
                socket.socket = self.original_socket
                return True

            try: # блок с приглашениями
                user_temp = await client.get_entity(user_name)
                user_invite = InputUser(user_temp.id, user_temp.access_hash)  # получение другого объекта пользователя
                await client(InviteToChannelRequest(channel=channel, users=[user_invite]))  # само приглашение

                self.task_done.emit(f'Пользователь "{user_name}" успешно приглашён в группу', [], True, False, False, '', False)
                count_invite_with_this_accounts += 1
                self.counter_invites += 1
                self.list_used_users.append(user_name)

                await asyncio.sleep(self.time_sleep)
            except (errors.UsernameInvalidError, ValueError, TypeError):
                self.list_used_users.append(user_name)
                self.task_done.emit(
                    f'Пользователь с юзернеймом "{user_name}" не найден!',
                    [], False, True, False, '', False)

            except (errors.ChannelPrivateError, errors.ChatAdminRequiredError, errors.ChatWriteForbiddenError,
                    errors.UserBannedInChannelError,):
                try:
                    await client.disconnect()
                except UnboundLocalError:
                    pass
                self.update_user_list()
                self.task_done.emit(f'У активного аккаунта "{me.username}" убрали права администратора. Он будет сменён!',
                                    [], False, False, False,'', False)
                socket.socket = self.original_socket
                return False

            except (errors.InputUserDeactivatedError, errors.UserChannelsTooMuchError, errors.UserKickedError,
                    errors.UserNotMutualContactError, errors.UserPrivacyRestrictedError):
                self.update_user_list()
                self.task_done.emit(f'Аккаунт "{user_name}" не удалось пригласить в группу, из-за настроек его приватности!',
                    [], False, True, False, '', False)
                self.list_used_users.append(user_name)

            except errors.UsersTooMuchError:
                try:
                    await client.disconnect()
                except UnboundLocalError:
                    pass
                self.update_user_list()
                self.task_done.emit(f'Превышено максимальное количество пользователей в этой группе',
                                    [], False, False, False,'', False)
                socket.socket = self.original_socket
                return True
            except errors.ChatIdInvalidError:
                try:
                    await client.disconnect()
                except UnboundLocalError:
                    pass
                self.update_user_list()
                self.task_done.emit(f'Группа не найден!',[], False, False, False, 'Чат не найден!', False)
                socket.socket = self.original_socket
                return True
            except Exception as e:
                try:
                    await client.disconnect()
                except UnboundLocalError:
                    pass

                self.update_user_list()

                connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
                cursor = connection.cursor()
                cursor.execute(f"SELECT user_name FROM accounts WHERE id = ? AND account_status = ?",
                               (self.active_account_counter, 'active'))
                user_name_from_db = cursor.fetchone()  # берём с БД т.к. мы можем даже не войти в аккаунт и тогда не получим его user_name для вывода
                connection.close()

                error_type = type(e)
                error_description_solution = get_description_and_solution(str(error_type.__name__))

                self.error_and_id_errors_active_accounts.append(error_description_solution)
                self.task_done.emit(f'На аккаунте "{user_name_from_db[0]}" произошла ошибка он будет сменён.'
                                f'\nОшибка: {error_description_solution[0]}', [], False, False, True, '',False)
                socket.socket = self.original_socket
                return False

        socket.socket = self.original_socket
        try:
            await client.disconnect()
        except UnboundLocalError:
            pass
        self.update_user_list()
        self.task_done.emit('Список с аккаунтами закончился!', [], False, False, False, '', False)
        socket.socket = self.original_socket
        return True

    def update_user_list(self):
        """убираем аккаунты из списка по которым уже прошлись
        (необходимо для того что бы один и тот же аккаунт не прглашался много раз)"""
        temp_list = []
        for item in self.user_list:
            if item not in self.list_used_users:  # Проверяем, НЕТ ли текущего элемента в списке аккаунтов по которым отработали
                temp_list.append(item)
        self.user_list = temp_list

    def working_witch_accounts_in_banned(self): # необходимо вызывать когда поток закончил работу (работа с аккаунтами в бане)
        if self.error_and_id_errors_main_accounts:  # работаем с аккаунтами в которые не смогли войти
            sorted_list = sorted(self.error_and_id_errors_main_accounts, key=lambda x: x[1], reverse=True)
            # обязательно сортируем список по убыванию для того что бы корректно работать с error_handler
            for error_and_id in sorted_list:
                error_handler(error_and_id[0], error_and_id[1], 'main')

        if self.error_and_id_errors_active_accounts:
            sorted_list = sorted(self.error_and_id_errors_active_accounts, key=lambda x: x[1], reverse=True)
            for error_and_id in sorted_list:
                error_handler(error_and_id[0], error_and_id[1], 'active')

    def update_last_used(self,account_id: int):
        now = dt.datetime.now()
        last_used = now.strftime('%H:%M %d-%m-%Y')  # Форматируем дату и время согласно формату

        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()
        cursor.execute(f"UPDATE accounts SET last_used = ? WHERE id_tg = ?",(last_used, account_id))
        connection.commit()
        connection.close()


class Window_invite(QtWidgets.QMainWindow):
    root_project_dir = '..'

    invite_start = False  # отображает запущенна ли инвайт
    file_path_for_invite = ''  # путь к файлу для инвайта

    def __init__(self, switch_window):
        super().__init__()
        self.switch_window = switch_window

        self.user_name_list_to = [] # список аккаунтов до инвайта
        self.count_attempts = 0 # количество попыток

        if not os.path.isfile(
                self.root_project_dir + '/working_files/user_names_for_invite.txt'):  # если файл с user_names_for_invite.txt не существует
            with open(self.root_project_dir + '/working_files/user_names_for_invite.txt',
                      'w') as file:  # Создаем файл в режиме записи (если файл существует, он будет перезаписан)
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
        self.gridLayout_8 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_8.setContentsMargins(0, 0, 20, 0)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setContentsMargins(25, 10, -1, -1)
        self.gridLayout_7.setVerticalSpacing(10)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "border-radius: 20px;")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout.setContentsMargins(25, 10, -1, 20)
        self.gridLayout.setHorizontalSpacing(15)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setStyleSheet("")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_name_group = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_name_group.setMinimumSize(QtCore.QSize(400, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lineEdit_name_group.setFont(font)
        self.lineEdit_name_group.setStyleSheet("QLineEdit {\n"
                                               "    background-color: rgb(255, 255, 255);      /* Цвет фона текстового поля */\n"
                                               "    border: 2px solid rgb(150, 150, 150); /* Рамка текстового поля */\n"
                                               "    border-radius: 12px; /* Закругление углов */\n"
                                               "    padding: 5px; /* Отступы внутри текстового поля */\n"
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
        self.lineEdit_name_group.setObjectName("lineEdit_name_group")
        self.gridLayout.addWidget(self.lineEdit_name_group, 0, 1, 1, 1)
        self.lineEdit_delay = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_delay.setMaximumSize(QtCore.QSize(70, 16777215))
        self.lineEdit_delay.setValidator(QIntValidator())
        validator = QIntValidator(0, 99999)  # Минимум 0, максимум большое число
        self.lineEdit_delay.setValidator(validator)
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
                                          "\n"
                                          "/* Состояние для отключенного текстового поля */\n"
                                          "QLineEdit:disabled {\n"
                                          "    background-color: rgb(220, 220, 220); /* Цвет фона для отключенного */\n"
                                          "    color: rgb(170, 170, 170); /* Цвет текста для отключенного */\n"
                                          "    border: 2px solid rgb(200, 200, 200); /* Цвет рамки для отключенного */\n"
                                          "}")
        self.lineEdit_delay.setPlaceholderText("")
        self.lineEdit_delay.setObjectName("lineEdit_delay")
        self.gridLayout.addWidget(self.lineEdit_delay, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_max_invite = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_max_invite.setMaximumSize(QtCore.QSize(70, 16777215))
        validator = QIntValidator(1, 99999)  # Минимум 0, максимум большое число
        self.lineEdit_max_invite.setValidator(validator)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lineEdit_max_invite.setFont(font)
        self.lineEdit_max_invite.setStyleSheet("QLineEdit {\n"
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
        self.lineEdit_max_invite.setPlaceholderText("")
        self.lineEdit_max_invite.setObjectName("lineEdit_max_invite")
        self.gridLayout.addWidget(self.lineEdit_max_invite, 2, 1, 1, 1)
        self.checkBox_use_proxy = QtWidgets.QCheckBox(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.checkBox_use_proxy.setFont(font)
        self.checkBox_use_proxy.setStyleSheet("QCheckBox {\n"
                                              "color: rgb(0, 0, 0);\n"
                                              "    spacing: 5px; /* Отступ между иконкой и текстом */\n"
                                              "    border: none;\n"
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
        self.checkBox_use_proxy.setObjectName("checkBox_use_proxy")
        self.gridLayout.addWidget(self.checkBox_use_proxy, 4, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_11.setFont(font)
        self.label_11.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_11.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 3, 0, 1, 1)
        self.lineEdit_max_invite_from_one_account = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_max_invite_from_one_account.setMaximumSize(QtCore.QSize(70, 16777215))
        validator = QIntValidator(1, 99999)  # Минимум 0, максимум большое число
        self.lineEdit_max_invite_from_one_account.setValidator(validator)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lineEdit_max_invite_from_one_account.setFont(font)
        self.lineEdit_max_invite_from_one_account.setStyleSheet("QLineEdit {\n"
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
        self.lineEdit_max_invite_from_one_account.setPlaceholderText("")
        self.lineEdit_max_invite_from_one_account.setObjectName("lineEdit_max_invite_from_one_account")
        self.gridLayout.addWidget(self.lineEdit_max_invite_from_one_account, 3, 1, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox_2, 1, 0, 1, 3)
        self.pushButton_info = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_info.setStyleSheet("border: none;\n"
                                           "")
        self.pushButton_info.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/icon/info.png"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.pushButton_info.setIcon(icon)
        self.pushButton_info.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_info.setObjectName("pushButton_info")
        self.gridLayout_7.addWidget(self.pushButton_info, 0, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.gridLayout_7.addWidget(self.label_13, 0, 0, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setText("")
        self.label_15.setObjectName("label_15")
        self.gridLayout_7.addWidget(self.label_15, 0, 2, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_7, 0, 1, 1, 2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(20, 10, 10, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setStyleSheet("border: 0;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 826, 541))
        self.scrollAreaWidgetContents.setStyleSheet("/* СТИЛЬ ВЕРТИКАЛЬНОГО СКРОЛЛБАРА */\n"
                                                    "QScrollBar:vertical {\n"
                                                    "    border-radius: 8px;\n"
                                                    "    background: rgb(210, 210, 213);\n"
                                                    "    width: 14px;\n"
                                                    "    margin: 0px 0 0px 0;\n"
                                                    "}\n"
                                                    "\n"
                                                    "/* HANDLE BAR ВЕРТИКАЛЬНОГО СКРОЛЛБАРА */\n"
                                                    "QScrollBar::handle:vertical {  \n"
                                                    "    background-color: rgb(210, 210, 213);\n"
                                                    "    min-height: 30px;\n"
                                                    "    border-radius: 0px;\n"
                                                    "    transition: background-color 0.2s ease;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QScrollBar::handle:vertical:hover {  \n"
                                                    "    background-color: rgb(180, 180, 184);\n"
                                                    "}\n"
                                                    "\n"
                                                    "QScrollBar::handle:vertical:pressed {  \n"
                                                    "    background-color: rgb(150, 150, 153);\n"
                                                    "}\n"
                                                    "\n"
                                                    "/* КНОПКА ВВЕРХУ - ВЕРТИКАЛЬНЫЙ СКРОЛЛБАР */\n"
                                                    "QScrollBar::sub-line:vertical {\n"
                                                    "    border: none;  \n"
                                                    "    background-color: rgb(190, 190, 193);  /* Более темный серый */\n"
                                                    "    height: 15px;\n"
                                                    "    border-top-left-radius: 7px;\n"
                                                    "    border-top-right-radius: 7px;\n"
                                                    "    subcontrol-position: top;\n"
                                                    "    subcontrol-origin: margin;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QScrollBar::sub-line:vertical:hover {  \n"
                                                    "    background-color: rgb(170, 170, 174);  /* Темнее при наведении */\n"
                                                    "}\n"
                                                    "\n"
                                                    "QScrollBar::sub-line:vertical:pressed {  \n"
                                                    "    background-color: rgb(140, 140, 143);  /* Еще темнее при нажатии */\n"
                                                    "}\n"
                                                    "\n"
                                                    "/* КНОПКА ВНИЗУ - ВЕРТИКАЛЬНЫЙ СКРОЛЛБАР */\n"
                                                    "QScrollBar::add-line:vertical {\n"
                                                    "    border: none;  \n"
                                                    "    background-color: rgb(190, 190, 193);  /* Более темный серый */\n"
                                                    "    height: 15px;\n"
                                                    "    border-bottom-left-radius: 7px;\n"
                                                    "    border-bottom-right-radius: 7px;\n"
                                                    "    subcontrol-position: bottom;\n"
                                                    "    subcontrol-origin: margin;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QScrollBar::add-line:vertical:hover {  \n"
                                                    "    background-color: rgb(170, 170, 174);  /* Темнее при наведении */\n"
                                                    "}\n"
                                                    "\n"
                                                    "QScrollBar::add-line:vertical:pressed {  \n"
                                                    "    background-color: rgb(140, 140, 143);  /* Еще темнее при нажатии */\n"
                                                    "}\n"
                                                    "\n"
                                                    "/* УБРАТЬ СТРЕЛКИ */\n"
                                                    "QScrollBar::up-arrow:vertical, \n"
                                                    "QScrollBar::down-arrow:vertical {\n"
                                                    "    background: none;\n"
                                                    "}\n"
                                                    "\n"
                                                    "/* УБРАТЬ ФОН */\n"
                                                    "QScrollBar::add-page:vertical, \n"
                                                    "QScrollBar::sub-page:vertical {\n"
                                                    "    background: none;\n"
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
        self.textEdit_conclusion.setMinimumSize(QtCore.QSize(350, 370))
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
        self.gridLayout_8.addLayout(self.verticalLayout_2, 1, 1, 2, 1)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setContentsMargins(-1, 0, -1, 15)
        self.gridLayout_6.setVerticalSpacing(19)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.gridLayout_6.addWidget(self.label_7, 0, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                    "border-radius: 20px;")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_count_attempts = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_count_attempts.setFont(font)
        self.label_count_attempts.setStyleSheet("")
        self.label_count_attempts.setObjectName("label_count_attempts")
        self.gridLayout_2.addWidget(self.label_count_attempts, 3, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_10.setFont(font)
        self.label_10.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_10.setStyleSheet("")
        self.label_10.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 3, 0, 1, 1)
        self.label_banned_account = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_banned_account.setFont(font)
        self.label_banned_account.setStyleSheet("")
        self.label_banned_account.setObjectName("label_banned_account")
        self.gridLayout_2.addWidget(self.label_banned_account, 4, 1, 1, 1)
        self.label_total_sent_invitations = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_total_sent_invitations.setFont(font)
        self.label_total_sent_invitations.setStyleSheet("")
        self.label_total_sent_invitations.setObjectName("label_total_sent_invitations")
        self.gridLayout_2.addWidget(self.label_total_sent_invitations, 0, 1, 1, 1)
        self.label_unsuccessful_invitations = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_unsuccessful_invitations.setFont(font)
        self.label_unsuccessful_invitations.setStyleSheet("")
        self.label_unsuccessful_invitations.setObjectName("label_unsuccessful_invitations")
        self.gridLayout_2.addWidget(self.label_unsuccessful_invitations, 2, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("")
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 4, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_5.setStyleSheet("")
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_16.setFont(font)
        self.label_16.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_16.setStyleSheet("")
        self.label_16.setObjectName("label_16")
        self.gridLayout_2.addWidget(self.label_16, 1, 0, 1, 1)
        self.label_remaining_message = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_remaining_message.setFont(font)
        self.label_remaining_message.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_remaining_message.setStyleSheet("")
        self.label_remaining_message.setObjectName("label_remaining_message")
        self.gridLayout_2.addWidget(self.label_remaining_message, 1, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_14.setFont(font)
        self.label_14.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_14.setStyleSheet("")
        self.label_14.setObjectName("label_14")
        self.gridLayout_2.addWidget(self.label_14, 2, 0, 1, 1)
        self.gridLayout_6.addWidget(self.groupBox, 2, 1, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setMinimumSize(QtCore.QSize(0, 59))
        self.groupBox_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                      "border-radius: 20px;")
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_6 = QtWidgets.QLabel(self.groupBox_3)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.pushButton_show_user_name = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_show_user_name.sizePolicy().hasHeightForWidth())
        self.pushButton_show_user_name.setSizePolicy(sizePolicy)
        self.pushButton_show_user_name.setMinimumSize(QtCore.QSize(0, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_show_user_name.setFont(font)
        self.pushButton_show_user_name.setStyleSheet("QPushButton {\n"
                                                     "  background: rgb(210, 210, 213);\n"
                                                     "text-align: center;\n"
                                                     "border-radius: 10px;\n"
                                                     "padding-left: 5px;"
                                                     "padding-right: 5px;"
                                                     "   }\n"
                                                     "   QPushButton:hover {\n"
                                                     "          background-color: rgb(180, 180, 184); /* Цвет при наведении */\n"
                                                     "   }\n"
                                                     "\n"
                                                     "QPushButton:pressed {\n"
                                                     "                   background-color: rgb(150, 150, 153); /* Цвет фона при нажатии */\n"
                                                     "            }\n"
                                                     "")
        self.pushButton_show_user_name.setObjectName("pushButton_show_user_name")
        self.horizontalLayout.addWidget(self.pushButton_show_user_name)
        self.gridLayout_6.addWidget(self.groupBox_3, 1, 1, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_6, 1, 2, 1, 1)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setContentsMargins(-1, -1, -1, 10)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setMinimumSize(QtCore.QSize(200, 80))
        font = QtGui.QFont()
        font.setPointSize(20)
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
        self.gridLayout_5.addWidget(self.pushButton_start, 0, 0, 2, 1)
        self.pushButton_clear_conclusion = QtWidgets.QPushButton(self.centralwidget)
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
                                                       "    padding-top: 10px;"
                                                       "    padding-bottom: 10px;"
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
        self.gridLayout_5.addWidget(self.pushButton_clear_conclusion, 1, 1, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_5, 2, 2, 1, 1)
        self.scrollArea_2 = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_2.sizePolicy().hasHeightForWidth())
        self.scrollArea_2.setSizePolicy(sizePolicy)
        self.scrollArea_2.setMinimumSize(QtCore.QSize(270, 0))
        self.scrollArea_2.setMaximumSize(QtCore.QSize(270, 16777215))
        self.scrollArea_2.setStyleSheet("background-color: rgb(14, 22, 33);\n"
                                        "border: none;")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 270, 850))
        self.scrollAreaWidgetContents_2.setStyleSheet("")
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_account_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
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
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/logo.PNG"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.pushButton_account_2.setIcon(icon2)
        self.pushButton_account_2.setIconSize(QtCore.QSize(300, 60))
        self.pushButton_account_2.setCheckable(False)
        self.pushButton_account_2.setObjectName("pushButton_account_2")
        self.verticalLayout.addWidget(self.pushButton_account_2)
        self.label_9 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QtCore.QSize(0, 0))
        self.label_9.setText("")
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9)
        self.pushButton_account = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
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
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/account.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.pushButton_account.setIcon(icon3)
        self.pushButton_account.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_account.setCheckable(False)
        self.pushButton_account.setObjectName("pushButton_account")
        self.verticalLayout.addWidget(self.pushButton_account)
        self.pushButton_mailing = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
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
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/mailing.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.pushButton_mailing.setIcon(icon4)
        self.pushButton_mailing.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_mailing.setObjectName("pushButton_mailing")
        self.verticalLayout.addWidget(self.pushButton_mailing)
        self.pushButton_mailing_chat = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
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
        self.pushButton_mailing_chat.setIcon(icon4)
        self.pushButton_mailing_chat.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_mailing_chat.setObjectName("pushButton_mailing_chat")
        self.verticalLayout.addWidget(self.pushButton_mailing_chat)
        self.pushButton_invite = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
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
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/invaite.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.pushButton_invite.setIcon(icon5)
        self.pushButton_invite.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_invite.setObjectName("pushButton_invite")
        self.verticalLayout.addWidget(self.pushButton_invite)
        self.pushButton_parser = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
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
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/parser.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.pushButton_parser.setIcon(icon6)
        self.pushButton_parser.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_parser.setObjectName("pushButton_parser")
        self.verticalLayout.addWidget(self.pushButton_parser)
        self.pushButton_proxy = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
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
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/proxy.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.pushButton_proxy.setIcon(icon7)
        self.pushButton_proxy.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_proxy.setObjectName("pushButton_proxy")
        self.verticalLayout.addWidget(self.pushButton_proxy)
        self.pushButton_bomber = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
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
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/bomber.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.pushButton_bomber.setIcon(icon8)
        self.pushButton_bomber.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_bomber.setObjectName("pushButton_bomber")
        self.verticalLayout.addWidget(self.pushButton_bomber)
        self.pushButton_enter_group = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
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
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/enter_the_group.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_enter_group.setIcon(icon9)
        self.pushButton_enter_group.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_enter_group.setObjectName("pushButton_enter_group")
        self.verticalLayout.addWidget(self.pushButton_enter_group)
        self.pushButton_reactions = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
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
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/like.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        self.pushButton_reactions.setIcon(icon10)
        self.pushButton_reactions.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_reactions.setObjectName("pushButton_reactions")
        self.verticalLayout.addWidget(self.pushButton_reactions)
        self.pushButton_comment = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
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
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/coment.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        self.pushButton_comment.setIcon(icon11)
        self.pushButton_comment.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_comment.setObjectName("pushButton_comment")
        self.verticalLayout.addWidget(self.pushButton_comment)
        self.pushButton_convert = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
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
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/convert.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        self.pushButton_convert.setIcon(icon12)
        self.pushButton_convert.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_convert.setObjectName("pushButton_convert")
        self.verticalLayout.addWidget(self.pushButton_convert)
        self.pushButton_doc = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
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
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/doc.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        self.pushButton_doc.setIcon(icon13)
        self.pushButton_doc.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_doc.setObjectName("pushButton_doc")
        self.verticalLayout.addWidget(self.pushButton_doc)
        self.label_8 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QtCore.QSize(0, 0))
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout_8.addWidget(self.scrollArea_2, 0, 0, 3, 1)
        self.setCentralWidget(self.centralwidget)
        self.action = QtWidgets.QAction(self)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(self)
        self.action_2.setObjectName("action_2")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        # события
        self.pushButton_account.clicked.connect(lambda: self._transition('accounts'))
        self.pushButton_mailing.clicked.connect(lambda: self._transition('mailing_by_users'))
        self.pushButton_mailing_chat.clicked.connect(lambda: self._transition('mailing_by_chats'))
        self.pushButton_parser.clicked.connect(lambda: self._transition('parser'))
        self.pushButton_proxy.clicked.connect(lambda: self._transition('proxy'))
        self.pushButton_bomber.clicked.connect(lambda: self._transition('bomber'))
        self.pushButton_enter_group.clicked.connect(lambda: self._transition('enter_group'))
        self.pushButton_reactions.clicked.connect(lambda: self._transition('reactions'))
        self.pushButton_comment.clicked.connect(lambda: self._transition('comment'))
        self.pushButton_convert.clicked.connect(lambda: self._transition('convert'))
        self.pushButton_doc.clicked.connect(lambda: self._transition('doc'))

        self.pushButton_clear_conclusion.clicked.connect(lambda: self._clear_conclusion())
        self.pushButton_show_user_name.clicked.connect(lambda: self._show_user_name())

        self.lineEdit_name_group.focusInEvent = lambda event: self._set_default_style(self.lineEdit_name_group)
        self.lineEdit_delay.focusInEvent = lambda event: self._set_default_style(self.lineEdit_delay)
        self.lineEdit_max_invite.focusInEvent = lambda event: self._set_default_style(self.lineEdit_max_invite)
        self.lineEdit_max_invite_from_one_account.focusInEvent = lambda event: self._set_default_style(self.lineEdit_max_invite_from_one_account)

        self.pushButton_start.clicked.connect(lambda: self._start_invite())
        # события


    def _transition(self, window: str):
        if self.invite_start:
            self.show_info('Внимание!', f'Для перехода на другую вкладку необходимо остановить инвайт')
        else:
            self.switch_window(window)

    def show_info(self,title: str, message: str):
        info = Dialog_info(title, message,'notification.mp3')  # Создаем экземпляр
        info.exec_()  # Открываем

    def _show_user_name(self):
        if not os.path.isfile(
                self.root_project_dir + '/working_files/user_names_for_invite.txt'):  # если файл с user_names_for_invite.txt не существует
            with open(self.root_project_dir + '/working_files/user_names_for_invite.txt',
                      'w') as file:  # Создаем файл в режиме записи (если файл существует, он будет перезаписан)
                file.write("")  # Записываем пустую строку, чтобы создать файл

        if shutil.which('notepad.exe') is not None:  # если блокнот есть на пк
            subprocess.Popen(['notepad.exe', self.root_project_dir + '/working_files/user_names_for_invite.txt'])
        else:
            self.show_info('Внимание!', f'На вашем ПК не установлен блокнот!\n'
                                        f'Установите его или откройте файл самостоятельно\nПуть к файлу: '
                                        f'{self.root_project_dir + '/working_files/user_names_for_invite.txt'}')

    def _set_default_style(self, line_edit: QLineEdit):
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

    def _stop_invite(self):
        while True:
            try:
                connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
                cursor = connection.cursor()
                cursor.execute(f"UPDATE stop_process SET stop_invite = ?", (1,))
                connection.commit()
                connection.close()
                break
            except Exception: # если БД занята
                pass

        self.invite_start = False
        self.lineEdit_delay.setEnabled(True)
        self.lineEdit_max_invite.setEnabled(True)
        self.lineEdit_name_group.setEnabled(True)
        self.lineEdit_max_invite_from_one_account.setEnabled(True)

        current_time = dt.datetime.now()
        formatted_time = current_time.strftime("%H:%M:%S")  # Форматируем время сейчас
        self.textEdit_conclusion.append(f'\n[{formatted_time}] ИВАЙТ ОСТАНОВЛЕН')
        self.pushButton_start.setText('ЗАПУСТИТЬ')

    def _clear_conclusion(self):
        self.textEdit_conclusion.setText('')
        self.label_total_sent_invitations.setText('0')
        self.label_remaining_message.setText('0')
        self.label_unsuccessful_invitations.setText('0')
        self.label_count_attempts.setText('0')
        self.label_banned_account.setText('0')

    def _start_invite(self):
        if not self.invite_start:  # если инвайт не запущен
            style = ("QLineEdit {\n"
                     "    background-color: rgb(252, 224, 228);      /* Цвет фона текстового поля */\n"
                     "    border: 2px solid rgb(150, 150, 150); /* Рамка текстового поля */\n"
                     "    border-radius: 10px; /* Закругление углов */\n"
                     "    padding: 2px; /* Отступы внутри текстового поля */\n"
                     "    color: rgb(50, 50, 50); /* Цвет текста */\n"
                     "}\n")
            if not self.lineEdit_name_group.text():
                self.lineEdit_name_group.setStyleSheet(style)
                self.show_info('Внимание!', 'Введите имя сообщества в который необходимо приглашать!')
                return

            if not self.lineEdit_delay.text():
                self.lineEdit_delay.setStyleSheet(style)
                self.show_info('Внимание!', 'Введите задержку между приглашениями!')
                return

            if not self.lineEdit_max_invite.text():
                self.lineEdit_max_invite.setStyleSheet(style)
                self.show_info('Внимание!', 'Введите необходимое количество приглашений!')
                return

            if not self.lineEdit_max_invite_from_one_account.text():
                self.lineEdit_max_invite_from_one_account.setStyleSheet(style)
                self.show_info('Внимание!', 'Введите необходимое количество приглашений одного аккаунта!')
                return

            try:
                # Открываем файл в режиме чтения
                with open(self.root_project_dir + '/working_files/user_names_for_invite.txt', 'r') as file:
                    lines = file.readlines()  # Читаем все строки файла в список
                    list_users = [  # Фильтруем строки, оставляя только те, что соответствуют критериям
                        line.strip() for line in lines
                        if re.fullmatch(r'^(?=.*[A-Za-z])[\w@]+$', line.strip())
                        # Поиск строк с буквами и разрешёнными символами
                    ]
                    list_users = list(set(list_users))  # Удаляем повторяющиеся элементы
                    self.label_remaining_message.setText(str(len(list_users)))  # Сохраняем количество всех строк которые остались

                if len(lines) != len(list_users):
                    self.show_info('Внимание!',
                                   'Некоторые строки не были добавлены в программу,\nт.к. не соответствуют критерию возможных юзернеймов')
                if not list_users:  # если в файле user_names_for_invite.txt нет записи
                    self.show_info('Внимание!', 'В файле c юзернеймами нет ни одной корректной записи!\n'
                                                'Юзернейм может быть написан только на английскими буквами.\n'
                                                'Так же строка может содержат только "@" в самом начале юзернейма,\n'
                                                'строка может содержать спец символов "_"')
                    return
            except FileNotFoundError:  # если файл не найден
                with open(self.root_project_dir + '/working_files/user_names_for_invite.txt',
                          'w') as file:  # Создаем файл в режиме записи
                    file.write("")  # Записываем пустую строку, чтобы создать файл
                self.show_info('Внимание!', 'В файле c юзернеймами нет ни одной записи!')
                return
            except PermissionError:
                self.show_info('Внимание!', 'Закройте файл c юзернеймами!')
                return
            except UnicodeDecodeError:
                self.show_info('Внимание!',
                               'В файле с юзернеймами введены некорректные данные!\nСимволы должны быть в формате UTF-8')
                return
            except Exception:
                self.show_info('Внимание!', 'Произошла неизвестная ошибка!\nПерезапустите программу.')
                return

            if not os.path.isdir(self.root_project_dir + f'/accounts/active_accounts/0'):  # проверяем есть ли аккаунты для рассылки (это если нету)
                self.show_info('Внимание!', 'У вас нет активных аккаунтов для рассылки!')
                return

            if not os.path.isdir(self.root_project_dir + f'/accounts/main_accounts/0'):  # проверяем есть ли аккаунты для рассылки (это если нету)
                self.show_info('Внимание!', 'У вас нет главных аккаунтов для инвайта!\nОни необходимы для того что бы приглашать'
                                            'активные аккаунты \nуже с которых будут отсылаться приглашения по списку @user_name')
                return

            proxy_from_db = ['', 0, '', '']

            if self.checkBox_use_proxy.isChecked():  # проверка прокси
                connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
                cursor = connection.cursor()
                cursor.execute(f"SELECT ip,port,login,password,use_proxy_to_enter FROM proxy")
                proxy_from_db = cursor.fetchone()
                connection.close()

                efficiency = check_proxy(proxy_from_db[0], int(proxy_from_db[1]), proxy_from_db[2], proxy_from_db[3])
                if not efficiency:  # если прокси не действительно
                    error_proxy = Dialog_error_proxy(proxy_from_db[0], str(proxy_from_db[1]), proxy_from_db[2],proxy_from_db[3])
                    error_proxy.show_info()
                    error_proxy.exec_()  # Открываем
                    return

            connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
            cursor = connection.cursor()
            cursor.execute(f"UPDATE stop_process SET stop_invite = ?", (0,))
            connection.commit()
            connection.close()

            self.label_remaining_message.setText('0') # устанавливаем количество оставшихся аккаунтов на ноль

            self.user_name_list_to = list_users # устанавливанем список аккаунтов по которому будет происходить инвайт
            self.invite_start = True
            self.invite = Invait_one_stream(self.lineEdit_name_group.text(),list_users, int(self.lineEdit_delay.text()),
                                            int(self.lineEdit_max_invite.text()), int(self.lineEdit_max_invite_from_one_account.text()),
                                            self.checkBox_use_proxy.isChecked(), proxy_from_db[0],proxy_from_db[0],
                                            proxy_from_db[1],proxy_from_db[2])
            self.invite.task_done.connect(self._handler_signal)  # Подключаем сигнал к слоту
            self.invite.start()  # Запускаем поток

            current_time = dt.datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S")  # Форматируем время сейчас
            self.textEdit_conclusion.append(f'[{formatted_time}] ИНВАЙТ ЗАПУЩЕННА\n')


            self.pushButton_start.setText('ОСТАНОВИТЬ')
            self.lineEdit_delay.setEnabled(False)
            self.lineEdit_max_invite.setEnabled(False)
            self.lineEdit_name_group.setEnabled(False)
            self.lineEdit_max_invite_from_one_account.setEnabled(False)
        else:
            Dialog1 = Dialog_yes_or_cancel('Внимание!',
                                           'Вы действительно хотите остановить инвайт?',
                                           'notification.mp3')  # Создаем экземпляр
            Dialog1.data_returned.connect(self._stop_invite)  # Подключаем сигнал
            Dialog1.exec_()  # Открываем модальное окно

    def _handler_signal(self, console_output: str, user_list_used: list, successful_invitation: bool,
                        unsuccessful_invitation: bool, account_ban: bool, error: str, end_work: bool):
        """
        принимает: \n
        console_output (str) - вывод в консоль  \n
        user_list_used (list) - список user по которым прошёлся инвайт  (это если поток завершил работу) \n
        successful_invitation (bool) - флаг успешного отосланного приглашения  \n
        unsuccessful_invitation (bool) - флаг неудачного отосланного приглашения \n
        account_ban (bool) - бан аккаунта  \n
        error (str) - ошибка (значит поток завершил работу) \n
        end_work (bool) - конец работы \n
        """

        if console_output:
            current_time = dt.datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S")  # Форматируем время сейчас
            self.textEdit_conclusion.append(f'[{formatted_time}] {console_output}')

        if successful_invitation:
            new_number = int(self.label_total_sent_invitations.text()) + 1
            self.label_total_sent_invitations.setText(str(new_number))

        if unsuccessful_invitation:
            new_number = int(self.label_unsuccessful_invitations.text()) + 1
            self.label_unsuccessful_invitations.setText(str(new_number))

        if successful_invitation or successful_invitation:
            new_number = int(self.label_remaining_message.text()) - 1
            self.label_remaining_message.setText(str(new_number))

            new_number = int(self.label_count_attempts.text()) + 1
            self.label_count_attempts.setText(str(new_number))

        if account_ban:
            new_number = int(self.label_banned_account.text()) + 1
            self.label_banned_account.setText(str(new_number))

        if error:
            self.show_info('Внимание!',error)

        if user_list_used:# это аккаунты по которым отработали
            self.user_name_list_to = [item for item in self.user_name_list_to if item not in user_list_used]

        if end_work:
            self._stop_invite()

            # формируем новый список из юзернеймов (убирая юзернеймы которые использовали)
            with open(self.root_project_dir + '/working_files/user_names_for_invite.txt', 'w',encoding='utf-8') as file:
                file.write('\n'.join(self.user_name_list_to))  # объединяем все строки из списка в одну строку

            self.show_info('Готово!', 'Инвайт завершён')


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Ссылка/имя сообщества для инвайта:"))
        self.lineEdit_name_group.setToolTip(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.lineEdit_name_group.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.lineEdit_name_group.setPlaceholderText(_translate("MainWindow", "t.me/durov"))
        self.label_3.setText(_translate("MainWindow", "Необходимое количество приглашений:"))
        self.label_2.setText(_translate("MainWindow", "Задержка между приглашениями в секундах:"))
        self.checkBox_use_proxy.setText(_translate("MainWindow", "Использовать прокси"))
        self.label_11.setText(_translate("MainWindow", "Максимум приглашений с одного аккаунта: "))
        self.label_13.setText(_translate("MainWindow", " Инвайт"))
        self.label_4.setText(_translate("MainWindow", "Консоль вывода:"))
        self.textEdit_conclusion.setHtml(_translate("MainWindow",
                                                    "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                    "p, li { white-space: pre-wrap; }\n"
                                                    "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                                                    "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label_count_attempts.setText(_translate("MainWindow", "0"))
        self.label_10.setText(_translate("MainWindow", "количество попыток: "))
        self.label_banned_account.setText(_translate("MainWindow", "0"))
        self.label_total_sent_invitations.setText(_translate("MainWindow", "0"))
        self.label_unsuccessful_invitations.setText(_translate("MainWindow", "0"))
        self.label_remaining_message.setText(_translate("MainWindow", "0"))
        self.label_12.setText(_translate("MainWindow", "Забаненных аккаунтов"))
        self.label_5.setText(_translate("MainWindow", "Отправленных приглашений: "))
        self.label_16.setText(_translate("MainWindow", "Осталось приглашений: "))
        self.label_14.setText(_translate("MainWindow", "Неудачных приглашений: "))
        self.label_6.setText(_translate("MainWindow", "Файл с @user_name для рассылки:"))
        self.pushButton_show_user_name.setText(_translate("MainWindow", "Просмотр"))
        self.pushButton_start.setText(_translate("MainWindow", "ЗАПУСТИТЬ"))
        self.pushButton_clear_conclusion.setText(_translate("MainWindow", "Очистить\nконсоль"))
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
        self.action.setText(_translate("MainWindow", "сохранить"))
        self.action_2.setText(_translate("MainWindow", "добавить"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Window_invite('test')
    ui.show()
    sys.exit(app.exec_())
