import sys
import sqlite3
import socks
import socket
import datetime as dt

from opentele.td import TDesktop
from opentele.api import UseCurrentSession
from opentele.exception import TFileNotFound

# для работы с архивами
import zipfile
import tarfile
import rarfile
import py7zr
# для работы с архивами
import shutil # для удаления папки
import asyncio
import os
import random
import string

from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.functions.account import UpdateProfileRequest, UpdateUsernameRequest
from telethon.errors import UsernameOccupiedError

from app.accounts.error_add_accounts import Dialog_error_add_accounts
from app.general.check_proxy import check_proxy
from app.general.ok_or_cancel import Dialog_ok_or_cancel
from app.general.error_proxy import Dialog_error_proxy
from app.general.info import Dialog_info

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")# 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():# 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path# 3. Установка пути

# 4. Только после этого импортируем PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import  QDialog, QLabel
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt

class DraggableLabel(QLabel): # спец класс для Label

    def __init__(self, parent=None):
        super().__init__( parent)
        self.oldPos = None  # Переменная для хранения позиции мыши

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:  # Проверка на левую кнопку мыши
            self.oldPos = event.globalPos() - self.parent().frameGeometry().topLeft()  # Запоминаем позицию мыши
            event.accept()  # Принять событие

    def mouseMoveEvent(self, event):
        if self.oldPos is not None and event.buttons() == Qt.LeftButton:  # Проверка, что кнопка мыши удерживается
            self.parent().move(event.globalPos() - self.oldPos)  # Перемещения окна
            event.accept()  # Принять событие

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:  # Проверка на отпускание кнопки мыши
            self.oldPos = None  # Обнуляем позицию
            event.accept()  # Принять событие

