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

from telethon import errors
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

from app.general.views.info import DialogInfo
from app.general.check_proxy import check_proxy
from app.general.views.error_proxy_for_work import DialogErrorProxyForWork
from app.general.error_handler import error_handler
from app.parser.ui.parser_ui import WindowParserUi
from app.general.views.yes_or_cancel import DialogYesOrCancel

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")# 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():# 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path# 3. Установка пути

# Только после этого импортируем PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QLineEdit, QFileDialog


class Parsing(QThread):
    error_and_id_errors_accounts = []  # хранит массивы в которых ошибка и id папки, где произошла эта ошибка
    original_socket = socket.socket  # запоминаем какой сокет был до
    task_done = pyqtSignal(str, list, bool)# Сигнал, который мы будем использовать для обновления интерфейса
    def __init__(self,all_chats: list, online_not_less_than: int = 0, online_more_than: int = 0, gender: str = '',
                 premium_filter: bool = False,photo_filter: bool = False,phone_filter: bool = False,
                 use_language_rus_name: bool = False,use_language_eng_name: bool = False,
                 use_proxy: bool = False,id_proxy: str = '', port: int = 0, login: str = '', password: str = ''):
        super().__init__()
        self.root_project_dir = '..'
        self.all_chats = all_chats
        self.online_not_less_than = int(online_not_less_than)
        self.online_more_than = int(online_more_than)
        self.gender = gender
        self.premium_filter = premium_filter
        self.photo_filter = photo_filter
        self.phone_filter = phone_filter
        self.use_language_rus_name = use_language_rus_name
        self.use_language_eng_name = use_language_eng_name
        self.use_proxy = use_proxy
        self.id_proxy = id_proxy
        self.port = port
        self.login = login
        self.password = password

        self.client = None

    def run(self):
        asyncio.run(self.parsing())

    async def parsing(self):
        if self.use_proxy:
            socks.set_default_proxy(socks.SOCKS5, self.id_proxy, self.port, True, self.login,self.password)  # Установка прокси-соединения
            socket.socket = socks.socksocket

        countSuccessful = 0  # счётчик успешных спарсшенных участников
        countAttempt = 0  # счётчик кол-во исходных пользователей

        me = None
        user_list_one_chat = []
        result_user_list = []
        id_account = 0

        while True:
            try:
                # вход в аккаунт
                if not os.path.isdir(f'{self.root_project_dir}/accounts/active_accounts/{id_account}'): # если аккаунтов нет
                    self.task_done.emit('Аккаунты закончились!', [], True)

                tdesk = TDesktop(f'{self.root_project_dir}/accounts/active_accounts/{id_account}/tdata')
                self.client = await tdesk.ToTelethon(session=f"{self.root_project_dir}/accounts/active_accounts/{id_account}/session.session",
                                                flag=UseCurrentSession)
<<<<<<< HEAD
                await asyncio.wait_for( self.client.connect(),15 ) # вход в аккаунт
=======
                await asyncio.wait_for( self.client.connect(),timeout=7 ) # вход в аккаунт
