import sys
import os
import requests
import psutil

from app.accounts.views.accounts import WindowAccounts
from app.mailing_by_users.views.mailing_by_users import WindowMailingByUsers
from app.general.views.info import DialogInfo
from app.proxy.views.proxy import WindowProxy
from app.parser.views.parser import WindowParser
from app.convert.views.convert import WindowConvert
from app.invite.views.invite import WindowInvite
from app.create_channel.views.create_channel import WindowCreateChannel

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
        self.accounts_window = WindowAccounts(self.switch_window)
        self.accounts_window.start_show_account('active')
        self.mailing_by_users_window = WindowMailingByUsers(self.switch_window)
        self.proxy_window = WindowProxy(self.switch_window)
        self.parser = WindowParser(self.switch_window)
        self.convert = WindowConvert(self.switch_window)
        self.invite = WindowInvite(self.switch_window)
        self.create_channel = WindowCreateChannel(self.switch_window)

        # Добавляем окна в QStackedWidget
        self.stacked_widget.addWidget(self.accounts_window)
        self.stacked_widget.addWidget(self.mailing_by_users_window)
        self.stacked_widget.addWidget(self.proxy_window)
        self.stacked_widget.addWidget(self.parser)
        self.stacked_widget.addWidget(self.convert)
        self.stacked_widget.addWidget(self.invite)
        self.stacked_widget.addWidget(self.create_channel)


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
        elif target_window == 'create_channel':
            self.stacked_widget.setCurrentWidget(self.create_channel)
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
        info = DialogInfo('Внимание!', 'Отсутствует подключение к интернету.\nБез него приложение не может корректно функционировать',
                           'notification.mp3')
        info.show()
        sys.exit()

    # это не работает
    script_name = os.path.basename(__file__)  # Получаем имя текущего скрипта
    for process in psutil.process_iter(['pid', 'name']):
        try:
            # Проверка по имени процесса
            if script_name in process.info['name']:
                info = DialogInfo('Внимание!',
                                   'Приложение уже запущенно!',
                                   'notification.mp3')
                info.show()
                sys.exit()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    # это не работает

    items = os.listdir('../working_files/file_from_user')  # Получаем список всех файлов и папок в указанной директории
    for item in items:
        file_path = os.path.join('../working_files/file_from_user', item)
        if os.path.isfile(file_path):  # Проверяем, является ли элемент файлом
            os.remove(file_path)  # Удаляем файл

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.resize(1500, 850)
    main_window.show()
    sys.exit(app.exec_())