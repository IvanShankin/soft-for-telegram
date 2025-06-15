import os  # это для действия ниже перед запуском функции
import sys  # информация о системе
import sqlite3

from app.general.views.info import DialogInfo
from app.general.check_proxy import check_proxy
from app.proxy.ui.window_proxy_ui import WindowProxyUi

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")  # 1. Автоматическое определение пути

if not Path(qt_plugins_path).exists():  # 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path  # 3. Установка пути

# 4. Только после этого импортируем QApplication
from PyQt5 import QtWidgets


class WindowProxy(WindowProxyUi):
    def __init__(self, switch_window=None):
        super().__init__()

        self.switch_window = switch_window
        self.root_project_dir = '..'

        self.show_data()

        # события
        self.pushButton_account.clicked.connect(lambda: self.switch_window('accounts'))
        self.pushButton_mailing.clicked.connect(lambda: self.switch_window('mailing_by_users'))
        self.pushButton_mailing_chat.clicked.connect(lambda: self.switch_window('mailing_by_chats'))
        self.pushButton_invite.clicked.connect(lambda: self.switch_window('invite'))
        self.pushButton_parser.clicked.connect(lambda: self.switch_window('parser'))
        self.pushButton_bomber.clicked.connect(lambda: self.switch_window('bomber'))
        self.pushButton_create_channel.clicked.connect(lambda: self.switch_window('create_channel'))
        self.pushButton_create_bot.clicked.connect(lambda: self.switch_window('create_bot'))
        self.pushButton_enter_group.clicked.connect(lambda: self.switch_window('enter_group'))
        self.pushButton_reactions.clicked.connect(lambda: self.switch_window('reactions'))
        self.pushButton_comment.clicked.connect(lambda: self.switch_window('comment'))
        self.pushButton_convert.clicked.connect(lambda: self.switch_window('convert'))
        self.pushButton_doc.clicked.connect(lambda: self.switch_window('doc'))

        self.pushButton_check_proxy.clicked.connect(lambda: self._check_proxy())

        self.checkBox_use_proxy_for_loading.clicked.connect(lambda: self._change_checkbox())
        self.pushButton_icon_info.clicked.connect(lambda: self._open_info())

        # при потери фокуса вызывается
        self.lineEdit_ip_socks5.editingFinished.connect(lambda: self._editing_finished())
        self.lineEdit_port_socks5.editingFinished.connect(lambda: self._editing_finished())
        self.lineEdit_login_socks5.editingFinished.connect(lambda: self._editing_finished())
        self.lineEdit_password_socks5.editingFinished.connect(lambda: self._editing_finished())
        # события

    def show_data(self): # показывает данны о прокси
        connection = sqlite3.connect(self.root_project_dir + "/working_files/data_base.sqlite3")
        cursor = connection.cursor()
        cursor.execute(f"SELECT ip, port, login, password, use_proxy_to_enter FROM proxy", )
        data_proxy = cursor.fetchone()
        connection.close()

        self.lineEdit_ip_socks5.setText(str(data_proxy[0]))
        self.lineEdit_port_socks5.setText(str(data_proxy[1]))
        self.lineEdit_login_socks5.setText(str(data_proxy[2]))
        self.lineEdit_password_socks5.setText(str(data_proxy[3]))

        if data_proxy[4] == 1:
            self.checkBox_use_proxy_for_loading.setChecked(True)

    def _change_checkbox(self):
        result = self.checkBox_use_proxy_for_loading.isChecked()

        connection = sqlite3.connect(self.root_project_dir + "/working_files/data_base.sqlite3")
        cursor = connection.cursor()
        if result: # если чекбокс включён, значит необходимо использовать прокси при загрузки аккаунтов
            cursor.execute(f"UPDATE proxy SET use_proxy_to_enter = ?",(1,))
        else:
            cursor.execute(f"UPDATE proxy SET use_proxy_to_enter = ?",(0,))

        connection.commit()
        connection.close()

    def _open_info(self):
        ui = DialogInfo('Информация!', 'Для получения актуальных данных о аккаунте, необходимо войти в него\n'
                                        'Вход происходит при запуске приложения. \nМожно входить в него с использованием прокси SOCKS5',
                         'notification.mp3')
        ui.exec_()  # Открываем

    def _editing_finished(self):
        port = None
        try:
            port = int(self.lineEdit_port_socks5.text())
        except:
            port = None

        connection = sqlite3.connect(self.root_project_dir + "/working_files/data_base.sqlite3")
        cursor = connection.cursor()
        cursor.execute(f"UPDATE proxy SET ip = ?, port = ?, login = ?, password = ?",
                       (self.lineEdit_ip_socks5.text(),port,
                                    self.lineEdit_login_socks5.text(), self.lineEdit_password_socks5.text(),))
        connection.commit()
        connection.close()

    def _check_proxy(self):
        result = check_proxy(self.lineEdit_ip_socks5.text(),int(self.lineEdit_port_socks5.text()),
                                    self.lineEdit_login_socks5.text(), self.lineEdit_password_socks5.text())

        if result:
            info = DialogInfo('Информация!', f'Успешное подключение к прокси! \nIP: {result}',
                            'notification.mp3')
        else:
            info = DialogInfo('Информация!', f'К прокси не удалось подключиться!',
                               'notification.mp3')

        info.exec_()  # Открываем

def application():
    try:
        app = QtWidgets.QApplication(sys.argv)
        account = WindowProxy()
        account.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Произошла ошибка при запуске приложения: {e}")

if __name__ == "__main__":
    application()
