import os  # это для действия ниже перед запуском функции
import sys  # информация о системе
import sqlite3
import socks
import socket
import asyncio
import shutil  # для удаления папки

from opentele.td import TDesktop
from opentele.api import UseCurrentSession
from opentele.exception import TFileNotFound
from opentele.tl import TelegramClient

from app.general.views.info import DialogInfo
from app.general.check_proxy import check_proxy
from app.general.views.error_proxy_for_work import DialogErrorProxyForWork
from app.convert.ui.window_convert_ui import WindowConvertUi

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")# 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():# 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path# 3. Установка пути

# Только после этого импортируем PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog


class WindowConvert(WindowConvertUi):
    def __init__(self,switch_window):
        super().__init__()
        self.switch_window = switch_window
        self.root_project_dir = '..'

        if os.path.isfile(f'{self.root_project_dir}/working_files/convert_file/account.session'):
            os.remove(f'{self.root_project_dir}/working_files/convert_file/account.session')  # удаляем остатки прошлой сессии

        if os.path.isdir(f'{self.root_project_dir}/working_files/convert_file/tdata'):
            shutil.rmtree(f'{self.root_project_dir}/working_files/convert_file/tdata')  # удаляем остатки прошлой сессии

        # события
        self.pushButton_account.clicked.connect(lambda: self.switch_window('accounts'))
        self.pushButton_mailing.clicked.connect(lambda: self.switch_window('mailing_by_users'))
        self.pushButton_mailing_chat.clicked.connect(lambda: self.switch_window('mailing_by_chats'))
        self.pushButton_invite.clicked.connect(lambda: self.switch_window('invite'))
        self.pushButton_parser.clicked.connect(lambda: self.switch_window('parser'))
        self.pushButton_proxy.clicked.connect(lambda: self.switch_window('proxy'))
        self.pushButton_bomber.clicked.connect(lambda: self.switch_window('bomber'))
        self.pushButton_create_channel.clicked.connect(lambda: self.switch_window('create_channel'))
        self.pushButton_enter_group.clicked.connect(lambda: self.switch_window('enter_group'))
        self.pushButton_reactions.clicked.connect(lambda: self.switch_window('reactions'))
        self.pushButton_comment.clicked.connect(lambda: self.switch_window('comment'))
        self.pushButton_doc.clicked.connect(lambda: self.switch_window('doc'))

        self.pushButton_info_convert_in_session.clicked.connect(lambda: self._info_convert_in_session())
        self.pushButton_info_convert_in_tdata.clicked.connect(lambda: self._info_convert_in_tdata())

        self.pushButton_choose_folder.clicked.connect(lambda: asyncio.run(self._convert_in_session()))
        self.pushButton_choose_file.clicked.connect(lambda: asyncio.run(self._convert_in_tdata()))
        # события

    def _info_convert_in_session(self):
        info = DialogInfo('Информация', 'Укажите путь к папке Tdata\n\nВ ней хранятся данные для входа в аккаунт и настройки аккаунта\n'
                                'Будет произведена попытка входа и в случае успеха сформируется файл .session',
                                'notification.mp3')  # Создаем экземпляр
        info.exec_()  # Открываем

    def _info_convert_in_tdata(self):
        info = DialogInfo('Информация', 'Укажите путь к файлу с расширением .session\n\nЭто файл с данными для входа в аккаунт\n'
                                         'Будет произведена попытка входа и в случае успеха сформируется папка Tdata',
                           'notification.mp3')  # Создаем экземпляр
        info.exec_()  # Открываем

    def _check_proxy(self):
        """Если успешно подключились к прокси, то вернёт данные для входа
           возвращаемые значения:
            proxy_from_db[0] = ip прокси
            proxy_from_db[1] = port прокси
            proxy_from_db[2] = login прокси
            proxy_from_db[3] = password прокси

            если не смогли подключиться, то ничего не вернёт"""

        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()
        cursor.execute(f"SELECT ip,port,login,password FROM proxy")
        proxy_from_db = cursor.fetchone()
        connection.close()

        efficiency = check_proxy(proxy_from_db[0], proxy_from_db[1], proxy_from_db[2], proxy_from_db[3])
        if efficiency:
            return [proxy_from_db[0], str(proxy_from_db[1]), proxy_from_db[2],proxy_from_db[3]]
        else:
            # если проблема с прокси, то вызываем спец окно и в независимо от результата выбора,
            # запускаем ещё раз добавление аккаунтов
            error_proxy = DialogErrorProxyForWork(proxy_from_db[0], str(proxy_from_db[1]), proxy_from_db[2],proxy_from_db[3])  # Создаем экземпляр
            error_proxy.show_info()
            error_proxy.exec_()  # Открываем
            return

    async def _convert_in_session(self):
        data_proxy = []
        original_socket = socket.socket  # запоминаем какой сокет был до
        if self.checkBox_use_proxy.isChecked():
            data_proxy = self._check_proxy()
            if not data_proxy: # если прокси не действительно
                return

        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")  # Получаем путь к рабочему столу
        # Открываем диалог выбора папки, начнем с рабочего стола
        # если пользователь выбрал папку, то вернётся путь иначе None
        tdata_path = QFileDialog.getExistingDirectory(self, "Выберите папку", desktop_path)

        if tdata_path:  # если пользователь выбрал папку (хранит выбранный путь)
            if os.path.isfile(f'{self.root_project_dir}/working_files/convert_file/account.session'):
                os.remove(f'{self.root_project_dir}/working_files/convert_file/account.session') # удаляем остатки прошлой сессии

            if data_proxy:
                socks.set_default_proxy(socks.SOCKS5, data_proxy[0], data_proxy[1], True, data_proxy[2],data_proxy[3])  # Установка прокси-соединения
                socket.socket = socks.socksocket

            try:
                tdesk = TDesktop(tdata_path)
                client = await tdesk.ToTelethon(session=f"{self.root_project_dir}/working_files/convert_file/account.session",
                                                flag=UseCurrentSession)
                await asyncio.wait_for(client.connect(), timeout=10)  # вход в аккаунт
                me = await client.get_me()
                test_id = me.id
                await client.disconnect()
            except (Exception, TFileNotFound) as e:
                try:
                    await client.disconnect()
                except UnboundLocalError:
                    pass
                info = DialogInfo('Внимание!',
                                   'Не удалось создать файл .session\n\nДанные для входа не корректны!\n'
                                   'С помощь данной папки вход в аккаунт невозможен!',
                                   'notification.mp3')  # Создаем экземпляр
                info.exec_()  # Открываем
                return

            socket.socket = original_socket
            info = DialogInfo('Успешно!',
                               'Файл .session успешно сформирован\nВыберите путь его сохранения',
                               'notification.mp3','Выбрать')  # Создаем экземпляр
            info.exec_()  # Открываем

            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")  # Получаем путь к рабочему столу
            # Открываем диалог выбора папки, начнем с рабочего стола
            # если пользователь выбрал папку, то вернётся путь иначе None
            save_path = QFileDialog.getExistingDirectory(self, "Выберите папку", desktop_path)

            if save_path:
                counts = 1
                folder_name = '/account.session'

                while True:
                    try:
                        shutil.copy(f"{self.root_project_dir}/working_files/convert_file/account.session",
                                        save_path + folder_name)  # копирование

                        error_info = DialogInfo('Успешно!',
                                                 f'Файл успешно сохранена по пути:\n{save_path}{folder_name}',
                                                 'notification.mp3')  # Создаем экземпляр
                        error_info.exec_()  # Открываем
                        if os.path.isfile(f'{self.root_project_dir}/working_files/convert_file/account.session'):
                            os.remove(f'{self.root_project_dir}/working_files/convert_file/account.session')  # удаляем остатки прошлой сессии
                        break
                    except FileExistsError:
                        folder_name = f'/account({counts}).session'
                        counts += 1
                    except FileNotFoundError:
                        error_info = DialogInfo('Ошибка!', 'Указанный путь не найден!',
                                                 'notification.mp3')  # Создаем экземпляр
                        error_info.exec_()  # Открываем
                        break

    async def _convert_in_tdata(self):
        data_proxy = []
        original_socket = socket.socket  # запоминаем какой сокет был до
        if self.checkBox_use_proxy.isChecked():
            data_proxy = self._check_proxy()
            if not data_proxy:  # если прокси не действительно
                return

        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")  # Получаем путь к рабочему столу
        # Открываем диалог выбора папки, начнем с рабочего стола
        # если пользователь выбрал папку, то вернётся путь иначе None
        session_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", desktop_path, "Файл для входа (*.session)")

        if session_path:  # если пользователь выбрал папку (хранит выбранный путь)
            if os.path.isdir(f'{self.root_project_dir}/working_files/convert_file/tdata'):
                shutil.rmtree(f'{self.root_project_dir}/working_files/convert_file/tdata')  # удаляем остатки прошлой сессии

            if data_proxy:
                socks.set_default_proxy(socks.SOCKS5, data_proxy[0], data_proxy[1], True, data_proxy[2],data_proxy[3])  # Установка прокси-соединения
                socket.socket = socks.socksocket

            try:
                client = TelegramClient(session_path)
                tdesk = await client.ToTDesktop(flag=UseCurrentSession)
                await asyncio.wait_for(client.connect(), timeout=7)  # вход в аккаунт
                me = await client.get_me()
                test_id = me.id
                await client.disconnect()
                tdesk.SaveTData(f'{self.root_project_dir}/working_files/convert_file/tdata')
            except Exception:
                info = DialogInfo('Ошибка!','Данный файл не удалось конвертировать в папку Tdata',
                                   'notification.mp3', )
                info.exec_()  # Открываем
                return

            socket.socket = original_socket
            info = DialogInfo('Успешно!',
                               'Папка Tdata успешно сформирована\nВыберите путь её сохранения',
                               'notification.mp3', 'Выбрать')  # Создаем экземпляр
            info.exec_()  # Открываем

            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")  # Получаем путь к рабочему столу
            save_path = QFileDialog.getExistingDirectory(self, "Выберите папку", desktop_path)

            if save_path:
                counts = 1
                folder_name = '/tdata'

                while True:
                    try:
                        shutil.copytree(f"{self.root_project_dir}/working_files/convert_file/tdata",
                                    save_path + folder_name)  # копирование

                        error_info = DialogInfo('Успешно!',
                                                 f'Файл успешно сохранена по пути:\n{save_path}{folder_name}',
                                                 'notification.mp3')  # Создаем экземпляр
                        error_info.exec_()  # Открываем
                        if os.path.isdir(f'{self.root_project_dir}/working_files/convert_file/tdata'):
                            shutil.rmtree(f'{self.root_project_dir}/working_files/convert_file/tdata')  # удаляем остатки прошлой сессии
                        break
                    except FileExistsError:
                        folder_name = f'/tdata({counts})'
                        counts += 1
                    except FileNotFoundError:
                        error_info = DialogInfo('Ошибка!', 'Указанный путь не найден!',
                                                 'notification.mp3')  # Создаем экземпляр
                        error_info.exec_()  # Открываем
                        break

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = WindowConvert('fbdgf')
    ui.show()
    sys.exit(app.exec_())
