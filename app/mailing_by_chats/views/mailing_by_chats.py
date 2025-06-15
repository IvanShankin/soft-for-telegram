import os  # это для действия ниже перед запуском функции
import sqlite3
import datetime as dt
import socks
import socket
import asyncio
import shutil  # для удаления папки

from opentele.td import TDesktop
from opentele.api import UseCurrentSession
from opentele.exception import TFileNotFound
from telethon import errors
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import InputChannel

from app.mailing_by_chats.ui.window_mailing_by_chats_ui import WindowMailingByChatsUi
from app.mailing_by_chats.views.list_used_chat import DialogListUsedChats
from app.general.views.info import DialogInfo
from app.general.check_proxy import check_proxy
from app.general.views.error_proxy_for_work import DialogErrorProxyForWork
from app.general.error_handler import get_description_and_solution, error_handler
from app.general.check_html_parse import check_html_parse
from app.mailing_by_chats.views.forwarded_message import DialogForwardedMessage

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")# 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():# 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path# 3. Установка пути

# Только после этого импортируем PyQt5
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QLineEdit, QFileDialog, QTextEdit


class MailingWithStreams(QThread): # затухание progress_bar
    task_done = pyqtSignal(str, list, bool, list, str, str, list,bool)  # Сигнал, который мы будем использовать для обновления интерфейса
    # вывод в консоль(str), количество успешных[0] и неудачных сообщений[1](list), Флаг получения бана аккаунта(bool),
    # id аккаунта и его последнее использование(list), user_name чата по которому отработали(str), ошибка(str),
    # id аккаунта и ошибка(list) конец работы(bool)

    def __init__(self, thread_id: int, list_id_accounts: list,user_name_chat: str, message: str,
                 use_forwarded_message: bool, user_name_group_for_forwarded_message: str, id_message_for_forwarded: int,
                 max_message_from_one_account: int, time_sleep: int,
                 use_file_for_message: bool, file_path: str, use_proxy: bool,ip: str, port: int, login: str, password: str):
        super().__init__()
        self.root_project_dir = '..'
        self.thread_id = thread_id
        self.list_id_accounts = list_id_accounts
        self.user_name_chat = user_name_chat
        self.message = message

        self.use_forwarded_message = use_forwarded_message
        self.user_name_group_for_forwarded_message = user_name_group_for_forwarded_message
        self.id_message_for_forwarded = id_message_for_forwarded

        self.max_message_from_one_account = int(max_message_from_one_account)
        self.time_sleep = int(time_sleep)
        self.use_file_for_message = use_file_for_message
        self.file_path = file_path

        self.use_proxy = use_proxy
        self.ip = ip
        self.port = port
        self.login = login
        self.password = password

        self.me = None
        self.client = None
        self.account_id = None
        self.last_used = ''
        self.counter_account = 0 # счётчик на каком аккаунте по счёту
        self.completed_accounts = 0 # количество аккаунтов которые завершили работу

        self.successful_send_message = 0
        self.successful_send_message_from_one_account = 0
        self.failed_send_message = 0

        self.stop_thread = False

    def run(self):
        asyncio.run(self.run_2())

    async def run_2(self):
        if self.use_proxy:
            socks.set_default_proxy(socks.SOCKS5, self.ip, self.port, True, self.login, self.password)
            socket.socket = socks.socksocket

        for id_account in self.list_id_accounts:
            try:  # пытаемся войти в аккаунт
                self.successful_send_message_from_one_account = 0
                self.counter_account += 1 # так и должно в самом начале прибавляться, ибо с нуля начинаем

                folder_path_account = self.root_project_dir + f'/accounts/active_accounts/{id_account}'  # путь к tdata
                tdesk = TDesktop(folder_path_account + '/tdata')

                self.client = await tdesk.ToTelethon(session=f"{folder_path_account}/session.session",
                                                     flag=UseCurrentSession, )

                await asyncio.wait_for(self.client.connect(), timeout=15)  # вход в аккаунт
                self.me = await self.client.get_me()
                self.account_id = self.me.id

                self.task_done.emit(f'Запущенна рассылка с аккаунта "{self.me.username}"\n'
                                    f'Аккаунт {self.counter_account} из {len(self.list_id_accounts)}\n'
                                    f'ID потока: {self.thread_id}',
                                    [], False, [], '', '', [], False)

                try:
                    temp_chat = await self.client.get_entity(self.user_name_chat)
                    target_chat = InputChannel(temp_chat.id, temp_chat.access_hash)
                    await self.client(JoinChannelRequest(target_chat)) # вход в чат
                except errors.ChannelPrivateError:
                    self.task_done.emit(
                        f'Аккаунт "{self.me.username}" будет сменён т.к. получил бан  в чате "{self.user_name_chat}" или в этот чат невозможно написать\n'
                        f'Отправлено сообщений c этого аккаунта: {self.successful_send_message_from_one_account}'
                        f' из {self.max_message_from_one_account}\n'
                        f'Аккаунт {self.counter_account} из {len(self.list_id_accounts)}\n'
                        f'ID потока: {self.thread_id}',
                        [], False, [], '', '', [], False)
                    await self.client.disconnect()
                    self.completed_accounts += 1
                    continue
                except (errors.ChannelInvalidError, errors.UsernameNotOccupiedError, errors.PeerIdInvalidError,
                        TypeError, ValueError, AttributeError) :
                    self.task_done.emit(
                        f'Поток завершил работу. Чат "{self.me.username} не найден"\n'
                        f'Отправлено сообщений: {self.successful_send_message_from_one_account} из {self.max_message_from_one_account}\n'
                        f'Аккаунт {self.counter_account} из {len(self.list_id_accounts)}\n'
                        f'ID потока: {self.thread_id}',
                        [], False, [], '', '', [], False)
                    await self.client.disconnect()

                    for _ in range(len(self.list_id_accounts) - self.completed_accounts): # отправляем сигнал, что каждый аккаунт закончил работу
                        self.task_done.emit('',[], False, [], '', '', [], True)
                    return
                except errors.ChannelsTooMuchError:
                    self.task_done.emit(
                        f'Аккаунт "{self.me.username} будет пропущен т.к. состоит в слишком большом количестве чатов"\n'
                        f'Аккаунт {self.counter_account} из {len(self.list_id_accounts)}\n'
                        f'ID потока: {self.thread_id}',
                        [], False, [], '', '', [], True)
                    await self.client.disconnect()
                    self.completed_accounts += 1
                    continue

                except errors.InviteRequestSentError:
                    self.task_done.emit(
                        f'Аккаунт "{self.me.username} будет пропущен т.к. мы отослали запрос на присоединение и его ещё не приняли"\n'
                        f'Аккаунт {self.counter_account} из {len(self.list_id_accounts)}\n'
                        f'ID потока: {self.thread_id}',
                        [], False, [], '', '', [], True)
                    await self.client.disconnect()
                    self.completed_accounts += 1
                    continue

                error_sent_message = False
                for _ in range(self.max_message_from_one_account):
                    now = dt.datetime.now()  # Получаем время именно тут, т.к. может возникнут ошибка и это тоже считается как использование аккаунта
                    self.last_used = now.strftime('%H:%M %d-%m-%Y')  # Форматируем дату и время согласно формату

                    if self.use_forwarded_message: # если необходимо переслать сообщение
                        try:
                            await self.client.forward_messages(
                                entity=target_chat.channel_id,  # куда необходимо отослать
                                messages=self.id_message_for_forwarded,
                                from_peer=self.user_name_group_for_forwarded_message
                            )
                        except errors.ChannelPrivateError:
                            self.task_done.emit(
                                f'Аккаунт "{self.me.username}" получил бан в чате "{self.user_name_chat}" и будет сменён\n'
                                f'Отправлено сообщений c этого аккаунта: {self.successful_send_message_from_one_account}'
                                f' из {self.max_message_from_one_account}\n'
                                f'Аккаунт {self.counter_account} из {len(self.list_id_accounts)}\n'
                                f'ID потока: {self.thread_id}',
                                [], False, [], '', '', [], False)
                            await self.client.disconnect()
                            self.completed_accounts += 1
                            continue
                        except errors.ChatAdminRequiredError:
                            self.task_done.emit(f'Поток будет остановлен\n'
                                                f'В чате "{self.user_name_chat}" нельзя писать! \n'
                                                f'ID потока: {self.thread_id}', [], False, [], '', f'',[], False)
                            error_sent_message = True
                        except (errors.BroadcastPublicVotersForbiddenError,errors.ChatAdminRequiredError,
                                errors.MediaEmptyError, errors.QuizAnswerMissingError,errors.TopicDeletedError):
                            self.task_done.emit(f'',[], False,[], '',
                                                'Ошибка отправки сообщения!\nНевозможно переслать данное сообщение!',
                                                [],False)
                        except (ValueError, errors.MessageIdsEmptyError, errors.ChannelInvalidError,
                                errors.MessageIdInvalidError):
                            self.task_done.emit(f'',[], False,[], '',
                                                'Ошибка отправки сообщения!\nНеверные данные для пересылки сообщения!',
                                                [],False)
                    else: # если необходимо создать новое сообщение
                        try:
                            if self.use_file_for_message:
                                file_extension = os.path.splitext(self.file_path)[1]
                                if (file_extension == '.jpg' or file_extension == '.jpeg' or file_extension == '.png' or
                                        file_extension == '.gif'):
                                    await self.client.send_file(
                                        entity=target_chat.channel_id,
                                        file=self.file_path,
                                        caption=self.message,
                                        parse_mode='html',
                                        force_document=False  # Важно! False - отправка как фото
                                    )
                                else:
                                    await self.client.send_file(
                                        entity=target_chat.channel_id,
                                        file=self.file_path,
                                        caption=self.message,
                                        parse_mode='html'
                                    )
                            else:
                                await self.client.send_message(
                                    entity=target_chat.channel_id,
                                    message=self.message,
                                    parse_mode='html'
                                )
                        except errors.ChatAdminRequiredError:
                            self.task_done.emit(f'Поток будет остановлен\n'
                                                f'В чате "{self.user_name_chat}" нельзя писать! \n'
                                                f'ID потока: {self.thread_id}', [], False, [], '', f'',[], False)
                            error_sent_message = True
                        except FileNotFoundError:
                            self.task_done.emit(f'', [], False,[], '','Ошибка отсылки файла!\nДобавьте новый файл', [], False)
                        except errors.MessageEmptyError:
                            self.task_done.emit(f'', [], False, [], '',
                                                'Ошибка отправки сообщения!\nСообщение в недопустимом формате UTF-8',
                                                [], False)
                        except errors.MessageTooLongError:
                            self.task_done.emit(f'', [], False,
                                                [], '',
                                                'Ошибка отправки сообщения!\nСообщение слишком длинное.'
                                                '\nМаксимальная длинная сообщения без файла = 4024 символов в UTF-8\n'
                                                'С файлом 1024 символов в UTF-8', [], False)
                        except (errors.ImageProcessFailedError, errors.PhotoInvalidError, errors.MediaInvalidError):
                            self.task_done.emit(f'', [], False,[], '',
                                                'Ошибка отправки сообщения!\nФайл прикреплённый к сообщению невозможно отправить!\n'
                                                'Поменяйте его!',
                                                [], False)

                    # если произошла ошибка при отсылке сообщения при которой необходимо остановить весь поток (проблемы с сообщением)
                    # это когда касается только данного потока, не затрагивая другие
                    if error_sent_message:
                        try:
                            await self.client.disconnect()
                        except UnboundLocalError:
                            pass
                        for _ in range(len(self.list_id_accounts) - self.completed_accounts):  # отправляем сигнал, что каждый аккаунт закончил работу
                            self.task_done.emit('', [], False, [], '', '', [], True)
                        return

                    self.successful_send_message += 1
                    self.successful_send_message_from_one_account += 1
                    self.task_done.emit('', [1,0], False, [], self.user_name_chat, '', [], False) # отсылаем что успешно отправили сообщение
                    await asyncio.sleep(self.time_sleep)
            except asyncio.exceptions.CancelledError:  # если экстренно остановили поток и в методе который вызывается с await может произойти такая ошибка
                return
            except (Exception, TFileNotFound) as e:  # здесь ошибки с аккаунтом откуда отсылаем
                try:
                    await self.client.disconnect()
                except UnboundLocalError:
                    pass
                error_name = str(type(e).__name__)
                if error_name == 'ConnectionError' and self.stop_thread:  # если экстренно остановили поток, может возникнуть такая ошибка
                    return
                connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
                cursor = connection.cursor()
                cursor.execute(f"SELECT user_name FROM accounts WHERE id = ? AND account_status = ?",
                               (id_account, 'active'))
                user_name_from_db = cursor.fetchone()  # берём с БД т.к. мы можем даже не войти в аккаунт и тогда не получим его user_name для вывода
                connection.close()
                error_description_solution = get_description_and_solution(error_name)

                self.task_done.emit(
                    f'На аккаунте "{user_name_from_db[0]}" произошла ошибка он будет убран из активных.\n'
                    f'Ошибка: {error_description_solution[0]}\nОтосланных сообщений c этого аккаунта: '
                    f'{self.successful_send_message_from_one_account} из {self.max_message_from_one_account}\n'
                    f'Аккаунт {self.counter_account} из {len(self.list_id_accounts)}\n'
                    f'ID потока: {self.thread_id}',
                    [], True, [self.account_id, self.last_used],
                    '', '', [error_name, id_account], True)
                self.completed_accounts += 1
                continue

            self.completed_accounts += 1
            if self.completed_accounts >= len(self.list_id_accounts): # если произвели рассылку все аккаунты
                self.task_done.emit(
                    f'Аккаунт "{self.me.username}" закончил рассылку\nОтправлено сообщений: '
                    f'{self.successful_send_message_from_one_account} из {self.max_message_from_one_account}\n'
                    f'Поток завершил рассылку\nОтправлено сообщений: '
                    f'{self.successful_send_message} из {self.max_message_from_one_account * len(self.list_id_accounts)}\n'
                    f'ID потока: {self.thread_id}',
                    [], False, [], '', '', [], True)
            else:
                self.task_done.emit(
                    f'Аккаунт "{self.me.username}" закончил рассылку\nОтправлено сообщений: '
                    f'{self.successful_send_message_from_one_account} из {self.max_message_from_one_account}\n'
                    f'ID потока: {self.thread_id}',
                    [], False, [self.account_id, self.last_used], '', '', [], True)

            try:
                await self.client.disconnect()
            except UnboundLocalError:
                pass

    async def quit_async(self):
        """Асинхронный метод для завершения потока"""
        self.stop_thread = True
        try:
            await self.client.disconnect()
        except Exception:
            pass

        self.task_done.emit(
            f'Поток остановлен. Отправлено сообщений: {self.successful_send_message} из {self.max_message_from_one_account * len(self.list_id_accounts)}\n'
            f'ID потока: {self.thread_id}',
            [], False,[], '', '', [], False)

        for _ in range( len(self.list_id_accounts) - self.completed_accounts):  # отправляем сигнал, что каждый аккаунт закончил работу
            self.task_done.emit('', [], False, [], '', '', [], True)
        self.terminate()  # Принудительное завершение