>>>>>>> d5cd4b4d78a37a2cf276f0ddebf12b9c08eeb563
                me = await self.client.get_me()
                test_id = me.id

                # парсинг по чатам
                user_names = []
                for chat in self.all_chats:  # проходится по всем чатам (chat это имя чата)

                    user_list_one_chat = []
                    try:
                        chat_test = await self.client.get_entity(chat)  # проверка на наличие такого чата

                        if not chat_test.megagroup:  # если не является мегагруппой (чатом)
                            self.task_done.emit(f'"{chat}" это канал. Требуется чат!', [], False)
                            continue

                        # выйдет ошибка если нет участников которые можно спарсить
                        await self.client(GetParticipantsRequest(chat_test.id, ChannelParticipantsSearch(''), offset=0, limit=1,hash=0))
                        user_list_one_chat = self.client.iter_participants(chat)  # собираем всех участников чата
                    except (errors.UsernameInvalidError, ValueError, AttributeError):
                        self.task_done.emit(f'Чат "{chat}" не найден', [], False)
                        continue
                    except (errors.ChatAdminRequiredError, errors.ChannelPrivateError):
                        self.task_done.emit(f'Чат "{chat}" является приватным', [], False)
                        continue

                    count_admin = 0
                    count_iteration = 0
                    async for user in user_list_one_chat:
                        count_iteration += 1
                        try:
                            if user.participant.admin_rights:  # если нашли админа
                                count_admin += 1
                        except AttributeError:  # у обычных пользователей нет такой переменной, тогда выйдет эта ошибка
                            pass
                        if user_list_one_chat.total == count_admin:  # если кол-во админов совпадает с кол-во участников чата
                            self.task_done.emit(f'У чата "{chat}" закрыт список пользователей', [], False)

                        if count_iteration > 100:  # если мы прошлись более 100 раз (не будет же в одном чате 100 админов)
                            async for user in user_list_one_chat:
                                countAttempt += 1
                                if not user.bot and user.username:
                                    user_names.append(user)

                            self.task_done.emit(f'Успешно спаршена база пользователей с чата: "{chat}"', [], False)
                            break

                await self.client.disconnect()
                break
            except (Exception, TFileNotFound) as e: # если с аккаунтом произошла ошибка
                try:
                    await self.client.disconnect()
                except UnboundLocalError:
                    pass
                error_type = type(e)
                self.error_and_id_errors_accounts.append([str(error_type.__name__), id_account])
                self.task_done.emit(f'У аккаунта с id = {test_id} возникла ошибка,'
                                    f'\nон будет перемещён из активных аккаунтов', [], False)
                self.task_done.emit(f'Парсинг начнётся заново', [], False)

                id_account += 1

        socket.socket = self.original_socket  # работа с телеграммом на этом этапе закончена -> можно убрать прокси

        if (self.online_not_less_than == 0 and self.online_more_than == 0 and not self.gender and not self.premium_filter
            and not self.photo_filter and not self.phone_filter and not self.use_language_rus_name
            and not self.use_language_eng_name): # если не надо использовать фильтры

            for user in user_names:
                countSuccessful += 1
                result_user_list.append(user.username)
        else: # если есть фильтры на парсинг
            self.task_done.emit(f'База успешно спаршена, производится фильтрация', [], False)
            moscow_tz = pytz.timezone('Europe/Moscow')

            if self.online_not_less_than != 0:  # последний онлайн не менее чем
                required_date = dt.datetime.now(moscow_tz) - dt.timedelta(days=self.online_not_less_than)

            if self.online_more_than != 0: # последний онлайн более чем
                required_date = dt.datetime.now(moscow_tz) - dt.timedelta(days=self.online_more_than)

            if self.gender or self.use_language_rus_name or self.use_language_eng_name:
                connection = sqlite3.connect(f'{self.root_project_dir}/working_files/data_base_for_parsing.sqlite3')
                cursor = connection.cursor()

            for user in user_names:  # смысл цикла: проходится по каждому пользователю и проходит фильтры который использует пользователь,
                try:  # если не удовлетворяет фильтру, то такому пользователю мы ставим add_user == False и не вписываем его в конечный массив

                    if self.online_not_less_than != 0: # фильтр по последнему заходу не менее чем
                        dt_user_format_UTF = user.status.was_online
                        dt_user = dt_user_format_UTF.astimezone(moscow_tz)
                        if dt_user < required_date:  # если заходил на аккаунт менее чем переданное значение
                            continue

                    if self.online_more_than != 0:  # если применён фильтр (Заход более чем 30 дней назад)
                        dt_user_format_UTF = user.status.was_online
                        dt_user = dt_user_format_UTF.astimezone(moscow_tz)
                        if dt_user > required_date:  # если заходил на аккаунт менее чем за выбранное значение
                            continue

                    if self.use_language_rus_name:
                        cursor.execute(f"SELECT name FROM {self.gender + '_rus'} WHERE name = ?",
                                       (f"{user.first_name.lower()}",))
                        result_db = cursor.fetchall()
                        if not result_db:  # если нет результата поиска
                            continue

                    if self.use_language_eng_name:
                        cursor.execute(f"SELECT name FROM {self.gender + '_eng'} WHERE name = ?",
                                       (f"{user.first_name.lower()}",))
                        result_db = cursor.fetchall()
                        if not result_db:  # если нет результата поиска
                            continue

                    if self.gender:
                        cursor.execute(f"SELECT name FROM {self.gender} WHERE name = ?",
                                       (f"{user.first_name.lower()}",))
                        result_db = cursor.fetchall()
                        if not result_db:  # если нет результата поиска
                            continue

                    if self.premium_filter:
                        if not user.premium:
                            continue

                    if self.photo_filter:
                        if not user.photo:
                            continue

                    if self.phone_filter:
                        if not user.phone:
                            continue
                    # если дошли до этого момента значит прошли все фильтры и можно включить в конечный список этого юзера
                    result_user_list.append(user.username)
                    countSuccessful += 1

                except (AttributeError, TypeError) as e:  # если нет даты захода
                    continue
            if self.gender or self.use_language_rus_name or self.use_language_eng_name:
                connection.close()

        sorted_list = sorted(self.error_and_id_errors_accounts, key=lambda x: x[1], reverse=True)
        for error_and_id in sorted_list:  # работаем с аккаунтами, где вышла ошибка
            error_handler(error_and_id[0], error_and_id[1], 'active')

        result_user_list = list(set(result_user_list)) # убираем повторяющиеся элементы
        self.task_done.emit(f'Парсинг завершён\nУспешно записано {countSuccessful} из {countAttempt}', result_user_list, True)

    async def quit_async(self):
        """Асинхронный метод для завершения потока"""
        try:
            await self.client.disconnect()
        except Exception:
            pass
        self.terminate()  # Принудительное завершение

