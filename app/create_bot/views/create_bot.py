import os
import sqlite3

import PyQt5
from pathlib import Path
import datetime as dt
import socks
import socket
import asyncio
import itertools
import random

from opentele.td import TDesktop
from opentele.api import UseCurrentSession
from opentele.exception import TFileNotFound
from telethon import errors

from app.general.views.info import DialogInfo
from app.general.check_proxy import check_proxy
from app.general.views.error_proxy_for_work import DialogErrorProxyForWork
from app.general.error_handler import get_description_and_solution, error_handler
from app.create_bot.ui.window_create_bot_ui import WindowCreateBotUi
from app.create_bot.views.list_created_bot import DialogCreateBot
from app.create_bot.views.user_name_for_bot import DialogUserNameForBot
from app.create_bot.views.list_BIO_bot import DialogListBIOBot

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")  # 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():  # 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path  # 3. Установка пути

# Только после этого импортируем PyQt5
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QLineEdit

class CreatingBotWithStreams(QThread):
    """
            __init__:
            :param id_account: id аккаунта (из активных аккаунтов)
            :param bot_names: имя канала
            :param delay: задержка между созданием каналов
            :param max_bot_from_one_account: максимум созданных каналов с одного аккаунта
            :param avatar_path: флаг необходимости установить аватар у канала и путь к нему
            :param user_names: user_name и флаг необходимости его установления
            :param set_numbers_end_user_name: флаг необходимости устанавливать цифры в конце user_name если такой занят
            :param descriptions: описание и флаг необходимости его установления
            :param use_proxy: флаг необходимости прокси
            :param ip: данные прокси
            :param port: данные прокси
            :param login: данные прокси
            :param password: данные прокси
            """
    task_done = pyqtSignal(str, list, bool, list, list, str, list, bool)  # Сигнал, который мы будем использовать для обновления интерфейса
    # вывод в консоль(str), количество успешных[0] и неудачных созданий[1](list), ошибка прокси(bool), ошибка(str), конец работы(bool)

    def __init__(self,id_account: int, bot_names: list, delay: int, max_bot_from_one_account: int,
                 user_names: list, set_numbers_end_user_name: bool,
                 avatar_path: list,
                 descriptions: list,
                 bios: list,
                 use_proxy: bool,ip: str, port: int, login: str, password: str):

        super().__init__()
        self.root_project_dir = '..'
        self.id_account = id_account
        self.bot_names = bot_names
        self.delay = delay
        self.max_bot_from_one_account = max_bot_from_one_account
        self.user_names = user_names
        self.set_numbers_end_user_name = set_numbers_end_user_name
        self.avatar_path = avatar_path
        self.descriptions = descriptions
        self.bios = bios
        self.use_proxy = use_proxy
        self.ip = ip
        self.port = port
        self.login = login
        self.password = password

        self.client = None
        self.me = None
        self.successful_create = 0
        self.failed_create = 0
        self.account_id = 0
        self.last_used = ''
        self.user_name_created_bot = [] # список user_name созданных ботов

        self.BOT_FATHER_USER_NAME = '@BotFather'

        self.stop_thread = False

    def run(self):
        asyncio.run(self.run_2())

    async def run_2(self):
        if self.use_proxy:
            socks.set_default_proxy(socks.SOCKS5, self.ip, self.port, True, self.login, self.password)
            socket.socket = socks.socksocket

        try:  # пытаемся войти в аккаунт
            folder_path_account = self.root_project_dir + f'/accounts/active_accounts/{self.id_account}'  # путь к tdata
            tdesk = TDesktop(folder_path_account + '/tdata')

            self.client = await tdesk.ToTelethon(session=f"{folder_path_account}/session.session",
                                                 flag=UseCurrentSession, )

            await asyncio.wait_for(self.client.connect(), timeout=15)  # вход в аккаунт
            self.me = await self.client.get_me()
            self.account_id = self.me.id

            self.task_done.emit(f'Запущенно создание с аккаунта "{self.me.username}"', [], False, [], [], '', [], False)

            for i in range(self.max_bot_from_one_account):
                try:
                    now = dt.datetime.now()  # Получаем время именно тут, т.к. может возникнут ошибка и это тоже считается как использование аккаунта
                    self.last_used = now.strftime('%H:%M %d-%m-%Y')  # Форматируем дату и время согласно формату

                    await self.client.send_message(self.BOT_FATHER_USER_NAME, '/start')  # запуск бот
                    await asyncio.sleep(2)

                    await self.client.send_message(self.BOT_FATHER_USER_NAME, '/newbot')  # запуск создания
                    await asyncio.sleep(2)
                    messages = await self.client.get_messages(self.BOT_FATHER_USER_NAME, limit=1)  # последнее сообщение с чата
                    if 'Sorry' in messages[0].text:  # если слишком много запросов на создание бота
                        waiting_time = ''.join(filter(str.isdigit, messages[0].text)) # изымаем только цифры
                        if int(waiting_time) > 15:
                            self.task_done.emit(f'Аккаунт "{self.me.username}" закончил создание '
                                                f'из за получения лимита ожидания между созданием ботов в {waiting_time} секунд!\n'
                                                f'Созданных ботов: {self.successful_create} из {self.max_bot_from_one_account}',
                                                [self.successful_create, self.failed_create], False,
                                                [self.account_id, self.last_used], self.user_name_created_bot, '', [],
                                                True)
                            return
                        else:
                            await asyncio.sleep(int(waiting_time))

                    await self.client.send_message(self.BOT_FATHER_USER_NAME, self.bot_names[i])  # установление имени
                    await asyncio.sleep(2)
                    messages = await self.client.get_messages(self.BOT_FATHER_USER_NAME, limit=1) # последнее сообщение с чата
                    if 'Sorry' in messages[0].text: # если получили отказ в создании имени
                        self.failed_create += 1
                        continue

                    await self.client.send_message(self.BOT_FATHER_USER_NAME, self.user_names[i])  # установление user_name
                    await asyncio.sleep(2)
                    messages = await self.client.get_messages(self.BOT_FATHER_USER_NAME,limit=1)  # последнее сообщение с чата
                    if 'Sorry, this username is already taken.' in messages[0].text: # когда такой user_name занят
                        if self.set_numbers_end_user_name: # если есть необходимость устанавливать цифры в конце user_name
                            not_create = False
                            while True: # цикл для добавления цифр в конец user_name для удачного его формирования
                                random_digits = ''.join([str(random.randint(0, 9)) for _ in range(4)])
                                # убираем приписку '_bot', добавляем цифры в конец и снова добавляем приписку '_bot'
                                new_user_name = self.user_names[i][:-3] + random_digits + '_bot'

                                await self.client.send_message(self.BOT_FATHER_USER_NAME, new_user_name)  # установление имени
                                await asyncio.sleep(2)
                                messages = await self.client.get_messages(self.BOT_FATHER_USER_NAME,limit=1)  # последнее сообщение с чата
                                if 'Sorry, this username is already taken.' in messages[0].text:  # когда такой user_name занят
                                    continue
                                elif 'Sorry' in messages[0].text: # если превысили длину user_name
                                    not_create = True
                                    break
                                else: # если успешно создали
                                    self.user_names[i] = new_user_name
                                    break

                            if not_create: # если из цикла выше не смогли создать бота
                                self.failed_create += 1
                                continue
                        else:
                            self.failed_create += 1
                            continue
                    elif 'Sorry' in messages[0].text:  # если получили отказ в создании user_name (слишком длинный или короткий или есть запрещённые символы)
                        self.failed_create += 1
                        continue

                    self.user_name_created_bot.append(self.user_names[i])

                    if self.avatar_path: # если необходимо установить автар
                        await self.client.send_message(self.BOT_FATHER_USER_NAME, '/setuserpic')  # установка аватара
                        await asyncio.sleep(2)
                        await self.client.send_message(self.BOT_FATHER_USER_NAME, f'@{self.user_names[i]}')  # выбор бота для установки
                        await asyncio.sleep(2)
                        await self.client.send_file(self.BOT_FATHER_USER_NAME, self.avatar_path[i])  # отсылка фото для аватара
                        await asyncio.sleep(2)

                    if self.descriptions: # если необходимо установить описание
                        await self.client.send_message(self.BOT_FATHER_USER_NAME, '/setdescription')  # установка описания
                        await asyncio.sleep(2)
                        await self.client.send_message(self.BOT_FATHER_USER_NAME,f'@{self.user_names[i]}')  # выбор бота для установки
                        await asyncio.sleep(2)
                        await self.client.send_message(self.BOT_FATHER_USER_NAME,self.descriptions[i])  # отсылка описания
                        await asyncio.sleep(2)

                        messages = await self.client.get_messages(self.BOT_FATHER_USER_NAME,limit=1)  # последнее сообщение с чата
                        if 'Sorry' in messages[0].text:  # если получили отказ в установки описания
                            self.failed_create += 1
                            continue

                    if self.bios: # если необходимо установить БИО
                        await self.client.send_message(self.BOT_FATHER_USER_NAME,'/setabouttext')  # установка БИО
                        await asyncio.sleep(2)
                        await self.client.send_message(self.BOT_FATHER_USER_NAME,f'@{self.user_names[i]}')  # выбор бота для установки
                        await asyncio.sleep(2)
                        await self.client.send_message(self.BOT_FATHER_USER_NAME,self.bios[i])  # отсылка БИО
                        await asyncio.sleep(2)

                        messages = await self.client.get_messages(self.BOT_FATHER_USER_NAME,limit=1) # последнее сообщение с чата
                        if 'Sorry' in messages[0].text:  # если получили отказ в установки БИО
                            self.failed_create += 1
                            continue

                    self.successful_create += 1
                    await asyncio.sleep(self.delay)
                except errors.MessageEmptyError:  # Было отправлено пустое или недопустимое сообщение в формате UTF-8.
                    self.failed_create += 1
                    continue
                except errors.MessageTooLongError:  # сообщение слишком длинное
                    self.failed_create += 1
                    continue
                except (ValueError, errors.UsernameInvalidError, errors.InputUserDeactivatedError,
                        errors.YouBlockedUserError, errors.UserIsBlockedError, errors.UserPrivacyRestrictedError,
                        errors.ForbiddenError): # все другие случаи где проблемы со стороны бота
                    self.failed_create += 1
                    continue

        except asyncio.exceptions.CancelledError: # если экстренно остановили поток и в методе который вызывается с await может произойти такая ошибка
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
            self.task_done.emit(f'На аккаунте "{user_name_from_db[0]}" произошла ошибка он будет убран из активных.\n'
                                f'Ошибка: {error_description_solution[0]}\n'
                                f'Созданных ботов: {self.successful_create} из {self.max_bot_from_one_account}',
                                [self.successful_create, self.failed_create], True, [self.account_id, self.last_used],
                                self.user_name_created_bot, '',[error_name, self.id_account], True)
            return

        self.task_done.emit(f'Аккаунт "{self.me.username}" закончил создание\n'
                            f'Созданных ботов: {self.successful_create} из {self.max_bot_from_one_account}',
                            [self.successful_create, self.failed_create], False,
                            [self.account_id, self.last_used], self.user_name_created_bot, '', [],True)
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

        if user_name_from_db[0]:
            user_name = user_name_from_db[0]
        else:
            user_name = "None"

        self.task_done.emit(
            f'Вы остановили создание ботов с аккаунта: "{user_name}"'
            f'\nСозданных ботов: {self.successful_create} из {self.max_bot_from_one_account}',
            [self.successful_create, self.failed_create], False,
            [self.account_id, self.last_used], self.user_name_created_bot, '', [], True)
        self.terminate()  # Принудительное завершение

