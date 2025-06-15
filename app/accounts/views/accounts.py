import os  # это для действия ниже перед запуском функции
import sqlite3
import datetime as dt

import socks
import socket
import asyncio
import shutil # для удаления папки
import faulthandler # для просмотра стека вызовов
import subprocess # для запуска exe файлов
import sys
sys.path.append("../..")  # Добавляет родительскую папку в путь поиска

from opentele.td import TDesktop
from opentele.api import UseCurrentSession
from opentele.exception import TFileNotFound

from app.accounts.ui.window_accounts_ui import WindowAccountsUi
from app.accounts.views.add_accounts import DialogAddAccounts
from app.accounts.views.info_add_accounts import DialogInfoAddAccounts
from app.accounts.flag import get_country_flag
from app.general.views.info import DialogInfo
from app.accounts.views.error_open_accounts import DialogErrorOpenAccounts
from app.general.views.error_proxy import DialogErrorProxy
from app.general.check_proxy import check_proxy
from app.general.error_handler import error_handler, get_description_and_solution
from app.accounts.views.more_info_account import DialogMoreInfoAccount
from app.general.views.yes_or_cancel import DialogYesOrCancel

# Включаем faulthandler для получения информации об ошибках
faulthandler.enable()

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")# 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():# 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path# 3. Установка пути

# 4. Только после этого импортируем PyQt5
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog, QPushButton, QGraphicsOpacityEffect
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QThread, pyqtSignal, QPropertyAnimation, Qt


class ShowAccount(QThread):

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
            await asyncio.wait_for( client.connect(),timeout=15 ) # вход в аккаунт
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