class WindowParser(WindowParserUi):
    def __init__(self,switch_window):
        super().__init__()
        self.launched_parsing = False  # отображает запущенна ли рассылка
        self.root_project_dir = '..'
        self.switch_window = switch_window
        self.active_threads = []  # ВАЖНО! хранит в себе запущенные потоки
        self._show_parsing_result()

        # события
        self.pushButton_account.clicked.connect(lambda: self._transition('accounts'))
        self.pushButton_mailing.clicked.connect(lambda: self._transition('mailing_by_users'))
        self.pushButton_mailing_chat.clicked.connect(lambda: self._transition('mailing_by_chats'))
        self.pushButton_invite.clicked.connect(lambda: self._transition('invite'))
        self.pushButton_proxy.clicked.connect(lambda: self._transition('proxy'))
        self.pushButton_bomber.clicked.connect(lambda: self._transition('bomber'))
        self.pushButton_create_channel.clicked.connect(lambda: self._transition('create_channel'))
<<<<<<< HEAD
        self.pushButton_create_bot.clicked.connect(lambda: self._transition('create_bot'))
=======
>>>>>>> d5cd4b4d78a37a2cf276f0ddebf12b9c08eeb563
        self.pushButton_enter_group.clicked.connect(lambda: self._transition('enter_group'))
        self.pushButton_reactions.clicked.connect(lambda: self._transition('reactions'))
        self.pushButton_comment.clicked.connect(lambda: self._transition('comment'))
        self.pushButton_convert.clicked.connect(lambda: self._transition('convert'))
        self.pushButton_doc.clicked.connect(lambda: self._transition('doc'))

        self.pushButton_start.clicked.connect(lambda: self._start_parsing())

        self.checkBox_online_not_less_than.clicked.connect(
            lambda: self._change_last_online(self.checkBox_online_not_less_than, self.checkBox_online_not_less_than.isChecked()))
        self.checkBox_online_more_than.clicked.connect(
            lambda: self._change_last_online(self.checkBox_online_more_than,self.checkBox_online_more_than.isChecked()))

        self.checkBox_man.clicked.connect(lambda: self._change_gender(self.checkBox_man,self.checkBox_man.isChecked()))
        self.checkBox_woman.clicked.connect(lambda: self._change_gender(self.checkBox_woman,self.checkBox_woman.isChecked()))

        self.checkBox_rus_name.clicked.connect(lambda: self._change_language_name(self.checkBox_rus_name,
                                                                                  self.checkBox_rus_name.isChecked()))
        self.checkBox_eng_name.clicked.connect(lambda: self._change_language_name(self.checkBox_eng_name,
                                                                                  self.checkBox_eng_name.isChecked()))
        self.pushButton_clear_conclusion.clicked.connect(lambda: self.textEdit_conclusion.clear())

        self.pushButton_uploads_the_list.clicked.connect(lambda: self._uploads_user_list())
        self.pushButton_download_list.clicked.connect(lambda: self._question_input_file())

        self.textEdit_name_chat.selectionChanged.connect(lambda: self._set_default_style(self.textEdit_name_chat)) # при получении фокуса
        self.textEdit_users_list.textChanged.connect(lambda: self._update_txt_file())
        # события

    def _transition(self, target_window: str):
        if self.launched_parsing:
            info = DialogInfo('Внимание!',
                                     'Дождитесь конца парсинга!\nЭто необходимо для предотвращения возможных ошибок.',
                                     'notification.mp3')  # Создаем экземпляр
            info.exec_()  # Открываем
        else:
            self.switch_window(target_window)

    def _show_parsing_result(self):
        with open(f'{self.root_project_dir}/working_files/parsing_result.txt', "r", encoding="utf-8") as file:
            self.textEdit_users_list.setText(file.read()) # Читает весь файл в одну строку

    def _uploads_user_list(self):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")  # Получаем путь к рабочему столу
        # Открываем диалог выбора папки, начнем с рабочего стола
        # если пользователь выбрал папку, то вернётся путь иначе None
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите путь", desktop_path)

        if folder_path:  # если пользователь выбрал папку (хранит выбранный путь)
            counts = 1
            file_name = '/список пользователей'

            while True:
                try:
                    # копирование
                    shutil.copy(f'{self.root_project_dir}/working_files/parsing_result.txt',f'{folder_path}{file_name}.txt')

                    info = DialogInfo('Успешно!',f'Файл успешно выгружен по пути:\n{folder_path}{file_name}.txt',
                                             'notification.mp3')  # Создаем экземпляр
                    info.exec_()  # Открываем
                    break
                except FileExistsError:
                    folder_name = f'/аккаунты с ошибкой входа ({counts}).txt'
                    counts += 1
                except FileNotFoundError:
                    error_info = DialogInfo('Ошибка!', 'Указанный путь не найден!','notification.mp3')  # Создаем экземпляр
                    error_info.exec_()  # Открываем
                    break

    def _question_input_file(self):
        Dialog1 = DialogYesOrCancel('Внимание!',
                                       'При загрузке вашего списка пользователей \n'
                                       'данные из файла имеющегося в программе будут удалены\n'
                                       'Вы действительно хотите это сделать?',
                                       'notification.mp3')  # Создаем экземпляр
        Dialog1.data_returned.connect(self._start_input_file)  # Подключаем сигнал
        Dialog1.exec_()  # Открываем модальное окно

    def _start_input_file(self, answer: bool):
        if not answer: # если пользователь отказался загружать файл
            return

        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")  # Получаем путь к рабочему столу
        # Открываем диалог выбора папки, начнем с рабочего стола
        # если пользователь выбрал папку, то вернётся путь иначе None
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", desktop_path, "Текстовые файлы (*.txt)"  )

        if file_path:  # если пользователь выбрал папку (хранит выбранный путь)
            while True:
                try:
                    text_in_file = ''
                    with open(file_path, "r", encoding="utf-8") as file:
                        text_in_file = file.read()  # Читает весь файл в одну строку


                    with open(f'{self.root_project_dir}/working_files/parsing_result.txt', "w", encoding="utf-8") as file:
                        file.write(text_in_file)  # записываем данные

                    self._show_parsing_result()

                    info = DialogInfo('Успешно!', f'Данные успешно загружены!','notification.mp3')  # Создаем экземпляр
                    info.exec_()  # Открываем
                    break
                except FileNotFoundError:
                    error_info = DialogInfo('Ошибка!', 'Указанный путь не найден!','notification.mp3')  # Создаем экземпляр
                    error_info.exec_()  # Открываем
                    break
                except Exception as e:
                    error_info = DialogInfo('Ошибка!', f'Ошибка: {e}!','notification.mp3')  # Создаем экземпляр
                    error_info.exec_()  # Открываем
                    break

    def _change_last_online(self, checkbox_target: QCheckBox,last_checked: bool):
        self.checkBox_online_not_less_than.setChecked(False)
        self.checkBox_online_more_than.setChecked(False)
        checkbox_target.setChecked(last_checked)

    def _change_gender(self, checkbox_target: QCheckBox,last_checked: bool):
        self.checkBox_man.setChecked(False)
        self.checkBox_woman.setChecked(False)
        checkbox_target.setChecked(last_checked)

        if not last_checked: # если убрали фильтр
            self.checkBox_rus_name.setChecked(False)
            self.checkBox_eng_name.setChecked(False)

    def _change_language_name(self, checkbox_target: QCheckBox,last_checked: bool):
        if not self.checkBox_man.isChecked() and not self.checkBox_woman.isChecked():
            self.checkBox_rus_name.setChecked(False)
            self.checkBox_eng_name.setChecked(False)
            info = DialogInfo('Внимание!', 'Данный фильтр используется только с выбранным полом!',
                               'notification.mp3')  # Создаем экземпляр
            info.exec_()  # Открываем
            return

        self.checkBox_rus_name.setChecked(False)
        self.checkBox_eng_name.setChecked(False)
        checkbox_target.setChecked(last_checked)

    def _set_default_style(self,line_edit: QLineEdit):
        style = ("""QTextEdit {
                  background-color: rgb(255, 255, 255);
                  color: rgb(0, 0, 0);
                  border-radius: 20px;
                padding-top: 15px; /* Отступ только слева */   
                padding-bottom: 15px; /* Отступ только снизу */
              }""")
        line_edit.setStyleSheet(style)

    def _update_txt_file(self):
        new_text = self.textEdit_users_list.toPlainText()
        with open(f'{self.root_project_dir}/working_files/parsing_result.txt', 'w', encoding='utf-8') as file:
            file.write(new_text)

    def _start_parsing(self):
        if self.launched_parsing:
            info = DialogInfo('Внимание!','Дождитесь конца парсинга!','notification.mp3')  # Создаем экземпляр
            info.exec_()  # Открываем
        else:
            proxy = False
            proxy_from_db = ['', 0, '', '']
            # Удаляем все пробелы (включая пробелы между словами)
            string_chat_list = self.textEdit_name_chat.toPlainText().replace(" ", "")

            if string_chat_list == '':
                self.textEdit_name_chat.setStyleSheet("background-color: rgb(252, 224, 228);"
                                                    "border-radius: 20px;"
                                                    "padding-top: 15px; /* Отступ только слева */   "
                                                    "padding-bottom: 15px; /* Отступ только снизу */")

                info = DialogInfo('Внимание!','Заполните поле с чатами!','notification.mp3')  # Создаем экземпляр
                info.exec_()  # Открываем
                return

            if self.checkBox_use_proxy.isChecked():
                proxy = True
                connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
                cursor = connection.cursor()
                cursor.execute(f"SELECT ip,port,login,password,use_proxy_to_enter FROM proxy")
                proxy_from_db = cursor.fetchone()
                connection.close()

                efficiency = check_proxy(proxy_from_db[0], int(proxy_from_db[1]), proxy_from_db[2], proxy_from_db[3])
                if not efficiency:  # если прокси не действительно
                    error_proxy = DialogErrorProxyForWork(proxy_from_db[0], str(proxy_from_db[1]), proxy_from_db[2],proxy_from_db[3])  # Создаем экземпляр
                    error_proxy.show_info()
                    error_proxy.exec_()  # Открываем
                    return

            if not os.path.isdir(f'{self.root_project_dir}/accounts/active_accounts/0'):
                info = DialogInfo('Внимание!', 'У вас нет ни одного аккаунта!', 'notification.mp3')  # Создаем экземпляр
                info.exec_()  # Открываем
                return

            # Разбиваем строку по переводам строки, удаляя пустые строки
            all_chats = [line for line in string_chat_list.split('\n') if line]
            all_chats = list(set(all_chats)) # убираем повторяющиеся элементы

            online_not_less_than = 0
            online_more_than = 0
            open_phone = False
            photo = False
            premium_filter = False
            gender = ''
            use_language_rus_name = False
            use_language_eng_name = False

            for thread in self.active_threads:
                asyncio.run(thread.quit_async())
            self.active_threads.clear()

            if self.checkBox_online_not_less_than.isChecked():
                online_not_less_than = self.lineEdit_online_not_less_than.text()

            if self.checkBox_online_more_than.isChecked():
                online_more_than = self.lineEdit_online_more_than.text()

            if self.checkBox_phone.isChecked():
                open_phone = True

            if self.checkBox_photo.isChecked():
                photo = True

            if self.checkBox_tg_premium.isChecked():
                premium_filter = True

            if self.checkBox_man.isChecked():
                gender = 'man'

            if self.checkBox_woman.isChecked():
                gender = 'woman'

            if self.checkBox_rus_name.isChecked():
                use_language_rus_name = True

            if self.checkBox_eng_name.isChecked():
                use_language_eng_name = True

            parsing_stream = Parsing(all_chats, online_not_less_than, online_more_than, gender, premium_filter,
                                    photo, open_phone, use_language_rus_name, use_language_eng_name,
                                    proxy, proxy_from_db[0],proxy_from_db[1], proxy_from_db[2], proxy_from_db[3])  # Инициализируем рабочий поток
            parsing_stream.task_done.connect(self._parsing_done)  # Подключаем сигнал к слоту
            parsing_stream.start()  # Запускаем поток

            self.active_threads.append(parsing_stream)

            self.launched_parsing = True

            current_time = dt.datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S")  # Форматируем время сейчас
            self.textEdit_conclusion.append(f'[{formatted_time}] Парсинг запущен...')
            self.pushButton_start.setText('В процессе...')

    def _parsing_done(self, console_output: str, result_user_list: list, end_parsing: bool):
        if console_output:
            current_time = dt.datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S")  # Форматируем время сейчас
            self.textEdit_conclusion.append(f'[{formatted_time}] {console_output}')

        if result_user_list:
            existing_items = list()  # Сюда будем сохранять уникальные значения из файла

            try:
                with open(f'{self.root_project_dir}/working_files/parsing_result.txt', 'r', encoding='utf-8') as file:
                    # Читаем файл построчно
                    for line in file:
                        cleaned_line = line.strip()# Удаляем пробелы
                        cleaned_line = cleaned_line.replace('@', '') # Удаляем символ @
                        if cleaned_line:  # Пропускаем пустые строки
                            existing_items.append(cleaned_line)
            except FileNotFoundError:# Если файла нет - начинаем с пустого множества
                pass

            items_to_add = [] # элементы для добавления в txt файл

            # Проверяем каждый новый элемент
            for user in result_user_list:
                if user not in existing_items:# Проверяем, есть ли он уже в файле
                    items_to_add.append(user)
                    # Добавляем в существующие, чтобы избежать дубликатов в новых данных
                    existing_items.append(user)

            with open(f'{self.root_project_dir}/working_files/parsing_result.txt', "a", encoding="utf-8") as file:
                for i, user in enumerate(items_to_add):
                    if i < len(items_to_add) - 1:  # Если элемент не последний
                        file.write(f"@{user}\n")
                    else:  # Последний элемент — без \n
                        file.write(f"@{user}")

            self._show_parsing_result()
        if end_parsing:
            self.launched_parsing = False
            self.pushButton_start.setText('ЗАПУСТИТЬ')
            self.textEdit_conclusion.append('\n')
            info = DialogInfo('Успешно!', f'Парсинг завершён!','notification.mp3')  # Создаем экземпляр
            info.exec_()  # Открываем


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = WindowParser('fbdgf')
    ui.show()
    sys.exit(app.exec_())