class add_accounts(QThread): # затухание progress_bar
    root_project_dir = '..'

    task_done = pyqtSignal(list, bool, str, bool)  # Сигнал, который посылаем

    proxy = False
    original_socket = socket.socket  # запоминаем какой сокет был до
    def __init__(self,path: str,this_folder: bool, use_proxy: bool, id_proxy: str, port: int, login: str, password: str):
        super().__init__()
        self.path = path
        self.this_folder = this_folder # указывает на то получили ли мы папку
        self.proxy = use_proxy
        self.id_proxy = id_proxy
        self.port = port
        self.login = login
        self.password = password

    def run(self):
        if self.this_folder:
            self.viewing_folder_in_path(self.path)
        else:
            self.viewing_folder_in_path_archive(self.path)

    def viewing_folder_in_path(self, path: str):
        tdata_path = path + '/tdata'
        if os.path.isdir(tdata_path): # если по указанному пути есть такая папка
            asyncio.run(self.check_account(path, tdata_path))
        else:
            self.task_done.emit([],False,'0',False)

    def viewing_folder_in_path_archive(self,archive_path):
        if not os.path.isfile(archive_path): #  если по такому пути ничего нет
            self.task_done.emit([], False, '0', False)
            return

        file_name, file_extension = os.path.splitext(os.path.basename(archive_path))  # берём имя файла и расширение
        destination_path = self.root_project_dir + f'/working_files/test_account/{file_name}' # путь куда будем копировать
        try:
            # проверяем расширение файла
            if file_extension in '.zip':# Проверяем, какое расширение у файла
                with zipfile.ZipFile(archive_path, 'r') as zip_file:
                    archive_contents = zip_file.namelist()# Получаем список всех файлов и папок в архиве
                    for item in archive_contents:# Проверяем наличие папки 'tdata'
                        if item.startswith('tdata/') and item.endswith('/'): # папки заканчиваются на "/"
                            zip_file.extractall(destination_path)
                            self.viewing_folder_in_path(destination_path)
                            return
                self.task_done.emit([], False, '0', False)  # это на тот случай если нет паки tdata в архиве

            elif file_extension in '.rar':
                with rarfile.RarFile(archive_path) as rar_file:
                    archive_contents = rar_file.namelist() # Получаем список всех файлов и папок в архиве
                    for item in archive_contents: # Проверяем наличие папки 'tdata'
                        if item.startswith('tdata/') and item.endswith('/'):
                            rar_file.extractall(destination_path)
                            self.viewing_folder_in_path(destination_path)
                            return
                self.task_done.emit([], False, '0', False)  # это на тот случай если нет паки tdata в архиве

            elif file_extension in '.tar':
                with tarfile.open(archive_path, 'r') as tar_file:
                    archive_contents = tar_file.getnames()# Получаем список всех файлов и папок в архиве
                    for item in archive_contents:
                        if item.startswith('tdata/') and item.endswith('/'):
                            tar_file.extractall(destination_path)
                            self.viewing_folder_in_path(destination_path)
                            return
                self.task_done.emit([], False, '0', False)  # это на тот случай если нет паки tdata в архиве

            elif file_extension in '.7z':
                with py7zr.SevenZipFile(archive_path, mode='r') as seven_zip_file:
                    archive_contents = seven_zip_file.getnames()
                    for item in archive_contents:# Проверяем наличие папки 'tdata'
                        if item.startswith('tdata/') and item.endswith('/'):
                            seven_zip_file.extractall(destination_path)
                            self.viewing_folder_in_path(destination_path)
                            return
                self.task_done.emit([], False, '0', False)  # это на тот случай если нет паки tdata в архиве

            else:# если файл не является архивом (по сути он сюда даже не попадёт)
                self.task_done.emit([], False, '0', False)
                return
        except FileNotFoundError: # если не нашли указанный путь
            self.task_done.emit([], False, '0', False)
            return
        except Exception as e: # на всякий случай
            self.task_done.emit([], False, '0', False)
            return


    async def check_account(self,folder_path_account: str, path_in_tdata: str):
        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()

        if self.proxy:
            socks.set_default_proxy(socks.SOCKS5, self.id_proxy, self.port, True, self.login,self.password)  # Установка прокси-соединения
            socket.socket = socks.socksocket

        me = None
        try:
            tdesk = TDesktop(path_in_tdata)
            client = await tdesk.ToTelethon(session=f"{folder_path_account}/session.session", flag=UseCurrentSession)
            await asyncio.wait_for( client.connect(),timeout=5) # вход в аккаунт
            me = await client.get_me() # получение информации об аккаунте

            cursor.execute(f"SELECT id_tg FROM accounts WHERE id_tg = {me.id}")
            results_from_db = cursor.fetchall()
            if results_from_db:  # если такой аккаунт уже есть в программе
                connection.close()
                await client.disconnect()
                self.task_done.emit([], False, str(me.id), False)
                return

            # тут автозаполнение
            cursor.execute(f"SELECT use,avatar,name, surname, user_name,description FROM autofill_settings")
            autofill_from_db = cursor.fetchone()
            if autofill_from_db[0] == 1: # если необходимо использовать автозаполнение

                if autofill_from_db[1] != 'None': # если необходимо задать аву
                    files = os.listdir(self.root_project_dir + f'/resources/autofill/avatar_picture/{autofill_from_db[1]}')# Получаем список файлов в указанной папке
                    image_extensions = {'.jpg', '.jpeg', '.png'} # Фильтруем только файлы с расширениями изображений
                    image_files = [file for file in files if os.path.splitext(file)[1].lower() in image_extensions]
                    if image_files:# Проверяем, есть ли изображения в папке
                        selected_image = random.choice(image_files)# Выбираем случайный файл из списка изображений
                        try:# установление нового фото
                            await client(UploadProfilePhotoRequest(
                                file= await client.upload_file(self.root_project_dir +
                                                               f'/resources/autofill/avatar_picture/{autofill_from_db[1]}/{selected_image}')))
                        except Exception:
                            pass

                if autofill_from_db[2] != 'None':
                    cursor.execute(f"SELECT name FROM autofill_data WHERE gender = ?", (autofill_from_db[2],))
                    names = [row[0] for row in cursor.fetchall()]

                    # Проверяем, есть ли username
                    if names:
                        name = random.choice(names)
                        try:
                            await client(UpdateProfileRequest(first_name=name))
                        except Exception:
                            pass

                if autofill_from_db[3] != 'None':
                    cursor.execute(f"SELECT surname FROM autofill_data WHERE gender = ?", (autofill_from_db[3],))
                    surnames = [row[0] for row in cursor.fetchall()]

                    # Проверяем, есть ли username
                    if surnames:
                        surname = random.choice(surnames)
                        try:
                            await client(UpdateProfileRequest(last_name=surname))
                        except Exception:
                            pass

                if autofill_from_db[4] != 0:
                    characters = string.ascii_letters + string.digits # Определяем набор символов: заглавные и строчные буквы, цифры
                    while True:
                        user_name = ''.join(random.choice(characters) for _ in range(15)) # Генерируем случайную строку
                        try:
                            await client(UpdateUsernameRequest(username=user_name))
                            break
                        except UsernameOccupiedError: # если имя уже занято
                            pass
                        except Exception:
                            break

                if autofill_from_db[5] != 0: # будем рандомно брать из БД
                    cursor.execute(f"SELECT description FROM autofill_data")
                    descriptions = [row[0] for row in cursor.fetchall()]
                    if descriptions:
                        description = random.choice(descriptions)
                        try:
                            await client(UpdateProfileRequest(about=description))
                        except Exception:
                            pass

            await client.disconnect()
            connection.close()

            # если всё прошло успешно и аккаунт добавлен в программу
            self.task_done.emit([folder_path_account, me.id, me.username, me.first_name, me.phone], True, '0', False)

        except (Exception, TFileNotFound):
            connection.close()
            # тут мы не смогли войти в аккаунт и значит необходимо скопировать папку tdata в папку с ошибкой входа
            try:  # копирование (принимает папку в которой хранится tdata, то есть мы копируем содержимое указанной папки)
                folder_name = os.path.basename(self.path)
                shutil.copytree(folder_path_account,self.root_project_dir + f'/working_files/error_enter_accounts/{folder_name}')
            except FileNotFoundError:
                pass
            self.task_done.emit([], False, '0', True)

