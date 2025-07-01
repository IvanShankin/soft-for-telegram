import sys
import sqlite3
import socks
import socket
import datetime as dt

from opentele.td import TDesktop
from opentele.api import UseCurrentSession
from opentele.exception import TFileNotFound

from telethon.tl.functions.account import UpdateProfileRequest, UpdateUsernameRequest
from telethon.errors import UsernameOccupiedError
from telethon.tl.functions.users import GetFullUserRequest

import asyncio
import os

from app.accounts.flag import get_country_flag
from app.general.views.error_proxy import DialogErrorProxy
from app.general.check_proxy import check_proxy
from app.general.views.info import DialogInfo
from app.general.error_handler import error_handler
from app.accounts.ui.dialog_more_info_account_ui import DialogMoreInfoAccountUi

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")# 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():# 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path# 3. Установка пути

# 4. Только после этого импортируем PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QFontMetrics

class DialogMoreInfoAccount(DialogMoreInfoAccountUi):
    def __init__(self, id: int, account_type: str):
        super().__init__()
        self.id = id
        self.account_type = account_type
        self.original_socket = socket.socket  # запоминаем какой сокет был до
        self.root_project_dir = '..'

        # события
        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_close_2.clicked.connect(self.close)
        self.pushButton_save.clicked.connect(lambda: asyncio.run(self.save_data()))
        # события

    async def save_data(self):
        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()
        if self.account_type == 'login_error':
            cursor.execute(f"UPDATE accounts SET notes = ?  WHERE id = ? AND account_status = ? ",
                           (self.lineEdit_notes.text(), self.id, self.account_type))
            connection.commit()
            connection.close()
            error_info = DialogInfo('Готово!',f'Данные успешно сохранены!','notification.mp3')  # Создаем экземпляр
            error_info.exec_()  # Открываем
            return

        cursor.execute(f"SELECT user_name,name,notes FROM accounts WHERE id = ? AND account_status = ? ",
                       (self.id, self.account_type))
        account_from_db = cursor.fetchone()

        cursor.execute(f"SELECT ip,port,login,password,use_proxy_to_enter FROM proxy")
        proxy_from_db = cursor.fetchone()

        if proxy_from_db[4] == 1:  # если необходимо использовать прокси
            efficiency = check_proxy(proxy_from_db[0], int(proxy_from_db[1]), proxy_from_db[2], proxy_from_db[3])
            if efficiency:  # если работает
                cursor.execute(f"SELECT ip,port,login,password,use_proxy_to_enter FROM proxy")
                proxy_from_db = cursor.fetchone()
                socks.set_default_proxy(socks.SOCKS5, proxy_from_db[0], proxy_from_db[1], True, proxy_from_db[2],
                                        proxy_from_db[3])  # Установка прокси-соединения
                socket.socket = socks.socksocket
            else:  # если не смогли подключиться к прокси
                socket.socket = self.original_socket
                cursor.execute(f"SELECT ip,port,login,password FROM proxy")
                proxy_from_db = cursor.fetchone()
                connection.close()
                self.show_error_proxy(proxy_from_db[0], proxy_from_db[1], proxy_from_db[2], proxy_from_db[3])
                return

        result_message = ''

        try:
            tdesk = TDesktop(self.root_project_dir + f'/accounts/{self.account_type}_accounts/{self.id}/tdata')
            client = await tdesk.ToTelethon(
                session = self.root_project_dir + f"/accounts/{self.account_type}_accounts/{self.id}/session.session",
                flag = UseCurrentSession)
<<<<<<< HEAD
            await asyncio.wait_for(client.connect(), timeout=15)  # вход в аккаунт
=======
            await asyncio.wait_for(client.connect(), timeout=5)  # вход в аккаунт
