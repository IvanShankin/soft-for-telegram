import os
import sys
import sqlite3
import time

import PyQt5
from pathlib import Path
import datetime as dt
import socks
import socket
import asyncio
import itertools
import random
import requests

from opentele.td import TDesktop
from opentele.api import UseCurrentSession
from opentele.exception import TFileNotFound
from telethon.tl.functions.channels import CreateChannelRequest, UpdateUsernameRequest, EditPhotoRequest
from telethon.tl.types import InputChatUploadedPhoto
from telethon import errors

from app.general.views.info import DialogInfo
from app.general.check_proxy import check_proxy
from app.general.views.error_proxy_for_work import DialogErrorProxyForWork
from app.general.error_handler import get_description_and_solution, error_handler
from app.create_channel.views.first_message_for_group import DialogFirstMessage
from app.create_channel.views.user_name_for_channel import DialogUserNameForChannel
from app.create_channel.views.list_created_channel import DialogListCreateChannel
from app.create_channel.ui.window_create_channel_ui import WindowCreateChannelUi

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")  # 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():  # 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path  # 3. Установка пути

# Только после этого импортируем PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QLineEdit


class CreatingChannelWithStreams(QThread): # затухание progress_bar
    """
            __init__:
            :param id_account: id аккаунта (из активных аккаунтов)
            :param channel_name: имя канала
            :param delay: задержка между созданием каналов
            :param max_channel_from_one_account: максимум созданных каналов с одного аккаунта
            :param avatar_path: флаг необходимости установить аватар у канала и путь к нему
            :param send_first_message: переменная с главного окна
            :param user_name: user_name и флаг необходимости его установления
            :param set_numbers_end_user_name: флаг необходимости устанавливать цифры в конце user_name если такой занят
            :param description: описание и флаг необходимости его установления
            :param use_proxy: флаг необходимости прокси
            :param ip: данные прокси
            :param port: данные прокси
            :param login: данные прокси
            :param password: данные прокси
            """
    task_done = pyqtSignal(str, list, bool, list, list, str, list, bool)  # Сигнал, который мы будем использовать для обновления интерфейса
    # вывод в консоль(str), количество успешных и неудачных сообщений(list), ошибка прокси(bool), ошибка(str), конец работы(bool)

    def __init__(self,id_account: int, channel_name: list, delay: int, max_channel_from_one_account: int,
                 avatar_path: list,
                 send_first_message: dict,
                 user_name: list, set_numbers_end_user_name: bool,
                 description: list,
                 use_proxy: bool,ip: str, port: int, login: str, password: str):

        super().__init__()
        self.root_project_dir = '..'
        self.id_account = id_account
        self.channel_name = channel_name
        self.delay = delay
        self.max_channel_from_one_account = max_channel_from_one_account
        self.avatar_path = avatar_path
        self.send_first_message = send_first_message
        self.user_name = user_name
        self.set_numbers_end_user_name = set_numbers_end_user_name
        self.description = description
        self.use_proxy = use_proxy
        self.ip = ip
        self.port = port
        self.login = login
        self.password = password

        self.client = None
        self.me = None
        self.successful_create_channel = 0
        self.failed_create_channel = 0
        self.account_id = 0
        self.last_used = ''
        self.user_name_created_channel = [] # список имён созданных каналов

    def run(self):
        asyncio.run(self.run_2())

    async def run_2(self):
        if self.use_proxy:
            socks.set_default_proxy(socks.SOCKS5, self.ip, self.port, True, self.login, self.password)
            socket.socket = socks.socksocket

        try:  # пытаемся войти в аккаунт
            folder_path_account = self.root_project_dir + f'/accounts/active_accounts/{self.id_account}'  # путь к tdata
            tdesk = TDesktop(folder_path_account + '/tdata')

            self.client = await tdesk.ToTelethon(session=f"{folder_path_account}/session.session", flag=UseCurrentSession, )

            await asyncio.wait_for(self.client.connect(), timeout=7)  # вход в аккаунт
            self.me = await self.client.get_me()
            self.account_id = self.me.id

            self.task_done.emit(f'Запущенно создание с аккаунта "{self.me.username}"', [],False, [], [], '', [], False)

            for counter in range(self.max_channel_from_one_account):
                channel_description = ''

                if self.description:
                    channel_description = self.description[counter]


                now = dt.datetime.now()  # Получаем время именно тут, т.к. может возникнут ошибка и это тоже считается как использование аккаунта
                self.last_used = now.strftime('%H:%M %d-%m-%Y')  # Форматируем дату и время согласно формату

                result = await  self.client(CreateChannelRequest(
                    title=self.channel_name[counter],
                    about=channel_description,
                    megagroup=False,  # False - для канала, True - для супергруппы
                ))

                channel_id =  result.chats[0].id

                error_change_user_name = False
                if self.user_name:
                    user_name_channel = self.user_name[counter]
                    while True:
                        try:
                            await self.client(UpdateUsernameRequest(
                            channel=channel_id,
                            username=user_name_channel))
                            self.user_name_created_channel.append(user_name_channel)
                            break
                        except errors.ChannelsAdminPublicTooMuchError:
                            self.task_done.emit(
                                f'Аккаунт "{self.me.username}" являетесь администратором слишком большого '
                                f'количества общедоступных каналов (максимум 10). Сделайте некоторые каналы закрытыми.\n'
                                f'Созданных каналов: {self.successful_create_channel} из {self.max_channel_from_one_account}',
                                [self.successful_create_channel, self.failed_create_channel], False, [self.account_id, self.last_used],
                                self.user_name_created_channel,'', [],
                                True)
                            try:
                                await self.client.disconnect()
                            except UnboundLocalError:
                                pass
                            return
                        # exception 1.если некорректный user_name 2.если такой user_name уже установлен у этого канала
                        except (errors.UsernameInvalidError, errors.UsernameNotModifiedError):
                            self.failed_create_channel += 1
                            error_change_user_name = True
                            break
                        except (errors.UsernameOccupiedError, errors.UsernamePurchaseAvailableError):  # если user_name занят
                            if self.set_numbers_end_user_name:
                                random_digits = ''.join([str(random.randint(0, 9)) for _ in range(4)])
                                user_name_channel = self.user_name[counter] + random_digits
                            else:
                                self.failed_create_channel += 1
                                error_change_user_name = True
                                break

                if error_change_user_name:
                    continue

                if self.avatar_path:
                    try:
                        uploaded_file = await  self.client.upload_file(random.choice(self.avatar_path)) # Загружаем фото
                    except FileNotFoundError:
                        self.task_done.emit(f'', [self.successful_create_channel, self.failed_create_channel], False,
                                            [self.account_id, self.last_used], self.user_name_created_channel,
                                            'Ошибка установления аватара!\nНе удалось установить фото в аватар канала!\n'
                                            'Проверьте папку с фото для случайного выбора!', [], True)
                        try:
                            await self.client.disconnect()
                        except UnboundLocalError:
                            pass
                        return

                    input_photo = InputChatUploadedPhoto(# Создаем объект InputChatUploadedPhoto
                        file=uploaded_file,
                        video=None,
                        video_start_ts=None,
                        video_emoji_markup=None
                    )

                    try:# Устанавливаем фото для канала
                        await self.client(EditPhotoRequest(
                            channel=channel_id,
                            photo=input_photo
                        ))
                    except errors.PhotoInvalidError: # если фотография недействительна
                        self.failed_create_channel += 1
                        continue

                error_sent_message = False
                if self.send_first_message['use_new_message']:
                    try:
                        if self.send_first_message['use_file_for_message']:
                            file_extension = os.path.splitext(self.send_first_message['file_path'])[1]
                            if  (file_extension == '.jpg' or file_extension == '.jpeg' or file_extension == '.png' or
                                file_extension == '.gif'):
                                await self.client.send_file(
                                    entity=channel_id,
                                    file=self.send_first_message['file_path'],
                                    caption= self.send_first_message['message'],
                                    force_document = False # Важно! False - отправка как фото
                                )
                            else:
                                await self.client.send_file(
                                    entity=channel_id,
                                    file=self.send_first_message['file_path'],
                                    caption=self.send_first_message['message']
                                )
                        else:
                            await self.client.send_message(
                                entity=channel_id,
                                message=self.send_first_message['file_path'],
                                parse_mode='html'
                            )
                    except FileNotFoundError:
                        self.task_done.emit(f'',[self.successful_create_channel, self.failed_create_channel], False,
                                            [self.account_id, self.last_used], self.user_name_created_channel,
                                            'Ошибка отсылки файла!\nДобавьте новый файл', [],True)
                        error_sent_message = True
                    except errors.MessageEmptyError:
                        self.task_done.emit(f'', [self.successful_create_channel, self.failed_create_channel], False,
                                            [self.account_id, self.last_used], self.user_name_created_channel,
                                            'Ошибка отправки сообщения!\nСообщение в недопустимом формате UTF-8', [], True)
                        error_sent_message = True
                    except errors.MessageTooLongError:
                        self.task_done.emit(f'', [self.successful_create_channel, self.failed_create_channel], False,
                                            [self.account_id, self.last_used], self.user_name_created_channel,
                                            'Ошибка отправки сообщения!\nСообщение слишком длинное.'
                                             '\nМаксимальная длинная сообщения без файла = 4024 символов в UTF-8\n'
                                             'С файлом 1024 символов в UTF-8', [],True)
                        error_sent_message = True
                    except (errors.ImageProcessFailedError, errors.PhotoInvalidError, errors.MediaInvalidError):
                        self.task_done.emit(f'', [self.successful_create_channel, self.failed_create_channel], False,
                                            [self.account_id, self.last_used], self.user_name_created_channel,
                                            'Ошибка отправки сообщения!\nФайл прикреплённый к сообщению невозможно отправить!\n'
                                            'Поменяйте его!',
                                            [], True)
                        error_sent_message = True


                if self.send_first_message['use_the_forwarded_message']:
                    try:
                        # target_entity = await client.get_entity(self.send_first_message['user_name_channel'])
                        await self.client.forward_messages(
                            entity=channel_id, # куда необходимо отослать
                            messages=int(self.send_first_message['message_ID']),
                            from_peer=self.send_first_message['user_name_channel'] # заменить везде на такое значение (здесь необходимо писать user_name)
                        )
                    except (errors.BroadcastPublicVotersForbiddenError, errors.ChannelPrivateError,
                            errors.ChatAdminRequiredError, errors.MediaEmptyError, errors.QuizAnswerMissingError,
                            errors.TopicDeletedError):
                        self.task_done.emit(f'',
                                            [self.successful_create_channel, self.failed_create_channel], False,
                                            [self.account_id, self.last_used], self.user_name_created_channel,
                                            'Ошибка отправки сообщения!\nНевозможно переслать данное сообщение!', [],
                                            True)
                        error_sent_message = True
                    except (ValueError, errors.MessageIdsEmptyError, errors.ChannelInvalidError, errors.MessageIdInvalidError) as e:
                        self.task_done.emit(f'',
                                            [self.successful_create_channel, self.failed_create_channel], False,
                                            [self.account_id, self.last_used], self.user_name_created_channel,
                                            'Ошибка отправки сообщения!\nНеверные данные для пересылки сообщения!', [],
                                            True)
                        error_sent_message = True

                if error_sent_message:
                    try:
                        await self.client.disconnect()
                    except UnboundLocalError:
                        pass
                    return

                self.successful_create_channel += 1
                await asyncio.sleep(self.delay)
        except asyncio.exceptions.CancelledError: # если экстренно остановили поток и в методе который вызывается с await может произойти такая ошибка
            return
        except (Exception, TFileNotFound) as e:  # здесь ошибки с аккаунтом откуда отсылаем
            try:
                await self.client.disconnect()
            except UnboundLocalError:
                pass

            connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
            cursor = connection.cursor()
            cursor.execute(f"SELECT user_name FROM accounts WHERE id = ? AND account_status = ?",(self.id_account, 'active'))
            user_name_from_db = cursor.fetchone()  # берём с БД т.к. мы можем даже не войти в аккаунт и тогда не получим его user_name для вывода
            connection.close()

            error_type = type(e)
            error_description_solution = get_description_and_solution(str(error_type.__name__))
            self.task_done.emit(f'На аккаунте "{user_name_from_db[0]}" произошла ошибка он будет убран из активных.\nОшибка: '
                                f'{error_description_solution[0]}\nСозданных каналов: {self.successful_create_channel} из {self.max_channel_from_one_account}',
                                [self.successful_create_channel, self.failed_create_channel], True, [self.account_id, self.last_used],
                                self.user_name_created_channel, '',[str(error_type.__name__), self.id_account], True)
            return

        self.task_done.emit(f'Аккаунт "{self.me.username}" закончил создание\nСозданных каналов: {self.successful_create_channel} из {self.max_channel_from_one_account}',
            [self.successful_create_channel, self.failed_create_channel], False,
            [self.account_id, self.last_used], self.user_name_created_channel, '', [],True)
        try:
            await self.client.disconnect()
        except UnboundLocalError:
            pass
        return


    async def quit_async(self):
        """Асинхронный метод для завершения потока"""
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

        if user_name_from_db[0]:
            user_name = user_name_from_db[0]
        else:
            user_name = "None"

        self.task_done.emit(
            f'Вы остановили создание каналов с аккаунта: "{user_name}"'
            f'\nСозданных каналов: {self.successful_create_channel} из {self.max_channel_from_one_account}',
            [self.successful_create_channel, self.failed_create_channel], False,
            [self.account_id, self.last_used], self.user_name_created_channel, '', [], True)
        self.terminate()  # Принудительное завершение