class Dialog_add_accounts(QDialog):

    def __del__(self): # деструктор (очищаем файлы с которыми работали)
        path_delete = self.root_project_dir + '/working_files/error_enter_accounts'
        try:  # удаление всех файлов из указаной дерректории выше
            if os.path.exists(path_delete):  # Проверяем, что указанный путь существует
                # Получаем список всех файлов и папок в директории
                for item in os.listdir(path_delete):
                    item_path = os.path.join(path_delete, item)
                    # Удаляем файл или директорию
                    if os.path.isfile(item_path):
                        os.remove(item_path)  # Удаляем файл
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)  # Удаляем директорию и её содержимое
        except Exception:
            pass

        # удаление папок которые скопировали из архива
        for item in os.listdir(self.root_project_dir + '/working_files/test_account'):  # удаление папки которая могла остаться после последнего добавления аккаунта
            item_path = os.path.join(self.root_project_dir + '/working_files/test_account/', item)  # Получаем полный путь к элементу
            try:
                if os.path.isdir(item_path):  # Если это папка, удаляем её вместе с содержимым
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)  # Если это файл, просто удаляем его
            except Exception:
                pass


    root_project_dir = '..'

    def __init__(self, path: str):
        super().__init__()

        self.active_threads = [] # ВАЖНО! хранит в себе запущенные потоки

        self.original_socket = socket.socket  # запоминаем какой прокси был до его подключения
        self.completed = False  # отображает закончен ли процесс загрузки аккаунтов
        self.existing_accounts = [] # список tg_id которые имеются в программе
        self.quantity_start_accounts = 0 # количество запущенных аккаунтов
        self.quantity_received_accounts = 0 # количество вернувшихся аккаунтов
        self.one_step = 0 # сколько необходимо прибавлять за один шаг к прогрессбару
        self.successful_additions = 0 # количество успешных добавлений аккаунтов в программу
        self.error_enter = False # если есть аккаунты в которые не удалось войти
        self.data_accounts = [] # хранит списки данных об аккаунте
        self.path = path

        path_delete = self.root_project_dir + '/working_files/error_enter_accounts'
        try: # удаление всех файлов из указаной дерректории выше
            if os.path.exists(path_delete): # Проверяем, что указанный путь существует
                # Получаем список всех файлов и папок в директории
                for item in os.listdir(path_delete):
                    item_path = os.path.join(path_delete, item)
                    # Удаляем файл или директорию
                    if os.path.isfile(item_path):
                        os.remove(item_path)  # Удаляем файл
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)  # Удаляем директорию и её содержимое
        except Exception:
           pass

        # удаление папок которые скопировали из архива
        for item in os.listdir(self.root_project_dir + '/working_files/test_account'): # удаление папки которая могла остаться после последнего добавления аккаунта
            item_path = os.path.join(self.root_project_dir + '/working_files/test_account/', item)  # Получаем полный путь к элементу
            try:
                if os.path.isdir(item_path):# Если это папка, удаляем её вместе с содержимым
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)# Если это файл, просто удаляем его
            except Exception:
                pass


        self.setWindowFlags(Qt.FramelessWindowHint)  # Убираем рамки окна, включая заголовок
        self.setObjectName("Dialog")
        self.setStyleSheet("border: 1px solid black;")  # Обводка по всему периметру окна
        self.resize(460, 127) # длинна изначально была 190
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_3.setContentsMargins(-1, -1, -1, 15)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_title = DraggableLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_title.sizePolicy().hasHeightForWidth())
        self.label_title.setSizePolicy(sizePolicy)
        self.label_title.setMaximumSize(QtCore.QSize(16777215, 33))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet("background-color: rgb(255, 255, 255);"
                                       "padding-left: 7px;"
                                       "border-bottom: none;"
                                       "border-right: none;")
        self.label_title.setObjectName("label_title")
        self.horizontalLayout_3.addWidget(self.label_title)
        self.pushButton_close = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_close.sizePolicy().hasHeightForWidth())
        self.pushButton_close.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_close.setFont(font)
        self.pushButton_close.setStyleSheet("\n"
"QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    text-align: center;\n"
"    border-bottom: none;"
"    border-left: none;"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"    padding-top: 3px;\n"
"    padding-bottom: 3px;\n"
"   }\n"
"QPushButton:hover {\n"
"    background-color: rgb(255, 1, 1); /* Цвет фона при наведении  */\n"
"    color: rgb(255,255,255)\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"     background: rgb(255, 100, 100); /* Цвет фона при нажатии (еще серее) */\n"
"     color: rgb(255,255,255)\n"
"}\n"
"")
        self.pushButton_close.setObjectName("pushButton_close")
        self.horizontalLayout_3.addWidget(self.pushButton_close)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(10, -1, 10, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox_progress_bar = QtWidgets.QGroupBox(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_progress_bar.sizePolicy().hasHeightForWidth())
        self.groupBox_progress_bar.setSizePolicy(sizePolicy)
        self.groupBox_progress_bar.setMinimumSize(QtCore.QSize(0, 66))
        self.groupBox_progress_bar.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.groupBox_progress_bar.setFont(font)
        self.groupBox_progress_bar.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius: 17px;\n"
"    border: none;"
"\n"
"")
        self.groupBox_progress_bar.setTitle("")
        self.groupBox_progress_bar.setObjectName("groupBox_progress_bar")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_progress_bar)
        self.horizontalLayout.setContentsMargins(11, 0, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.progressBar = QtWidgets.QProgressBar(self.groupBox_progress_bar)
        self.progressBar.setMaximumSize(QtCore.QSize(16777215, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.progressBar.setFont(font)
        self.progressBar.setStyleSheet("QProgressBar {\n"
"                border: 2px solid  rgb(255, 255, 255); /* Цвет рамки */\n"
"                border-radius: 5px; /* Закругленные углы */\n"
"                background-color: #f3f3f3; /* Цвет фона */\n"
"\n"
"            }\n"
"\n"
"QProgressBar::chunk {\n"
"                background: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:1, \n"
"                    stop:1 #4CAF50, stop:1 #81C784); /* Градиент зеленого цвета */\n"
"                border-radius: 5px; /* Закругленные углы заполненной части */\n"
"            }\n"
"")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        self.pushButton_info = QtWidgets.QPushButton(self.groupBox_progress_bar)
        self.pushButton_info.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.root_project_dir + "/resources/icon/success.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_info.setIcon(icon)
        self.pushButton_info.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_info.setObjectName("pushButton_info")
        self.pushButton_info.hide()
        self.pushButton_info.setStyleSheet(" border: none;")
        self.horizontalLayout.addWidget(self.pushButton_info)
        self.label_info = QtWidgets.QLabel(self.groupBox_progress_bar)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_info.setFont(font)
        self.label_info.setObjectName("label_info")
        self.label_info.hide()
        self.label_info.setStyleSheet('border: none;')
        self.horizontalLayout.addWidget(self.label_info)
        self.horizontalLayout_2.addWidget(self.groupBox_progress_bar)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 15, -1, 7)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_5 = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_5.setStyleSheet("    border-bottom: none;"
                                   "    border-right: none;"
                                   "    border-top: none;")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.pushButton_close_bottom = QtWidgets.QPushButton(self)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_close_bottom.setFont(font)
        self.pushButton_close_bottom.setStyleSheet("\n"
"QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    text-align: center;\n"
"    border: none;"
"    border-radius: 12px;\n"
"    padding-top:     3px;\n"
"    padding-bottom: 3px;    \n"
"    padding-left:     7px;\n"
"    padding-right: 7px;    \n"
"   }\n"
"QPushButton:hover {\n"
"    background-color: rgb(230, 230, 230); /* Цвет фона при наведении (немного серый) */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"     background: rgb(210, 210, 213); /* Цвет фона при нажатии (еще серее) */\n"
"}")
        self.pushButton_close_bottom.setObjectName("pushButton_close_bottom")
        self.pushButton_close_bottom.hide()
        self.horizontalLayout_4.addWidget(self.pushButton_close_bottom)
        self.pushButton_chooes = QtWidgets.QPushButton(self)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_chooes.setFont(font)
        self.pushButton_chooes.setStyleSheet("\n"
"QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    text-align: center;\n"
"    border: none;"
"    border-radius: 12px;\n"
"    padding-top:     3px;\n"
"    padding-bottom: 3px;    \n"
"    padding-left:     7px;\n"
"    padding-right: 7px;    \n"
"   }\n"
"QPushButton:hover {\n"
"    background-color: rgb(230, 230, 230); /* Цвет фона при наведении (немного серый) */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"     background: rgb(210, 210, 213); /* Цвет фона при нажатии (еще серее) */\n"
"}")
        self.pushButton_chooes.setObjectName("pushButton_chooes")
        self.pushButton_chooes.hide() # скрыли
        self.horizontalLayout_4.addWidget(self.pushButton_chooes)
        self.pushButton_report = QtWidgets.QPushButton(self)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_report.setFont(font)
        self.pushButton_report.setStyleSheet("\n"
"QPushButton {\n"
"    background-color: rgb(255, 255, 255);\n"
"    text-align: center;\n"
"    border: none;"
"    border-radius: 12px;\n"
"    padding-top:     3px;\n"
"    padding-bottom: 3px;    \n"
"    padding-left:     7px;\n"
"    padding-right: 7px;    \n"
"   }\n"
"QPushButton:hover {\n"
"    background-color: rgb(230, 230, 230); /* Цвет фона при наведении (немного серый) */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"     background: rgb(210, 210, 213); /* Цвет фона при нажатии (еще серее) */\n"
"}")
        self.pushButton_report.setObjectName("pushButton_report")
        self.pushButton_report.hide()  # скрыли
        self.horizontalLayout_4.addWidget(self.pushButton_report)
        self.label_6 = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setStyleSheet("border-left: none;"
                                   "border-top: none;"
                                   "border-bottom: none;")
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        # события
        self.pushButton_close.clicked.connect(lambda: self.def_close())
        self.pushButton_close_bottom.clicked.connect(lambda: self.def_close_2())

        self.pushButton_chooes.clicked.connect(lambda: self.selecting_folder_save()) # выбор куда сохранить аккаунты с ошибкой входа
        self.pushButton_report.clicked.connect(lambda: self.open_report()) # покажет аккаунты которые уже есть в проге
        # события


    def start(self):

        self.progressBar.setValue(0)
        self.label_title.setText('Ищем папки/архивы по указанному пути...')
        # работа с прогрессбаром и вычисления сколько папок/архивов есть
        folders_and_archives = []  # Список для хранения папок и архивов
        try:  # узнаём кол-во папок и архивов
            # Получаем список всех элементов в указанном пути
            for entry in os.listdir(self.path):
                full_path = os.path.join(self.path, entry)  # Формируем полный путь

                if os.path.isdir(full_path):  # Проверка, является ли элемент папкой
                    folders_and_archives.append(entry)  # Добавляем папку в список

                elif entry.endswith(('.zip', '.rar', '.tar','.7z')):  # Проверка, является ли элемент архивом (с нужными расширениями)
                    folders_and_archives.append(entry)  # Добавляем архив в список
        except FileNotFoundError:
            error_info = Dialog_info('Ошибка!', 'Не удалось найти указанный путь','notification.mp3')  # Создаем экземпляр
            error_info.exec_()  # Открываем
            self.close()
            return
        except Exception:
            error_info = Dialog_info('Ошибка!', 'Неизвестная ошибка при \nпроверки указанного пути', 'notification.mp3')  # Создаем экземпляр
            error_info.exec_()  # Открываем
            self.close()
            return

        quantity_folder_archive = len(folders_and_archives)  # кол-во папок и архивов указанных по пути пользователя
        if quantity_folder_archive != 0:
            self.one_step = 100 / quantity_folder_archive  # сколько необходимо прибавлять к прогрессбару за один аккаунт
        else:  # если выбранного типа аккаунтов нету
            error_info = Dialog_info('Ошибка!', 'В выбранной папки нет\nнеобходимых данных!','notification.mp3')  # Создаем экземпляр
            error_info.exec_()  # Открываем
            self.close()
            return


        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()
        cursor.execute(f"SELECT ip,port,login,password,use_proxy_to_enter FROM proxy")
        proxy_from_db = cursor.fetchone()
        connection.close()
        proxy = False
        if proxy_from_db[4] == 1:  # если необходимо использовать прокси
            self.label_title.setText('Проверяем прокси...')

            efficiency = check_proxy(proxy_from_db[0], proxy_from_db[1], proxy_from_db[2], proxy_from_db[3])
            if efficiency:
                proxy = True  # если тру значит необходимо использовать прокси
            else:
                # если проблема с прокси, то вызываем спец окно и в независимо от результата выбора,
                # запускаем ещё раз добавление аккаунтов
                error_proxy = Dialog_error_proxy(proxy_from_db[0], str(proxy_from_db[1]), proxy_from_db[2],
                                                 proxy_from_db[3])  # Создаем экземпляр
                error_proxy.show_info()
                error_proxy.exec_()  # Открываем
                self.start()
                return

        self.label_title.setText(f'0 из {quantity_folder_archive}')

        self.completed = False  # отображает закончен ли процесс загрузки аккаунтов
        self.existing_accounts = []  # список tg_id которые имеются в программе
        self.quantity_start_accounts = 0  # количество запущенных аккаунтов
        self.quantity_received_accounts = 0  # количество вернувшихся аккаунтов
        self.successful_additions = 0  # количество успешных добавлений аккаунтов в программу
        self.error_enter = False  # если есть аккаунты в которые не удалось войти
        self.data_accounts = []  # хранит списки данных об аккаунте

        # ниже запуск отдельных потоков
        try:
            counter_folder = 0  # счётчик пройденных папок
            for entry in os.listdir(self.path):  # получаем список всех файлов и папок
                try:
                    full_path = os.path.join(self.path,entry)  # указывает на папку/архив на которой сейчас находимся (в них должна содеражаться папка tdata)
                    this_folder = True

                    if os.path.isdir(full_path):  # если нашли папку
                        this_folder = True
                    elif entry.endswith(('.zip', '.rar', '.tar', '.7z')):  # если нашли архив
                        this_folder = False

                    add_account = add_accounts(full_path, this_folder, proxy, proxy_from_db[0],
                                               proxy_from_db[1], proxy_from_db[2],proxy_from_db[3])
                    add_account.task_done.connect(self.add_account_done)  # Подключаем сигнал к слоту
                    add_account.start()  # Запускаем поток

                    self.active_threads.append(add_account) # обязательно добавляем в массив к другим потокам

                    self.quantity_start_accounts += 1
                except FileNotFoundError:
                    counter_folder += 1
        except FileNotFoundError:
            error_info = Dialog_info('Ошибка!', 'Не удалось найти указанный путь', 'notification.mp3')
            error_info.exec_()  # Открываем
            self.close()
            return
        except Exception:
            error_info = Dialog_info('Ошибка!', 'Неизвестная ошибка!','notification.mp3')
            error_info.exec_()  # Открываем
            self.close()
            return

    def open_report(self):
        error_add_accounts = Dialog_error_add_accounts(self.existing_accounts)  # Создаем экземпляр
        error_add_accounts.exec_()  # Открываем

    def selecting_folder_save(self):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")# Получаем путь к рабочему столу
        # Открываем диалог выбора папки, начнем с рабочего стола
        # если пользователь выбрал папку, то вернётся путь иначе None
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку", desktop_path)

        if folder_path: # если пользователь выбрал папку (хранит выбранный путь)
            counts = 1
            folder_name = '/аккаунты с ошибкой входа'

            while True:
                try:
                    shutil.copytree(self.root_project_dir + '/working_files/error_enter_accounts', folder_path + folder_name) # копирование

                    error_info = Dialog_info('Успешно!', f'Папка успешно сохранена по пути:\n{folder_path}{folder_name}',
                                             'notification.mp3')  # Создаем экземпляр
                    error_info.exec_()  # Открываем
                    break
                except FileExistsError:
                    folder_name = f'/аккаунты с ошибкой входа ({counts})'
                    counts += 1
                except FileNotFoundError:
                    error_info = Dialog_info('Ошибка!', 'Указанный путь не найден!', 'notification.mp3')  # Создаем экземпляр
                    error_info.exec_()  # Открываем
                    break

    def add_account_done(self,data_account: list,success: bool = False,
                         existing_account: str = '0',error_enter: bool = False):
        """
        success Флаг успешного добавления аккаунта
        data_account[0] хранит путь к папке откуда необходимо скопировать данные для входа (tdata) \n
        остальное содержит данные об аккаунте \n
        existing_account это tg_id аккаунта который уже находится в программе (если его нет в проги, то вернётся 0) \n
        existing_account необходимо передавать именно str т. к. при передаче int отсылаются некорректные данные
        error_enter = True если получили ошибку входа в аккаунт \n
        """

        self.quantity_received_accounts += 1
        self.progressBar.setValue(int(self.progressBar.value()) + int(self.one_step))
        self.label_title.setText(f'{self.quantity_received_accounts} из {self.quantity_start_accounts}')

        # если аккаунт успешно добавлен в программу и его нет в списке уже добавленных аккаунтов
        if success and data_account not in self.data_accounts:
            self.successful_additions += 1
            self.data_accounts.append(data_account)

        if existing_account != '0': # если такой аккаунт уже есть в программе
            self.existing_accounts.append(int(existing_account)) # добавляем tg_id этого аккаунта

        if self.error_enter == False and error_enter == True: # если до этого момента не было ошибки добавления аккаунта, а сейчас она произошла
            self.error_enter = True # значит помечаем, что имеются аккаунты с ошибкой входа

        if self.quantity_received_accounts >= self.quantity_start_accounts: # если число запущенных и вернувшихся аккаунтов совпало
            socket.socket = self.original_socket  # убираем прокси

            self.active_threads.clear()

            self.progressBar.setValue(100)

            # создаёт новую папку c соблюдение правильной id последовательности в active_accounts
            # и копируем из указанного пути папку tdata
            connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
            cursor = connection.cursor()

            now = dt.datetime.now()  # Получаем текущее время
            formatted_date = now.strftime('%H:%M %d-%m-%Y')  # Форматируем дату и время согласно формату

            path_active_accounts = self.root_project_dir + '/accounts/active_accounts'
            counter_id = 0  # счётчик id директорий

            while True:
                if os.path.isdir(path_active_accounts + f'/{counter_id}'):  # если такой путь есть
                    counter_id += 1
                else:
                    break

            for data_account_2 in self.data_accounts:
                result_copy_path = path_active_accounts + f'/{counter_id}'

                try:  # копирование
                    shutil.copytree(data_account_2[0], result_copy_path)  # копируем папку (создавая новую папку с id)

                    cursor.execute(f"INSERT INTO accounts (id,id_tg,user_name,name,phone,data_time_add,last_used) VALUES (?,?,?,?,?,?,?)",
                        (counter_id, data_account_2[1], data_account_2[2], data_account_2[3], data_account_2[4], formatted_date, formatted_date))
                    connection.commit()  # сохранение

                    counter_id += 1
                except FileNotFoundError:
                    pass

            connection.close()

            self.label_title.setText('Готово')
            self.pushButton_close_bottom.show()
            self.resize(460, 190)

            info_result = f'Успешно добавлено {self.successful_additions} из {self.quantity_start_accounts} аккаунтов'

            if error_enter:
                self.pushButton_chooes.show()
                info_result += ('\n\nНе удалось войти в некоторые аккаунты\n'
                                'Нажмите кнопку "Выбрать" для выбора места\n'
                                'сохранения аккаунтов в которые не удалось войти')

            if self.existing_accounts:
                self.pushButton_report.show()
                info_result += ('\n\nНекоторые аккаунты уже имеются в программе\n'
                                'Нажмите кнопку "Отчёт" для подробной информации')

            self.completed = True # помечаем что процесс загрузки закончен

            error_info = Dialog_info('Готово', info_result, 'notification.mp3')  # Создаем экземпляр
            error_info.exec_()  # Открываем


    def wait_result_cancel(self, result: bool):
        if result == True:
            self.close()

    def def_close(self):
        if self.completed == True: # если процесс загрузки завершён
            self.close()
        else:
            error_proxy = Dialog_ok_or_cancel('Внимание!',
                                              'Вы действительно хотите остановить процесс\nдобавления новых аккаунтов?\nЭто может привести к поломке программы!',
                                                'notification.mp3')  # Создаем экземпляр
            error_proxy.data_returned.connect(self.wait_result_cancel)  # Подключаем сигнал
            error_proxy.exec_()  # Открываем модальное окно

    def def_close_2(self):
        self.close()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_title.setText(_translate("Dialog", "В процессе..."))
        self.pushButton_close.setText(_translate("Dialog", "✕"))
        self.label_info.setText(_translate("Dialog", "TextLabel"))
        self.pushButton_close_bottom.setText(_translate("Dialog", "Закрыть"))
        self.pushButton_chooes.setText(_translate("Dialog", "Выбрать"))
        self.pushButton_report.setText(_translate("Dialog", "Отчёт"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Dialog_add_accounts('fds')
    ui.show()
    ui.start()
    sys.exit(app.exec_())