>>>>>>> d5cd4b4d78a37a2cf276f0ddebf12b9c08eeb563
            me = await client.get_me()

            if account_from_db[1] != self.lineEdit_name.text():
                try:
                    await client(UpdateProfileRequest(first_name = self.lineEdit_name.text()))
                    cursor.execute(f"UPDATE accounts SET name = ?  WHERE id = ? AND account_status = ? ",
                                   (self.lineEdit_name.text(), self.id, self.account_type))
                    connection.commit()
                except Exception:
                    result_message += 'Произошла ошибка при обновлении имени.\n'

            if me.last_name != self.lineEdit_surname.text():
                try:
                    await client(UpdateProfileRequest(last_name = self.lineEdit_surname.text()))
                except Exception:
                    result_message += 'Произошла ошибка при обновлении Фамилии.\n'

            if account_from_db[0] != self.lineEdit_user_name.text():
                try:
                    await client(UpdateUsernameRequest(username = self.lineEdit_user_name.text()))
                    cursor.execute(f"UPDATE accounts SET user_name = ?  WHERE id = ? AND account_status = ? ",
                                   (self.lineEdit_user_name.text(), self.id, self.account_type))
                    connection.commit()
                except UsernameOccupiedError:  # если имя уже занято
                    result_message += 'Данный юзернейм занят!\n'
                except Exception as e:
                    result_message += 'Произошла ошибка при обновлении юзернейма.\n'

            try:
                await client(UpdateProfileRequest(about = self.lineEdit_bio.text()))
            except Exception:
                result_message += 'Произошла ошибка при обновлении информации о себе.\n'

            cursor.execute(f"UPDATE accounts SET notes = ?  WHERE id = ? AND account_status = ? ",
                           (self.lineEdit_notes.text(), self.id, self.account_type))
            connection.commit()

            await client.disconnect()
            socket.socket = self.original_socket
        except (Exception, TFileNotFound) as e:
            try:
                await client.disconnect()
            except UnboundLocalError:
                pass
            socket.socket = self.original_socket
            connection.close()
            error_type = type(e)
            description_error_and_solution = error_handler(str(error_type.__name__), self.id, self.account_type)

            error_info = DialogInfo('Внимание!',
                                     f'Данный аккаунт с ошибкой входа\nОшибка: {description_error_and_solution[0]}\n'
                                     f'Решение: {description_error_and_solution[1]}',
                                     'notification.mp3')  # Создаем экземпляр
            error_info.exec_()  # Открываем
            self.close()
            return

        connection.close()

        if result_message == '': # если не словили ошибку
            result_message = 'Данные успешно сохранены!'
        else:
            result_message = 'При загрузке данных произошла ошибка:\n' + result_message + 'Попробуйте вписать другие значения'

        error_info = DialogInfo('Готово!', result_message,'notification.mp3')  # Создаем экземпляр
        error_info.exec_()  # Открываем


    def comparison_with_DB(self, id_tg: int, user_name: str, name: str,phone: str):
        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()
        cursor.execute(f"SELECT id_tg,user_name,name,phone FROM accounts WHERE id = ? AND account_status = ? ",
                       (self.id, self.account_type))
        account_from_db = cursor.fetchone()
        if  id_tg != account_from_db[0]:
            cursor.execute(f"UPDATE accounts SET id_tg = ?  WHERE id = ? AND account_status = ? ",(id_tg, self.id, self.account_type))
            connection.commit()
        if  user_name != account_from_db[1]:
            cursor.execute(f"UPDATE accounts SET user_name = ?  WHERE id = ? AND account_status = ? ",(user_name, self.id, self.account_type))
            connection.commit()
        if  name != account_from_db[2]:
            cursor.execute(f"UPDATE accounts SET name = ?  WHERE id = ? AND account_status = ? ",(name, self.id, self.account_type))
            connection.commit()
        if  phone != account_from_db[3]:
            cursor.execute(f"UPDATE accounts SET phone = ?  WHERE id = ? AND account_status = ? ",(phone, self.id, self.account_type))
            connection.commit()

    def show_error_proxy(self,ip: str,port: str,login: str,password: str):
        error_proxy = DialogErrorProxy(ip,port,login,password)  # Создаем экземпляр
        error_proxy.show_info()
        error_proxy.exec_()  # Открываем
        self.show_info_account()

    def show_from_db(self):
        self.label_13.hide()
        self.label_14.hide()
        self.lineEdit_surname.hide()
        self.lineEdit_bio.hide()

        self.label_3.setGeometry(67, 159, 99, 23)
        self.label_4.setGeometry(125, 201, 41, 23)
        self.label_5.setGeometry(82, 241, 84, 23)
        self.label_6.setGeometry(83, 281, 83, 23)
        self.label_7.setGeometry(26, 321, 140, 23)
        self.label_9.setGeometry(126, 361, 40, 23)
        self.label_8.setGeometry(50, 401, 116, 23)

        self.lineEdit_user_name.setGeometry(180, 159, 471, 29)
        self.label_geo.setGeometry(185, 201, 40, 26)
        self.label_phone.setGeometry(180, 241, 141, 27)
        self.label_recuperation.setGeometry(180, 281, 141, 27)
        self.label_last_used.setGeometry(180, 321, 141, 27)
        self.label_type.setGeometry(180, 361, 141, 27)
        self.lineEdit_notes.setGeometry(180, 401, 471, 29 )

        style_for_lineEdit = ("border: none;\n"
                              "  background-color: rgb(255, 255, 255);\n"
                              "    text-align: center;\n"
                              "    border-radius: 10px;\n"
                              "padding: 4px;"
                              "    padding-left: 10px;"
                              "    padding-right: 10px;"
                              )

        self.lineEdit_user_name.setStyleSheet(style_for_lineEdit)
        self.lineEdit_name.setStyleSheet(style_for_lineEdit)
        self.lineEdit_name.setReadOnly(True)
        self.lineEdit_user_name.setReadOnly(True)

        self.pushButton_save.setGeometry(163, 520, 221, 41)
        self.pushButton_close_2.setGeometry(390, 520, 101, 41)

        self.resize(679,575)
        self.label_erro_info.show()
        self.label_error.show()
        self.label_solution_error_info.show()
        self.label_solution_error.show()

        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()
        cursor.execute(f"SELECT id_tg, user_name, name, phone, data_time_add, last_used, notes, error, solution_error FROM accounts WHERE id = ? AND account_status = ? ",
            (self.id, self.account_type))
        account_from_db = cursor.fetchone()

        dt_from_db = dt.datetime.strptime(account_from_db[4],'%H:%M %d-%m-%Y')  # первый принимаемый параметр это входная строка с датой, второй это формат даты
        time_difference = dt.datetime.now() - dt_from_db  # Вычисляем разницу во времени
        days_difference = time_difference.days
        resting_place = f"{days_difference} {'день' if days_difference == 1 else 'дня' if 2 <= days_difference <= 4 else 'дней'}"
        geo_name = get_country_flag(account_from_db[3])

        # вывод данных
        self.label_id.setText(str(self.id))
        self.label_tg_id.setText(str(account_from_db[0]))
        self.lineEdit_name.setText(account_from_db[2])
        self.lineEdit_user_name.setText(account_from_db[1])

        pixmap = QPixmap(self.root_project_dir + f"/resources/pictures_flag/{geo_name}.png")  # Замените путь к изображению
        if not pixmap.isNull():  # Проверяем, что изображение загружено успешно
            self.label_geo.setPixmap(pixmap)  # Устанавливаем изображение
        else:
            pixmap = QPixmap(self.root_project_dir + f'/resources/pictures_flag/default_flag.png')  # Путь к изображению флага
            self.label_geo.setPixmap(pixmap)  # Устанавливаем изображение

        self.label_phone.setText(account_from_db[3])
        self.label_recuperation.setText(resting_place)
        self.label_last_used.setText(account_from_db[5])
        self.label_type.setText('С ошибкой входа')
        self.lineEdit_notes.setText(account_from_db[6])
        self.label_error.setText(account_from_db[7])
        self.label_solution_error.setText(account_from_db[8])

        self.label_id.adjustSize()
        self.label_tg_id.adjustSize()
        metrics = QFontMetrics(self.lineEdit_name.font())
        text_width = metrics.width(self.lineEdit_name.text())
        self.lineEdit_name.setFixedWidth(text_width)
        metrics = QFontMetrics(self.lineEdit_user_name.font())
        text_width = metrics.width(self.lineEdit_user_name.text())
        self.lineEdit_user_name.setFixedWidth(text_width)
        self.label_phone.adjustSize()
        self.label_recuperation.adjustSize()
        self.label_last_used.adjustSize()
        self.label_type.adjustSize()
        self.label_error.adjustSize()
        self.label_solution_error.adjustSize()

    async def show_info_account(self):

        if self.account_type == 'login_error':
            self.show_from_db()
            return

        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()
        cursor.execute(f"SELECT ip,port,login,password,use_proxy_to_enter FROM proxy")
        proxy_from_db = cursor.fetchone()

        if proxy_from_db[4] == 1:  # если необходимо использовать прокси
            efficiency = check_proxy(proxy_from_db[0], int(proxy_from_db[1]), proxy_from_db[2], proxy_from_db[3])
            if efficiency: # если работает
                cursor.execute(f"SELECT ip,port,login,password,use_proxy_to_enter FROM proxy")
                proxy_from_db = cursor.fetchone()
                socks.set_default_proxy(socks.SOCKS5, proxy_from_db[0], proxy_from_db[1], True, proxy_from_db[2],proxy_from_db[3])  # Установка прокси-соединения
                socket.socket = socks.socksocket
            else:  # если не смогли подключиться к прокси
                socket.socket = self.original_socket
                cursor.execute(f"SELECT ip,port,login,password FROM proxy")
                proxy_from_db = cursor.fetchone()
                connection.close()
                self.show_error_proxy(proxy_from_db[0], proxy_from_db[1], proxy_from_db[2], proxy_from_db[3])
                return

        connection.close()

        try:
            tdesk = TDesktop(self.root_project_dir + f'/accounts/{self.account_type}_accounts/{self.id}/tdata')
            client = await tdesk.ToTelethon(session=self.root_project_dir + f"/accounts/{self.account_type}_accounts/{self.id}/session.session",flag=UseCurrentSession)
