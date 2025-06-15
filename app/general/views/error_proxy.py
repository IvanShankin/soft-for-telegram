import sys
import os
import sqlite3

from app.general.views.info import DialogInfo
from app.general.check_proxy import check_proxy
from app.general.ui.dialog_error_proxy_ui import DialogErrorProxyUi

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")# 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():# 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path# 3. Установка пути

# 4. Только после этого импортируем PyQt5
from PyQt5 import QtWidgets


class DialogErrorProxy(DialogErrorProxyUi):
    def __init__(self,ip: str,port: str,login: str,password: str):
        super().__init__()
        self.ip = ip
        self.port = port
        self.login = login
        self.password = password
        self.root_project_dir = '..'

        self.lineEdit_ip.setText(self.ip)
        self.lineEdit_port.setText(str(self.port))
        self.lineEdit_login.setText(self.login)
        self.lineEdit_password.setText(self.password)

        # события
        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_enter.clicked.connect(lambda: self._enter_proxy())
        self.pushButton_not_use_proxy.clicked.connect(lambda: self._not_use_proxy())
        # события

    def show_info(self):
        error_info = DialogInfo('Внимание!', 'При попытке подключиться к прокси\nпроизошла ошибка входа',
                                 'notification.mp3')  # Создаем экземпляр
        error_info.exec_()  # Открываем


    def _enter_proxy(self):
        ip = self.lineEdit_ip.text()
        port = self.lineEdit_port.text()
        login = self.lineEdit_login.text()
        password = self.lineEdit_password.text()

        if ip == '':
            self.lineEdit_ip.setStyleSheet("QLineEdit {\n"
                                           "    background-color: rgb(252, 224, 228);      /* Цвет фона текстового поля */\n"
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
                                           "    border: 2px solid rgb(1, 1, 1); /* Цвет рамки при фокусировке */\n"
                                           "    background-color: rgb(255, 255, 255); /* Цвет фона при фокусировке */\n"
                                           "}\n"
                                           "\n"
                                           "/* Состояние для отключенного текстового поля */\n"
                                           "QLineEdit:disabled {\n"
                                           "    background-color: rgb(220, 220, 220); /* Цвет фона для отключенного */\n"
                                           "    color: rgb(170, 170, 170); /* Цвет текста для отключенного */\n"
                                           "    border: 2px solid rgb(200, 200, 200); /* Цвет рамки для отключенного */\n"
                                           "}")
        if port == '':
            self.lineEdit_port.setStyleSheet("QLineEdit {\n"
                                           "    background-color: rgb(252, 224, 228);      /* Цвет фона текстового поля */\n"
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
                                           "    border: 2px solid rgb(1, 1, 1); /* Цвет рамки при фокусировке */\n"
                                           "    background-color: rgb(255, 255, 255); /* Цвет фона при фокусировке */\n"
                                           "}\n"
                                           "\n"
                                           "/* Состояние для отключенного текстового поля */\n"
                                           "QLineEdit:disabled {\n"
                                           "    background-color: rgb(220, 220, 220); /* Цвет фона для отключенного */\n"
                                           "    color: rgb(170, 170, 170); /* Цвет текста для отключенного */\n"
                                           "    border: 2px solid rgb(200, 200, 200); /* Цвет рамки для отключенного */\n"
                                           "}")

        if ip == '' or port == '':
            error_info = DialogInfo('Внимание!', 'Не все данные заполнены','notification.mp3')  # Создаем экземпляр
            error_info.exec_()  # Открываем
            return

        result =  check_proxy(ip, int(port), login, password)

        if result:
            connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
            cursor = connection.cursor()
            cursor.execute(f"UPDATE proxy SET ip = ?, port = ?, login = ?, password = ?", (ip, port, login, password))
            connection.commit()  # сохранение
            connection.close()

            error_info = DialogInfo('Успех!', f'К прокси удалось подключиться.\nВаш IP: {result}\nДанные сохранены!','notification.mp3')  # Создаем экземпляр
            error_info.exec_()  # Открываем
            self.close()
        else:
            error_info = DialogInfo('Ошибка!', 'К прокси не удалось подключиться.\nПроверьте корректность введённых данных','notification.mp3')  # Создаем экземпляр
            error_info.exec_()  # Открываем

    def _not_use_proxy(self):
        connection = sqlite3.connect(self.root_project_dir + '/working_files/data_base.sqlite3')
        cursor = connection.cursor()
        cursor.execute(f"UPDATE proxy SET use_proxy_to_enter = ?",(0,))
        connection.commit()  # сохранение
        connection.close()

        error_info = DialogInfo('Готово!', 'Теперь при загрузке аккаунтов\nне будет использоваться прокси','notification.mp3')  # Создаем экземпляр
        error_info.exec_()  # Открываем
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = DialogErrorProxy('83.217.5.96','11225','FvngSoSAQj','LNyr1N65pR')
    ui.show()
    sys.exit(app.exec_())
