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


class parsing(QThread):
    root_project_dir = '..'

    error_and_id_errors_accounts = []  # хранит массивы в которых ошибка и id папки, где произошла эта ошибка
    original_socket = socket.socket  # запоминаем какой сокет был до
    task_done = pyqtSignal(str, list, bool)# Сигнал, который мы будем использовать для обновления интерфейса
    def __init__(self,all_chats: list, online_not_less_than: int = 0, online_more_than: int = 0, gender: str = '',
                 premium_filter: bool = False,photo_filter: bool = False,phone_filter: bool = False,
                 use_language_rus_name: bool = False,use_language_eng_name: bool = False,
                 use_proxy: bool = False,id_proxy: str = '', port: int = 0, login: str = '', password: str = ''):
        super().__init__()
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
                client = await tdesk.ToTelethon(session=f"{self.root_project_dir}/accounts/active_accounts/{id_account}/session.session",
                                                flag=UseCurrentSession)
                await asyncio.wait_for( client.connect(),timeout=7 ) # вход в аккаунт
                me = await client.get_me()
                test_id = me.id

                # парсинг по чатам
                user_names = []
                for chat in self.all_chats:  # проходится по всем чатам (chat это имя чата)

                    user_list_one_chat = []
                    try:
                        chat_test = await client.get_entity(chat)  # проверка на наличие такого чата

                        if not chat_test.megagroup:  # если не является мегагруппой (чатом)
                            self.task_done.emit(f'"{chat}" это канал. Требуется чат!', [], False)
                            continue

                        # выйдет ошибка если нет участников которые можно спарсить
                        await client(GetParticipantsRequest(chat_test.id, ChannelParticipantsSearch(''), offset=0, limit=1,hash=0))
                        user_list_one_chat = client.iter_participants(chat)  # собираем всех участников чата
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

                await client.disconnect()
                break
            except (Exception, TFileNotFound) as e: # если с аккаунтом произошла ошибка
                try:
                    await client.disconnect()
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