class WindowCreateBot(WindowCreateBotUi):
    def __init__(self, switch_window):
        super().__init__()
        self.switch_window = switch_window

        self.root_project_dir = '..'

        self.data_for_user_name = {
            'first_list': '',
            'second_list': '',
            'third_list': '',
            'use_first_list': False,
            'use_second_list': False,
            'use_third_list': False,
            'set_numbers_end_user_name': False,
        }

        self.list_BIO_for_bots = ''

        self.active_threads = []  # ВАЖНО! хранит в себе запущенные потоки
        self.launched_create = False  # отображает запущенно ли создание
        self.original_socket = socket.socket  # проки который был до
        self.id_and_last_use = []  # хранит массивы в которых tg_id аккаунта и его последнее использование
        self.quantity_accounts_for_create_bots = 0  # количество аккаунтов для создания ботов
        self.quantity_accounts_ending_create_bots = 0  # количество аккаунтов закончивших создание
        self.error_and_id_errors_accounts = []  # хранит массивы в которых ошибка и id папки, где произошла эта ошибка
        self.user_names_created_bots = [] # user_name список созданных ботов

        self.count_attempts = 0 # количество попыток создания канала

        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()
        cursor.execute(f"SELECT "
                       f"name, "
                       f"description, "
                       f"max_creating_bot_from_one_account, "
                       f"delay, "
                       f"first_user_name_list, "
                       f"second_user_name_list, "
                       f"third_user_name_list,  "
                       f"BIO "
                       f"FROM saved_data_creating_bots")
        data_from_db = cursor.fetchone()  # берём с БД т.к. мы можем даже не войти в аккаунт и тогда не получим его user_name для вывода
        connection.close()

        # заполнение данных с БД
        self.textEdit_name_list.setText(data_from_db[0])
        self.textEdit_description_list.setText(data_from_db[1])
        self.lineEdit_max_create_from_one_account.setText(data_from_db[2])
        self.lineEdit_delay.setText(data_from_db[3])
        self.data_for_user_name['first_list'] = data_from_db[4]
        self.data_for_user_name['second_list'] = data_from_db[5]
        self.data_for_user_name['third_list'] = data_from_db[6]
        self.list_BIO_for_bots = data_from_db[7]


        # события
        self.pushButton_account.clicked.connect(lambda: self._transition('accounts'))
        self.pushButton_mailing.clicked.connect(lambda: self._transition('mailing_by_users'))
        self.pushButton_mailing_chat.clicked.connect(lambda: self._transition('mailing_by_chats'))
        self.pushButton_invite.clicked.connect(lambda: self._transition('invite'))
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
        self.pushButton_info_streams.clicked.connect(lambda: self._info_streams())
        self.pushButton_info_list_description.clicked.connect(lambda: self._info_list_description())
        self.pushButton_info_list_name_bot.clicked.connect(lambda: self._info_list_name_channel())

        self.textEdit_name_list.focusLost.connect(self._update_data_in_db)  # ЭТО СОБЫТИЕ СОЗДАННО В ПЕРЕОПРЕДЕЛЁННОМ КЛАСС
        self.textEdit_description_list.focusLost.connect(self._update_data_in_db)  # ЭТО СОБЫТИЕ СОЗДАННО В ПЕРЕОПРЕДЕЛЁННОМ КЛАСС
        self.lineEdit_max_create_from_one_account.editingFinished.connect(lambda: self._update_data_in_db(
            self.lineEdit_max_create_from_one_account.text(), 'max_creating_bot_from_one_account'))
        self.lineEdit_delay.editingFinished.connect(lambda: self._update_data_in_db(
            self.lineEdit_delay.text(), 'delay'))

        self.lineEdit_max_create_from_one_account.focusInEvent = lambda event: self._set_default_style_line_edit(
            self.lineEdit_max_create_from_one_account)
        self.lineEdit_delay.focusInEvent = lambda event: self._set_default_style_line_edit(
            self.lineEdit_delay)
        self.lineEdit_quantity_streams.focusInEvent = lambda event: self._set_default_style_line_edit(
            self.lineEdit_quantity_streams)
        self.textEdit_name_list.focusInEvent = lambda event: self._set_default_style_text_edit(
            self.textEdit_name_list)
        self.textEdit_description_list.focusInEvent = lambda event: self._set_default_style_text_edit(
            self.textEdit_description_list)

        self.lineEdit_quantity_streams.textChanged.connect(lambda: self._line_edit_quantity_editing_finished())

        self.pushButton_choose_user_name.clicked.connect(lambda: self._choice_user_name())
        self.pushButton_random_choice_photo.clicked.connect(lambda: self._choice_photo())
        self.pushButton_set_BIO.clicked.connect(lambda: self._set_bio())

        self.pushButton_start.clicked.connect(lambda: self._start())

    def _transition(self, window: str):
        if self.launched_create:
            self.show_info('Внимание!', f'Для перехода на другую вкладку необходимо остановить создание')
        else:
            self.switch_window(window)

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

    def _set_default_style_line_edit(self, line_edit: QLineEdit):
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

    def _set_default_style_text_edit(self, text_edit: QTextEdit):
        text_edit.setStyleSheet(
            """
            background-color: rgb(255, 255, 255);
            border-radius: 20px;
            padding-top: 15px; /* Отступ только слева */   
            padding-bottom: 15px; /* Отступ только снизу */
            """)

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

    def _choice_photo(self):
        path = os.path.abspath(self.root_project_dir + "/working_files/photo_for_creating_bot")
        os.startfile(path)

    def _choice_user_name(self):
        dialog = DialogUserNameForBot(self.data_for_user_name)  # Создаем экземпляр
        dialog.data_returned.connect(self.set_data_for_user_name)  # Подключаем сигнал
        dialog.exec_()  # Открываем модальное окно

    def _set_bio(self):
        dialog = DialogListBIOBot(self.list_BIO_for_bots)  # Создаем экземпляр
        dialog.data_returned.connect(self.set_data_bio)  # Подключаем сигнал
        dialog.exec_()  # Открываем модальное окно

    def set_data_for_user_name(self, data: dict):
        self.data_for_user_name = data

    def set_data_bio(self, data: str):
        self.list_BIO_for_bots = data

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
            if len(user_name) < 1 or len(user_name) > 28:
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

            result.append(user_name + '_bot')

        result = list((set(result))) # убираем повторяющиеся элементы
        random.shuffle(result)  # перемешивание всех элементов списка

        return {"user_names": result, "there_are_inappropriate_values": there_are_inappropriate_values}

    def _set_enabled_for_elements(self, enabled: bool):
        self.lineEdit_max_create_from_one_account.setEnabled(enabled)
        self.lineEdit_delay.setEnabled(enabled)
        self.lineEdit_quantity_streams.setEnabled(enabled)
        self.textEdit_name_list.setReadOnly(enabled)
        self.textEdit_description_list.setReadOnly(enabled)
        self.checkBox_random_choice_photo.setEnabled(enabled)
        self.checkBox_set_BIO.setEnabled(enabled)
        self.checkBox_set_description.setEnabled(enabled)
        self.checkBox_use_proxy.setEnabled(enabled)

    def _handler_signal_with_streams(self, console_output: str, counter_created_and_uncreated: list,
                                    account_banned: bool, id_and_last_use: list, user_names_created_bots: list,
                                    error: str, error_and_id_account: list, end_create_from_this_account: bool):
        if console_output:
            current_time = dt.datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S")  # Форматируем время сейчас
            self.textEdit_conclusion.append(f'[{formatted_time}] {console_output}')

        if counter_created_and_uncreated:
            self.count_attempts += counter_created_and_uncreated[0] + counter_created_and_uncreated[1]
            self.label_successfully.setText(str(counter_created_and_uncreated[0] + int(self.label_successfully.text())))
            self.label_unsuccessful.setText(str(counter_created_and_uncreated[1] + int(self.label_unsuccessful.text())))
            self.label_count_attempts.setText(str(
                counter_created_and_uncreated[0] + counter_created_and_uncreated[1] + int(
                    self.label_count_attempts.text())))

        if account_banned:
            self.label_banned_account.setText(str(int(self.label_banned_account.text()) + 1))

        if id_and_last_use:  # добавление для учёта времени последнего использования аккаунта (такое возвращается только один раз с одного аккаунта)
            if id_and_last_use[1]:  # будем работать если есть время последнего использования
                self.id_and_last_use.append(id_and_last_use)

        if error:
            if self.launched_create:  # если создание запущено
                for thread in self.active_threads: # принудительно завершаем потоки
                    asyncio.run(thread.quit_async())

                self._set_enabled_for_elements(True)
                self.launched_create = False  # останавливаем создание
                info = DialogInfo("Внимание!", error, "notification.mp3")
                info.exec_()

        if error_and_id_account:
            self.error_and_id_errors_accounts.append(error_and_id_account)

        if user_names_created_bots:
            for user_name in user_names_created_bots:
                self.user_names_created_bots.append("@" + user_name)

        if end_create_from_this_account:
            self.quantity_accounts_ending_create_bots += 1

            # если кол-во закончивших создание аккаунтов больше или равно запущенных аккаунтов
            if self.quantity_accounts_ending_create_bots >= self.quantity_accounts_for_create_bots:
                self.active_threads.clear()
                socket.socket = self.original_socket  # восстанавливаем сокет

                connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
                cursor = connection.cursor()
                for id_and_last_use in self.id_and_last_use:  # установления последнего использования аккаунта
                    cursor.execute(f"UPDATE accounts SET last_used = ? WHERE id_tg = ?",
                                   (id_and_last_use[1], id_and_last_use[0]))
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
                self.textEdit_conclusion.append(f'\n[{formatted_time}] СОЗДАНИЕ БОТОВ ОСТАНОВЛЕННО')
                self.pushButton_start.setText('ЗАПУСТИТЬ')
                self.launched_create = False

                self._set_enabled_for_elements(True)
                info = DialogInfo("Готово!", 'Создание ботов успешно завершено!', "notification.mp3")
                info.exec_()

                if self.user_names_created_bots:  # если есть user_name ботов, которые создали
                    info_bots_user_name = DialogCreateBot(self.user_names_created_bots)
                    info_bots_user_name.exec_()

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

            if self.lineEdit_max_create_from_one_account.text() == "":
                error_message += "Введите максимум созданных ботов с одного аккаунта!\n"
                self.lineEdit_max_create_from_one_account.setStyleSheet(style_line_edit)

            if self.lineEdit_delay.text() == "":
                error_message += "Введите задержка между созданием!\n"
                self.lineEdit_delay.setStyleSheet(style_line_edit)

            if self.lineEdit_quantity_streams.text() == "":
                error_message += "Введите количество запущенных потоков!\n"
                self.lineEdit_quantity_streams.setStyleSheet(style_line_edit)

            if (self.data_for_user_name['use_first_list'] == False and
                self.data_for_user_name['use_second_list'] == False and
                self.data_for_user_name['use_third_list'] == False):
                error_message += 'Вы не заполнили user_name для ботов!\n'

            bot_name_list = []
            for one_name in self.textEdit_name_list.toPlainText().split('\n'):
                if one_name.replace(" ", "").replace("\n", "").replace("\t", ""):  # если имя не пустое
                    bot_name_list.append(one_name)
            if not bot_name_list:
                error_message += "Введите корректные данные для имени бота!\n"
                self.textEdit_name_list.setStyleSheet(style_text_edit)

            description_list = []
            if self.checkBox_set_description.isChecked():  # если необходимо установить БИО
                for one_description in self.textEdit_description_list.toPlainText().split('&'):
                    if one_description.replace(" ", "").replace("\n", "").replace("\t", ""):  # если БИО не пустое
                        description_list.append(one_description)
                if not description_list:
                    error_message += "Введите корректные данные для описания!\n"
                    self.textEdit_description_list.setStyleSheet(style_text_edit)


            bio_list = []
            if self.checkBox_set_BIO.isChecked():  # если необходимо установить БИО
                for one_bio in self.list_BIO_for_bots.split('&'):
                    if one_bio.replace(" ", "").replace("\n", "").replace("\t", ""):  # если БИО не пустое
                        bio_list.append(one_bio)
                if not bio_list:
                    error_message += "Введите корректные данные для БИО!\n"

            if error_message:
                info = DialogInfo("Внимание!", error_message, "notification.mp3")
                info.exec_()
                return

            zero_account = self.root_project_dir + f'/accounts/active_accounts/0'
            if not os.path.isdir(zero_account):  # проверяем есть ли аккаунты для рассылки (это если нету)
                info = DialogInfo("Внимание!", 'У вас нет активных аккаунтов для создания каналов!', "notification.mp3")
                info.exec_()
                return

            photos_names_list = []
            if self.checkBox_random_choice_photo.isChecked():
                photo_extensions = ('.jpg', '.jpeg', '.png', '.gif')  # Расширения фото
                photos_names_list = [
                    filename
                    for filename in os.listdir(self.root_project_dir + '/working_files/photo_for_creating_bot')
                    if filename.lower().endswith(photo_extensions)
                ]
                if not photos_names_list:
                    info = DialogInfo("Внимание!", 'У вас нет загруженных фото для аватара ботов!',
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
            if self.data_for_user_name['use_first_list']:
                list_for_generate_user_name.append(self.data_for_user_name['first_list'])
            if self.data_for_user_name['use_second_list']:
                list_for_generate_user_name.append(self.data_for_user_name['second_list'])
            if self.data_for_user_name['use_third_list']:
                list_for_generate_user_name.append(self.data_for_user_name['third_list'])

            dict_witch_user_names = self._generate_unique_user_name(list_for_generate_user_name)

            if (self.data_for_user_name['use_first_list'] == True or self.data_for_user_name['use_second_list'] == True
                or self.data_for_user_name['use_third_list']): # если необходимо установить user_name
                if (len(dict_witch_user_names['user_names']) < int(self.lineEdit_quantity_streams.text()) *
                        int(self.lineEdit_max_create_from_one_account.text())):
                    if dict_witch_user_names["there_are_inappropriate_values"]:
                        info = DialogInfo("Внимание!",
                                           'Некоторые сформированные user_name не соответствуют\n'
                                           'по ограничениям телеграмма, такие не будут созданы!',
                                           "notification.mp3")
                        info.exec_()
                    info = DialogInfo("Внимание!", 'Список всех возможных user_name ботов должен превышать \n'
                                                                'необходимое количество созданных ботов!\n\n'
                                                                'У вас:\n'
                                                                f'Количество возможных user_name: {len(dict_witch_user_names['user_names'])}\n'
                                                                f'Необходимое количество ботов: {int(self.lineEdit_quantity_streams.text()) * 
                                                                int(self.lineEdit_max_create_from_one_account.text())}',
                                       "notification.mp3")
                    info.exec_()
                    return

            if dict_witch_user_names["there_are_inappropriate_values"]:
                info = DialogInfo("Внимание!", 'Некоторые сформированные user_name не соответствуют по ограничениям \n'
                                                           'телеграмма, такие не будут созданы!',
                                   "notification.mp3")
                info.exec_()

            self.count_attempts = 0
            self.launched_create = True
            self.id_and_last_use = []
            self.quantity_accounts_for_create_bots = 0
            self.quantity_accounts_ending_create_bots = 0
            self.error_and_id_errors_accounts = []
            self.user_names_created_channel = []

            self._set_enabled_for_elements(False)

            current_time = dt.datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S")  # Форматируем время сейчас
            self.textEdit_conclusion.append(f'[{formatted_time}] СОЗДАНИЕ БОТОВ ЗАПУЩЕННО\n')

            counter_for_name = 0
            counter_for_avatar_path = 0
            counter_for_user_name = 0
            counter_for_description = 0
            counter_for_bio = 0
            for id_account in range(int(self.lineEdit_quantity_streams.text())):  # проходимся по кол-ву потоков
                names = []
                avatar_paths = []
                user_names = []
                descriptions = []
                bios = []

                for _ in range(int(self.lineEdit_max_create_from_one_account.text())): # формируется
                    if counter_for_name < len(bot_name_list):
                        names.append(bot_name_list[counter_for_name])
                        counter_for_name += 1
                    else:
                        names.append(random.choice(bot_name_list))

                    if counter_for_user_name < len(dict_witch_user_names['user_names']):
                        user_names.append(dict_witch_user_names['user_names'][counter_for_user_name])
                        counter_for_user_name += 1
                    else:
                        user_names.append(random.choice(dict_witch_user_names['user_names']))

                    if self.checkBox_random_choice_photo.isChecked():
                        if counter_for_avatar_path < len(photos_names_list):
                            avatar_paths.append(self.root_project_dir + '/working_files/photo_for_creating_bot/'
                                               + photos_names_list[counter_for_avatar_path])
                            counter_for_avatar_path += 1
                        else:
                            avatar_paths.append(self.root_project_dir + '/working_files/photo_for_creating_bot/'
                                               + random.choice(photos_names_list))

                    if self.checkBox_set_description.isChecked():
                        if counter_for_description < len(description_list):
                            descriptions.append(description_list[counter_for_description])
                            counter_for_description += 1
                        else:
                            descriptions.append(random.choice(description_list))

                    if self.checkBox_set_BIO.isChecked():
                        if counter_for_bio < len(bio_list):
                            bios.append(bio_list[counter_for_bio])
                            counter_for_bio += 1
                        else:
                            bios.append(random.choice(bio_list))

                if os.path.isdir(self.root_project_dir + f'/accounts/active_accounts/{id_account}'):  # если аккаунт есть
                    create_bot = CreatingBotWithStreams(
                        id_account=id_account,
                        bot_names=names,
                        delay=int(self.lineEdit_delay.text()),
                        max_bot_from_one_account=int(self.lineEdit_max_create_from_one_account.text()),
                        avatar_path=avatar_paths,
                        user_names=user_names,
                        set_numbers_end_user_name=self.data_for_user_name['set_numbers_end_user_name'],
                        descriptions=descriptions,
                        bios=bios,
                        use_proxy=self.checkBox_use_proxy.isChecked(),
                        ip=proxy_from_db[0], port=proxy_from_db[1], login=proxy_from_db[2], password=proxy_from_db[3])
                    create_bot.task_done.connect(self._handler_signal_with_streams)  # Подключаем сигнал к слоту
                    create_bot.start()  # Запускаем поток

                    self.active_threads.append(create_bot)
                    self.quantity_accounts_for_create_bots += 1

            self.pushButton_start.setText('ОСТАНОВИТЬ')
            self.launched_create = True
        else:
            for thread in self.active_threads:
                asyncio.run(thread.quit_async())