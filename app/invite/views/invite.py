import re  # для проверки txt файла на правильность записи
import os  # это для действия ниже перед запуском функции
import sys  # информация о системе
import sqlite3
import datetime as dt

import socks
import socket
import asyncio
import shutil  # для удаления папки
import subprocess  # для запуска exe файлов

from opentele.td import TDesktop
from opentele.api import UseCurrentSession
from telethon import errors

from telethon.tl.functions.channels import InviteToChannelRequest, EditAdminRequest, JoinChannelRequest
from telethon.tl.types import InputUser, InputChannel, ChatAdminRights
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact

from app.general.views.info import DialogInfo
from app.general.check_proxy import check_proxy
from app.general.views.error_proxy_for_work import DialogErrorProxyForWork
from app.general.error_handler import get_description_and_solution, error_handler
from app.invite.ui.window_invite_ui import WindowInviteUi
from app.general.views.yes_or_cancel import DialogYesOrCancel

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")  # 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():  # 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path  # 3. Установка пути

# 4. Только после этого импортируем PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QLineEdit


class InvaiteOneStream(QThread): # затухание progress_bar
    task_done = pyqtSignal(str, list,bool, bool, bool, str, bool)  # Сигнал, который мы будем использовать для обновления интерфейса
    # вывод в консоль(str), количество успешных и неудачных сообщений(list), ошибка(str), конец работы(bool)

    original_socket = socket.socket  # запоминаем какой сокет был до
    def __init__(self,name_group: str, user_list: list,time_sleep: int,max_invite: int,max_invite_from_one_account: int,
                      use_proxy: bool,ip: str, port: int, login: str, password: str):
        super().__init__()
        self.root_project_dir = '..'
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

        self.main_client = None
        self.client = None
        self.me_main_account = None
        self.me_active_account = None

    def run(self):
        asyncio.run(self.run_2())

    async def run_2(self):

        if self.use_proxy: # подключение к прокси если необходимо
            socks.set_default_proxy(socks.SOCKS5, self.ip, self.port, True, self.login,self.password)  # Установка прокси-соединения
            socket.socket = socks.socksocket

        while True:
            try:
                id_main_account = 0
                if os.path.isdir(f'{self.root_project_dir}/accounts/main_accounts/{self.main_account_counter}'):
                    folder_path_main_account = f'{self.root_project_dir}/accounts/main_accounts/{self.main_account_counter}'  # путь к tdata
                    tdesk = TDesktop(f'{folder_path_main_account}/tdata')

                    self.main_client = await tdesk.ToTelethon(session=f"{folder_path_main_account}/session.session",flag=UseCurrentSession,)

                    await asyncio.wait_for(self.main_client.connect(), timeout=10)  # вход в аккаунт
                    self.me_main_account = await self.main_client.get_me()
                    id_main_account = self.me_main_account.id # выйдет ошибка если не смогли получить данные с аккаунта

                    self.task_done.emit(f'Вошли в главный аккаунт "{self.me_main_account.username}"',
                                        self.list_used_users, False, False, False,'',False)

                    # необходим для добавления во взаимные контакты
                    main_contact = InputPhoneContact(client_id=0, phone=self.me_main_account.phone,
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

                                self.client = await tdesk.ToTelethon(session=f"{folder_path_active_account}/session.session",flag=UseCurrentSession,)

                                await asyncio.wait_for(self.client.connect(), timeout=10)  # вход в аккаунт
                                self.me_active_account = await self.client.get_me()
                                id_active_account = self.me_active_account.id  # выйдет ошибка если не смогли получить данные с аккаунта

                                active_contact = InputPhoneContact(client_id=0, phone=self.me_active_account.phone,
                                                                    first_name=f"{self.me_active_account.id} ", last_name="аккаунт")
                                # Добавляем во взаимные контакты
                                await self.client(ImportContactsRequest(contacts=[main_contact])) # добавляем в контакт у активного аккаунта

                                try:
                                    channel_temp = await self.client.get_entity(self.name_group)
                                    channel = InputChannel(channel_temp.id, channel_temp.access_hash)
                                except (AttributeError, ValueError, TypeError, errors.PeerIdInvalidError):
                                    await self.client.disconnect()
                                    await self.main_client.disconnect()
                                    self.task_done.emit('Неверно указан user_name группы или группа не имеет открытый статус!',
                                                        self.list_used_users, False, False, False,
                                                        'Неверно указан user_name группы или группа не имеет открытый статус!',
                                                        True)
                                    socket.socket = self.original_socket
                                    self.working_witch_accounts_in_banned()
                                    return
                                except (errors.ChannelPrivateError, errors.ChatAdminRequiredError):
                                    await self.client.disconnect()
                                    await self.main_client.disconnect()
                                    self.task_done.emit('Невозможно пригласить в группу. Сделайте группу открытой!',
                                                        self.list_used_users, False, False, False,
                                                        'Невозможно пригласить в группу. Сделайте группу открытой!', True)
                                    socket.socket = self.original_socket
                                    self.working_witch_accounts_in_banned()
                                    return
                                except errors.RPCError as e:
                                    await self.client.disconnect()
                                    await self.main_client.disconnect()
                                    self.task_done.emit(f'Возникла ошибка: {e}!',
                                                        self.list_used_users, False, False, False, e, True)
                                    socket.socket = self.original_socket
                                    self.working_witch_accounts_in_banned()
                                    return

                                await self.client(JoinChannelRequest(channel))  # вхождение в канал

                                await self.client.disconnect()

                            else:
                                self.task_done.emit('Активные аккаунты закончились!', self.list_used_users,
                                                    False, False,False, '', True)
                                socket.socket = self.original_socket
                                self.working_witch_accounts_in_banned()
                                return

                        except Exception as e: # здесь обрабатываются ошибки связанные с активными аккаунтами
                            try:
                                await self.client.disconnect()
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

                        await self.main_client(ImportContactsRequest(contacts=[active_contact]))  # добавляем в контакт у главного аккаунта

                        try:
                            channel_temp_for_admin = await self.main_client.get_entity(self.name_group)  # для админа нужен свой канал
                            channel_for_admin = InputChannel(channel_temp_for_admin.id,channel_temp_for_admin.access_hash)  # для админа нужен свой канал
                        except (AttributeError, ValueError, TypeError, errors.PeerIdInvalidError):
                            await self.client.disconnect()
                            await self.main_client.disconnect()
                            self.task_done.emit('Неверно указан user_name группы или группа не имеет открытый статус!',
                                                self.list_used_users, False, False, False,
                                                'Неверно указан user_name группы или группа не имеет открытый статус!',
                                                True)
                            socket.socket = self.original_socket
                            self.working_witch_accounts_in_banned()
                            return
                        except (errors.ChannelPrivateError, errors.ChatAdminRequiredError):
                            await self.client.disconnect()
                            await self.main_client.disconnect()
                            self.task_done.emit('Невозможно пригласить в группу. Сделайте группу открытой!',
                                                self.list_used_users, False, False, False,
                                                'Невозможно пригласить в группу. Сделайте группу открытой!', True)
                            socket.socket = self.original_socket
                            self.working_witch_accounts_in_banned()
                            return
                        except errors.RPCError as e:
                            await self.client.disconnect()
                            await self.main_client.disconnect()
                            self.task_done.emit(f'Возникла ошибка: {e}!',
                                                self.list_used_users, False, False, False, e, True)
                            socket.socket = self.original_socket
                            self.working_witch_accounts_in_banned()
                            return

                        rights = ChatAdminRights(invite_users=True, )  # список предоставляемых разрешений

                        try:# назначение админом (в user_id необходимо передать user_name пользователя)
                            await self.main_client(EditAdminRequest(channel=channel_for_admin, user_id=self.me_active_account.id,
                                                 admin_rights=rights, rank='Админ'))

                        except errors.ChatAdminRequiredError:  # если главный аккаунт не назначен админом
                            await self.client.disconnect()
                            await self.main_client.disconnect()
                            self.main_account_counter += 1
                            self.task_done.emit(f'Главный аккаунт "{self.me_main_account.username}" не назначен админом '
                                                f'с возможностью добавлять других администраторов. Он будет пропущен!',
                                                [], False, False, False, '', False)
                            break

                        except errors.AdminsTooMuchError:  # если админов слишком много
                            await self.client.disconnect()
                            await self.main_client.disconnect()
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
                            await self.client.disconnect()
                            await self.main_client.disconnect()
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
                        await self.main_client(EditAdminRequest(
                            channel=channel_for_admin,
                            user_id=self.me_active_account.id,
                            admin_rights=admin_rights,
                            rank=''
                        ))

                        if stop_invite:  # если с метода вернулось True, то необходимо остановить инвайт
                            self.task_done.emit('', self.list_used_users, False, False, False, '', True)
                            try:
                                await self.main_client.disconnect()
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
                    await self.main_client.disconnect()
                    await self.client.disconnect()
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
            try:
                tdesk = TDesktop(f'{path_in_account}/tdata')
                self.client = await tdesk.ToTelethon(session=f"{path_in_account}/session.session", flag=UseCurrentSession, )
                await asyncio.wait_for(self.client.connect(), timeout=10)  # вход в аккаунт
                me = await self.client.get_me()
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
                        await self.client.disconnect()
                    except UnboundLocalError:
                        pass
                    self.task_done.emit('', [], False, False, False, '', False)
                    self.update_user_list()
                    socket.socket = self.original_socket
                    return True

                if count_invite_with_this_accounts >= self.max_invite_from_one_account:
                    try:
                        await self.client.disconnect()
                    except UnboundLocalError:
                        pass
                    self.update_user_list()
                    self.task_done.emit(f'на аккаунте "{me.username}" достигнуто максимально количество сообщений с одного аккаунта '
                                        f'\nОн будет сменён', [], False, False, False,'', False)
                    socket.socket = self.original_socket
                    return False

                if self.counter_invites >= self.max_invite:
                    try:
                        await self.client.disconnect()
                    except UnboundLocalError:
                        pass
                    self.update_user_list()
                    self.task_done.emit(f'Достигнут лимит приглашений. Инвайт будет остановлен!', [], False, False, False, '', False)
                    socket.socket = self.original_socket
                    return True

                try: # блок с приглашениями
                    user_temp = await self.client.get_entity(user_name)
                    user_invite = InputUser(user_temp.id, user_temp.access_hash)  # получение другого объекта пользователя
                    await self.client(InviteToChannelRequest(channel=channel, users=[user_invite]))  # само приглашение

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
                        await self.client.disconnect()
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
                        await self.client.disconnect()
                    except UnboundLocalError:
                        pass
                    self.update_user_list()
                    self.task_done.emit(f'Превышено максимальное количество пользователей в этой группе',
                                        [], False, False, False,'', False)
                    socket.socket = self.original_socket
                    return True
                except errors.ChatIdInvalidError:
                    try:
                        await self.client.disconnect()
                    except UnboundLocalError:
                        pass
                    self.update_user_list()
                    self.task_done.emit(f'Группа не найден!',[], False, False, False, 'Чат не найден!', False)
                    socket.socket = self.original_socket
                    return True
                except Exception as e:
                    try:
                        await self.client.disconnect()
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
        except asyncio.exceptions.CancelledError: # если экстренно остановили поток и в методе который вызывается с await может произойти такая ошибка
            socket.socket = self.original_socket
            return True

        socket.socket = self.original_socket
        try:
            await self.client.disconnect()
        except UnboundLocalError:
            pass
        self.update_user_list()
        self.task_done.emit('Список с аккаунтами закончился!', [], False, False, False, '', False)
        socket.socket = self.original_socket
        return True

    def update_user_list(self):
        """убираем аккаунты из списка по которым уже прошлись
        (необходимо для того что бы один и тот же аккаунт не приглашался много раз)"""
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

    async def quit_async(self):
        """Асинхронный метод для завершения потока"""
        try:
            await self.client.disconnect()
            await self.main_client.disconnect()
        except Exception:
            pass

        self.task_done.emit(f'',[], False, False, False, '', True)
        self.terminate()  # Принудительное завершение

class WindowInvite(WindowInviteUi):
    def __init__(self, switch_window):
        super().__init__()
        self.root_project_dir = '..'
        self.invite_start = False  # отображает запущенна ли инвайт
        self.file_path_for_invite = ''  # путь к файлу для инвайта
        self.switch_window = switch_window

        self.user_name_list_to = []  # список аккаунтов до инвайта
        self.count_attempts = 0 # количество попыток

        self.active_threads = [] # хранит активные потоки

        if not os.path.isfile(
                self.root_project_dir + '/working_files/user_names_for_invite.txt'):  # если файл с user_names_for_invite.txt не существует
            with open(self.root_project_dir + '/working_files/user_names_for_invite.txt',
                      'w') as file:  # Создаем файл в режиме записи (если файл существует, он будет перезаписан)
                file.write("")  # Записываем пустую строку, чтобы создать файл

        # события
        self.pushButton_account.clicked.connect(lambda: self._transition('accounts'))
        self.pushButton_mailing.clicked.connect(lambda: self._transition('mailing_by_users'))
        self.pushButton_mailing_chat.clicked.connect(lambda: self._transition('mailing_by_chats'))
        self.pushButton_parser.clicked.connect(lambda: self._transition('parser'))
        self.pushButton_proxy.clicked.connect(lambda: self._transition('proxy'))
        self.pushButton_bomber.clicked.connect(lambda: self._transition('bomber'))
        self.pushButton_create_channel.clicked.connect(lambda: self._transition('create_channel'))
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
        info = DialogInfo(title, message,'notification.mp3')  # Создаем экземпляр
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

        for thread in self.active_threads:
            asyncio.run(thread.quit_async())
        self.active_threads.clear()

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
                    error_proxy = DialogErrorProxyForWork(proxy_from_db[0], str(proxy_from_db[1]), proxy_from_db[2],proxy_from_db[3])
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

            thread = self.invite = InvaiteOneStream(self.lineEdit_name_group.text(),list_users, int(self.lineEdit_delay.text()),
                                            int(self.lineEdit_max_invite.text()), int(self.lineEdit_max_invite_from_one_account.text()),
                                            self.checkBox_use_proxy.isChecked(), proxy_from_db[0],proxy_from_db[0],
                                            proxy_from_db[1],proxy_from_db[2])
            self.invite.task_done.connect(self._handler_signal)  # Подключаем сигнал к слоту
            self.invite.start()  # Запускаем поток

            self.active_threads.append(thread)

            current_time = dt.datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S")  # Форматируем время сейчас
            self.textEdit_conclusion.append(f'[{formatted_time}] ИНВАЙТ ЗАПУЩЕННА\n')


            self.pushButton_start.setText('ОСТАНОВИТЬ')
            self.lineEdit_delay.setEnabled(False)
            self.lineEdit_max_invite.setEnabled(False)
            self.lineEdit_name_group.setEnabled(False)
            self.lineEdit_max_invite_from_one_account.setEnabled(False)
        else:
            Dialog1 = DialogYesOrCancel('Внимание!',
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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = WindowInvite('test')
    ui.show()
    sys.exit(app.exec_())