class WindowMailingByChats(WindowMailingByChatsUi):
    def __init__(self, switch_window):
        super().__init__()
        self.switch_window = switch_window

        self.root_project_dir = '..'

        self.active_threads = []  # ВАЖНО! хранит в себе запущенные потоки
        self.launched_mailing = False  # отображает запущена ли рассылка
        self.original_socket = socket.socket  # прокси который был до
        self.id_and_last_use = []  # хранит массивы в которых tg_id аккаунта и его последнее использование
        self.quantity_accounts_for_mailing = 0  # количество аккаунтов для рассылки
        self.quantity_accounts_ending_mailing = 0  # количество аккаунтов закончивших рассылку
        self.error_and_id_errors_accounts = []  # хранит массивы в которых ошибка и id папки, где произошла эта ошибка
        self.count_attempts = 0 # количество попыток отправки

        self.file_path_for_mailing = '' # путь к файлу для рассылки
        self.user_names_used_chats = [] # чаты по которым отработали

        self.data_forwarded_message = {
            'user_name_channel': '',
            'message_ID': '',
        }

        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()
        cursor.execute(f"SELECT "
                       f"message, "
                       f"quantity_accounts_for_chat, "
                       f"max_message_from_one_account, "
                       f"delay, "
                       f"list_chats, "
                       f"use_file_for_message, "
                       f"user_forwarded_message, "
                       f"user_name_group_for_forwarded, "
                       f"message_ID_for_forwarded_message "
                       f"FROM saved_data_mailing_by_chats")
        data_from_db = cursor.fetchone()
        connection.close()

        # заполнение данных с БД
        self.textEdit_message.setText(data_from_db[0])
        self.lineEdit_quantity_accounts_for_chat.setText(data_from_db[1])
        self.lineEdit_max_message_from_one_account.setText(data_from_db[2])
        self.lineEdit_delay.setText(data_from_db[3])
        self.textEdit_list_chats.setText(data_from_db[4])
        self.checkBox_use_file_for_message.setChecked(data_from_db[5])
        self.checkBox_use_forwarded_message.setChecked(data_from_db[6])
        self.data_forwarded_message['user_name_channel'] = data_from_db[7]
        self.data_forwarded_message['message_ID'] = data_from_db[8]

        # события
        self.pushButton_account.clicked.connect(lambda: self._transition('accounts'))
        self.pushButton_mailing.clicked.connect(lambda: self._transition('mailing_by_users'))
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

        self.pushButton_clear_conclusion.clicked.connect(lambda: self._clear_conclusion())
        self.pushButton_info_quantity_accounts_for_chat.clicked.connect(lambda: self._info_accounts_for_chat())
        self.pushButton_info_streams.clicked.connect(lambda: self._info_streams())
        self.pushButton_info_list_chats.clicked.connect(lambda: self._info_list_chats())

        self.lineEdit_quantity_accounts_for_chat.focusInEvent = lambda event: self._set_default_style_line_edit(
            self.lineEdit_quantity_accounts_for_chat)
        self.lineEdit_max_message_from_one_account.focusInEvent = lambda event: self._set_default_style_line_edit(
            self.lineEdit_max_message_from_one_account)
        self.lineEdit_delay.focusInEvent = lambda event: self._set_default_style_line_edit(
            self.lineEdit_delay)
        self.lineEdit_quantity_streams.focusInEvent = lambda event: self._set_default_style_line_edit(
            self.lineEdit_quantity_streams)
        self.textEdit_message.focusInEvent = lambda event: self._set_default_style_text_edit(self.textEdit_message)
        self.textEdit_list_chats.focusInEvent = lambda event: self._set_default_style_text_edit(self.textEdit_list_chats)

        self.lineEdit_quantity_streams.textChanged.connect(lambda: self._line_edit_quantity_editing_finished())

        self.pushButton_choose_file.clicked.connect(lambda: self._choose_file_for_mailing())
        self.pushButton_choose_forwarded_message.clicked.connect(lambda: self._choose_forwarded_message())

        self.pushButton_start.clicked.connect(lambda: self._start())

        self.textEdit_message.focusLost.connect(self._update_data_in_db) # ЭТО СОБЫТИЕ СОЗДАННО В ПЕРЕОПРЕДЕЛЁННОМ КЛАСС
        self.textEdit_list_chats.focusLost.connect(self._update_data_in_db) # ЭТО СОБЫТИЕ СОЗДАННО В ПЕРЕОПРЕДЕЛЁННОМ КЛАСС
        self.lineEdit_quantity_accounts_for_chat.editingFinished.connect(lambda: self._update_data_in_db(
            self.lineEdit_quantity_accounts_for_chat.text(), 'quantity_accounts_for_chat'))
        self.lineEdit_max_message_from_one_account.editingFinished.connect(lambda: self._update_data_in_db(
            self.lineEdit_max_message_from_one_account.text(), 'max_message_from_one_account'))
        self.lineEdit_delay.editingFinished.connect(lambda: self._update_data_in_db(
            self.lineEdit_delay.text(), 'delay'))
        self.checkBox_use_file_for_message.clicked.connect(lambda: self._update_data_in_db(
            int(self.checkBox_use_file_for_message.isChecked()), 'use_file_for_message'))
        self.checkBox_use_forwarded_message.clicked.connect(lambda: self._update_data_in_db(
            int(self.checkBox_use_forwarded_message.isChecked()), 'user_forwarded_message'))

    def _transition(self, target_window: str):
        if self.launched_mailing:
            error_info = DialogInfo('Внимание!',
                                     'Дождитесь конца рассылки или остановите её!',
                                     'notification.mp3')  # Создаем экземпляр
            error_info.exec_()  # Открываем
        else:
            self.switch_window(target_window)

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

    def _clear_conclusion(self):
        self.textEdit_conclusion.setText('')
        self.label_successfully.setText('0')
        self.label_unsuccessful.setText('0')
        self.label_count_attempts.setText('0')
        self.label_banned_account.setText('0')

    def _info_accounts_for_chat(self):
        info = DialogInfo('Информация',
"""
Определяет, сколько аккаунтов будут поочередно отправлять сообщения в один и тот же чат.

Как это работает?
Первый аккаунт начинает отправлять сообщения.
Он работает до тех пор, пока:
Не получит бан, или
Не исчерпает лимит сообщений для одного аккаунта.
После этого управление переходит к следующему аккаунту, который повторяет процесс.

Пример:
Вы выбрали значение 5. Это значит, что в чате будут работать 5 аккаунтов по очереди:
Аккаунт 1 → Аккаунт 2 → ... → Аккаунт 5 -> конец рассылки.
""",
                          'notification.mp3')  # Создаем экземпляр
        info.exec_()  # Открываем

    def _info_streams(self):
        quantity_accounts = 0
        while True:  # переименовываем папки откуда скопировали
            directory_name = self.root_project_dir + "/accounts/active_accounts/" + str(quantity_accounts)
            if os.path.isdir(directory_name):
                quantity_accounts += 1
            else:
                break

        try:
            thread_limit = str(quantity_accounts // int(self.lineEdit_quantity_accounts_for_chat.text()))
        except ValueError:
            thread_limit = 'Невозможно посчитать\n"Вы не заполнили количество аккаунтов на один чат"'

        info = DialogInfo('Информация',
                           f'Количество потоков - это сколько аккаунтов будут одновременно выполнять рассылку.\n\n'
                           f'Внимание!\n'
                           f'Количество потоков не может превышать: количество аккаунтов / количество выделенных аккаунтов на чат .\n'
                           f'У вас аккаунтов: {quantity_accounts}\n'
                           f'Ваш лимит потоков при данном количестве выделенных аккаунтов на чат: {thread_limit}',
                           'notification.mp3')  # Создаем экземпляр
        info.exec_()  # Открываем

    def _info_list_chats(self):
        info = DialogInfo('Информация',
                          """
Список чатов по которым будет проходить рассылка.

Один чат - одна строка.
Чаты разделяется по переходу на новую строку.
Все пробелы автоматически убираются.

Примеры user_name:
http://t.me/durov
https://t.me/durov
@durov
durov
                          """
                          'notification.mp3')  # Создаем экземпляр
        info.exec_()  # Открываем

    def _line_edit_quantity_editing_finished(self):
        if self.lineEdit_quantity_streams.text() == '0':
            self.lineEdit_quantity_streams.setText('')

        quantity_accounts = 0
        while True:  # переименовываем папки откуда скопировали
            directory_name = self.root_project_dir + "/accounts/active_accounts/" + str(quantity_accounts)
            if os.path.isdir(directory_name):
                quantity_accounts += 1
            else:
                break

        try: # устанавливаем лимит в количество разрешённых потоков
            thread_limit = quantity_accounts // int(self.lineEdit_quantity_accounts_for_chat.text())
        except ValueError: # если не пользователь не написал количество аккаунтов на чат, то лимит будет равен количеству аккаунтов
            thread_limit = quantity_accounts

        try:
            if int(self.lineEdit_quantity_streams.text()) > thread_limit:
                self.lineEdit_quantity_streams.setText(str(thread_limit))
        except ValueError:
            pass

    def _choose_file_for_mailing(self):
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

                info = DialogInfo(title_dialog, message_dialog, "notification.mp3")
                info.exec_()

    def _choose_forwarded_message(self):
        dialog = DialogForwardedMessage(self.data_forwarded_message)  # Создаем экземпляр
        dialog.data_returned.connect(self._set_data_forwarded_message)  # Подключаем сигнал
        dialog.exec_()  # Открываем модальное окно

    def _set_data_forwarded_message(self, data: dict):
        self.data_forwarded_message = data

    def _set_enabled_for_elements(self, enabled: bool):
        self.textEdit_message.setEnabled(enabled)
        self.lineEdit_quantity_accounts_for_chat.setEnabled(enabled)
        self.lineEdit_max_message_from_one_account.setEnabled(enabled)
        self.lineEdit_delay.setEnabled(enabled)
        self.checkBox_use_file_for_message.setEnabled(enabled)
        self.lineEdit_quantity_streams.setEnabled(enabled)
        self.checkBox_use_proxy.setEnabled(enabled)
        self.textEdit_list_chats.setEnabled(enabled)
        self.pushButton_choose_file.setEnabled(enabled)

    def _handler_signal_with_streams(self, console_output: str, counter_created_and_uncreated: list,
                                    account_banned: bool, id_and_last_use: list, user_name_used_chat: str,
                                    error: str, error_and_id_account: list, end_mailing_from_this_account: bool):
        if console_output:
            current_time = dt.datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S")  # Форматируем время сейчас
            self.textEdit_conclusion.append(f'\n[{formatted_time}] {console_output}')

        if counter_created_and_uncreated:
            self.count_attempts += counter_created_and_uncreated[0] + counter_created_and_uncreated[1]
            self.label_successfully.setText(str(counter_created_and_uncreated[0] + int(self.label_successfully.text())))
            self.label_unsuccessful.setText(str(counter_created_and_uncreated[1] + int(self.label_unsuccessful.text())))
            self.label_count_attempts.setText(str(counter_created_and_uncreated[0] + counter_created_and_uncreated[1] + int(self.label_count_attempts.text())))

        if account_banned:
            self.label_banned_account.setText( str(int(self.label_banned_account.text()) + 1))

        if id_and_last_use: # добавление для учёта времени последнего использования аккаунта
            if id_and_last_use[1]:# будем работать если есть время последнего использования
                self.id_and_last_use.append(id_and_last_use)

        if error:
            if self.launched_mailing: # если рассылка запущена
                for thread in self.active_threads: # принудительно завершаем потоки
                    asyncio.run(thread.quit_async())
                self._set_enabled_for_elements(True)
                self.launched_mailing = False # останавливаем рассылку
                info = DialogInfo("Внимание!", error, "notification.mp3")
                info.exec_()

        if error_and_id_account:
            self.error_and_id_errors_accounts.append(error_and_id_account)

        if user_name_used_chat:
            if "@" + user_name_used_chat not in user_name_used_chat: # если такого чата нет
                self.user_names_used_chats.append("@" + user_name_used_chat)

        if end_mailing_from_this_account:
            self.quantity_accounts_ending_mailing += 1

            # если кол-во закончивших рассылку аккаунтов больше или равно запущенных аккаунтов
            if self.quantity_accounts_ending_mailing >= self.quantity_accounts_for_mailing:
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
                self.textEdit_conclusion.append(f'\n[{formatted_time}] РАССЫЛКА ОСТАНОВЛЕННА')
                self.pushButton_start.setText('ЗАПУСТИТЬ')
                self.launched_mailing = False

                self._set_enabled_for_elements(True)
                info = DialogInfo("Готово!", 'Рассылка успешно завершено!',"notification.mp3")
                info.exec_()

                if self.user_names_used_chats: # если есть user_name чатов по которым производили рассылку
                    info_chat_user_name = DialogListUsedChats(self.user_names_used_chats)
                    info_chat_user_name.exec_()

    def _start(self):
        if not self.launched_mailing:  # если создание не запущенно
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

            if (self.textEdit_message.toPlainText().replace('\n', '').replace(' ', '').replace('\t', '') == "" and
                    not self.checkBox_use_forwarded_message.isChecked()):
                error_message += "Введите сообщение для рассылки!\n"
                self.textEdit_message.setStyleSheet(style_text_edit)

            if not check_html_parse(self.textEdit_message.toPlainText()) and self.checkBox_use_forwarded_message.isChecked(): # если неверный HTML синтаксис
                error_message += "В сообщении для рассылки \nвведён некорректный HTML синтаксис!\n"
                self.textEdit_message.setStyleSheet(style_text_edit)

            if self.lineEdit_quantity_accounts_for_chat.text() == "":
                error_message += "Введите количество выделенных аккаунтов на один чат!\n"
                self.lineEdit_quantity_accounts_for_chat.setStyleSheet(style_line_edit)

            if self.lineEdit_max_message_from_one_account.text() == "":
                error_message += "Введите максимум сообщений с одного аккаунта!\n"
                self.lineEdit_max_message_from_one_account.setStyleSheet(style_line_edit)

            if self.lineEdit_delay.text() == "":
                error_message += "Введите задержка между отправкой!\n"
                self.lineEdit_delay.setStyleSheet(style_line_edit)

            if self.lineEdit_quantity_streams.text() == "":
                error_message += "Введите количество запущенных потоков!\n"
                self.lineEdit_quantity_streams.setStyleSheet(style_line_edit)

            chat_name_list = []
            original_chat_list = self.textEdit_list_chats.toPlainText().split('\n')
            for one_name in self.textEdit_list_chats.toPlainText().split('\n'):
                one_name = (one_name.replace(" ", "").replace("\n", "").replace("\t", "").replace('http://t.me/', '')
                            .replace('https://t.me/', '').replace('@', '')) # убираем лишние символы и если остался чат, то добавляем его
                if one_name and one_name not in chat_name_list: # если user_name нет в chat_name_list
                    chat_name_list.append(one_name)

            if not chat_name_list:
                error_message += "Введите корректный список чатов!\n"
                self.textEdit_list_chats.setStyleSheet(style_text_edit)

            if (self.checkBox_use_forwarded_message.isChecked() and
                    not self.data_forwarded_message['user_name_channel'] and
                    not self.data_forwarded_message['message_ID']):
                error_message += "Вы не заполнили данные для пересылки сообщения!"

            if error_message:
                info = DialogInfo("Внимание!", error_message, "notification.mp3")
                info.exec_()
                return

            if len(original_chat_list) > len(chat_name_list):
                info = DialogInfo("Внимание!", "Некоторые чаты не были добавлены в программу "
                                  "из-за несоответствия возможных юзернеймов чата,"
                                  "по ним не будет происходить рассылка!", "notification.mp3")
                info.exec_()

            zero_account = self.root_project_dir + f'/accounts/active_accounts/0'
            if not os.path.isdir(zero_account):  # проверяем есть ли аккаунты для рассылки (это если нету)
                info = DialogInfo("Внимание!", 'У вас нет активных аккаунтов для рассылки!', "notification.mp3")
                info.exec_()
                return

            quantity_accounts = 0
            while True:
                directory_name = self.root_project_dir + "/accounts/active_accounts/" + str(quantity_accounts)
                if os.path.isdir(directory_name):
                    quantity_accounts += 1
                else:
                    break

            thread_limit = quantity_accounts // int(self.lineEdit_quantity_accounts_for_chat.text())

            if int(self.lineEdit_quantity_streams.text()) > thread_limit: # если пользователь указал количество потоков больше чем ему можно
                info = DialogInfo("Внимание!", f'Вы превысили возможное количество потоков!\nВаш лимит: {thread_limit}',
                                  "notification.mp3")
                info.exec_()
                return

            if len(chat_name_list) > thread_limit:
                info = DialogInfo("Информация",
                                  f'У вас чатов больше чем потоков,\n'
                                       f'Последние {len(chat_name_list) - thread_limit} чатов не будут использоваться',
                                  "notification.mp3")
                info.exec_()
            elif thread_limit > len(chat_name_list):
                info = DialogInfo("Информация",
                                  f'У вас потоков больше чем чатов,\n'
                                  f'{thread_limit - len(chat_name_list)} потоков не будет использоваться',
                                  "notification.mp3")
                info.exec_()

            if self.quantity_accounts_ending_mailing < self.quantity_accounts_for_mailing:
                info = DialogInfo("Внимание!", 'Дождитесь завершения работы аккаунтов!', "notification.mp3")
                info.exec_()
                return

            if self.checkBox_use_file_for_message.isChecked():
                if not os.path.isfile(self.file_path_for_mailing):
                    info = DialogInfo("Внимание!", 'Укажите файл для рассылки!', "notification.mp3")
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

            self.count_attempts = 0
            self.launched_mailing = True
            self.id_and_last_use = []
            self.quantity_accounts_for_mailing = 0
            self.quantity_accounts_ending_mailing = 0
            self.error_and_id_errors_accounts = []
            self.used_chats = []

            self._set_enabled_for_elements(False)

            current_time = dt.datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S")  # Форматируем время сейчас
            self.textEdit_conclusion.append(f'[{formatted_time}] РАССЫЛКА ЗАПУЩЕНА\n')

            id_account = 0
            counter_chats = 0
            for thread_id in range(int(self.lineEdit_quantity_streams.text())):  # проходимся по кол-ву потоков
                try:
                    chat_name_list[counter_chats] # тут будет ошибка если чатов меньше чем аккаунтов
                except IndexError:
                    break

                list_id_accounts = []

                for _ in range(int(self.lineEdit_quantity_accounts_for_chat.text())): # формирует id аккаунтов для одного потока
                    if os.path.isdir(self.root_project_dir + f'/accounts/active_accounts/{id_account}'):  # если аккаунт есть
                        list_id_accounts.append(id_account)
                        self.quantity_accounts_for_mailing += 1
                        id_account += 1

                mailing = MailingWithStreams(
                        thread_id=thread_id,
                        list_id_accounts=list_id_accounts,
                        user_name_chat=chat_name_list[counter_chats],
                        message = self.textEdit_message.toPlainText(),
                        use_forwarded_message = self.checkBox_use_forwarded_message.isChecked(),
                        user_name_group_for_forwarded_message = self.data_forwarded_message['user_name_channel'],
                        id_message_for_forwarded = int(self.data_forwarded_message['message_ID']),
                        max_message_from_one_account=self.lineEdit_max_message_from_one_account.text(),
                        time_sleep=self.lineEdit_delay.text(),
                        use_file_for_message=self.checkBox_use_file_for_message.isChecked(),
                        file_path=self.file_path_for_mailing,
                        use_proxy=self.checkBox_use_proxy.isChecked(),
                        ip=proxy_from_db[0], port=proxy_from_db[1], login=proxy_from_db[2], password=proxy_from_db[3])
                mailing.task_done.connect(self._handler_signal_with_streams)  # Подключаем сигнал к слоту
                mailing.start()  # Запускаем поток

                self.active_threads.append(mailing)
                counter_chats += 1

            self.pushButton_start.setText('ОСТАНОВИТЬ')
            self.launched_mailing = True
        else:
            for thread in self.active_threads:
                asyncio.run(thread.quit_async())