<<<<<<< HEAD
            await asyncio.wait_for(client.connect(), timeout=15)  # вход в аккаунт
=======
            await asyncio.wait_for(client.connect(), timeout=5)  # вход в аккаунт
>>>>>>> d5cd4b4d78a37a2cf276f0ddebf12b9c08eeb563
            me = await client.get_me()
            full_user = await client(GetFullUserRequest(me.id))
            await client.disconnect()

            socket.socket = self.original_socket
        except (Exception, TFileNotFound) as e:
            try:
                await client.disconnect()
            except UnboundLocalError:
                pass
            socket.socket = self.original_socket
            connection.close()
            error_type = type(e)
            description_error_and_solution = error_handler(str(error_type.__name__),self.id,self.account_type)

            error_info = DialogInfo('Внимание!', f'Данный аккаунт с ошибкой входа\nОшибка: {description_error_and_solution[0]}\n'
                                                  f'Решение: {description_error_and_solution[1]}','notification.mp3')  # Создаем экземпляр
            error_info.exec_()  # Открываем
            self.close()
            return

        self.comparison_with_DB(me.id,me.username,me.first_name,me.phone)

        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()
        cursor.execute(f"SELECT data_time_add,notes,last_used FROM accounts WHERE id = ? AND account_status = ? ",
            (self.id, self.account_type))
        account_from_db = cursor.fetchone()

        dt_from_db = dt.datetime.strptime(account_from_db[0],'%H:%M %d-%m-%Y')  # первый принимаемый параметр это входная строка с датой, второй это формат даты
        time_difference = dt.datetime.now() - dt_from_db  # Вычисляем разницу во времени
        days_difference = time_difference.days
        resting_place = f"{days_difference} {'день' if days_difference == 1 else 'дня' if 2 <= days_difference <= 4 else 'дней'}"
        geo_name = get_country_flag(me.phone)

        if self.account_type == 'active':
            account_type = 'Активный'
        elif self.account_type == 'archive':
            account_type = 'В архиве'
        elif self.account_type == 'main':
            account_type = 'Главный'
        elif self.account_type == 'temporary_ban':
            account_type = 'Во временном бане'
        else:
            account_type = 'С ошибкой входа'


        # вывод данных
        self.label_id.setText(str(self.id))
        self.label_tg_id.setText(str(me.id))
        self.lineEdit_name.setText(me.first_name)
        self.lineEdit_surname.setText(me.last_name)
        self.lineEdit_user_name.setText(me.username)

        pixmap = QPixmap(self.root_project_dir + f"/resources/pictures_flag/{geo_name}.png")  # Замените путь к изображению
        if not pixmap.isNull():  # Проверяем, что изображение загружено успешно
            self.label_geo.setPixmap(pixmap)  # Устанавливаем изображение
        else:
            pixmap = QPixmap(self.root_project_dir + f'/resources/pictures_flag/default_flag.png')  # Путь к изображению флага
            self.label_geo.setPixmap(pixmap) # Устанавливаем изображение

        self.label_phone.setText(str(me.phone))
        self.lineEdit_bio.setText(full_user.full_user.about)
        self.label_recuperation.setText(resting_place)
        self.label_last_used.setText(account_from_db[2])
        self.label_type.setText(account_type)
        self.lineEdit_notes.setText(account_from_db[1])

        self.label_id.adjustSize()
        self.label_tg_id.adjustSize()
        self.label_phone.adjustSize()
        self.label_recuperation.adjustSize()
        self.label_last_used.adjustSize()
        self.label_type.adjustSize()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = DialogMoreInfoAccount(1,'login_error')
    ui.show()
    asyncio.run( ui.show_info_account()) # вызываем показ аккунта
    sys.exit(app.exec_())