class Window_parser(QtWidgets.QMainWindow):
    root_project_dir = '..'

    launched_parsing = False  # отображает запущенна ли рассылка

    def __init__(self,switch_window):
        super().__init__()
        self.switch_window = switch_window

        self.active_threads = []  # ВАЖНО! хранит в себе запущенные потоки

        self.setObjectName("MainWindow")
        self.resize(1500, 850)
        self.setMinimumSize(QtCore.QSize(1200, 750))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.setFont(font)
        self.setStyleSheet("background-color: rgb(236, 237, 240);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_5.setContentsMargins(0, 0, -1, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.scrollArea_4 = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_4.sizePolicy().hasHeightForWidth())
        self.scrollArea_4.setSizePolicy(sizePolicy)
        self.scrollArea_4.setMinimumSize(QtCore.QSize(270, 0))
        self.scrollArea_4.setMaximumSize(QtCore.QSize(270, 16777215))
        self.scrollArea_4.setStyleSheet("background-color: rgb(14, 22, 33);\n"
                                        "border: none;")
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollArea_4.setObjectName("scrollArea_4")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 270, 850))
        self.scrollAreaWidgetContents_4.setStyleSheet("")
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_4)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_account_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
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
        self.label_12 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setMinimumSize(QtCore.QSize(0, 0))
        self.label_12.setText("")
        self.label_12.setObjectName("label_12")
        self.verticalLayout.addWidget(self.label_12)
        self.pushButton_account = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
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
        self.pushButton_mailing = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
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
        icon2.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/mailing.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.pushButton_mailing.setIcon(icon2)
        self.pushButton_mailing.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_mailing.setObjectName("pushButton_mailing")
        self.verticalLayout.addWidget(self.pushButton_mailing)
        self.pushButton_mailing_chat = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
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
        self.pushButton_invite = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
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
        self.pushButton_parser = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
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
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/panel/parser.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.pushButton_parser.setIcon(icon4)
        self.pushButton_parser.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_parser.setObjectName("pushButton_parser")
        self.verticalLayout.addWidget(self.pushButton_parser)
        self.pushButton_proxy = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
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
        self.pushButton_bomber = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
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
        self.pushButton_enter_group = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
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
        self.pushButton_reactions = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
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
        self.pushButton_comment = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
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
        self.pushButton_convert = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
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
        self.pushButton_doc = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
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
        self.label_13 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setMinimumSize(QtCore.QSize(0, 0))
        self.label_13.setText("")
        self.label_13.setObjectName("label_13")
        self.verticalLayout.addWidget(self.label_13)
        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)
        self.gridLayout_5.addWidget(self.scrollArea_4, 0, 0, 4, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(27, -1, -1, 10)
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
        self.gridLayout_5.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setContentsMargins(20, -1, 20, -1)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("")
        self.label_7.setObjectName("label_7")
        self.gridLayout_9.addWidget(self.label_7, 0, 0, 1, 1)
        self.scrollArea_5 = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_5.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea_5.setStyleSheet("border: 0;")
        self.scrollArea_5.setWidgetResizable(True)
        self.scrollArea_5.setObjectName("scrollArea_5")
        self.scrollAreaWidgetContents_5 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_5.setGeometry(QtCore.QRect(0, 0, 524, 315))
        self.scrollAreaWidgetContents_5.setStyleSheet("""
                                                    /* СТИЛЬ ВЕРТИКАЛЬНОГО СКРОЛЛБАРА */
                                                    QScrollBar:vertical {
                                                        border-radius: 8px;
                                                        background-color: rgb(255, 255, 255);
                                                        width: 14px;
                                                        margin: 0px 0 0px 0;
                                                    }
                                                    
                                                    /* HANDLE BAR ВЕРТИКАЛЬНОГО СКРОЛЛБАРА */
                                                    QScrollBar::handle:vertical {  
                                                        background-color: rgb(210, 210, 213);
                                                        min-height: 30px;
                                                        border-radius: 0px;
                                                        margin: 15px 0 15px 0;  /* Добавлены отступы сверху и снизу */
                                                        transition: background-color 0.2s ease;
                                                    }
                                                    
                                                    QScrollBar::handle:vertical:hover {  
                                                        background-color: rgb(180, 180, 184);
                                                    }
                                                    
                                                    QScrollBar::handle:vertical:pressed {  
                                                        background-color: rgb(150, 150, 153);
                                                    }
                                                    
                                                    /* КНОПКА ВВЕРХУ - ВЕРТИКАЛЬНЫЙ СКРОЛЛБАР */
                                                    QScrollBar::sub-line:vertical {
                                                        border: none;  
                                                        background-color: rgb(190, 190, 193);
                                                        height: 15px;
                                                        border-top-left-radius: 7px;
                                                        border-top-right-radius: 7px;
                                                        subcontrol-position: top;
                                                        subcontrol-origin: margin;
                                                    }
                                                    
                                                    QScrollBar::sub-line:vertical:hover {  
                                                        background-color: rgb(170, 170, 174);
                                                    }
                                                    
                                                    QScrollBar::sub-line:vertical:pressed {  
                                                        background-color: rgb(140, 140, 143);
                                                    }
                                                    
                                                    /* КНОПКА ВНИЗУ - ВЕРТИКАЛЬНЫЙ СКРОЛЛБАР */
                                                    QScrollBar::add-line:vertical {
                                                        border: none;  
                                                        background-color: rgb(190, 190, 193);
                                                        height: 15px;
                                                        border-bottom-left-radius: 7px;
                                                        border-bottom-right-radius: 7px;
                                                        subcontrol-position: bottom;
                                                        subcontrol-origin: margin;
                                                    }
                                                    
                                                    QScrollBar::add-line:vertical:hover {  
                                                        background-color: rgb(170, 170, 174);
                                                    }
                                                    
                                                    QScrollBar::add-line:vertical:pressed {  
                                                        background-color: rgb(140, 140, 143);
                                                    }
                                                    
                                                    /* УБРАТЬ СТРЕЛКИ */
                                                    QScrollBar::up-arrow:vertical, 
                                                    QScrollBar::down-arrow:vertical {
                                                        background: none;
                                                    }
                                                    
                                                    /* УБРАТЬ ФОН */
                                                    QScrollBar::add-page:vertical, 
                                                    QScrollBar::sub-page:vertical {
                                                        background: none;
                                                    }
                                                    """)
        self.scrollAreaWidgetContents_5.setObjectName("scrollAreaWidgetContents_5")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_5)
        self.gridLayout_10.setContentsMargins(-1, -1, -1, 10)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.gridLayout_11 = QtWidgets.QGridLayout()
        self.gridLayout_11.setContentsMargins(0, -1, -1, -1)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.textEdit_name_chat = QtWidgets.QTextEdit(self.scrollAreaWidgetContents_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_name_chat.sizePolicy().hasHeightForWidth())
        self.textEdit_name_chat.setSizePolicy(sizePolicy)
        self.textEdit_name_chat.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.textEdit_name_chat.setFont(font)
        self.textEdit_name_chat.setStyleSheet("""
                                                  QTextEdit {
                                                    background-color: rgb(255, 255, 255);
                                                    color: rgb(0, 0, 0);
                                                    border-radius: 20px;
                                                    padding-top: 15px; /* Отступ только слева */   
                                                    padding-bottom: 15px; /* Отступ только снизу */
                                                  }
                                              """)
        self.textEdit_name_chat.setAcceptRichText(False) # 1. Запрещаем форматированный текст
        self.textEdit_name_chat.setDocumentTitle("")
        self.textEdit_name_chat.setReadOnly(False)
        self.textEdit_name_chat.setPlaceholderText(
            "t.me/durov\nt.me/durov\n@durov\n@durov")
        self.textEdit_name_chat.setObjectName("textEdit_name_chat")
        self.gridLayout_11.addWidget(self.textEdit_name_chat, 0, 0, 1, 1)
        self.gridLayout_10.addLayout(self.gridLayout_11, 1, 0, 1, 1)
        self.scrollArea_5.setWidget(self.scrollAreaWidgetContents_5)
        self.gridLayout_9.addWidget(self.scrollArea_5, 1, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_9, 1, 1, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setStyleSheet("")
        self.label_3.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.checkBox_online_not_less_than = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox_online_not_less_than.setFont(font)
        self.checkBox_online_not_less_than.setStyleSheet("QCheckBox {\n"
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
        self.checkBox_online_not_less_than.setObjectName("checkBox_online_not_less_than")
        self.gridLayout.addWidget(self.checkBox_online_not_less_than, 1, 0, 1, 2)
        self.lineEdit_online_not_less_than = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_online_not_less_than.setMaximumSize(QtCore.QSize(50, 31))
        validator = QIntValidator(1, 999)  # Минимум 0, максимум большое число
        self.lineEdit_online_not_less_than.setValidator(validator)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_online_not_less_than.setFont(font)
        self.lineEdit_online_not_less_than.setMaxLength(3)
        self.lineEdit_online_not_less_than.setStyleSheet("QLineEdit {"
                                                        "	background-color: rgb(255, 255, 255);      /* Цвет фона текстового поля */"
                                                        "    border: 2px solid rgb(150, 150, 150); /* Рамка текстового поля */"
                                                        "    border-radius: 6px; /* Закругление углов */"
                                                        "    padding: 2px; /* Отступы внутри текстового поля */"
                                                        "    color: rgb(50, 50, 50); /* Цвет текста */"
                                                        "}"
                                                        ""
                                                        "/* Состояние при наведении */"
                                                        "QLineEdit:hover {"
                                                        "    border: 2px solid rgb(160, 160, 160); /* Цвет рамки при наведении */"
                                                        "}"
                                                        ""
                                                        "/* Состояние при фокусировке */"
                                                        "QLineEdit:focus {"
                                                        "    border: 2px solid rgb(0, 0, 0); /* Цвет рамки при фокусировке */"
                                                        "    background-color: rgb(255, 255, 255); /* Цвет фона при фокусировке */"
                                                        "}"
                                                        ""
                                                        "/* Состояние для отключенного текстового поля */"
                                                        "QLineEdit:disabled {"
                                                        "    background-color: rgb(220, 220, 220); /* Цвет фона для отключенного */"
                                                        "    color: rgb(170, 170, 170); /* Цвет текста для отключенного */"
                                                        "    border: 2px solid rgb(200, 200, 200); /* Цвет рамки для отключенного */"
                                                        "}")
        self.lineEdit_online_not_less_than.setObjectName("lineEdit_online_not_less_than")
        self.gridLayout.addWidget(self.lineEdit_online_not_less_than, 1, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
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
        self.gridLayout.addWidget(self.label_5, 1, 3, 1, 1)
        self.checkBox_online_more_than = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox_online_more_than.setFont(font)
        self.checkBox_online_more_than.setStyleSheet("QCheckBox {\n"
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
        self.checkBox_online_more_than.setObjectName("checkBox_online_more_than")
        self.gridLayout.addWidget(self.checkBox_online_more_than, 2, 0, 1, 2)
        self.lineEdit_online_more_than = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_online_more_than.setMaximumSize(QtCore.QSize(50, 31))
        validator = QIntValidator(1, 999)  # Минимум 0, максимум большое число
        self.lineEdit_online_more_than.setValidator(validator)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineEdit_online_more_than.setFont(font)
        self.lineEdit_online_more_than.setMaxLength(3)
        self.lineEdit_online_more_than.setStyleSheet("QLineEdit {"
                                                    "	background-color: rgb(255, 255, 255);      /* Цвет фона текстового поля */"
                                                    "    border: 2px solid rgb(150, 150, 150); /* Рамка текстового поля */"
                                                    "    border-radius: 6px; /* Закругление углов */"
                                                    "    padding: 2px; /* Отступы внутри текстового поля */"
                                                    "    color: rgb(50, 50, 50); /* Цвет текста */"
                                                    "}"
                                                    ""
                                                    "/* Состояние при наведении */"
                                                    "QLineEdit:hover {"
                                                    "    border: 2px solid rgb(160, 160, 160); /* Цвет рамки при наведении */"
                                                    "}"
                                                    ""
                                                    "/* Состояние при фокусировке */"
                                                    "QLineEdit:focus {"
                                                    "    border: 2px solid rgb(0, 0, 0); /* Цвет рамки при фокусировке */"
                                                    "    background-color: rgb(255, 255, 255); /* Цвет фона при фокусировке */"
                                                    "}"
                                                    ""
                                                    "/* Состояние для отключенного текстового поля */"
                                                    "QLineEdit:disabled {"
                                                    "    background-color: rgb(220, 220, 220); /* Цвет фона для отключенного */"
                                                    "    color: rgb(170, 170, 170); /* Цвет текста для отключенного */"
                                                    "    border: 2px solid rgb(200, 200, 200); /* Цвет рамки для отключенного */"
                                                    "}")
        self.lineEdit_online_more_than.setObjectName("lineEdit_online_more_than")
        self.gridLayout.addWidget(self.lineEdit_online_more_than, 2, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("")
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 3, 1, 1)
        self.checkBox_phone = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox_phone.setFont(font)
        self.checkBox_phone.setStyleSheet("QCheckBox {\n"
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
        self.checkBox_phone.setObjectName("checkBox_phone")
        self.gridLayout.addWidget(self.checkBox_phone, 3, 0, 1, 2)
        self.checkBox_photo = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox_photo.setFont(font)
        self.checkBox_photo.setStyleSheet("QCheckBox {\n"
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
        self.checkBox_photo.setObjectName("checkBox_photo")
        self.gridLayout.addWidget(self.checkBox_photo, 4, 0, 1, 1)
        self.checkBox_tg_premium = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox_tg_premium.setFont(font)
        self.checkBox_tg_premium.setStyleSheet("QCheckBox {\n"
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
        self.checkBox_tg_premium.setObjectName("checkBox_tg_premium")
        self.gridLayout.addWidget(self.checkBox_tg_premium, 4, 1, 1, 3)
        self.checkBox_man = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox_man.setFont(font)
        self.checkBox_man.setStyleSheet("QCheckBox {\n"
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
        self.checkBox_man.setObjectName("checkBox_man")
        self.gridLayout.addWidget(self.checkBox_man, 5, 0, 1, 1)
        self.checkBox_woman = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox_woman.setFont(font)
        self.checkBox_woman.setStyleSheet("QCheckBox {\n"
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
        self.checkBox_woman.setObjectName("checkBox_woman")
        self.gridLayout.addWidget(self.checkBox_woman, 5, 1, 1, 2)
        self.checkBox_rus_name = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox_rus_name.setFont(font)
        self.checkBox_rus_name.setStyleSheet("QCheckBox {\n"
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
        self.checkBox_rus_name.setObjectName("checkBox_rus_name")
        self.gridLayout.addWidget(self.checkBox_rus_name, 6, 0, 1, 4)
        self.checkBox_eng_name = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox_eng_name.setFont(font)
        self.checkBox_eng_name.setStyleSheet("QCheckBox {\n"
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
        self.checkBox_eng_name.setObjectName("checkBox_eng_name")
        self.gridLayout.addWidget(self.checkBox_eng_name, 7, 0, 1, 4)
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_9.setText("")
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 8, 0, 1, 2)
        self.checkBox_use_proxy = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox_use_proxy.setFont(font)
        self.checkBox_use_proxy.setStyleSheet("QCheckBox {\n"
                                              "color: rgb(0, 0, 0);\n"
                                              "    spacing: 5px; /* Отступ между иконкой и текстом */\n"
                                              "    border: none;\n"
                                              "    margin-bottom: 15px;\n"
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
        self.gridLayout.addWidget(self.checkBox_use_proxy, 9, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout, 1, 2, 1, 2)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setStyleSheet("")
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("")
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 3, 0, 1, 1)
        self.pushButton_uploads_the_list = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_uploads_the_list.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_uploads_the_list.setFont(font)
        self.pushButton_uploads_the_list.setStyleSheet("\n"
                                                       "QPushButton {\n"
                                                       "    background-color: rgb(255, 255, 255);\n"
                                                       "    text-align: center;\n"
                                                       "    border-radius: 10px;\n"
                                                       "    padding: 5px;"
                                                       "   }\n"
                                                       "QPushButton:hover {\n"
                                                       "    background-color: rgb(230, 230, 230); /* Цвет фона при наведении (немного серый) */\n"
                                                       "}\n"
                                                       "\n"
                                                       "QPushButton:pressed {\n"
                                                       "     background: rgb(210, 210, 213); /* Цвет фона при нажатии (еще серее) */\n"
                                                       "}")
        self.pushButton_uploads_the_list.setObjectName("pushButton_uploads_the_list")
        self.gridLayout_2.addWidget(self.pushButton_uploads_the_list, 3, 1, 1, 1)
        self.pushButton_download_list = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_download_list.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_download_list.setFont(font)
        self.pushButton_download_list.setStyleSheet("\n"
                                                    "QPushButton {\n"
                                                    "    background-color: rgb(255, 255, 255);\n"
                                                    "    text-align: center;\n"
                                                    "    border-radius: 10px;\n"
                                                    "    padding: 5px;"
                                                    "   }\n"
                                                    "QPushButton:hover {\n"
                                                    "    background-color: rgb(230, 230, 230); /* Цвет фона при наведении (немного серый) */\n"
                                                    "}\n"
                                                    "\n"
                                                    "QPushButton:pressed {\n"
                                                    "     background: rgb(210, 210, 213); /* Цвет фона при нажатии (еще серее) */\n"
                                                    "}")
        self.pushButton_download_list.setObjectName("pushButton_download_list")
        self.gridLayout_2.addWidget(self.pushButton_download_list, 2, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 0, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_2, 2, 2, 1, 1)
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setContentsMargins(-1, -1, -1, 10)
        self.gridLayout_8.setObjectName("gridLayout_8")
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
        self.gridLayout_8.addWidget(self.pushButton_start, 0, 0, 2, 1)
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
                                                       "    padding: 10px;\n "
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
        self.gridLayout_5.addLayout(self.gridLayout_8, 3, 2, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(20, 10, 20, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setMinimumSize(QtCore.QSize(420, 0))
        self.scrollArea.setStyleSheet("border: 0;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 524, 433))
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
        self.textEdit_conclusion.setMinimumSize(QtCore.QSize(350, 340))
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
        self.gridLayout_5.addLayout(self.verticalLayout_2, 2, 1, 2, 1)
        self.gridLayout_12 = QtWidgets.QGridLayout()
        self.gridLayout_12.setContentsMargins(20, -1, 0, -1)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("")
        self.label_10.setObjectName("label_10")
        self.gridLayout_12.addWidget(self.label_10, 0, 0, 1, 1)
        self.scrollArea_6 = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_6.sizePolicy().hasHeightForWidth())
        self.scrollArea_6.setSizePolicy(sizePolicy)
        self.scrollArea_6.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea_6.setStyleSheet("border: 0;")
        self.scrollArea_6.setWidgetResizable(True)
        self.scrollArea_6.setObjectName("scrollArea_6")
        self.scrollAreaWidgetContents_6 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_6.setGeometry(QtCore.QRect(0, 0, 276, 411))
        self.scrollAreaWidgetContents_6.setStyleSheet("""
                                                    /* СТИЛЬ ВЕРТИКАЛЬНОГО СКРОЛЛБАРА */
                                                    QScrollBar:vertical {
                                                        border-radius: 8px;
                                                        background-color: rgb(255, 255, 255);
                                                        width: 14px;
                                                        margin: 0px 0 0px 0;
                                                    }
                                                    
                                                    /* HANDLE BAR ВЕРТИКАЛЬНОГО СКРОЛЛБАРА */
                                                    QScrollBar::handle:vertical {  
                                                        background-color: rgb(210, 210, 213);
                                                        min-height: 30px;
                                                        border-radius: 0px;
                                                        margin: 15px 0 15px 0;  /* Добавлены отступы сверху и снизу */
                                                        transition: background-color 0.2s ease;
                                                    }
                                                    
                                                    QScrollBar::handle:vertical:hover {  
                                                        background-color: rgb(180, 180, 184);
                                                    }
                                                    
                                                    QScrollBar::handle:vertical:pressed {  
                                                        background-color: rgb(150, 150, 153);
                                                    }
                                                    
                                                    /* КНОПКА ВВЕРХУ - ВЕРТИКАЛЬНЫЙ СКРОЛЛБАР */
                                                    QScrollBar::sub-line:vertical {
                                                        border: none;  
                                                        background-color: rgb(190, 190, 193);
                                                        height: 15px;
                                                        border-top-left-radius: 7px;
                                                        border-top-right-radius: 7px;
                                                        subcontrol-position: top;
                                                        subcontrol-origin: margin;
                                                    }
                                                    
                                                    QScrollBar::sub-line:vertical:hover {  
                                                        background-color: rgb(170, 170, 174);
                                                    }
                                                    
                                                    QScrollBar::sub-line:vertical:pressed {  
                                                        background-color: rgb(140, 140, 143);
                                                    }
                                                    
                                                    /* КНОПКА ВНИЗУ - ВЕРТИКАЛЬНЫЙ СКРОЛЛБАР */
                                                    QScrollBar::add-line:vertical {
                                                        border: none;  
                                                        background-color: rgb(190, 190, 193);
                                                        height: 15px;
                                                        border-bottom-left-radius: 7px;
                                                        border-bottom-right-radius: 7px;
                                                        subcontrol-position: bottom;
                                                        subcontrol-origin: margin;
                                                    }
                                                    
                                                    QScrollBar::add-line:vertical:hover {  
                                                        background-color: rgb(170, 170, 174);
                                                    }
                                                    
                                                    QScrollBar::add-line:vertical:pressed {  
                                                        background-color: rgb(140, 140, 143);
                                                    }
                                                    
                                                    /* УБРАТЬ СТРЕЛКИ */
                                                    QScrollBar::up-arrow:vertical, 
                                                    QScrollBar::down-arrow:vertical {
                                                        background: none;
                                                    }
                                                    
                                                    /* УБРАТЬ ФОН */
                                                    QScrollBar::add-page:vertical, 
                                                    QScrollBar::sub-page:vertical {
                                                        background: none;
                                                    }
                                                    """)
        self.scrollAreaWidgetContents_6.setObjectName("scrollAreaWidgetContents_6")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_6)
        self.gridLayout_13.setContentsMargins(-1, -1, -1, 10)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.gridLayout_14 = QtWidgets.QGridLayout()
        self.gridLayout_14.setContentsMargins(0, -1, -1, -1)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.textEdit_users_list = QtWidgets.QTextEdit(self.scrollAreaWidgetContents_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_users_list.sizePolicy().hasHeightForWidth())
        self.textEdit_users_list.setSizePolicy(sizePolicy)
        self.textEdit_users_list.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.textEdit_users_list.setFont(font)
        self.textEdit_users_list.setStyleSheet("""
                                                  QTextEdit {
                                                    background-color: rgb(255, 255, 255);
                                                    color: rgb(0, 0, 0);
                                                    border-radius: 20px;
                                                    padding-top: 15px; /* Отступ только слева */   
                                                    padding-bottom: 15px; /* Отступ только снизу */
                                                  }
                                              """)
        self.textEdit_users_list.setObjectName("textEdit_users_list")
        self.gridLayout_14.addWidget(self.textEdit_users_list, 0, 0, 1, 1)
        self.gridLayout_13.addLayout(self.gridLayout_14, 1, 0, 1, 1)
        self.scrollArea_6.setWidget(self.scrollAreaWidgetContents_6)
        self.gridLayout_12.addWidget(self.scrollArea_6, 1, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_12, 2, 3, 2, 1)
        self.setCentralWidget(self.centralwidget)
        self.action = QtWidgets.QAction(self)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(self)
        self.action_2.setObjectName("action_2")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self._show_parsing_result()

        # события
        self.pushButton_mailing.clicked.connect(lambda: self._transition('accounts'))
        self.pushButton_mailing.clicked.connect(lambda: self._transition('mailing_by_users'))
        self.pushButton_mailing_chat.clicked.connect(lambda: self._transition('mailing_by_chats'))
        self.pushButton_invite.clicked.connect(lambda: self._transition('invite'))
        self.pushButton_proxy.clicked.connect(lambda: self._transition('proxy'))
        self.pushButton_bomber.clicked.connect(lambda: self._transition('bomber'))
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
            info = Dialog_info('Внимание!',
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

                    info = Dialog_info('Успешно!',f'Файл успешно выгружен по пути:\n{folder_path}{file_name}.txt',
                                             'notification.mp3')  # Создаем экземпляр
                    info.exec_()  # Открываем
                    break
                except FileExistsError:
                    folder_name = f'/аккаунты с ошибкой входа ({counts}).txt'
                    counts += 1
                except FileNotFoundError:
                    error_info = Dialog_info('Ошибка!', 'Указанный путь не найден!','notification.mp3')  # Создаем экземпляр
                    error_info.exec_()  # Открываем
                    break

    def _question_input_file(self):
        Dialog1 = Dialog_yes_or_cancel('Внимание!',
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

                    info = Dialog_info('Успешно!', f'Данные успешно загружены!','notification.mp3')  # Создаем экземпляр
                    info.exec_()  # Открываем
                    break
                except FileNotFoundError:
                    error_info = Dialog_info('Ошибка!', 'Указанный путь не найден!','notification.mp3')  # Создаем экземпляр
                    error_info.exec_()  # Открываем
                    break
                except Exception as e:
                    error_info = Dialog_info('Ошибка!', f'Ошибка: {e}!','notification.mp3')  # Создаем экземпляр
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
            info = Dialog_info('Внимание!', 'Данный фильтр используется только с выбранным полом!',
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
            info = Dialog_info('Внимание!','Дождитесь конца парсинга!','notification.mp3')  # Создаем экземпляр
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

                info = Dialog_info('Внимание!','Заполните поле с чатами!','notification.mp3')  # Создаем экземпляр
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
                    error_proxy = Dialog_error_proxy(proxy_from_db[0], str(proxy_from_db[1]), proxy_from_db[2],proxy_from_db[3])  # Создаем экземпляр
                    error_proxy.show_info()
                    error_proxy.exec_()  # Открываем
                    return

            if not os.path.isdir(f'{self.root_project_dir}/accounts/active_accounts/0'):
                info = Dialog_info('Внимание!', 'У вас нет ни одного акаунта!', 'notification.mp3')  # Создаем экземпляр
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

            parsing_stream = parsing(all_chats, online_not_less_than, online_more_than, gender, premium_filter,
                                    photo, open_phone, use_language_rus_name, use_language_eng_name,
                                    proxy, proxy_from_db[0],proxy_from_db[1], proxy_from_db[2], proxy_from_db[3])  # Инициализируем рабочий поток
            parsing_stream.task_done.connect(self._parsing_done)  # Подключаем сигнал к слоту
            parsing_stream.start()  # Запускаем поток

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
            info = Dialog_info('Успешно!', f'Парсинг завершён!','notification.mp3')  # Создаем экземпляр
            info.exec_()  # Открываем


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_account.setText(_translate("MainWindow", "   Аккаунты"))
        self.pushButton_mailing.setText(_translate("MainWindow", "   Рассылка"))
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
        self.label_18.setText(_translate("MainWindow", "Парсер"))
        self.label_7.setText(_translate("MainWindow", " Ссылки/имена чатов для парсинга:"))
        self.textEdit_name_chat.setHtml(_translate("MainWindow", ""))
        self.label_3.setText(_translate("MainWindow", "Фильтры:"))
        self.checkBox_online_not_less_than.setText(_translate("MainWindow", "Последний онлайн не менее чем:"))
        self.label_5.setText(_translate("MainWindow", "дней"))
        self.checkBox_online_more_than.setText(_translate("MainWindow", "Последний онлайн более чем:"))
        self.label_6.setText(_translate("MainWindow", "дней"))
        self.checkBox_phone.setText(_translate("MainWindow", "По наличию открытого номера"))
        self.checkBox_photo.setText(_translate("MainWindow", "По наличию фото"))
        self.checkBox_tg_premium.setText(_translate("MainWindow", "По наличию tg premium"))
        self.checkBox_man.setText(_translate("MainWindow", "По муж. полу"))
        self.checkBox_woman.setText(_translate("MainWindow", "По жен. полу"))
        self.checkBox_rus_name.setText(_translate("MainWindow", "По имени написанное на русском языке"))
        self.checkBox_eng_name.setText(_translate("MainWindow", "По имени написанное на английском языке"))
        self.checkBox_use_proxy.setText(_translate("MainWindow", "Использоват прокси"))
        self.label.setText(_translate("MainWindow", "Загрузить список        "))
        self.label_2.setText(_translate("MainWindow", "Выгрузить список"))
        self.pushButton_uploads_the_list.setText(_translate("MainWindow", "Выбрать"))
        self.pushButton_download_list.setText(_translate("MainWindow", "Выбрать"))
        self.pushButton_start.setText(_translate("MainWindow", "Запустить"))
        self.pushButton_clear_conclusion.setText(_translate("MainWindow", "Очистить \nконсоль"))
        self.label_4.setText(_translate("MainWindow", " Консоль вывода:"))
        self.textEdit_conclusion.setHtml(_translate("MainWindow",""))
        self.label_10.setText(_translate("MainWindow", "  Список пользователей:"))
        self.textEdit_users_list.setHtml(_translate("MainWindow",""))
        self.action.setText(_translate("MainWindow", "сохранить"))
        self.action_2.setText(_translate("MainWindow", "добавить"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Window_parser('fbdgf')
    ui.show()
    sys.exit(app.exec_())
