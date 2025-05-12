import sys
import os
import time
from pathlib import Path
import requests
import psutil

from accounts.accounts import Window_accounts
from mailing_by_users.mailing_by_users import Window_mailing_by_users
from general.info import Dialog_info
from proxy.proxy import Window_proxy
from parser.parser import Window_parser
from convert.convert import Window_convert
from invite.invite import Window_invite

from pathlib import Path
import PyQt5

qt_plugins_path = str(Path(PyQt5.__file__).parent / "Qt5" / "plugins")# 1. Автоматическое определение пути
if not Path(qt_plugins_path).exists():# 2. Проверка существования
    raise RuntimeError(f"Qt plugins not found at: {qt_plugins_path}")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path# 3. Установка пути

# 4. Только после этого импортируем PyQt5
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QStackedWidget
from PyQt5.QtWidgets import QWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Black Smm")

        # Создаем QStackedWidget для хранения окон
        self.stacked_widget = QStackedWidget(self)

        # Создаем экземпляры окон
        self.accounts_window = Window_accounts(self.switch_window)
        self.accounts_window.start_show_account('active')
        self.mailing_by_users_window = Window_mailing_by_users(self.switch_window)
        self.proxy_window = Window_proxy(self.switch_window)
        self.parser = Window_parser(self.switch_window)
        self.convert = Window_convert(self.switch_window)
        self.invite = Window_invite(self.switch_window)

        # Добавляем окна в QStackedWidget
        self.stacked_widget.addWidget(self.accounts_window)
        self.stacked_widget.addWidget(self.mailing_by_users_window)
        self.stacked_widget.addWidget(self.proxy_window)
        self.stacked_widget.addWidget(self.parser)
        self.stacked_widget.addWidget(self.convert)
        self.stacked_widget.addWidget(self.invite)


        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        # Показываем первое окно при старте
        self.stacked_widget.setCurrentWidget(self.accounts_window)

    def switch_window(self, target_window: str):
        if target_window == 'accounts':
            self.accounts_window.show_accounts_from_db()
            self.stacked_widget.setCurrentWidget(self.accounts_window)  # Переключаемся на окно аккаунты
        elif target_window == 'mailing_by_users':
            self.stacked_widget.setCurrentWidget(self.mailing_by_users_window)
        elif target_window == 'proxy':
            self.stacked_widget.setCurrentWidget(self.proxy_window)
        elif target_window == 'bomber':
            pass
        elif target_window == 'comment':
            pass
        elif target_window == 'convert':
            self.stacked_widget.setCurrentWidget(self.convert)
        elif target_window == 'doc':
            pass
        elif target_window == 'enter_group':
            pass
        elif target_window == 'invite':
            self.stacked_widget.setCurrentWidget(self.invite)
        elif target_window == 'mailing_by_chats':
            pass
        elif target_window == 'parser':
            self.stacked_widget.setCurrentWidget(self.parser)
        elif target_window == 'reactions':
            pass


if __name__ == "__main__":
    try:
        # Попытка отправить запрос к Google
        response = requests.get("http://www.google.com", timeout=5)
    except Exception:  # Если есть ошибка соединения, интернета нет
        info = Dialog_info('Внимание!', 'Отсутствует подключение к интернету.\nБез него приложение не может корректно функционировать',
                           'notification.mp3')
        info.show()
        sys.exit()

    script_name = os.path.basename(__file__)  # Получаем имя текущего скрипта
    for process in psutil.process_iter(['pid', 'name']):
        try:
            # Проверка по имени процесса
            if script_name in process.info['name']:
                info = Dialog_info('Внимание!',
                                   'Приложение уже запущенно!',
                                   'notification.mp3')
                info.show()
                sys.exit()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.resize(1500, 850)
    main_window.show()
    sys.exit(app.exec_())