class WindowAccounts(WindowAccountsUi):
    open_account = True # True если аккаунты открываются
    program_launch = True # True если программа запускается (необходимо для отображения аккаунтов)
    selected_account_type = 'active' # отображает вкладка с какими аккаунтами открыта

    original_socket = socket.socket  # запоминаем какой сокет был до

    accounts = [] # список данных об аккаунтах (хранит в себе массивы с инфой об аккаунте)
    error_accounts = [] # список аккаунтов с которыми произошла ошибка входа (первое значение значение ошибка второе id аккаунта )
    quantity_start_accounts = 0 # количество аккаунтов запущенных для дальнейшего вывода
    quantity_received_accounts = 0 # количество аккаунтов вернувшихся аккаунтов после получения информации о нём
    active_threads = []  # ВАЖНО! хранит в себе запущенные потоки

    def __init__(self, switch_window = None):
        super().__init__()
        self.switch_window = switch_window
        self.root_project_dir = '..'
        # события
        self.pushButton_mailing.clicked.connect(lambda: self._transition('mailing_by_users'))
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
            error_info = DialogInfo('Внимание!', 'Дождитесь загрузки аккаунтов!\nЭто необходимо для предотвращения возможных ошибок.',
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
                    show_account_stream = ShowAccount(self.root_project_dir + f'/accounts/{type_accounts}_accounts/{id_account}',
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
                            error_info = DialogInfo('Внимание!', 'В данной вкладке нет аккаунтов', 'notification.mp3')
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
                    self._update_account_data({'id': account_info[0], 'id_tg':account_info[1], 'user_name': account_info[2],
                                               'name': account_info[3], 'phone': account_info[5]}) # обновление данных в БД (если не сходятся с имеющимися)

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

                error_info = DialogErrorOpenAccounts(full_list_error_account)
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
                error_info = DialogInfo('Внимание!', 'В данной вкладке нет аккаунтов','notification.mp3')
                error_info.exec_()

            self._update_count_accounts()
            self.open_account = False # устанавливаем что аккаунты загружены
            self.program_launch = False # устанавливаем, что программа больше не загружается

    def _show_tab_account(self, button: QPushButton):
        if self.open_account:
            error_info = DialogInfo('Внимание!', 'Уже происходит открытие аккаунтов!','notification.mp3')  # Создаем экземпляр
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
        if self.open_account:
            error_info = DialogInfo('Внимание!', 'Дождитесь загрузки аккаунтов!','notification.mp3')  # Создаем экземпляр
            error_info.exec_()  # Открываем
            return

        info_add_accounts = DialogInfoAddAccounts()  # Создаем экземпляр
        info_add_accounts.data_returned.connect(self._start_add_accounts)  # Подключаем сигнал
        info_add_accounts.exec_()  # Открываем модальное окно

    def _start_add_accounts(self,path: str):
        add_accounts = DialogAddAccounts(path)  # Создаем экземпляр
        add_accounts.start()
        add_accounts.exec_()  # Открываем модальное окно

        if self.label_account.text() == 'Активные:': # если открыты активные аккаунты, то необходимо добавить в список новые добавленные аккаунты
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
        selected_rows = set()
        for item in self.tableWidget_account.selectedItems():
            selected_rows.add(item.row())  # добавляем номер строки и добавляем в множество

        if not selected_rows: # если пользователь не выбрал строки
            error_info = DialogInfo('Внимание!', 'Для данного действия выберите аккаунты!','notification.mp3')
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
            error_info = DialogInfo('Внимание!', 'Выбранные аккаунты уже\nнаходятся в этом разделе!', 'notification.mp3')
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
        error_info = DialogInfo('Готово!', message, 'notification.mp3')
        error_info.exec_()  # Открываем

    def _show_more_info_account(self):
        selected_rows = set()
        for item in self.tableWidget_account.selectedItems():
            selected_rows.add(item.row())  # Получаем номер строки и добавляем в множество

        if len(selected_rows) != 1:
            error_info = DialogInfo('Внимание!', 'Выберите только один аккаунт!', 'notification.mp3')
            error_info.exec_()  # Открываем
            return

        element = next(iter(selected_rows)) # хранит первый элемент из множества

        more_info = DialogMoreInfoAccount(int(element),self.selected_account_type)
        asyncio.run(more_info.show_info_account()) # выводим данные об аккаунте
        more_info.exec_()  # Открываем

        self.show_accounts_from_db()
        self._update_count_accounts()

    def _enter_account(self):
        if self.selected_account_type == 'login_error':
            error_info = DialogInfo('Внимание!', 'В данные аккаунты невозможно войти!', 'notification.mp3')
            error_info.exec_()  # Открываем
            return

        selected_rows = set()
        for item in self.tableWidget_account.selectedItems():
            selected_rows.add(item.row())  # Получаем номер строки и добавляем в множество

        if len(selected_rows) != 1:
            error_info = DialogInfo('Внимание!', 'Выберите только один аккаунт!', 'notification.mp3')
            error_info.exec_()  # Открываем
            return
        if os.path.exists(self.root_project_dir + '/Telegram Desktop/tdata') and os.path.isdir(self.root_project_dir + '/Telegram Desktop/tdata'): # проверяем есть ли такой путь и есть ли по такому пути папка
            try:
                shutil.rmtree(self.root_project_dir + '/Telegram Desktop/tdata')
            except PermissionError:
                error_info = DialogInfo('Внимание!', 'Невозможно войти в аккаунт!\nФайлы для входа заняты другим процессом\nЗакройте телеграмм который открывали через программу!', 'notification.mp3')
                error_info.exec_()  # Открываем
                return
            except Exception as e:
                error_info = DialogInfo('Внимание!', 'Не удалось войти в аккаунт!', 'notification.mp3')
                error_info.exec_()  # Открываем
                return

        id_folder = next(iter(selected_rows))  # хранит первый элемент из множества

        try:
            # Проверяем, существует ли директория-исходник
            if not os.path.exists(self.root_project_dir + f'/accounts/{self.selected_account_type}_accounts/{id_folder}'): # если нету по указанному пути папки
                error_info = DialogInfo('Внимание!', f'Произошла ошибка!\nПапки с выбранным id = {id_folder} нет.\nУдалите аккаунт под таким id!', 'notification.mp3')
                error_info.exec_()  # Открываем
                return
            else:
                shutil.copytree(self.root_project_dir + f'/accounts/{self.selected_account_type}_accounts/{id_folder}/tdata', self.root_project_dir + '/Telegram Desktop/tdata')# Копируем директорию
        except Exception as e:
            error_info = DialogInfo('Внимание!',f'Произошла ошибка!\nУдалите аккаунт под id = {id_folder}!','notification.mp3')
            error_info.exec_()  # Открываем
            return

        try:
            subprocess.Popen(self.root_project_dir + '/Telegram Desktop/Telegram.exe')# Запускаем исполняемый файл
        except (subprocess.CalledProcessError,Exception )as e:
            error_info = DialogInfo('Внимание!', f'Ошибка при запуске exe файла\n{e}!','notification.mp3')
            error_info.exec_()  # Открываем
            return

    def _upload_tdata(self):
        selected_rows = set()
        for item in self.tableWidget_account.selectedItems():
            selected_rows.add(item.row())  # Получаем номер строки и добавляем в множество

        if len(selected_rows) < 1:
            error_info = DialogInfo('Внимание!', 'Выберите как минимум один аккаунт!', 'notification.mp3')
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
                    error_info = DialogInfo('Внимание!', f"Ошибка при копировании:\n{e}", 'notification.mp3')
                    error_info.exec_()  # Открываем
                    return

            error_info = DialogInfo('Готово!', f'Выгрузка произошла успешно в:\n{folder_path}/{name_copy_folder}', 'notification.mp3')
            error_info.exec_()  # Открываем

    def _delete_accounts(self):
        selected_rows = set()
        for item in self.tableWidget_account.selectedItems():
            selected_rows.add(item.row())  # Получаем номер строки и добавляем в множество

        if len(selected_rows) < 1:
            error_info = DialogInfo('Внимание!', 'Выберите хотя бы один аккаунт!', 'notification.mp3')
            error_info.exec_()  # Открываем
            return

        Dialog1 = DialogYesOrCancel('Внимание!',
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
            error_info = DialogInfo('Внимание!', 'Выберите хотя бы один аккаунт!', 'notification.mp3')
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
        error_proxy = DialogErrorProxy(ip,port,login,password)  # Создаем экземпляр
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

    def _update_account_data(self, account_data: dict):
        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()
        cursor.execute(f"SELECT id_tg,user_name,name,phone,data_time_add,notes,last_used FROM accounts WHERE id = ? AND account_status = ? ",
                       (account_data['id'], self.selected_account_type))
        account_from_db = cursor.fetchone()

        if account_from_db:
            if account_from_db[0] != account_data['id_tg']:
                cursor.execute(f"UPDATE accounts SET id_tg = ?  WHERE id = ? AND account_status = ?",
                               (account_data['id_tg'], account_data['id'], self.selected_account_type))
                connection.commit()  # сохранение
            if account_from_db[1] != account_data['user_name']:
                cursor.execute(f"UPDATE accounts SET user_name = ?  WHERE id = ? AND account_status = ? ",
                               (account_data['user_name'], account_data['id'],self.selected_account_type))
                connection.commit()
            if account_from_db[2] != account_data['name']:
                cursor.execute(f"UPDATE accounts SET name = ?  WHERE id = ? AND account_status = ? ",
                               (account_data['name'], account_data['id'],self.selected_account_type))
                connection.commit()
            if account_from_db[3] != account_data['phone']:
                cursor.execute(f"UPDATE accounts SET phone = ?  WHERE id = ? AND account_status = ? ",
                               (account_data['phone'], account_data['id'], self.selected_account_type))
                connection.commit()
        else:
            now = dt.datetime.now()  # Получаем текущее время
            formatted_date = now.strftime('%H:%M %d-%m-%Y')  # Форматируем дату и время согласно формату

            cursor.execute(f"INSERT INTO accounts (id,id_tg,user_name,name,phone,data_time_add,last_used, account_status)"
                           f" VALUES (?,?,?,?,?,?,?,?)",
                (account_data['id'], account_data['id_tg'], account_data['user_name'], account_data['name'],
                            account_data['phone'], formatted_date, formatted_date, self.selected_account_type))
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

def application():
    try:
        app =  QtWidgets.QApplication(sys.argv)
        account = WindowAccounts()
        account.show()
        account.start_show_account('active')
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Произошла ошибка при запуске приложения: {e}")

if __name__ == "__main__":
    application()