class WindowCreateChannel(WindowCreateChannelUi):
    def __init__(self, switch_window):
        super().__init__()
        self.switch_window = switch_window

        self.root_project_dir = '..'

        self.data_first_message = {
            'message': '',
            'user_name_channel': '',
            'message_ID': '',
            'file_path': '',
            'use_file_for_message': False,
            'use_new_message': False,
            'use_the_forwarded_message': False
        }

        self.data_for_user_name_channel = {
            'first_list': '',
            'second_list': '',
            'third_list': '',
            'use_first_list': False,
            'use_second_list': False,
            'use_third_list': False,
            'set_numbers_end_user_name': False,
        }

        self.active_threads = []  # ВАЖНО! хранит в себе запущенные потоки
        self.launched_create = False  # отображает запущенно ли создание
        self.original_socket = socket.socket  # проки который был до
        self.id_and_last_use = []  # хранит массивы в которых tg_id аккаунта и его последнее использование
        self.quantity_accounts_for_create_channel = 0  # количество аккаунтов для создания каналов
        self.quantity_accounts_ending_create_channel = 0  # количество аккаунтов закончивших рассылку
        self.error_and_id_errors_accounts = []  # хранит массивы в которых ошибка и id папки, где произошла эта ошибка
        self.user_names_created_channel = [] # user_name список созданных каналов

        self.count_attempts = 0 # количество попыток создания канала

        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()
        cursor.execute(f"SELECT "
                       f"name, "
                       f"description, "
                       f"max_creating_channel_from_one_account, "
                       f"delay, "
                       f"first_user_name_list, "
                       f"second_user_name_list, "
                       f"third_user_name_list,  "
                       f"new_message, "
                       f"forwarding_username, "
                       f"forwarding_id_message "
                       f"FROM saved_data_creating_channels")
        data_from_db = cursor.fetchone()  # берём с БД т.к. мы можем даже не войти в аккаунт и тогда не получим его user_name для вывода
        connection.close()

        # заполнение данных с БД
        self.textEdit_name_channel_list.setText(data_from_db[0])
        self.textEdit_description_list.setText(data_from_db[1])
        self.lineEdit_max_create_channel_from_one_account.setText(data_from_db[2])
        self.lineEdit_delay.setText(data_from_db[3])
        self.data_for_user_name_channel['first_list'] = data_from_db[4]
        self.data_for_user_name_channel['second_list'] = data_from_db[5]
        self.data_for_user_name_channel['third_list'] = data_from_db[6]
        self.data_first_message['message'] = data_from_db[7]
        self.data_first_message['user_name_channel'] = data_from_db[8]
        self.data_first_message['message_ID'] = data_from_db[9]

        # события
        self.pushButton_account.clicked.connect(lambda: self._transition('accounts'))
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

        self.pushButton_clear_conclusion.clicked.connect(lambda: self._clear_conclusion())
        self.pushButton_info_streams.clicked.connect(lambda: self._info_streams())
        self.pushButton_info_list_description.clicked.connect(lambda: self._info_list_description())
        self.pushButton_info_list_name_channel.clicked.connect(lambda: self._info_list_name_channel())

        self.lineEdit_max_create_channel_from_one_account.focusInEvent = lambda event: self._set_default_style_line_edit(
            self.lineEdit_max_create_channel_from_one_account)
        self.lineEdit_delay.focusInEvent = lambda event: self._set_default_style_line_edit(
            self.lineEdit_delay)
        self.lineEdit_quantity_streams.focusInEvent = lambda event: self._set_default_style_line_edit(
            self.lineEdit_quantity_streams)

        self.textEdit_name_channel_list.focusInEvent = lambda event: self._set_default_style_text_edit(
            self.textEdit_name_channel_list)
        self.textEdit_description_list.focusInEvent = lambda event: self._set_default_style_text_edit(
            self.textEdit_description_list)

        self.lineEdit_quantity_streams.textChanged.connect(lambda: self._line_edit_quantity_editing_finished())

        self.pushButton_random_choice_photo.clicked.connect(lambda: self._choice_photo())
        self.pushButton_choose_file_for_mailing.clicked.connect(lambda: self._choose_file_for_mailing())
        self.pushButton_choose_user_name.clicked.connect(lambda: self._choose_user_name())

        self.pushButton_start.clicked.connect(lambda: self._start())

        self.textEdit_name_channel_list.focusLost.connect(self._update_data_in_db) # ЭТО СОБЫТИЕ СОЗДАННО В ПЕРЕОПРЕДЕЛЁННОМ КЛАСС
        self.textEdit_description_list.focusLost.connect(self._update_data_in_db) # ЭТО СОБЫТИЕ СОЗДАННО В ПЕРЕОПРЕДЕЛЁННОМ КЛАСС
        self.lineEdit_max_create_channel_from_one_account.editingFinished.connect(lambda: self._update_data_in_db(
            self.lineEdit_max_create_channel_from_one_account.text(), 'max_creating_channel_from_one_account'))
        self.lineEdit_delay.editingFinished.connect(lambda: self._update_data_in_db(
            self.lineEdit_delay.text(), 'delay'))

        # события

    def _transition(self, target_window: str):
        if self.launched_create:
            error_info = DialogInfo('Внимание!',
                                     'Дождитесь конца создания каналов или остановите его!',
                                     'notification.mp3')  # Создаем экземпляр
            error_info.exec_()  # Открываем
        else:
            self.switch_window(target_window)

    def _update_data_in_db(self, data, column):
        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()
        cursor.execute(f"UPDATE saved_data_creating_channels SET {column} = ?",(data,))
        connection.commit()
        connection.close()

    def _set_default_style_line_edit(self,line_edit: QLineEdit):
        line_edit.setStyleSheet("""QLineEdit {
         background-color: rgb(255, 255, 255);      /* Цвет фона текстового поля */
         border: 2px solid rgb(150, 150, 150); /* Рамка текстового поля */
         border-radius: 6px; /* Закругление углов */
         padding: 2px; /* Отступы внутри текстового поля */
         color: rgb(50, 50, 50); /* Цвет текста */
         }
        
         /* Состояние при наведении */
         QLineEdit:hover {
             border: 2px solid rgb(160, 160, 160); /* Цвет рамки при наведении */
         }
        
         /* Состояние при фокусировке */
         QLineEdit:focus {
             border: 2px solid rgb(0, 0, 0); /* Цвет рамки при фокусировке */
             background-color: rgb(255, 255, 255); /* Цвет фона при фокусировке */
         }
        
         /* Состояние для отключенного текстового поля */
         QLineEdit:disabled {
             background-color: rgb(220, 220, 220); /* Цвет фона для отключенного */
             color: rgb(170, 170, 170); /* Цвет текста для отключенного */
             border: 2px solid rgb(200, 200, 200); /* Цвет рамки для отключенного */
         }""")

    def _set_default_style_text_edit(self,text_edit: QTextEdit):
        text_edit.setStyleSheet(
        """
        background-color: rgb(255, 255, 255);
        border-radius: 20px;
        padding-top: 15px; /* Отступ только слева */   
        padding-bottom: 15px; /* Отступ только снизу */
        """)

    def _clear_conclusion(self):
        self.textEdit_conclusion.setText('')
        self.label_successfully.setText('0')
        self.label_unsuccessful.setText('0')
        self.label_count_attempts.setText('0')
        self.label_banned_account.setText('0')

    def _info_streams(self):
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

        info = DialogInfo('Информация',
                           f'Количество потоков - это сколько аккаунтов\nбудут одновременно выполнять создание канала.'
                           f'\n\nВнимание!\nКоличество потоков не может превышать количество аккаунтов.\n'
                           f'Ваш лимит {message}',
                           'notification.mp3')  # Создаем экземпляр
        info.exec_()  # Открываем

    def _info_list_description(self):
        info = DialogInfo('Информация',
                           f'Из данного списка будет случайно выбрано описание,\n'
                           f'если описание одно, то можно не указывать разделение\n\n'
                           f'Описания разделяется по этому символу: &\n',
                           'notification.mp3')  # Создаем экземпляр
        info.exec_()  # Открываем

    def _info_list_name_channel(self):
        info = DialogInfo('Информация',
                           f'Из данного списка будет случайно выбрано имя для канала\n\n'
                           f'Имена разделяется по переходу на новую строку\n',
                           'notification.mp3')  # Создаем экземпляр
        info.exec_()  # Открываем

    def _choice_photo(self):
        path = os.path.abspath(self.root_project_dir + "/working_files/for_create_channel/photo_for_avatar_channel")
        os.startfile(path)

    def _choose_file_for_mailing(self):
        dialog = DialogFirstMessage(self.data_first_message)  # Создаем экземпляр
        dialog.data_returned.connect(self._set_data_for_first_message)  # Подключаем сигнал
        dialog.exec_()  # Открываем модальное окно

    def _choose_user_name(self):
        dialog = DialogUserNameForChannel(self.data_for_user_name_channel)  # Создаем экземпляр
        dialog.data_returned.connect(self._set_data_for_user_name_channel)  # Подключаем сигнал
        dialog.exec_()  # Открываем модальное окно

    def _set_data_for_first_message(self, data: dict):
        self.data_first_message = data

    def _set_data_for_user_name_channel(self, data: dict):
        self.data_for_user_name_channel = data

    def _line_edit_quantity_editing_finished(self):
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

    def _set_enabled_for_elements(self, enabled: bool):
        self.lineEdit_max_create_channel_from_one_account.setEnabled(enabled)
        self.lineEdit_delay.setEnabled(enabled)
        self.lineEdit_quantity_streams.setEnabled(enabled)
        self.textEdit_name_channel_list.setReadOnly(enabled)
        self.textEdit_description_list.setReadOnly(enabled)
        self.checkBox_random_choice_photo.setEnabled(enabled)
        self.checkBox_mailing_first_message.setEnabled(enabled)
        self.checkBox_set_user_name.setEnabled(enabled)
        self.checkBox_set_description.setEnabled(enabled)
        self.checkBox_use_proxy.setEnabled(enabled)

    def _generate_unique_user_name(self, data: list[str])-> dict:
        """Генерирует уникальные имена пользователей из входных данных.

        Разделяет строки по переходам на новую строку, проверяет их на соответствие
        критериям валидности и возвращает словарь с результатами.

        Args:
            data (list[str]): Список строк, содержащих потенциальные имена пользователей.
                Каждая строка может содержать несколько имён, разделённых переводом строки.

        Returns:
            dict: Словарь с двумя ключами:
                - "user_names" (list): Список валидных имён пользователей.
                - "there_are_inappropriate_values" (bool): Флаг, указывающий на наличие
                  невалидных имён во входных данных.
        """
        generated_list = []
        try:
            counter = 0
            while True:
                generated_list.append(data[counter].lower().split('\n'))
                counter += 1
        except IndexError:
            pass

        if len(generated_list) == 1:
            user_name_list = generated_list[0]
        else:
            combinations = itertools.product(*generated_list)  # Генерируем все возможные комбинации
            user_name_list = [''.join(combination) for combination in combinations]  # Объединяем слова в каждой комбинации

        result = []
        there_are_inappropriate_values = False
        for user_name in user_name_list:
            if len(user_name) < 5 or len(user_name) > 32:
                there_are_inappropriate_values = True
                continue
            if user_name[0] == '_':
                there_are_inappropriate_values = True
                continue
            if user_name == "admin" or user_name == "telegram" or user_name == "support":
                there_are_inappropriate_values = True
                continue
            if user_name[0].isdigit(): # если первый символ цифра
                there_are_inappropriate_values = True
                continue
            result.append(user_name)

        result = list((set(result))) # убираем повторяющиеся элементы
        random.shuffle(result)  # перемешивание всех элементов списка

        return {"user_names": result, "there_are_inappropriate_values": there_are_inappropriate_values}

    def _handler_signal_with_streams(self, console_output: str, counter_sent_and_unsuccessful_message: list,
                                    account_banned: bool, id_and_last_use: list, user_names_created_channel: list,
                                    error: str, error_and_id_account: list, end_create_from_this_account: bool):
        if console_output:
            current_time = dt.datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S")  # Форматируем время сейчас
            self.textEdit_conclusion.append(f'[{formatted_time}] {console_output}')

        if counter_sent_and_unsuccessful_message:
            self.count_attempts += counter_sent_and_unsuccessful_message[0] + counter_sent_and_unsuccessful_message[1]
            self.label_successfully.setText(str(counter_sent_and_unsuccessful_message[0] + int(self.label_successfully.text())))
            self.label_unsuccessful.setText(str(counter_sent_and_unsuccessful_message[1] + int(self.label_unsuccessful.text())))
            self.label_count_attempts.setText(str(counter_sent_and_unsuccessful_message[0] + counter_sent_and_unsuccessful_message[1] + int(self.label_count_attempts.text())))

        if account_banned:
            self.label_banned_account.setText( str(int(self.label_banned_account.text()) + 1))

        if id_and_last_use: # добавление для учёта времени последнего использования аккаунта (такое возращается только один раз с одного аккаунта)
            if id_and_last_use[1]:# будем работать если есть время последнего использования
                self.id_and_last_use.append(id_and_last_use)

        if error:
            if self.launched_create: # если создание запущено
                self._set_enabled_for_elements(True)
                self.launched_create = False # останавливаем создание
                info = DialogInfo("Внимание!", error, "notification.mp3")
                info.exec_()

        if error_and_id_account:
            self.error_and_id_errors_accounts.append(error_and_id_account)

        if user_names_created_channel:
            for user_name in user_names_created_channel:
                self.user_names_created_channel.append("@" + user_name)

        if end_create_from_this_account:
            self.quantity_accounts_ending_create_channel += 1

            # если кол-во закончивших создание аккаунтов больше или равно запущенных аккаунтов
            if self.quantity_accounts_ending_create_channel >= self.quantity_accounts_for_create_channel:
                self.active_threads.clear()
                socket.socket = self.original_socket  # восстанавливаем сокет

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

                self.lineEdit_quantity_streams.setText('')  # убираем количество запущенных потоков
                current_time = dt.datetime.now()
                formatted_time = current_time.strftime("%H:%M:%S")  # Форматируем время сейчас
                self.textEdit_conclusion.append(f'\n[{formatted_time}] СОЗДАНИЕ КАНАЛОВ ОСТАНОВЛЕННО')
                self.pushButton_start.setText('ЗАПУСТИТЬ')
                self.launched_create = False

                self._set_enabled_for_elements(True)
                info = DialogInfo("Готово!", 'Создание каналов успешно завершено!',"notification.mp3")
                info.exec_()

                if self.user_names_created_channel: # если есть user_name каналов, которые создали
                    info_channel_user_name = DialogListCreateChannel(self.user_names_created_channel)
                    info_channel_user_name.exec_()






    def _start(self):
        if not self.launched_create: # если создание не запущенно
            style_line_edit = ("QLineEdit {\n"
                     "    background-color: rgb(252, 224, 228);      /* Цвет фона текстового поля */\n"
                     "    border: 2px solid rgb(150, 150, 150); /* Рамка текстового поля */\n"
                     "    border-radius: 6px; /* Закругление углов */\n"
                     "    padding: 2px; /* Отступы внутри текстового поля */\n"
                     "    color: rgb(50, 50, 50); /* Цвет текста */\n"
                     "}\n")
            style_text_edit = ("QTextEdit {\n"
                               "background-color: rgb(252, 224, 228);"
                                "border-radius: 20px;"
                                "padding-top: 15px; /* Отступ только слева */   "
                                " padding-bottom: 15px; /* Отступ только снизу */"
                               "}\n")

            error_message = ""

            if self.textEdit_name_channel_list.toPlainText() == "":
                error_message += "Введите список имён канала!\n"
                self.textEdit_name_channel_list.setStyleSheet(style_text_edit)

            if self.textEdit_description_list.toPlainText() == "" and self.checkBox_set_description.isChecked() == True:
                error_message += "Введите список описаний канала!\n"
                self.textEdit_description_list.setStyleSheet(style_text_edit)

            if self.lineEdit_max_create_channel_from_one_account.text() == "":
                error_message += "Введите максимум созданных каналов с одного аккаунта!\n"
                self.lineEdit_max_create_channel_from_one_account.setStyleSheet(style_line_edit)

            if self.lineEdit_delay.text() == "":
                error_message += "Введите задержка между созданием!\n"
                self.lineEdit_delay.setStyleSheet(style_line_edit)

            if self.lineEdit_quantity_streams.text() == "":
                error_message += "Введите количество запущенных потоков!\n"
                self.lineEdit_quantity_streams.setStyleSheet(style_line_edit)

            if error_message:
                info = DialogInfo("Внимание!", error_message, "notification.mp3")
                info.exec_()
                return

            zero_account = self.root_project_dir + f'/accounts/active_accounts/0'
            if not os.path.isdir(zero_account):  # проверяем есть ли аккаунты для рассылки (это если нету)
                info = DialogInfo("Внимание!", 'У вас нет активных аккаунтов для создания каналов!', "notification.mp3")
                info.exec_()
                return

            if self.quantity_accounts_ending_create_channel < self.quantity_accounts_for_create_channel:
                info = DialogInfo("Внимание!", 'Дождитесь завершения работы аккаунтов!', "notification.mp3")
                info.exec_()
                return

            photos_names_list = []
            if self.checkBox_random_choice_photo.isChecked():
                photo_extensions = ('.jpg', '.jpeg', '.png', '.gif')  # Расширения фото
                photos_names_list = [
                    filename
                    for filename in os.listdir(self.root_project_dir + '/working_files/for_create_channel/photo_for_avatar_channel')
                    if filename.lower().endswith(photo_extensions)
                ]
                if not photos_names_list:
                    info = DialogInfo("Внимание!", 'У вас нет загруженных фото для аватара канала!',
                                       "notification.mp3")
                    info.exec_()
                    return

            if (self.checkBox_mailing_first_message.isChecked() and
                (self.data_first_message['use_new_message'] == False and self.data_first_message['use_the_forwarded_message'] == False)):
                info = DialogInfo("Внимание!", 'Вы не заполнили первое сообщение в канал!',
                                   "notification.mp3")
                info.exec_()
                return

            if (self.checkBox_set_user_name.isChecked() and self.data_for_user_name_channel['use_first_list'] == False and
                self.data_for_user_name_channel['use_second_list'] == False and self.data_for_user_name_channel['use_third_list'] == False):
                info = DialogInfo("Внимание!", 'Вы не заполнили user_name для канала!',
                                   "notification.mp3")
                info.exec_()
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

            list_for_generate_user_name = []  # список для формирования всех возможных user_name для канала
            if self.data_for_user_name_channel['use_first_list']:
                list_for_generate_user_name.append(self.data_for_user_name_channel['first_list'])
            if self.data_for_user_name_channel['use_second_list']:
                list_for_generate_user_name.append(self.data_for_user_name_channel['second_list'])
            if self.data_for_user_name_channel['use_third_list']:
                list_for_generate_user_name.append(self.data_for_user_name_channel['third_list'])

            channel_name_list = self.textEdit_name_channel_list.toPlainText().split('\n')
            channel_name_list = list(filter(None, channel_name_list)) # убираем все пустые элементы ""
            description_list = self.textEdit_description_list.toPlainText().split('&')
            dict_witch_user_names = self._generate_unique_user_name(list_for_generate_user_name)

            if (self.data_for_user_name_channel['use_first_list'] == True or self.data_for_user_name_channel['use_second_list'] == True
                or self.data_for_user_name_channel['use_third_list']): # если необходимо установить user_name
                if (len(dict_witch_user_names['user_names']) < int(self.lineEdit_quantity_streams.text()) *
                        int(self.lineEdit_max_create_channel_from_one_account.text())):
                    if dict_witch_user_names["there_are_inappropriate_values"]:
                        info = DialogInfo("Внимание!",
                                           'Некоторые сформированные user_name не соответствуют\n'
                                           'по ограничениям телеграмма, такие не будут созданы!',
                                           "notification.mp3")
                        info.exec_()
                    info = DialogInfo("Внимание!", 'Список всех возможных user_name канала должен превышать \n'
                                                                'необходимое количество созданных каналов!\n\n'
                                                                'У вас:\n'
                                                                f'Количество возможных user_name: {len(dict_witch_user_names['user_names'])}\n'
                                                                f'Необходимое количество каналов: {int(self.lineEdit_quantity_streams.text()) * 
                                                                int(self.lineEdit_max_create_channel_from_one_account.text())}',
                                       "notification.mp3")
                    info.exec_()
                    return

            if dict_witch_user_names["there_are_inappropriate_values"] and self.checkBox_set_user_name.isChecked():
                info = DialogInfo("Внимание!", 'Некоторые сформированные user_name не соответствуют по ограничениям \n'
                                                           'телеграмма, такие не будут созданы!',
                                   "notification.mp3")
                info.exec_()

            self.count_attempts = 0
            self.launched_create = True
            self.id_and_last_use = []
            self.quantity_accounts_for_create_channel = 0
            self.quantity_accounts_ending_create_channel = 0
            self.error_and_id_errors_accounts = []
            self.user_names_created_channel = []

            self._set_enabled_for_elements(False)

            current_time = dt.datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S")  # Форматируем время сейчас
            self.textEdit_conclusion.append(f'[{formatted_time}] СОЗДАНИЕ КАНАЛОВ ЗАПУЩЕННО\n')

            counter_for_channel_name = 0
            counter_for_avatar_path = 0
            counter_for_user_name = 0
            counter_for_description = 0
            for id_account in range(int(self.lineEdit_quantity_streams.text())):  # проходимся по кол-ву потоков
                channel_names = []
                avatar_paths = []
                user_names = []
                descriptions = []


                for _ in range(int(self.lineEdit_max_create_channel_from_one_account.text())): # формируется
                    if counter_for_channel_name < len(channel_name_list):
                        channel_names.append(channel_name_list[counter_for_channel_name])
                        counter_for_channel_name += 1
                    else:
                        channel_names.append(random.choice(channel_name_list))

                    if self.checkBox_random_choice_photo.isChecked():
                        if counter_for_avatar_path < len(photos_names_list):
                            avatar_paths.append(self.root_project_dir + '/working_files/for_create_channel/photo_for_avatar_channel/'
                                               + photos_names_list[counter_for_avatar_path])
                            counter_for_avatar_path += 1
                        else:
                            avatar_paths.append(self.root_project_dir + '/working_files/for_create_channel/photo_for_avatar_channel/'
                                               + random.choice(photos_names_list))

                    if self.checkBox_set_user_name.isChecked():
                        if counter_for_user_name < len(dict_witch_user_names['user_names']):
                            user_names.append(dict_witch_user_names['user_names'][counter_for_user_name])
                            counter_for_user_name += 1
                        else:
                            user_names.append(random.choice(dict_witch_user_names['user_names']))

                    if self.checkBox_set_description.isChecked():
                        if counter_for_description < len(description_list):
                            descriptions.append(description_list[counter_for_description])
                            counter_for_description += 1
                        else:
                            descriptions.append(random.choice(description_list))

                if os.path.isdir(self.root_project_dir + f'/accounts/active_accounts/{id_account}'):  # если аккаунт есть
                    create_channel = CreatingChannelWithStreams(
                        id_account=id_account,
                        channel_name=channel_names,
                        delay=int(self.lineEdit_delay.text()),
                        max_channel_from_one_account=int(self.lineEdit_max_create_channel_from_one_account.text()),
                        avatar_path=avatar_paths,
                        send_first_message=self.data_first_message,
                        user_name=user_names,
                        set_numbers_end_user_name=self.data_for_user_name_channel['set_numbers_end_user_name'],
                        description=descriptions,
                        use_proxy=self.checkBox_use_proxy.isChecked(),
                        ip=proxy_from_db[0], port=proxy_from_db[1], login=proxy_from_db[2], password=proxy_from_db[3])
                    create_channel.task_done.connect(self._handler_signal_with_streams)  # Подключаем сигнал к слоту
                    create_channel.start()  # Запускаем поток

                    self.active_threads.append(create_channel)
                    self.quantity_accounts_for_create_channel += 1

            self.pushButton_start.setText('ОСТАНОВИТЬ')
            self.launched_create = True
        else:
            for thread in self.active_threads:
                asyncio.run(thread.quit_async())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = WindowCreateChannel('fdsfds')
    ui.show()
    sys.exit(app.exec_())
